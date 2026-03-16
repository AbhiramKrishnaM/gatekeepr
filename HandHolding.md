# Agent Guard — Build Log & Learning Guide

> A personal guide to building this project, learning the stack, and turning it into a business.

---

## What We're Actually Building

An **interception proxy for AI agents**. When an AI agent decides to take an action (delete a record, send an email, charge a card), that action passes through Agent Guard *before* it hits the real system. Guard evaluates it and says Allow, Rewrite, or Block.

The two-step evaluation:
1. **Policy Engine** — fast rule check from a JSON file. E.g., "never delete on weekends", "max spend $100". No LLM needed. Instant.
2. **Risk Scorer** — if rules pass, an LLM reads the action's intent and returns a score 0.0–1.0.
   - `< 0.4` → Allow
   - `0.4–0.7` → Rewrite (suggest safer version)
   - `> 0.7` → Block + alert human

Why two steps? The rule check is deterministic and free. The LLM call costs money and takes time. So only run the LLM when hard rules don't already decide the outcome.

---

## Current State of the Code

- `app/main.py` — FastAPI app with `/intercept` POST endpoint. Returns a hardcoded stub (`status: allowed, risk_score: 0.3`). The Pydantic models `InterceptRequest` and `InterceptResponse` are defined here.
- `app/api/routes.py` — Empty (1 line). Hasn't been used yet.
- `app/data/policies/default_rules.json` — Empty placeholder.
- `app/data/prompts/risk_scorer.txt` — Empty placeholder.

Everything else is yet to be built.

---

## The Build Plan

### Phase 1 — Policy Engine (Next Up)

**What to build:** `app/services/policy_engine.py` + populate `default_rules.json`.

**What to learn: How JSON config-driven logic works**

The idea is that business rules live in a JSON file, not hardcoded in Python. This means a non-engineer (a compliance officer, a product manager) can change rules without touching code.

```json
{
  "rules": [
    {
      "id": "no-delete-weekends",
      "action_type": "delete",
      "condition": "day_of_week in ['Saturday', 'Sunday']",
      "verdict": "block",
      "reason": "Deletions not permitted on weekends"
    },
    {
      "id": "max-spend",
      "action_type": "create",
      "target_resource": "payment",
      "condition": "amount > 100",
      "verdict": "block",
      "reason": "Spend limit exceeded"
    }
  ]
}
```

Your `policy_engine.py` reads this file at startup, loops over the rules, and checks each one against the incoming `InterceptRequest`. If any rule matches, return `blocked` immediately with the reason. If nothing matches, return `pass`.

**Key Python you'll use:**
- `json.load()` to read the file
- `datetime.now().weekday()` to get day of week
- A simple `for rule in rules:` loop with `if/elif` conditions

**The deeper concept — why not just use if/else in Python?** Because if-else is code. To change it, you redeploy. A JSON config file can be reloaded without restarting the server. At scale, you'd store these rules in a database so they can be updated via an admin UI. That's how tools like NeMo Guardrails and Lakera work — the rules are data, not code.

---

### Phase 2 — LLM Risk Scorer

**What to build:** `app/services/risk_scorer.py` + populate `risk_scorer.txt`.

**What to learn: How to prompt an LLM to return structured output**

The hardest part here isn't calling the API — it's getting the LLM to reliably return a number between 0 and 1, not a paragraph of explanation.

Your prompt template (`risk_scorer.txt`) will look something like:

```
You are a security evaluator for AI agent actions.
Given the following action, return ONLY a JSON object with a risk_score between 0.0 and 1.0.
0.0 = completely safe. 1.0 = highly dangerous or irreversible.

Action: {action_type} on {target_resource} (id: {target_id})
Details: {action_details}
Context: {context}

Respond with ONLY this JSON, nothing else:
{"risk_score": <number>, "reason": "<one sentence>"}
```

The trick is being extremely explicit. LLMs are verbose by default. You force structure by:
1. Saying "ONLY this JSON" in the prompt
2. Using a low-temperature setting (e.g., `temperature=0.1`) — lower temperature = more predictable, less creative output
3. Parsing with a try/except in case it still returns garbage

**Parsing strategy:**
```python
import json, re

def parse_score(llm_response: str) -> float:
    # Try clean JSON parse first
    try:
        data = json.loads(llm_response.strip())
        return float(data["risk_score"])
    except:
        pass
    # Fallback: regex to find a float
    match = re.search(r'"risk_score"\s*:\s*([0-9.]+)', llm_response)
    if match:
        return float(match.group(1))
    return 0.5  # safe default if parsing fails
```

