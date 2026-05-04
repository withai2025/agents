# ⚒️ AppForge

> **Forge your app idea into a working product with 13 AI agents.**
>
> One sentence in → fully functional app out. No human coding required.

<p align="center">
  <b>English</b> · <a href="README_CN.md">中文</a>
</p>

> 💡 **Looking for the Claude (Anthropic) version?** → [AppForge](https://github.com/withAIx/AppForge)

<p align="center">
  <a href="https://github.com/withAIx/DeepSeek-AppForge/stargazers"><img src="https://img.shields.io/github/stars/withAIx/DeepSeek-AppForge?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/withAIx/DeepSeek-AppForge/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+"></a>
  <a href="https://github.com/openai/openai-python"><img src="https://img.shields.io/badge/OpenAI%20SDK-1.0+-green.svg" alt="OpenAI SDK (DeepSeek compatible)"></a>
  <a href="https://github.com/withAIx/DeepSeek-AppForge/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

---

## 🤔 What Is AppForge?

AppForge is an **AI-native APP development assembly line**. You describe what you want to build—in plain language—and 13 specialized AI agents take it from idea to a complete, runnable application.

No more piecemeal AI coding assistants. AppForge runs the entire **product lifecycle**:

```
YOU SAY:                          APPFORGE DELIVERS:
"I want a running tracker app      ✅ docs/PRD.md          (9-chapter product spec)
 that logs routes, pace,           ✅ docs/TECH_ARCHITECTURE (tech stack, directory tree)
 calories, and friend PvP"         ✅ docs/CODING_STANDARDS (DO/DON'T code rules)
                                   ✅ docs/DB_SCHEMA        (ER diagram, SQL, RLS)
                                   ✅ docs/API_CONTRACT     (endpoints, types, error codes)
                                   ✅ docs/TASK_BOOK        (phased task plan, Mock strategy)
                                   ✅ Working React Native app (Expo + Supabase)
```

> **Think of it as**: Assembling a 13-person full-stack team—1 tech lead, 6 architects, 6 engineers—that never sleeps, never complains, and ships end-to-end.

---

## 🎯 Why AppForge?

| Instead of... | AppForge... |
|--------------|-------------|
| Manually writing PRDs, tech specs, coding standards | **6 planning agents** generate all 6 documents in strict sequence, each validated against the previous |
| Figuring out what to build next | **Orchestrator** reads project state and routes to the right agent automatically |
| Switching between 5 different AI tools | **Single pipeline**: one conversation, 13 agents, zero context switching |
| Hoping code quality stays consistent | **CODING_STANDARDS.md** is generated first, then enforced by every coding agent |
| Manually tracking what's done | **project_state.json** tracks every task, retry count, and degradation status |
| Abandoning projects mid-way | **Graceful degradation**: failed agents produce simplified output rather than blocking the pipeline |

---

## 🚀 Powered by DeepSeek V4

AppForge is built entirely on the **DeepSeek V4 model family**, delivering unparalleled performance at a fraction of the cost.

### Why DeepSeek?

| Capability | DeepSeek V4 Pro | Claude Opus 4.6 | Advantage |
|-----------|----------------|---------------|-----------|
| Context window | **1,000,000 tokens** | 200,000 tokens | 5x larger — load all 6 planning docs in one prompt |
| Input price (per 1M tokens) | **$1.74** | $15.00 | 8.6x cheaper |
| Output price (per 1M tokens) | **$3.48** | $75.00 | 21.5x cheaper |
| Thinking mode | **thinking / thinking_max** | Extended thinking | Fine-grained control per agent |
| Prefix caching | **Automatic (80-92% discount)** | Manual | Phase 0 serial chain: ~60% cost savings |
| Chinese language | **Native-level** | Good | System prompts are primarily Chinese |

### Smart Model Routing

Not every task needs a heavyweight model. AppForge assigns models intelligently:

| Tier | Model | Thinking Mode | Agents | Use Case |
|------|-------|--------------|--------|----------|
| Heavy | `deepseek-v4-pro` | `thinking_max` | PRD Expert, Schema Architect, API Contract, Task Decomposer | Complex reasoning, multi-document synthesis |
| Standard | `deepseek-v4-pro` | `thinking` | Orchestrator, Tech Architect, Coding Standards, Agent-BE, Agent-FE, Agent-FIX | Architecture decisions, code generation |
| Light | `deepseek-v4-flash` | `non-thinking` | Agent-DB, Agent-CONNECT, Agent-VERIFY | Mechanical SQL/field mapping/validation |

### DeepSeek-Exclusive Features

**1M Context Cross-Document Review**
After all 6 planning documents are generated, `cross_doc_checker.py` loads **every document into a single API call** and performs a holistic consistency audit — catching field name mismatches, schema-API inconsistencies, and logic contradictions across the entire doc set. Impossible on a 200K context window.

**Automatic Prefix Caching**
DeepSeek caches repeated prompt prefixes at block boundaries automatically. Phase 0's serial chain (where each agent loads the previous agent's output) sees **80-92% cache hit rates**, cutting prompt costs by ~60%. The `prefix_cache_utils.py` helper structures messages to maximize cache overlap.

