# 🚀 Project Orchestrator v2.0

> **Full-lifecycle AI orchestration system — from product concept to a complete, runnable app**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Anthropic SDK](https://img.shields.io/badge/Anthropic%20SDK-0.40+-green.svg)](https://github.com/anthropics/anthropic-sdk-python)

<p align="center">
  <b>English</b> · <a href="README_CN.md">中文</a>
</p>

---

## 🤔 What is this?

**Project Orchestrator** is an Orchestrator-Workers architecture system powered by Anthropic Claude that turns a single sentence — "I have an app idea" — into a **complete, runnable app**.

It is not a single AI agent, but an **orchestration system that coordinates 13 specialized AI agents**. Each agent has a carefully crafted system prompt, explicit input/output contracts, and validation gates.

> Imagine you have a 13-person full-stack dev team: 1 project manager + 6 planning experts + 6 execution engineers. You just tell the project manager "I want to build a food delivery app," and the entire team starts working autonomously.

---

## 🎯 Core Capabilities

| Capability | Description |
|------|------|
| 🧭 **Full-Lifecycle Management** | From product concept → six planning documents → code execution → verified delivery, all in one pipeline |
| 🔗 **Strict Serial Chain** | Phase 0's six-step document generation is strictly ordered; each step's output feeds the next step |
| ⚡ **Hybrid Serial/Parallel** | Phase 1-N coding phase auto-detects parallelizable tasks for maximum execution efficiency |
| 🔧 **Tool Use Scheduling** | Orchestrator dynamically routes sub-agents via Claude's Tool Use mechanism |
| 📊 **State Persistence** | JSON file tracks progress, retry count, and degradation flags for every task |
| 🛡️ **Three-Layer Verification** | Pre-execution review → node-level output validation → milestone independent review |
| 🔄 **Failure Degradation** | Each agent retries up to 2 times; on failure, automatically degrades without blocking the pipeline |

---

## 🏗️ Architecture Overview

```
                          ┌──────────────────────────┐
                          │    🧠 Orchestrator        │
                          │   (Claude Opus 4.6)       │
                          │                          │
                          │  Tool Use-driven dispatch │
                          │  Auto-detects current     │
                          │  phase / next step        │
                          └────┬───────┬─────────┬───┘
                               │       │         │
                    route_to_agent  read_project_state  update_state
                               │                         │
          ┌────────────────────┼─────────────────────────┤
          │                    │                         │
    ┌─────▼──────┐    ┌───────▼────────┐    ┌───────────▼───────────┐
    │  Phase 0   │    │   Phase 1-N     │    │  project_state.json   │
    │ Document   │    │  Code Execution │    │  Progress / Retries /  │
    │ Generation │    │  (Hybrid S/P)   │    │  Degradation Tracking  │
    │ (Strictly  │    │                 │    └───────────────────────┘
    │  Serial)   │    │                 │
    └────────────┘    └────────────────┘
```

### Phase 0: Document Generation (Strictly Serial — 6 Steps)

```
User Concept
    │
    ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ ① PRD Expert  │────▶│ ② Tech Architect  │────▶│ ③ Coding Standards│
│ docs/PRD.md  │     │ TECH_ARCHITECTURE │     │ CODING_STANDARDS │
└──────────────┘     └──────────────────┘     └────────┬─────────┘
                                                       │
              ┌────────────────────────────────────────┘
              ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ ④ Schema Arch │────▶│ ⑤ API Contract   │────▶│ ⑥ Task Decomposer │
│ DB_SCHEMA.md │     │ API_CONTRACT.md  │     │ TASK_BOOK.md     │
└──────────────┘     └──────────────────┘     └──────────────────┘
```

### Phase 1-N: Code Execution (Hybrid Serial/Parallel)

```
TASK_BOOK.md
    │
    ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Agent-DB │───▶│ Agent-FE │║│ Agent-BE │  ← Frontend/Backend can run in parallel
│ DB Migr  │    │ Frontend │║│ Backend   │
└──────────┘    └────┬─────┘║└────┬─────┘
                     │      ║     │
                     └──────╫─────┘
                            ▼
                     ┌──────────────┐
                     │ Agent-CONNECT │
                     │  FE/BE Link   │
                     └──────┬───────┘
                            ▼
                     ┌──────────────┐
                     │ Agent-VERIFY  │────── FAIL ──▶ Agent-FIX
                     │  Verification │                  Bug Fix
                     └──────┬───────┘
                            │ PASS
                            ▼
                     ┌──────────────┐
                     │ Agent-REVIEW  │
                     │ Indep. Review │
                     │ (New Session) │
                     └──────────────┘
                            │
                            ▼
                    🎉 Complete, Runnable APP
```

---

## 👥 Full Agent Roster

### 🧭 Orchestrator (Master Scheduler)

| Agent | Model | Responsibility |
|-------|------|------|
| 🎛️ Orchestrator | Claude Opus 4.6 | Read project state, dynamically route sub-agents, manage serial/parallel decisions |

### 📋 Phase 0: Planning Expert Team (6 agents, strictly serial)

| # | Agent | Output Document | Input Dependency | Core Responsibility |
|---|-------|---------|---------|---------|
| 1 | 📝 PRD Expert | `docs/PRD.md` | User concept | Transform vague ideas into a 9-chapter structured PRD with Given-When-Then acceptance criteria |
| 2 | 🏗️ Tech Architect | `docs/TECH_ARCHITECTURE.md` | PRD | Tech stack comparison & rationale, directory structure, MVP phase breakdown, environment setup |
| 3 | 📏 Coding Standards Expert | `docs/CODING_STANDARDS.md` | PRD + Tech Architecture | 13-chapter coding standards with DO/DON'T examples and Cursor Prompt templates |
| 4 | 🗄️ Schema Architect | `docs/DB_SCHEMA.md` | PRD + Tech Architecture + Standards | ER diagram, PostgreSQL/SQLite DDL, RLS policies, Redis cache keys |
| 5 | 🔌 API Contract Architect | `docs/API_CONTRACT.md` | PRD + Tech Architecture + Schema + Standards | API endpoint definitions, TypeScript types, error code system, weak-network fault tolerance |
| 6 | 📋 Task Decomposer | `docs/TASK_BOOK.md` | All five prior documents | Phased task book, dependency graph, mock strategy, copy-paste ready Claude Code instructions |

### 💻 Phase 1-N: Coding Execution Team (6 agents, hybrid serial/parallel)

| Agent | Trigger Condition | Output |
|-------|---------|------|
| 🗃️ Agent-DB | Task book database migration tasks | Supabase DDL SQL + RLS policies |
| 🔧 Agent-BE | Backend Edge Function tasks | TypeScript Edge Function code |
| 🎨 Agent-FE | Frontend page/component tasks | React Native pages + mock data |
| 🔗 Agent-CONNECT | Both frontend & backend complete | Replace mocks with real API calls |
| ✅ Agent-VERIFY | After any coding task completes | Item-by-item verification report |
| 🩹 Agent-FIX | Build errors / verification failures | Fix plan with line-level precision |

---

## ⚡ Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/withAIx/AppForge.git
cd AppForge/project-orchestrator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key

```bash
cp .env.example .env
# Edit .env and fill in your ANTHROPIC_API_KEY
```

`.env` content:

```env
ANTHROPIC_API_KEY=sk-ant-...
ORCHESTRATOR_MODEL=claude-opus-4-6    # Orchestrator model
WORKER_MODEL_HEAVY=claude-opus-4-6    # Document generation agent model
WORKER_MODEL_LIGHT=claude-sonnet-4-6  # Code execution agent model
PROJECT_NAME=my_app                    # Project name
```

### 4. Launch the system

```bash
python main.py
```

### 5. Start your first project

```
> I want to build a running tracker app where users can log routes, pace, calories burned, and compete with friends

Orchestrator will automatically:
1. Analyze current state (project_state.json)
2. Output status report and scheduling plan
3. Call Agent-PRD to generate the product requirements document
4. Save output to docs/PRD.md
5. Prompt for the next step
```

---

## 📊 Interactive Demo

```text
$ python main.py

🚀 Project Orchestrator v2.0
Orchestrator-Workers Full-Lifecycle APP Development Orchestration System

Commands:
  status  → View current development progress
  exit    → Exit the system
  anything else → Send to Orchestrator for analysis and scheduling

┌───────────────── 📊 Project Development Progress ─────────────────┐
│ Agent              │ Document                    │ Status         │
│─────────────────── ┼──────────────────────────── ┼───────────────│
│ PRD Expert         │ docs/PRD.md                │ ⏳ Pending     │
│ Tech Architect     │ docs/TECH_ARCHITECTURE.md   │ ⏳ Pending     │
│ Coding Standards   │ docs/CODING_STANDARDS.md    │ ⏳ Pending     │
│ Schema Architect   │ docs/DB_SCHEMA.md           │ ⏳ Pending     │
│ API Contract       │ docs/API_CONTRACT.md        │ ⏳ Pending     │
│ Task Decomposer    │ docs/TASK_BOOK.md           │ ⏳ Pending     │
└──────────────────────────────────────────────────────────────────┘

➡️  Phase 0 In Progress: Next → PRD Expert

> I want to build a running tracker app

🧠 Orchestrator analyzing...

┌───────────────── 📊 Orchestrator ─────────────────┐
│                                                   │
│ 📊 Current State: Phase 0 Document Generation      │
│ Step 1: PRD Expert — turn product concept into     │
│         a structured PRD                           │
│                                                   │
│ Routing reason: docs/PRD.md does not exist;        │
│ calling Agent-PRD per Rule 0                       │
│ Expected output: 9-chapter PRD with                │
│ Given-When-Then acceptance criteria                │
│                                                   │
└───────────────────────────────────────────────────┘

┌───────────────── 🗺️ Scheduling Plan ─────────────────┐
│ Routing to: PRD Expert                                │
│ Reason: Product concept received; must generate PRD   │
│         as the baseline input for all subsequent      │
│         experts                                       │
│ Expected output: docs/PRD.md                          │
└──────────────────────────────────────────────────────┘

🤖 PRD Expert starting up...
[Streaming full PRD document...]

✅ Document saved: docs/PRD.md

➡️  Next: Tech Architect (input: docs/PRD.md)
```

---

## 🔧 System Architecture

```
project-orchestrator/
│
├── main.py                  # CLI interactive entry point (REPL loop)
├── orchestrator.py          # Master scheduler (Claude Tool Use loop)
├── worker.py                # Sub-agent execution wrapper (streaming + save)
├── state.py                 # JSON state machine (progress tracking + retries/degradation)
├── config.py                # 12-agent registry + dependency resolution
│
├── agents/                  # System prompt library (13 .md files)
│   ├── orchestrator.md      # Master scheduler prompt
│   ├── phase0/              # 6 document-generation expert prompts
│   │   ├── prd_expert.md          (15KB, 387 lines)
│   │   ├── tech_architect.md      (16KB, 413 lines)
│   │   ├── coding_standards.md    (22KB, 694 lines)
│   │   ├── schema_architect.md    (26KB, 739 lines)
│   │   ├── api_contract.md        (29KB, 901 lines)
│   │   └── task_decomposer.md     (15KB, 381 lines)
│   └── phase1n/             # 6 code-execution agent prompts
│       ├── agent_db.md
│       ├── agent_be.md
│       ├── agent_fe.md
│       ├── agent_connect.md
│       ├── agent_verify.md
│       └── agent_fix.md
│
├── docs/                    # Document output directory (auto-created)
├── project_state.json       # Project state file (auto-created and managed)
├── requirements.txt
└── .env.example
```

---

## 🎛️ Orchestrator's Tool Use Mechanism

The Orchestrator uses Claude's native Tool Use to make scheduling decisions. It has 4 tools:

| Tool | Purpose | When Called |
|------|------|---------|
| `read_project_state` | Read current `project_state.json` | Every turn start, to understand project progress |
| `route_to_agent` | Dispatch a sub-agent to execute a task | After analysis, when the next step is determined |
| `update_state` | Update project state file | After agent execution completes, to record progress |
| `read_file` | Read project file contents | When document content or code needs inspection |

Scheduling flow:

```
User input → Orchestrator reads state → Analyzes & plans
    → Calls route_to_agent (with plan parameter)
    → Worker executes sub-agent (streaming output + auto-save)
    → Orchestrator updates project_state.json
    → Outputs next-step preview
```

---

## 🔄 Failure Handling Strategy

### Retry & Degradation

Each agent retries at most **2 times**. After 2 full failures:

| Agent | Degradation Strategy |
|-------|---------|
| PRD Expert | Generate "Minimum PRD" (product overview + P0 feature list) |
| Tech Architect | Use default tech stack (Expo + Supabase + Zustand + NativeWind) |
| Coding Standards Expert | Use minimum standards set (naming conventions + directory structure + banned words list) |
| Schema Architect | Generate only profiles table + 1–2 core business tables |
| API Contract Architect | Generate only auth module + the most critical business endpoints |
| Task Decomposer | Generate simplified task book (task ID + name + dependencies) |

Degraded versions are marked `"degraded": true` in `project_state.json`. Subsequent agents continue working from the degraded version without blocking the pipeline.

---

## 🚦 Conflict Resolution Priority

When contradictions arise between documents (common issue: inconsistent field names), resolve by this priority order:

```
Level 1: PRD Document      ← Final arbiter of feature behavior
Level 2: Tech Architecture ← Architecture decisions are not overridable by downstream docs
Level 3: Coding Standards  ← Naming style follows standards as authoritative
Level 4: Schema Document   ← Field names follow Schema as authoritative
Level 5: API Contract      ← Endpoint formats follow Contract as authoritative
```

Process: Identify conflict → Check PRD for business intent → Defer to higher-level document → Record conflict decision in `project_state.json`

---

## 📝 Common Commands

```bash
# Launch the system
python main.py

# In-system commands
> status          # View current development progress
> exit            # Exit the system

# Reset project (delete all docs and state, start fresh)
rm -rf docs/ project_state.json
python main.py
```

---

## 🔗 Relationship with the agents Library

This system is the companion orchestration system for the [AppForge](https://github.com/withAIx/AppForge) Python library:

| Component | Purpose |
|------|------|
| `agents/` Python library | Programmatic invocation of individual agents (`from agents import PRDExpert`) |
| `project-orchestrator/` | 13-agent full-lifecycle orchestration system (Tool Use auto-scheduling) |

Each agent's system prompt in the `agents/` library is reused as a worker prompt in `project-orchestrator/agents/phase0/`.

---

## 📄 License

MIT
