# Learning Path: Build & Learn Step by Step

## 🎯 Overview

This guide breaks down the entire project into small, manageable steps. You'll learn FastAPI, AI/ML concepts, and Python as you build.

---

## 📅 Phase 1: FastAPI Basics (Week 1)

**Goal:** Understand FastAPI fundamentals

### Step 1.1: Understand What You Already Have (Day 1)

You already have:

- ✅ A working FastAPI server
- ✅ A GET endpoint (`/`)
- ✅ A POST endpoint (`/items`)

**What to Learn:**

- **What is FastAPI?** A Python web framework for building APIs
- **What is an endpoint?** A URL path that responds to requests
- **What is GET vs POST?** GET = read data, POST = send data

**Action:** Run your server and test it:

```bash
make dev
# Then visit http://localhost:8000/docs
```

### Step 1.2: Create Your First Guardian Endpoint (Day 2-3)

**Goal:** Create `/intercept` endpoint that receives JSON

**What You'll Learn:**

- How to receive JSON data
- What Pydantic models are (data validation)
- How to return JSON responses

**What to Build:**

- A simple `/intercept` endpoint that receives an action
- Returns a mock response like `{"status": "allowed", "risk_score": 0.3}`

**Why This Step:**

- You'll understand request/response
- You'll see how FastAPI validates data
- No AI/ML yet - just HTTP basics

---

## 📅 Phase 2: Understanding the Data Flow (Week 2)

**Goal:** Understand how data moves through your system

### Step 2.1: Create Data Models (Day 4-5)

**Goal:** Define what an "action" looks like

**What You'll Learn:**

- **What is a data model?** A blueprint for data structure
- **What is Pydantic?** A library that validates data automatically
- **What is JSON?** A way to represent data

**What to Build:**

- `app/models/domain.py` with `ActionRequest` model
- This defines: agent_id, action_type, target_resource, etc.

**Why This Step:**

- You'll understand data structures
- You'll see how Python classes work
- Foundation for everything else

### Step 2.2: Read JSON Files (Day 6-7)

**Goal:** Read policy rules from a JSON file

**What You'll Learn:**

- How to read files in Python
- What JSON is and how to parse it
- How to structure configuration files

**What to Build:**

- `app/data/policies/default_rules.json` with simple rules
- `app/services/policy_engine.py` that reads this file
- Function that checks: "Is DELETE allowed?"

**Why This Step:**

- You'll learn file I/O
- You'll understand configuration
- Still no AI - just file reading

---

## 📅 Phase 3: Your First AI Integration (Week 3)

**Goal:** Call an LLM for the first time

### Step 3.1: Understand What an LLM Is (Day 8)

**What is an LLM?**

- **Large Language Model** = AI that understands text
- Examples: ChatGPT, Claude, Llama
- You give it text, it gives you text back

**Key Terms:**

- **Prompt** = The text you send to the LLM
- **Response** = The text the LLM sends back
- **Model** = The specific AI (like "llama3.2")

### Step 3.2: Call Ollama (Day 9-10)

**Goal:** Make your first LLM call

**What You'll Learn:**

- **What is an API?** A way for programs to talk to each other
- **What is HTTP?** The protocol for web communication
- How to make HTTP requests in Python

**What to Build:**

- `app/services/risk_scorer.py`
- Function that sends a prompt to Ollama
- Gets back a risk score (just a number for now)

**Why This Step:**

- You'll make your first AI call
- You'll understand APIs
- Simple: send text, get text back

### Step 3.3: Parse LLM Response (Day 11)

**Goal:** Extract risk score from LLM response

**What You'll Learn:**

- How to extract information from text
- String manipulation in Python
- Error handling (what if LLM returns weird text?)

**What to Build:**

- Parse the LLM response to get a number (0.0 to 1.0)
- Handle cases where LLM doesn't return what you expect

---

## 📅 Phase 4: Putting It Together (Week 4)

**Goal:** Connect all pieces

### Step 4.1: Create the Guardian Service (Day 12-13)

**Goal:** Orchestrate policy check + risk scoring

**What You'll Learn:**

- How to combine multiple functions
- Control flow (if/else)
- How services work together

**What to Build:**

- `app/services/guardian.py`
- Function that:
  1. Checks policy rules
  2. If passed, calls risk scorer
  3. Makes decision based on score

**Why This Step:**

- You'll see how everything connects
- You'll understand the full flow
- Still manageable - just combining what you built

### Step 4.2: Wire It All Together (Day 14)

**Goal:** Connect endpoint → service → response

**What You'll Learn:**

- How to import modules
- How to call functions
- How FastAPI routes work

**What to Build:**

- Update `app/api/routes.py` to call guardian service
- Return proper response