**Reasoning Content Streaming**
When `thinking` mode is enabled, DeepSeek returns `delta.reasoning_content` (the model's internal chain of thought) alongside `delta.content` (visible output). The Orchestrator displays its reasoning so you can understand why it made each scheduling decision.

---

## 🏗️ Architecture

### The Assembly Line

```
                         ⚒️ AppForge
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────────────────────────────────────────┐
     │              🧠 Orchestrator                     │
     │         DeepSeek V4 Pro + Function Calling             │
     │                                                 │
     │   Reads project_state.json → Decides next step  │
     │            → Routes to correct agent            │
     │            → Updates progress                   │
     └──────────────────────┬──────────────────────────┘
                            │
          ┌─────────────────┴──────────────────┐
          ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│   PHASE 0: Planning   │          │  PHASE 1-N: Building  │
│   (Strict Serial)     │          │  (Hybrid Parallel)    │
│   ①→②→③→④→⑤→⑥       │          │  DB │ FE║BE │ CONNECT │
│   6 docs auto-gen     │          │  VERIFY → FIX → SHIP  │
└──────────────────────┘          └──────────────────────┘
```

### Phase 0: The Planning Pipeline (Strict Serial Chain)

Every step consumes the output of the previous step. No skipping, no parallel execution—each document is the foundation for the next.

```
USER IDEA  "I want a running tracker app..."
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ① 📝 PRD EXPERT                                                  │
│    Input:  User's idea (even a single sentence)                   │
│    Output: docs/PRD.md — 9 chapters, Given-When-Then criteria    │
│    Gate:   ✅ No banned words  ✅ P0 ≤ 40% of total features      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ② 🏗️ TECH ARCHITECT                                              │
│    Input:  docs/PRD.md                                          │
│    Output: docs/TECH_ARCHITECTURE.md                            │
│    Content: 2+ alternatives per tech choice, full directory tree,│
│             MVP phases, zero-experience setup guide             │
│    Gate:   ✅ Comparison table per choice  ✅ No vague language   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ③ 📏 CODING STANDARDS                                            │
│    Input:  PRD + TECH_ARCHITECTURE                              │
│    Output: docs/CODING_STANDARDS.md — 13 chapters                │
│    Content: Naming rules, component/store/service patterns,      │
│             Git conventions, Cursor AI prompt template          │
│    Gate:   ✅ DO/DON'T code examples  ✅ Dir tree matches ARCH   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ④ 🗄️ SCHEMA ARCHITECT                                            │
│    Input:  PRD + ARCH + STANDARDS (3 docs)                      │
│    Output: docs/DB_SCHEMA.md                                    │
│    Content: Mermaid ER diagram, PostgreSQL DDL, SQLite DDL,     │
│             RLS policies, indexes, sync strategy, Redis keys    │
│    Gate:   ✅ Every table traceable to PRD  ✅ SQL executable    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ⑤ 🔌 API CONTRACT ARCHITECT                                      │
│    Input:  PRD + ARCH + STANDARDS + SCHEMA (4 docs)             │
│    Output: docs/API_CONTRACT.md                                 │
│    Content: Error code system, auth tiers, TypeScript types,     │
│             pagination, file upload, weak-network resilience     │
│    Gate:   ✅ Every PRD action → API  ✅ Fields match Schema      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ⑥ 📋 TASK DECOMPOSER                                             │
│    Input:  ALL 5 docs above                                     │
│    Output: docs/TASK_BOOK.md                                    │
│    Content: Dependency graph (Mermaid), per-task file list,      │
│             Mock data plan, copy-paste Claude Code prompts      │
│    Gate:   ✅ Every page → task  ✅ Criteria = terminal commands  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 INDEPENDENT REVIEW (fresh conversation, zero context bias)    │
│    Cross-document consistency → Operability → Completeness       │
│    Output: Must Fix / Should Fix / Ignore / Score (1-10)         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                     All clear ✅
                             │
                             ▼
                  PHASE 1-N CODING BEGINS
```

### Phase 1-N: The Build Pipeline (Hybrid Serial-Parallel)

```
TASK_BOOK.md
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: INFRASTRUCTURE (forced serial — no parallel possible)   │
│                                                                 │
│ T00 ──▶ T01 ──▶ T02 ──▶ T03 ──▶ T04                            │
│ Init     Config   Types    API      UI                           │
│ project  files    defs     client   components                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: AUTH MODULE                                            │
│                                                                 │
│ T05 (Auth Store) ──▶ T06 (Register) ║ T07 (Login) ← can parallel│
│                           │                                      │
│                           ▼                                      │
│                   T08 (Auth Edge Function)                       │
│                           │                                      │
│                           ▼                                      │
│                   T06 + T07: swap Mock → real API                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3+: CORE FEATURES (frontend ‖ backend allowed)            │
│                                                                 │
│                 ┌──────────────┐                                 │
│                 │  🗃️ Agent-DB  │   Run migrations               │
│                 └──────┬───────┘                                 │
│                        │                                         │
│          ┌─────────────┼─────────────┐                           │
│          ▼             ▼             ▼                           │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│   │ 🎨 FE    │ │ 🔧 BE    │ │ 🎨 FE    │  ← up to 3 in parallel  │
│   │ Feed pg  │ │ Post API │ │ New Post │                        │
│   │ +Mock    │ │          │ │ +Mock    │                        │
│   └────┬─────┘ └────┬─────┘ └────┬─────┘                        │
│        │            │            │                                │
│        └────────────┼────────────┘                                │
│                     ▼                                            │
│             ┌──────────────┐                                     │
│             │ 🔗 CONNECT    │  Replace Mock → real API            │
│             └──────┬───────┘                                     │
│                    ▼                                             │
│             ┌──────────────┐                                     │
│             │ ✅ VERIFY     │  Run acceptance tests               │
│             └──┬───────┬───┘                                     │
│                │       │                                         │
│           Pass ✅   Fail ❌                                       │
│                │       ▼                                         │
│                │  ┌──────────┐                                    │
│                │  │ 🩹 FIX    │  Fix → re-verify                  │
│                │  └────┬─────┘                                    │
│                ▼       │                                         │
│           Next Task ◀──┘                                         │
└─────────────────────────────────────────────────────────────────┘
                             │
                    All tasks done
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 MILESTONE REVIEW (fresh conversation)                         │
│    Zero "must fix" items → 🎉 COMPLETE, RUNNING APP               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 The 13-Agent Roster

### 🎛️ Orchestrator

| Agent | Model | Role |
|-------|-------|------|
| 🧠 **Orchestrator** | DeepSeek V4 Pro + thinking | Reads project state → decides next agent → dispatches via Function Calling → updates progress |

### 📋 Phase 0: The Planning Crew (strict serial, 6 agents)

| # | Agent | Output | Depends On | What It Does |
|---|-------|--------|------------|--------------|
| 1 | 📝 **PRD Expert** | `docs/PRD.md` | User idea | Vague idea → 9-chapter structured PRD with Given-When-Then acceptance criteria |
| 2 | 🏗️ **Tech Architect** | `docs/TECH_ARCHITECTURE.md` | PRD | Tech comparison tables, directory tree, MVP phases, zero-experience setup guide |
| 3 | 📏 **Coding Standards** | `docs/CODING_STANDARDS.md` | Tech Arch | 13-chapter coding bible with DO/DON'T examples, Cursor AI prompt template |
| 4 | 🗄️ **Schema Architect** | `docs/DB_SCHEMA.md` | Standards | Mermaid ER diagrams, PostgreSQL + SQLite DDL, RLS policies, sync strategies |
| 5 | 🔌 **API Contract** | `docs/API_CONTRACT.md` | Schema | Endpoint definitions, TypeScript types, error code system, weak-network resilience |
| 6 | 📋 **Task Decomposer** | `docs/TASK_BOOK.md` | All 5 docs | Phased task plan with dependency graph, Mock plan, copy-paste Claude Code prompts |

### 💻 Phase 1-N: The Build Crew (hybrid serial-parallel, 6 agents)

| Agent | Trigger | Delivers |
|-------|---------|----------|
| 🗃️ **Agent-DB** | Migration task in TASK_BOOK | Supabase `CREATE TABLE` + RLS SQL |
| 🔧 **Agent-BE** | Edge Function task | TypeScript Deno Edge Function code |
| 🎨 **Agent-FE** | Page/component task | React Native page + inline Mock data + `// TODO: TXX` markers |
| 🔗 **Agent-CONNECT** | FE + BE both complete | Mock → real API, snake_case/camelCase field mapping |
| ✅ **Agent-VERIFY** | Any coding task done | Per-criterion pass/fail report (no vague "looks good") |
| 🩹 **Agent-FIX** | Compile error / verify fail | Fix with exact file path + line number, minimal diff |

---

## 🎛️ The Orchestrator's Tool Belt

The Orchestrator doesn't guess—it uses 4 Function Calling tools to make data-driven scheduling decisions:

```
┌──────────────────────────────────────────────────────────────────┐
│                        🧠 Orchestrator                            │
│                                                                  │
│  ┌─────────────────────┐          ┌─────────────────────┐        │
│  │ read_project_state   │          │ read_file            │        │
│  │ "What's the current  │          │ "Show me what's in   │        │
│  │  status of every     │          │  this doc/code file" │        │
│  │  agent and task?"    │          │                      │        │
│  └─────────────────────┘          └─────────────────────┘        │
│                                                                  │
│  ┌─────────────────────┐          ┌─────────────────────┐        │
│  │ route_to_agent       │          │ update_state         │        │
│  │ "Dispatch Agent-X    │          │ "Mark task complete,  │        │
│  │  with this task +    │          │  record failure,      │        │
│  │  all required docs"  │          │  update retry count"  │        │
│  └─────────────────────┘          └─────────────────────┘        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### One Complete Scheduling Cycle

```
User: "I want to build a running tracker app..."
                │
                ▼
┌──────────────────────────────┐
│ Orchestrator reads state     │
│ → PRD.md missing             │
│ → Phase 0, Step 1 needed     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Orchestrator outputs:        │
│ 📊 Status: Phase 0, Step 1   │
│ 🗺️ Plan:   Route to PRD      │
│    Expert — no input docs    │
│    needed, just the user's   │
│    product idea              │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Function Calling: route_to_agent(    │
│   agent="prd_expert",        │
│   task="Generate PRD for     │
│         running tracker...", │
│   plan={reason: "...",       │
│         expected_output:     │
│         "docs/PRD.md"}       │
│ )                            │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Worker executes:             │
│ 1. Load prd_expert.md prompt │
│ 2. Stream PRD to terminal    │
│ 3. Save to docs/PRD.md       │
│ 4. Mark state: completed     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Orchestrator: update_state() │
│ ➡️ Next: Tech Architect      │
│    (input: docs/PRD.md)      │
└──────────────────────────────┘
```

---

## ⚡ Quick Start

### The Full Pipeline (Recommended)

```bash
git clone https://github.com/withAIx/DeepSeek-AppForge.git
cd AppForge/project-orchestrator

pip install -r requirements.txt
cp .env.example .env   # add your DEEPSEEK_API_KEY

python main.py
```

```text
> I want a calorie-tracking app with barcode scanning and meal logging...

The Orchestrator fires up and dispatches:
  Agent-PRD → Agent-ARCH → Agent-STANDARDS → Agent-SCHEMA
  → Agent-API → Agent-DECOMP → Coding begins...
```

### Notes for Users in China

If GitHub is slow, use a mirror:
```bash
git clone https://ghproxy.com/https://github.com/withAIx/DeepSeek-AppForge.git
```

DeepSeek API requires a proxy or API forwarding service when accessed from mainland China. Set your proxy before running:
```bash
export HTTPS_PROXY=http://127.0.0.1:7890   # your proxy address
python main.py
```

### Individual Agent (Python Library)

```bash
pip install -e .
```

```python
from agents import PRDExpert, MobileArchitect, TaskDecomposer

prd = PRDExpert()
result = prd.run("I want to build a food delivery app for campus students...")
print(result)
```

### CLI

```bash
python -m agents.cli run prd-expert "Write a PRD for a pet adoption app"
python -m agents.cli list                          # list all 10 agents
python -m agents.cli run-stream task-decomposer "..."  # streaming mode
```

### Claude Code Skill

Copy any `.md` file from `skills/` into your Claude Code skills directory. Activate it mid-conversation:

```
/activate prd-expert
```

---

## 🛡️ Resilience: Graceful Degradation

Every agent gets **2 retries**. If both fail, the pipeline doesn't stop—it degrades gracefully:

| Agent | Degradation Strategy |
|-------|---------------------|
| PRD Expert | Minimal PRD: product overview + P0 feature list only |
| Tech Architect | Default stack: Expo + Supabase + Zustand + NativeWind |
| Coding Standards | Minimal rule set: naming conventions + directory tree + banned words |
| Schema Architect | Core tables only: profiles + top 1-2 business tables |
| API Contract | Auth endpoints + the single most critical business endpoint |
| Task Decomposer | Simplified task book: task IDs + names + dependencies, no Claude Code prompts |

Degraded outputs are marked `"degraded": true` in `project_state.json`. Downstream agents work with what's available—the assembly line keeps moving.

---

## 🚦 Conflict Resolution

When documents disagree (e.g., a field name differs between Schema and API Contract):

```
Level 1: PRD           ← The final authority on feature behavior
Level 2: Tech Arch     ← Architecture choices cannot be overridden downstream
Level 3: Coding Standards ← Naming style takes precedence here
Level 4: Schema        ← Field names are canonical from here
Level 5: API Contract  ← Interface format follows from above
```

Process: identify conflict → consult the higher-level document → fix the lower-level document → log the decision in `project_state.json`. The LLM never decides which side "looks more reasonable."

---

## 📂 Repo Layout

```
AppForge/                                  # ← you are here
│
├── README.md                              # this page
├── pyproject.toml                         # Python package config
│
├── 📦 src/agents/                         # Python library (programmatic access)
│   ├── _base.py                           # BaseAgent + AgentConfig
│   ├── prd_expert.py .. orchestrator.py   # 10 agent implementations
│   └── cli.py                             # click-based CLI
│
├── ⚒️ project-orchestrator/               # The full assembly line
│   ├── README.md                          # detailed orchestrator docs
│   ├── main.py                            # interactive REPL entry point
│   ├── orchestrator.py                    # Function Calling scheduling loop
│   ├── worker.py                          # agent executor (stream + save)
│   ├── state.py                           # JSON state machine
│   ├── config.py                          # 12-agent registry + dep graph
│   ├── agents/                            # 13 system prompt files (.md)
│   │   ├── orchestrator.md
│   │   ├── phase0/                        # 6 planning agent prompts
│   │   └── phase1n/                       # 6 coding agent prompts
│   └── docs/                              # auto-generated output documents
│
└── 📋 skills/                             # Claude Code skill files (10 agents)
    ├── prd-expert.md
    ├── mobile-architect.md
    └── ...
```

---

## 📄 License

MIT — forge away.