**Which LLM to use:** Start with Ollama locally (free, no API key, runs on your machine). Later swap to Claude or GPT-4 for production quality. The code stays the same — you just change the endpoint/model name.

---

### Phase 3 — Guardian Orchestrator

**What to build:** `app/services/guardian.py`

This is the simplest file conceptually. It imports the policy engine and risk scorer, runs them in sequence, and returns the final verdict.

```python
async def evaluate(request: InterceptRequest) -> InterceptResponse:
    # Step 1: Policy check (fast, free)
    policy_result = policy_engine.check(request)
    if policy_result.blocked:
        return InterceptResponse(status="blocked", risk_score=1.0, blocked_reason=policy_result.reason)

    # Step 2: LLM risk score (slow, costs money)
    risk_score = await risk_scorer.score(request)

    if risk_score < 0.4:
        return InterceptResponse(status="allowed", risk_score=risk_score)
    elif risk_score < 0.7:
        return InterceptResponse(status="rewrite", risk_score=risk_score, message="Consider a safer approach")
    else:
        return InterceptResponse(status="blocked", risk_score=risk_score, blocked_reason="High risk action detected")
```

**What to learn: async/await**

FastAPI is async. When your guardian calls the LLM, it makes an HTTP request that takes 1–5 seconds. `async/await` means Python doesn't freeze and wait — it can handle other requests in the meantime. Think of it like a waiter taking multiple tables' orders instead of standing at one table waiting for food.

- `async def` marks a function as async
- `await` pauses that function until a slow operation completes, while the rest of the app keeps running
- If you forget `await`, your LLM call will return a coroutine object (a promise), not the actual result

---

### Phase 4 — Wire It to the Endpoint

Move the models out of `main.py` into `app/models/domain.py`. Wire `/intercept` in `routes.py` to call `guardian.evaluate()`. Update `main.py` to import the router.

This is also when you add a real `InterceptResponse` with all fields:

```python
class InterceptResponse(BaseModel):
    status: str              # "allowed" | "blocked" | "rewrite"
    risk_score: float
    message: Optional[str] = None
    blocked_reason: Optional[str] = None
    suggested_action: Optional[dict] = None
    original_action: dict
```

---

### Phase 5 — Database (Audit Log)

**What to build:** PostgreSQL via SQLModel or SQLAlchemy.

Every intercepted action should be logged — whether it was allowed or blocked, what the risk score was, which agent sent it. This is called an **audit trail**. It's not optional for a real product — it's how your customers prove compliance to their own auditors.

**What to learn: ORMs**

An ORM (Object Relational Mapper) lets you write Python objects instead of raw SQL. SQLModel is the best choice here because it works with Pydantic natively.

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class ActionLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    agent_id: str
    action_type: str
    target_resource: str
    target_id: str
    status: str          # allowed / blocked / rewrite
    risk_score: float
    blocked_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

Use `docker-compose.yml` to spin up Postgres locally. You don't install Postgres on your machine — Docker runs it in a container.

---

### Phase 6 — Redis Streams (Optional, Advanced)

This is for when you want the Guardian to evaluate asynchronously — the Worker Agent fires off the action and gets an immediate acknowledgment (`"received, evaluating"`), then the result comes back via a callback or polling.

Skip this until the synchronous version works well. The sync version (request → evaluate → response in one HTTP call) is fine for v1.

---

### Phase 7 — Testing with DeepEval

**What is DeepEval?** A testing framework specifically for LLM outputs. Normal unit tests check exact values. LLM outputs are fuzzy — you can't assert `score == 0.73`. DeepEval lets you assert things like "this response contains a risk score" or "the guardian correctly blocked this obviously dangerous action."

Write tests like:
- DELETE on a user resource should always have risk_score > 0.5
- READ actions should generally be allowed
- Actions with "reason: test" shouldn't be auto-blocked

This is how you "guard the guardian" — make sure your own safety system isn't broken.

---

## Architecture Reference

```
HTTP Request (from Worker Agent)
    ↓
main.py → routes.py
    ↓
guardian.py (orchestrator)
    ├── policy_engine.py (checks default_rules.json)
    └── risk_scorer.py (calls Ollama/LLM with risk_scorer.txt prompt)
    ↓
ActionLog saved to PostgreSQL
    ↓
HTTP Response (status + risk_score)
```

**File responsibilities (short version):**

