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