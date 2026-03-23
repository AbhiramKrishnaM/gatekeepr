# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make dev      # Start FastAPI dev server with auto-reload
make run      # Alias for make dev
```

The FastAPI entrypoint is defined in `pyproject.toml` as `app.main:app`. No linting or test setup exists yet.

## Architecture

**Agent Guard** is an interception proxy for AI agents. Before a worker agent's action (delete, read, update, create) reaches the real system, Agent Guard evaluates it and returns one of three verdicts: `allowed`, `blocked`, or `rewrite`.

### Evaluation Pipeline (two-step, planned)

1. **Policy Engine** — fast JSON DSL rule check (`app/data/policies/default_rules.json`)
2. **LLM Risk Scorer** — scores 0.0–1.0 using a system prompt (`app/data/prompts/risk_scorer.txt`)

Only actions that pass Step A proceed to Step B. The orchestrator (`app/services/guardian.py`, not yet implemented) coordinates both steps.

### Current State

The `/intercept` POST endpoint exists in `app/main.py` but returns a hardcoded stub (`status="allowed", risk_score=0.3`). All Pydantic models (`ActionType`, `InterceptRequest`, `InterceptResponse`) are defined there too.

`app/api/routes.py` exists but is currently empty — intended for future endpoint organization.

### Planned Phases

1. Policy Engine (`app/services/policy_engine.py`) — evaluate JSON rules
2. LLM Risk Scorer (`app/services/risk_scorer.py`) — call LLM, parse score
3. Guardian Orchestrator (`app/services/guardian.py`) — coordinate both
4. Move models to `app/models/domain.py`, wire guardian into routes
5. PostgreSQL audit logs via SQLModel (`app/models/database.py`)
6. Redis Streams for async queuing (optional)
7. DeepEval tests for LLM output validation

### API Contract

`POST /intercept` request fields: `action` (enum: delete/read/update/create), `agent_id`, `target_resource`, `target_id`, `action_details` (optional dict), `context` (optional dict).

Full planned response: `status`, `risk_score`, `message`, `blocked_reason`, `suggested_action`, `original_action`.

See `app/stubs/intercept.json` for a concrete example request payload.

## Key Documentation

- **README.md** — Architectural Decision Records and rationale for design choices
- **WHAT_I_AM_BUILDING.md** — Deep dive into what Agent Guard is, how it works in the real world, and why it's designed this way (no code)
- **ROADMAP.md** — Week-by-week learning and build plan
- **Questions.md** — Q&A log covering flow and architecture decisions