| File | Job |
|------|-----|
| `main.py` | Creates FastAPI app, mounts router |
| `routes.py` | Defines HTTP endpoints |
| `models/domain.py` | Pydantic data shapes |
| `services/guardian.py` | Orchestrates evaluation |
| `services/policy_engine.py` | JSON rule checking |
| `services/risk_scorer.py` | LLM call + score parsing |
| `core/config.py` | Env vars, API keys |
| `models/database.py` | SQLModel table definitions |

---

## Business Model

### The Problem You're Solving

Companies are deploying AI agents that can take real-world actions — sending emails, writing to databases, making API calls, spending money. Most of them have no safety layer between the agent's decision and the real world. One hallucination, one prompt injection, one misconfigured agent — and real damage happens. This is a real, unsolved, growing problem.

### Who Would Pay for This

**Primary:** Startups and mid-size companies building agent-based products (customer support bots, code agents, data pipeline agents). They don't want to build a safety layer themselves — they want to plug one in.

**Secondary:** Enterprises (banks, healthcare, legal) that need AI governance for compliance. They're already spending on Zenity and AppOmni at $50k+/year.

### Monetization Options

**1. API-as-a-Service (most realistic starting point)**
- Charge per intercept call, like Stripe charges per transaction
- Pricing: ~$0.001–$0.005 per intercept call
- 1 million calls/month = $1,000–$5,000 MRR per customer
- Companies running agents at scale easily hit 1M calls/month

**2. SaaS Subscription with tiers**
- Free: 10k calls/month (enough for dev/testing)
- Starter: $99/month — 500k calls, basic rules
- Pro: $499/month — 5M calls, custom policies, audit dashboard
- Enterprise: Custom — SLA, SSO, on-prem deploy

**3. Open Source + Paid Cloud**
- Release the core engine as open source (builds trust, community)
- Charge for the hosted version, the dashboard, and enterprise features
- This is the NeMo Guardrails / LangSmith model

### What Makes It Defensible

- **Policy DSL** — your JSON rule format becomes a standard. If people write rules for Agent Guard, switching costs go up.
- **Audit logs** — compliance-heavy customers (fintech, healthcare) need provable logs. Whoever owns the audit trail owns the relationship.
- **Integrations** — SDK wrappers for LangChain, CrewAI, Claude's tool use. Whoever integrates first into these ecosystems wins distribution.

### MVP to Validate With

Before building the dashboard or billing, validate with one real customer:
1. Find a startup using LangChain agents or similar
2. Give them free API access
3. Ask: "Would you pay $99/month to know every action your agent takes before it happens?"

If yes → build the billing. If no → understand why and iterate.

### Comparable Products (and Their Pricing Signal)

- **Lakera Guard** — prompt injection detection API. Enterprise pricing ($$$). Raised $20M.
- **NeMo Guardrails** — open source, NVIDIA backs it. No direct monetization (yet).
- **Zenity** — enterprise only, $50k+ contracts.
- **Braintrust / LangSmith** — observability, not safety. Freemium → $500+/month.

The gap: there's no affordable, developer-friendly, action-level safety API. That's the space.

---

## Progress Checklist

- [x] FastAPI server running
- [x] `/intercept` endpoint stub
- [x] Pydantic models (`InterceptRequest`, `InterceptResponse`)
- [ ] `default_rules.json` with at least 3 rules
- [ ] `policy_engine.py` — reads and evaluates rules
- [ ] `risk_scorer.txt` — prompt template
- [ ] `risk_scorer.py` — calls Ollama, parses score
- [ ] `guardian.py` — orchestrates policy + scorer
- [ ] Wire `/intercept` to call guardian (not a stub)
- [ ] `models/domain.py` — move models out of main.py
- [ ] `models/database.py` — SQLModel table for ActionLog
- [ ] Postgres via docker-compose
- [ ] Audit log: save every intercept call to DB
- [ ] DeepEval tests for at least 5 scenarios
- [ ] `mock_agent.py` — script that simulates a worker agent hitting your API

---

## Resources (Only the Useful Ones)

- FastAPI docs: https://fastapi.tiangolo.com/tutorial/ — read "Request Body", "Dependencies", "Bigger Applications"
- SQLModel: https://sqlmodel.tiangolo.com — same author as FastAPI, works natively with Pydantic
- Ollama: https://github.com/ollama/ollama — run LLMs locally, free
- DeepEval: https://docs.confident-ai.com — LLM testing framework
- httpx: https://www.python-httpx.org — async HTTP client for calling Ollama (use this instead of `requests` in async FastAPI)
