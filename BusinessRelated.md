# Business Notes — Agent Guard

---

## Is the Business Model Good?

The problem is real and growing. Companies are deploying agents faster than they're thinking about safety. Market timing is genuinely good.

**The core weakness — commodity risk.**
The major AI platforms will build this natively over time. OpenAI's operator controls, Anthropic's tool use policies, Google's agent frameworks — they'll all add guardrails at the SDK/platform level. When that happens, a standalone interceptor loses its reason to exist for basic use cases.

**What survives that?**
Cross-platform, cross-model enforcement. A company running 5 different agents (some on Claude, some on GPT, some on open source) needs one unified policy layer — not one from each vendor. Be the neutral third party. That's the defensible angle.

---

## Can I Generate Revenue?

Not easily in the short term. Two real blockers:

**The trust problem.**
Companies have to route sensitive agent actions through your API. That means their data and business logic flows through you. Enterprises won't do that without SOC 2 certification, privacy policy, DPAs, legal review. That process takes 6–12 months and costs money before you make any.

**The developer tool problem.**
Developers hate paying for tools. They'll use the free/open source version and only upgrade when their company forces them. Free tier will always have far more users than paid.

**What early revenue actually looks like:**
- Consulting: help a company set up Agent Guard for their use case — $5k–$20k contracts. Not scalable but validates demand.
- One design partner paying even $500/month proves someone values it.
- Grant programs: Anthropic, Google, and Microsoft all have funds for AI safety tooling. Underused.

---

## What Happens If I Open Source It?

Two outcomes depending on execution:

**Bad open source:** Dump code on GitHub, nobody stars it, dies quietly.

**Good open source:** Right license, build in public, write good docs, post on Hacker News / r/MachineLearning, accumulate users who spread the word.

**The model that works here is open core:**
- Engine = free and open source
- Hosted cloud version with dashboard, audit logs, integrations = paid
- This is exactly how LangSmith and Braintrust operate

**Real benefit of open source right now isn't revenue — it's credibility.**
A public repo with working code and real stars is worth more than a pitch deck when applying to YC, grants, or approaching design partners.

**One risk:** Open sourcing too early with half-built code signals "unfinished". Get it working first, then open source.

---

## How Do I Get Funding?

Three realistic paths:

### 1. Grants (most accessible right now)
- **Anthropic startup fund / Claude developer program** — they give credits and sometimes cash to safety-adjacent projects.
- **Mozilla Builders** — funds open source AI projects. Small grants ($10k–$50k), no equity taken.
- **NSF SBIR** — government grant for early-stage tech companies. Slow (months), but non-dilutive.

### 2. Accelerators (most leverage)
- **Y Combinator** — $500k for 7% equity. They fund AI safety tooling. But they want traction — a working product and at least one real user. Get the MVP working first, then apply.
- **Entrepreneur First** — accepts individuals, helps find a co-founder, then funds. Good if solo.

### 3. Angel Investors (hardest without a network)
Hard to access without warm intros. Not worth spending energy on until there's traction.

---

## Comparable Products (Market Signal)

| Product | Focus | Pricing Signal |
|---|---|---|
| Lakera Guard | Prompt injection detection | Enterprise ($$$), raised $20M |
| NeMo Guardrails | Open source policy rules (Colang DSL) | No direct monetization yet |
| Zenity | Enterprise agent monitoring | $50k+ contracts |
| Braintrust / LangSmith | Observability (not safety) | Freemium → $500+/month |
| AppOmni AgentGuard | Agent firewall | Enterprise only |

**The gap:** No affordable, developer-friendly, action-level safety API. That's the space.

---

## What to Do Right Now (Priority Order)

1. **Finish the MVP** — policy engine + LLM risk scorer working end-to-end
2. **Find one real user** — one startup using LangChain/CrewAI agents who'll actually call your API
3. **Apply for a grant or YC** once you have that

Revenue, funding, and the open source decision all get easier once you have working code and one person who cares. Right now the code is the business.

---

## Open Questions to Revisit Later

- Which license to use if open sourcing? (MIT = most permissive, AGPL = forces cloud users to contribute back)
- What does the paid dashboard actually look like? (Audit log viewer, rule editor, alert config)
- Which integrations give the most distribution? (LangChain, CrewAI, Claude tool use)
- What's the minimum to apply for YC? (Working API + 1 real user who cares)