---

## 🗺️ Learning Roadmap Summary

```text
Week 1: FastAPI Basics
├── Day 1: Understand what you have ✅
├── Day 2-3: Create /intercept endpoint
└── Learn: HTTP, JSON, FastAPI basics

Week 2: Data & Files
├── Day 4-5: Create data models
├── Day 6-7: Read JSON files
└── Learn: Python classes, file I/O, JSON

Week 3: First AI Integration
├── Day 8: Learn what LLMs are
├── Day 9-10: Call Ollama API
├── Day 11: Parse LLM responses
└── Learn: APIs, HTTP requests, LLMs

Week 4: Connect Everything
├── Day 12-13: Create Guardian service
├── Day 14: Wire it all together
└── Learn: Service architecture, imports
```

---

## 📚 Key Concepts Explained Simply

### FastAPI Terms

- **Endpoint** = A URL path that does something (like `/intercept`)
- **Route** = Same as endpoint
- **Request** = Data coming IN to your API
- **Response** = Data going OUT from your API
- **Model (Pydantic)** = A blueprint for data structure
- **Router** = A way to organize endpoints

### AI/ML Terms

- **LLM** = Large Language Model (AI that understands text)
- **Prompt** = Text you send to the LLM
- **Model** = Specific AI (like "llama3.2")
- **API** = Way for programs to talk to each other
- **Risk Score** = A number (0.0 to 1.0) representing how risky something is

### Python Terms

- **Function** = A reusable piece of code
- **Class** = A blueprint for creating objects
- **Module** = A Python file you can import
- **Package** = A folder with Python files

---

## 🚀 Where to Start Right Now

### Today: Step 1.1 - Understand What You Have

1. **Run your server:**

   ```bash
   make dev
   ```

2. **Open Swagger UI:**

   - Go to `http://localhost:8000/docs`
   - This is FastAPI's automatic documentation

3. **Test your endpoints:**

   - Click on `GET /` → Try it out → Execute
   - Click on `POST /items` → Try it out → Add JSON:

     ```json
     {
       "name": "test",
       "description": "test item",
       "price": 100
     }
     ```

   - Execute and see the response

4. **What You Just Learned:**

   - FastAPI auto-generates documentation
   - You can test APIs in the browser
   - JSON is how data is sent/received

---

## 📝 Tomorrow: Step 1.2 - Create `/intercept` Endpoint

**Goal:** Create an endpoint that receives an action and returns a mock decision.

**What You'll Build:**

- A POST endpoint at `/intercept`
- It receives JSON with action details
- Returns a simple response like `{"status": "allowed"}`

**Why Start Here:**

- You already know how to create POST endpoints
- No AI/ML complexity yet
- You'll see the basic flow

---

## 🎓 Learning Strategy

### 1. One Thing at a Time

- Don't try to learn everything at once
- Focus on one concept per day
- Master it before moving on

### 2. Build, Don't Just Read

- Code along with each step
- Make mistakes and fix them
- Experiment and break things

### 3. Use the Docs

- FastAPI docs: <https://fastapi.tiangolo.com>
- Python docs: <https://docs.python.org>
- Ask questions when stuck

### 4. Don't Worry About Perfection

- Working code > perfect code
- You can refactor later
- Learning > optimization

---

## 📖 Resources for Each Phase

### Phase 1: FastAPI Basics

- FastAPI Tutorial: <https://fastapi.tiangolo.com/tutorial/>
- Focus on: First Steps, Path Parameters, Request Body

### Phase 2: Data & Files

- Python JSON: <https://docs.python.org/3/library/json.html>
- Python File I/O: <https://docs.python.org/3/tutorial/inputoutput.html>

### Phase 3: AI Integration

- Ollama Python: <https://github.com/ollama/ollama-python>
- HTTP Requests: <https://requests.readthedocs.io/>

### Phase 4: Architecture

- FastAPI Bigger Applications: <https://fastapi.tiangolo.com/tutorial/bigger-applications/>

---

## ✅ Your Action Plan

### This Week

- **Day 1 (today):** Understand your current code, test it
- **Day 2-3:** Create `/intercept` endpoint with mock response
- **Day 4-5:** Create `ActionRequest` model
- **Day 6-7:** Read JSON policy file

### Next Week

- **Day 8:** Research what LLMs are (watch videos, read articles)
- **Day 9-10:** Make your first Ollama call
- **Day 11:** Parse the response

### Week After

- **Day 12-13:** Create Guardian service
- **Day 14:** Connect everything

---

## ❓ Questions to Ask Yourself Each Day

1. What did I learn today?
2. What confused me?
3. What do I want to learn tomorrow?
4. Did I write code or just read?

