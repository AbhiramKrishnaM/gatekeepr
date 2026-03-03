# AI Agent Guard

1. Architectural Decision Record (ADR)

Status: Proposed

Context: We need a way to ensure that "Worker Agents" (AI that performs tasks) do not perform harmful or hallucinated actions.

Decision: We will implement an Interception Proxy pattern. Every action a Worker Agent wants to take must pass through a "Guardian" before it reaches the real world (the database or API).

Rationale:

    Safety: No action happens without a second "opinion."

    Learning: This stack (FastAPI + Redis + LLM) is the industry standard for scalable AI apps.

    Flexibility: Using a JSON-based DSL (Domain Specific Language) allows us to change rules without rewriting the Python code.

2. Concept Log: How It Works

The system acts like a Security Guard at a gate.

    The Intent: The Worker Agent says, "I want to delete User 2's data."

    The Interception: Instead of deleting it, the request is caught by the Guardian API.

    The Verification (Two-Step):

        Step A (The Rulebook): The Guardian checks the JSON DSL. If a rule says "No deletions on weekends," it blocks it immediately (Fast, cheap).

        Step B (The Brain): If the rulebook is okay, the LLM + DeepEval looks at the intent. Is it "risky"? It assigns a Risk Score (0 to 1).

    The Verdict:

        Score < 0.4: "Allow" (Proceed to action).

        Score 0.4 - 0.7: "Rewrite" (The Guardian suggests a safer version).

        Score > 0.7: "Block" (Alert the human user).

3. Implementation: Component Interaction

Here is how your chosen tech stack communicates:
A. The Infrastructure Layer

    FastAPI: The "Brain Center." It hosts the endpoints where agents send their proposed actions.

    Postgres: The "Memory." Stores your user data, the logs of every blocked action, and your Policy Rules.

    Redis Streams: The "Conveyor Belt." Used to pass messages between the Worker and the Guardian if you want them to run at the same time without waiting for each other.

B. The Logic Layer (The Guard)

    Policy Rules (JSON/DSL): A simple file where you define "Hard Red Lines" (e.g., max_spend: 100).

    LLM Risk Scorer: A small, fast LLM prompt that evaluates the context of an action.

    DeepEval: A testing framework that ensures the Guardian itself isn't making mistakes (Guard the Guardian).

C. The Interaction Flow

    Worker Agent sends a POST request to FastAPI.

    FastAPI saves the request in Postgres (for auditing).

    FastAPI checks the JSON Policy.

    FastAPI calls the LLM to get a Risk Score.

    FastAPI returns a "Go" or "No-Go" to the Worker.


# Existing Applications that focuses on AI Security and Guard (AI Generated)

1. Enterprise "Guardian" Platforms

These are high-end, expensive softwares used by big companies to watch their agents in real-time.

    Zenity (AIDR):  It monitors "Agent Intent." If an agent tries to do something it shouldn't (like accessing a database it doesn't need), Zenity blocks it in real-time.

    AppOmni AgentGuard: Acts like a firewall specifically for agents. It reviews every "instruction" an agent receives before the agent can act on it.

    Silverfort: They focus on "Identity." They treat the AI agent like a digital employee. If the agent suddenly asks for "Admin" permissions, Silverfort blocks the request.

    Wayfound: This is more of a "Supervisor" dashboard. It shows you a transcript of what the agent is doing and highlights where it broke your company's rules.

2. Developer Tools & Frameworks

These are closer to what you are building with your tech stack.

    NVIDIA NeMo Guardrails: This is the "Gold Standard" for open-source policy rules. It uses a language called Colang (similar to your DSL idea) to define exactly what an agent can and cannot say or do.

    Lakera Guard: A real-time API that sits in front of your LLM. It's famous for stopping "Prompt Injections" (when a user tries to trick your agent into breaking its rules).

    Braintrust & LangSmith: These are "Observability" tools. They don't always block actions, but they record everything so you can see exactly why an agent made a "risky" decision.

    DeepEval (Which you mentioned): In 2026, DeepEval is widely used for "Unit Testing" agents.




# Project Structure (AI Generated - Might need to review and change this)

ai-agent-guard/
├── app/
│   ├── __init__.py
│   ├── main.py                # The FastAPI entry point (The "Brain Center")
│   ├── core/
│   │   ├── config.py          # API keys (OpenAI, Postgres URL)
│   │   └── security.py        # Logic for API keys/auth
│   ├── api/
│   │   ├── routes.py          # API endpoints (e.g., /intercept, /approve)
│   │   └── dependencies.py    # Shared logic for routes
│   ├── services/
│   │   ├── guardian.py        # The "Guardian" logic (Risk scoring + DeepEval)
│   │   ├── policy_engine.py   # Code that reads your JSON/DSL rules
│   │   └── queue_manager.py   # Redis Streams / Kafka interaction logic
│   ├── models/
│   │   ├── domain.py          # Pydantic models (What an "Action" looks like)
│   │   └── database.py        # SQLAlchemy/SQLModel definitions for Postgres
│   └── data/
│       ├── policies/
│       │   └── default_rules.json # Your JSON DSL (The "Rulebook")
│       └── prompts/
│           └── risk_scorer.txt    # System prompt for the LLM Scorer
├── scripts/
│   └── mock_agent.py          # A script to simulate a "Worker Agent" for testing
├── tests/
│   └── test_compliance.py     # DeepEval test cases
├── .env                       # Secret environment variables (DO NOT COMMIT)
├── docker-compose.yml         # To spin up Postgres and Redis easily
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation and ADR