---

## 💡 Remember

- ✅ **It's okay to be overwhelmed** - break it into small steps
- ✅ **You don't need to know everything** - learn as you go
- ✅ **Mistakes are normal** - they help you learn
- ✅ **Progress over perfection** - working code is the goal
- ✅ **Ask for help** - use documentation, search, ask questions

---

## 🎯 Start Here (Right Now)

1. Open your terminal
2. Run `make dev`
3. Open `http://localhost:8000/docs`
4. Play with your existing endpoints
5. Understand what they do

Once you're comfortable with that, move to **Step 1.2**: creating the `/intercept` endpoint.

---

## 🏗️ FastAPI Architecture Overview

### The Entry Point: `app/main.py`

**Purpose:** Creates the FastAPI app instance and wires everything together.

**What it does:**

- Creates `app = FastAPI()` instance
- Imports and includes routers from `app/api/routes.py`
- Sets up middleware (CORS, logging, etc.)
- Can include startup/shutdown events

**Flow:**

```text
main.py → Creates FastAPI app → Includes routers → Server starts
```

---

### The API Layer: `app/api/routes.py`

**Purpose:** Defines all your HTTP endpoints (the "what" users can call).

**What goes here:**

- `@app.post("/intercept")` - The main Guardian endpoint
- `@app.get("/health")` - Health check
- `@app.get("/actions/{action_id}")` - Get action history
- Other endpoints

**What it does:**

- Receives HTTP requests
- Validates input using Pydantic models (from `app/models/domain.py`)
- Calls service functions (from `app/services/`)
- Returns responses

**Flow:**

```text
HTTP Request → routes.py → Validates input → Calls service → Returns response
```

---

### The Models Layer: `app/models/domain.py`

**Purpose:** Defines data structures (request/response shapes).

**What goes here:**

- `ActionRequest` - What Worker Agent sends
- `GuardianResponse` - What Guardian returns
- `ActionType` enum - CREATE, READ, UPDATE, DELETE
- Other data models

**Why separate:**

- Reusable across routes and services
- Type safety and validation
- Clear contracts

**Flow:**

```text
routes.py imports models → Validates incoming data → Passes to services
```

---

### The Services Layer: `app/services/`

**Purpose:** Business logic (the "how" things work).

#### `app/services/guardian.py`

- Orchestrates the Guardian flow
- Calls policy engine → Calls risk scorer → Makes decision
- Returns ALLOW/BLOCK/REWRITE

**Flow:**

```text
guardian.py receives action → Calls policy_engine → Calls risk_scorer → Returns decision
```

#### `app/services/policy_engine.py`

- Reads JSON rules from `app/data/policies/default_rules.json`
- Checks if action violates rules
- Returns pass/fail

**Flow:**

```text
policy_engine.py → Reads JSON file → Checks rules → Returns True/False
```

#### `app/services/risk_scorer.py`

- Uses LLM (Ollama/OpenAI) to score risk
- Reads prompt from `app/data/prompts/risk_scorer.txt`
- Returns risk score (0.0 to 1.0)

**Flow:**

```text
risk_scorer.py → Reads prompt template → Calls LLM → Parses score → Returns float
```

---

### The Configuration Layer: `app/core/config.py`

**Purpose:** Centralized settings and environment variables.

**What goes here:**

- Database connection strings
- API keys (Ollama, OpenAI)
- Feature flags
- App settings

**Flow:**

```text
config.py → Reads .env file → Exports settings → Used by services
```

---

### The Data Layer: `app/data/`

**Purpose:** Static files (rules, prompts).

- `app/data/policies/default_rules.json` - Policy rules
- `app/data/prompts/risk_scorer.txt` - LLM prompt template

**Flow:**

```text
Services → Read files from data/ → Use in logic
```

---

## 🔄 Complete Request Flow

```text
1. HTTP Request arrives
   ↓
2. main.py (FastAPI app receives it)
   ↓
3. routes.py (Endpoint handler catches it)
   ↓
4. domain.py (Validates request structure)
   ↓
5. guardian.py (Main logic orchestrator)
   ↓
6. policy_engine.py (Checks JSON rules)
   ↓
7. risk_scorer.py (Calls LLM for risk score)
   ↓
8. guardian.py (Makes final decision)
   ↓
9. routes.py (Formats response)
   ↓
10. HTTP Response sent back
```

---

## 📁 File Dependencies (What Imports What)

```text
main.py
  └─→ imports routes.py
      └─→ imports models/domain.py
      └─→ imports services/guardian.py
          └─→ imports services/policy_engine.py
          └─→ imports services/risk_scorer.py
          └─→ imports models/domain.py
              └─→ imports core/config.py
                  └─→ reads .env file
```

---

## 📂 Folder Structure Breakdown

```text
app/
├── main.py              # Entry point - Creates app, includes routers
│
├── api/                 # API Layer (HTTP endpoints)
│   ├── routes.py        # All @app.get/@app.post endpoints
│   └── dependencies.py  # Shared functions (auth, DB connections)
│
├── services/            # Business Logic Layer
│   ├── guardian.py      # Main orchestrator
│   ├── policy_engine.py # Rule checking
│   └── risk_scorer.py   # LLM risk scoring
│
├── models/              # Data Models Layer
│   └── domain.py       # Pydantic models (ActionRequest, etc.)
│
├── core/                # Configuration Layer
│   └── config.py       # Settings, API keys, env vars
│
└── data/                # Static Data Layer
    ├── policies/       # JSON rule files
    └── prompts/        # LLM prompt templates
```

---

## 🔧 How to Wire It Together

### Step 1: `main.py` Sets Up the App

- Creates FastAPI instance
- Includes router from `routes.py`
- Can add middleware, CORS, etc.

### Step 2: `routes.py` Defines Endpoints

- Imports FastAPI router
- Imports models from `domain.py`
- Imports service functions from `services/guardian.py`
- Defines endpoints that call services

### Step 3: `services/guardian.py` Orchestrates

- Imports `policy_engine.py`
- Imports `risk_scorer.py`
- Imports models from `domain.py`
- Imports config from `core/config.py`
- Combines policy check + risk score → decision

### Step 4: `policy_engine.py` Checks Rules

- Reads JSON from `data/policies/`
- Validates against rules
- Returns True/False

### Step 5: `risk_scorer.py` Scores Risk

- Reads prompt from `data/prompts/`
- Uses config for LLM API key
- Calls LLM
- Returns score

---

## 🎯 Example: How `/intercept` Endpoint Flows

```text
1. Client sends POST /intercept with JSON
   ↓
2. main.py → FastAPI receives request
   ↓
3. routes.py → @router.post("/intercept") catches it
   ↓
4. domain.py → ActionRequest model validates JSON structure
   ↓
5. routes.py → Calls guardian.validate_action(action)
   ↓
6. guardian.py → Calls policy_engine.check_rules(action)
   ↓
7. policy_engine.py → Reads default_rules.json → Returns pass/fail
   ↓
8. guardian.py → If passed, calls risk_scorer.score(action)
   ↓
9. risk_scorer.py → Reads risk_scorer.txt → Calls Ollama → Returns 0.7
   ↓
10. guardian.py → Score 0.7 = "rewrite" → Returns decision
   ↓
11. routes.py → Formats GuardianResponse → Returns HTTP 200
   ↓
12. Client receives response
```

---

## 📋 What Each File Is Responsible For

| File               | Responsibility              | Doesn't Do                 |
|--------------------|-----------------------------|----------------------------|
| `main.py`          | App setup, router inclusion | Business logic             |
| `routes.py`        | HTTP handling, validation   | Decision making            |
| `guardian.py`      | Orchestrates flow           | HTTP handling, rule check  |
| `policy_engine.py` | Rule validation             | LLM calls, HTTP            |
| `risk_scorer.py`   | LLM risk scoring            | Rule checking, HTTP        |
| `domain.py`        | Data structures             | Logic                      |
| `config.py`        | Settings                    | Business logic             |

---

## ✨ Benefits of This Structure

1. **Separation of Concerns** - Each file has one job
2. **Testability** - Test services without HTTP
3. **Reusability** - Services can be used elsewhere
4. **Maintainability** - Easy to find and change code
5. **Scalability** - Easy to add new endpoints/services

---

## 🎓 Next Steps After Understanding Architecture

1. Create the folder structure
2. Set up `config.py` to read environment variables
3. Create `domain.py` with Pydantic models
4. Create `policy_engine.py` to read JSON rules
5. Create `risk_scorer.py` to call LLM
6. Create `guardian.py` to orchestrate
7. Create `routes.py` with the `/intercept` endpoint
8. Wire everything in `main.py`

---

## 🚦 Progress Checklist

- [ ] Day 1: Understand current code, test endpoints
- [ ] Day 2-3: Create `/intercept` endpoint
- [ ] Day 4-5: Create data models (`domain.py`)
- [ ] Day 6-7: Read JSON files (`policy_engine.py`)
- [ ] Day 8: Learn about LLMs
- [ ] Day 9-10: Call Ollama (`risk_scorer.py`)
- [ ] Day 11: Parse LLM responses
- [ ] Day 12-13: Create Guardian service
- [ ] Day 14: Wire everything together

---

**Remember:** Take it one step at a time. You've got this! 🚀
