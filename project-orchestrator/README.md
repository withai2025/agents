# 🚀 Project Orchestrator v2.0

> **从产品构想到完整可运行 APP 的全生命周期 AI 编排系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![DeepSeek SDK](https://img.shields.io/badge/DeepSeek%20SDK-0.40+-green.svg)](https://github.com/openais/openai-sdk-python)

---

## 🤔 这是什么？

**Project Orchestrator** 是一个基于 DeepSeek Claude 的 Orchestrator-Workers 架构系统，
将「我有一个 APP 想法」这一句话，转化为一个**完整可运行的 APP**。

它不是单个 AI Agent，而是一个**编排 13 个专业 AI Agent 的总调度系统**。每个 Agent 都拥有经过精心设计的系统提示词、明确的输入/输出契约、以及校验门禁。

> 想象你有一个 13 人的全栈开发团队：1 个项目经理 + 6 个规划专家 + 6 个执行工程师。你只需告诉项目经理「我想做一个外卖 APP」，整个团队就会自动运转起来。

---

## 🎯 核心能力

| 能力 | 描述 |
|------|------|
| 🧭 **全生命周期管理** | 从产品构想 → 六份规划文档 → 编码执行 → 验收交付，一站式覆盖 |
| 🔗 **严格串行链** | Phase 0 六步文档生成严格有序，每步产出是下一步的输入 |
| ⚡ **混合串并行** | Phase 1-N 编码阶段自动识别可并行任务，最大化执行效率 |
| 🔧 **Tool Use 调度** | Orchestrator 通过 DeepSeek Tool Use 机制动态路由子 Agent |
| 📊 **状态持久化** | JSON 文件记录每个任务的进度、重试次数、降级标记 |
| 🛡️ **三层验证** | 执行前审查 → 节点级输出校验 → 里程碑独立审查 |
| 🔄 **失败降级** | 每个 Agent 最多重试 2 次，失败后自动降级、不阻塞流程 |

---

## 🏗️ 架构总览

```
                          ┌──────────────────────────┐
                          │    🧠 Orchestrator        │
                          │   (DeepSeek V4 Pro 4.7)       │
                          │                          │
                          │  Tool Use 驱动调度决策     │
                          │  自动判断当前阶段/下一步    │
                          └────┬───────┬─────────┬───┘
                               │       │         │
                    route_to_agent  read_project_state  update_state
                               │                         │
          ┌────────────────────┼─────────────────────────┤
          │                    │                         │
    ┌─────▼──────┐    ┌───────▼────────┐    ┌───────────▼───────────┐
    │  Phase 0   │    │   Phase 1-N     │    │   project_state.json    │
    │ 文档生成阶段│    │  编码执行阶段     │    │  进度/重试/降级追踪     │
    │ (严格串行)  │    │  (混合串并行)    │    └───────────────────────┘
    └────────────┘    └────────────────┘
```

### Phase 0：文档生成（严格串行 6 步）

```
用户构想
    │
    ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ ① PRD 专家    │────▶│ ② 技术架构师      │────▶│ ③ 编码规范专家    │
│ docs/PRD.md  │     │ TECH_ARCHITECTURE │     │ CODING_STANDARDS │
└──────────────┘     └──────────────────┘     └────────┬─────────┘
                                                       │
              ┌────────────────────────────────────────┘
              ▼
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ ④ Schema 架构师│────▶│ ⑤ API 契约架构师  │────▶│ ⑥ 任务拆分专家    │
│ DB_SCHEMA.md │     │ API_CONTRACT.md  │     │ TASK_BOOK.md     │
└──────────────┘     └──────────────────┘     └──────────────────┘
```

### Phase 1-N：编码执行（混合串并行）

```
TASK_BOOK.md
    │
    ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Agent-DB │───▶│ Agent-FE │║│ Agent-BE │  ← 前后端可并行
│ 数据库迁移│    │ 前端页面  │║│ 后端接口  │
└──────────┘    └────┬─────┘║└────┬─────┘
                     │      ║     │
                     └──────╫─────┘
                            ▼
                     ┌──────────────┐
                     │ Agent-CONNECT │
                     │   前后端联调   │
                     └──────┬───────┘
                            ▼
                     ┌──────────────┐
                     │ Agent-VERIFY  │────── 不通过 ──▶ Agent-FIX
                     │   验收测试    │                   报错修复
                     └──────┬───────┘
                            │ 通过
                            ▼
                     ┌──────────────┐
                     │ Agent-REVIEW  │
                     │ 独立审查(新对话)│
                     └──────────────┘
                            │
                            ▼
                    🎉 完整可运行的 APP
```

---

## 👥 Agent 全名册

### 🧭 Orchestrator（总调度器）

| Agent | 模型 | 职责 |
|-------|------|------|
| 🎛️ Orchestrator | DeepSeek V4 Pro 4.7 | 读取项目状态、动态路由子 Agent、管理串并行决策 |

### 📋 Phase 0：规划专家团队（6 人，严格串行）

| # | Agent | 输出文档 | 输入依赖 | 核心职责 |
|---|-------|---------|---------|---------|
| 1 | 📝 PRD 专家 | `docs/PRD.md` | 用户构想 | 将模糊想法转化为 9 章节结构化 PRD，Given-When-Then 验收标准 |
| 2 | 🏗️ 技术架构师 | `docs/TECH_ARCHITECTURE.md` | PRD | 技术选型对比论证、目录结构、MVP 阶段划分、环境搭建步骤 |
| 3 | 📏 编码规范专家 | `docs/CODING_STANDARDS.md` | PRD + 技术方案 | 13 章节编码规范，含 DO/DON'T 示例、Cursor Prompt 模板 |
| 4 | 🗄️ Schema 架构师 | `docs/DB_SCHEMA.md` | PRD + 技术方案 + 规范 | ER 图、PostgreSQL/SQLite DDL、RLS 策略、Redis 缓存键 |
| 5 | 🔌 API 契约架构师 | `docs/API_CONTRACT.md` | PRD + 技术方案 + Schema + 规范 | API 接口定义、TypeScript 类型、错误码体系、弱网容错 |
| 6 | 📋 任务拆分专家 | `docs/TASK_BOOK.md` | 全部五份文档 | 分阶段任务书、依赖图、Mock 策略、可复制 Claude Code 指令 |

### 💻 Phase 1-N：编码执行团队（6 人，混合串并行）

| Agent | 触发条件 | 产出 |
|-------|---------|------|
| 🗃️ Agent-DB | 任务书数据库迁移任务 | Supabase 建表 SQL + RLS 策略 |
| 🔧 Agent-BE | 后端 Edge Function 任务 | TypeScript Edge Function 代码 |
| 🎨 Agent-FE | 前端页面/组件任务 | React Native 页面 + Mock 数据 |
| 🔗 Agent-CONNECT | 前后端均完成时 | Mock 替换为真实 API 调用 |
| ✅ Agent-VERIFY | 任意编码任务完成后 | 逐条验收报告 |
| 🩹 Agent-FIX | 编译报错/验收失败 | 精确到行号的修复方案 |

---

## ⚡ 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/withAIx/agents.git
cd agents/project-orchestrator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY
```

`.env` 内容：

```env
DEEPSEEK_API_KEY=sk-ant-...
ORCHESTRATOR_MODEL=deepseek-v4-pro    # 总调度器模型
WORKER_MODEL_HEAVY=deepseek-v4-pro    # 文档生成 Agent 模型
WORKER_MODEL_LIGHT=deepseek-v4-flash   # 编码执行 Agent 模型
PROJECT_NAME=my_app                    # 项目名称
```

### 4. 启动系统

```bash
python main.py
```

### 5. 开始你的第一个项目

```
> 我想做一个跑步打卡 APP，用户可以记录跑步路线、配速、消耗卡路里，还能加好友互相PK

Orchestrator 会自动：
1. 分析当前状态（project_state.json）
2. 输出状态报告和调度计划
3. 调用 Agent-PRD 生成产品需求文档
4. 保存输出到 docs/PRD.md
5. 提示下一步操作
```

---

## 📊 交互示例

```text
$ python main.py

🚀 Project Orchestrator v2.0
Orchestrator-Workers APP 全生命周期开发编排系统

命令：
  status  → 查看当前开发进度
  exit    → 退出系统
  其他输入 → 交给 Orchestrator 分析并调度

┌───────────────── 📊 项目开发进度 ─────────────────┐
│ Agent          │ 文档                       │ 状态    │
│─────────────── ┼─────────────────────────── ┼────────│
│ PRD 专家       │ docs/PRD.md               │ ⏳ 待启动 │
│ 技术架构师     │ docs/TECH_ARCHITECTURE.md  │ ⏳ 待启动 │
│ 编码规范专家   │ docs/CODING_STANDARDS.md   │ ⏳ 待启动 │
│ Schema 架构师  │ docs/DB_SCHEMA.md          │ ⏳ 待启动 │
│ API 契约架构师 │ docs/API_CONTRACT.md       │ ⏳ 待启动 │
│ 任务拆分专家   │ docs/TASK_BOOK.md          │ ⏳ 待启动 │
└─────────────────────────────────────────────────────┘

➡️  Phase 0 进行中：下一步 → PRD 专家

> 我想做一个跑步打卡APP

🧠 Orchestrator 分析中...

┌───────────────── 📊 Orchestrator ─────────────────┐
│                                                   │
│ 📊 当前状态：Phase 0 文档生成阶段                    │
│ 第一步：PRD 专家 — 将产品构想转化为结构化 PRD         │
│                                                   │
│ 路由理由：docs/PRD.md 不存在，根据规则 0 调用 Agent-PRD│
│ 预期产出：9 章节 PRD 文档，含 Given-When-Then 验收标准 │
│                                                   │
└───────────────────────────────────────────────────┘

┌───────────────── 🗺️ 调度计划 ─────────────────┐
│ 路由到：PRD 专家                                │
│ 理由：产品构想已收到，需要先生成 PRD 文档作为所有   │
│       后续专家的输入基准                          │
│ 预期产出：docs/PRD.md                           │
└───────────────────────────────────────────────┘

🤖 PRD 专家 启动中...
[流式输出完整 PRD 文档...]

✅ 文档已保存：docs/PRD.md

➡️  下一步：技术架构师（输入：docs/PRD.md）
```

---

## 🔧 系统架构

```
project-orchestrator/
│
├── main.py                  # CLI 交互式入口（REPL 循环）
├── orchestrator.py          # 总调度器（DeepSeek Tool Use 循环）
├── worker.py                # 子 Agent 执行封装（流式 + 保存）
├── state.py                 # JSON 状态机（进度追踪 + 重试/降级）
├── config.py                # 12 Agent 注册表 + 依赖解析
│
├── agents/                  # 系统提示词库（13 个 .md 文件）
│   ├── orchestrator.md      # 总调度器提示词
│   ├── phase0/              # 6 个文档生成专家提示词
│   │   ├── prd_expert.md          (15KB, 387 行)
│   │   ├── tech_architect.md      (16KB, 413 行)
│   │   ├── coding_standards.md    (22KB, 694 行)
│   │   ├── schema_architect.md    (26KB, 739 行)
│   │   ├── api_contract.md        (29KB, 901 行)
│   │   └── task_decomposer.md     (15KB, 381 行)
│   └── phase1n/             # 6 个编码执行 Agent 提示词
│       ├── agent_db.md
│       ├── agent_be.md
│       ├── agent_fe.md
│       ├── agent_connect.md
│       ├── agent_verify.md
│       └── agent_fix.md
│
├── docs/                    # 文档输出目录（自动创建）
├── project_state.json       # 项目状态文件（自动创建和管理）
├── requirements.txt
└── .env.example
```

---

## 🎛️ Orchestrator 的 Tool Use 机制

Orchestrator 通过 DeepSeek 原生 Tool Use 实现调度决策。它拥有 4 个工具：

| Tool | 用途 | 调用时机 |
|------|------|---------|
| `read_project_state` | 读取当前 `project_state.json` | 每轮对话开始时，了解项目进度 |
| `route_to_agent` | 调度指定子 Agent 执行任务 | 分析后确定下一步应执行哪个 Agent |
| `update_state` | 更新项目状态文件 | Agent 执行完成后，记录进度 |
| `read_file` | 读取项目文件内容 | 需要检查文档内容或代码时 |

调度流程：

```
用户输入 → Orchestrator 读取状态 → 分析调度计划
    → 调用 route_to_agent（携带 plan 参数）
    → Worker 执行子 Agent（流式输出 + 自动保存）
    → Orchestrator 更新 project_state.json
    → 输出下一步预告
```

---

## 🔄 失败处理策略

### 重试与降级

每个 Agent 最多重试 **2 次**。2 次全部失败后：

| Agent | 降级策略 |
|-------|---------|
| PRD 专家 | 生成「最小 PRD」（产品概述 + P0 功能列表） |
| 技术架构师 | 使用默认技术栈（Expo + Supabase + Zustand + NativeWind） |
| 编码规范专家 | 使用最小规范集（命名规范 + 目录结构 + 禁用词列表） |
| Schema 架构师 | 只生成 profiles 表 + 1-2 张核心业务表 |
| API 契约架构师 | 只生成认证模块 + 最核心业务接口 |
| 任务拆分专家 | 生成简化任务书（任务 ID + 名称 + 依赖关系） |

降级版本在 `project_state.json` 中标记 `"degraded": true`，后续 Agent 基于降级版继续执行，不阻塞流程。

---

## 🚦 冲突解决优先级

当多份文档之间出现矛盾时（常见：字段名不一致），按以下优先级裁决：

```
Level 1: PRD 文档      ← 功能行为的最终裁决
Level 2: 技术方案文档   ← 架构选型不可被后续覆盖
Level 3: 编码规范文档   ← 命名风格以规范为准
Level 4: Schema 文档    ← 字段名以 Schema 为准
Level 5: API 契约文档   ← 接口格式以契约为准
```

处理步骤：识别冲突 → 查 PRD 确认业务意图 → 以更高层级文档为准 → 记录冲突决策到 `project_state.json`

---

## 📝 常用命令

```bash
# 启动系统
python main.py

# 系统内命令
> status          # 查看当前开发进度
> exit            # 退出系统

# 重置项目（删除所有文档和状态，重新开始）
rm -rf docs/ project_state.json
python main.py
```

---

## 🔗 与 agents 库的关系

本系统是 [agents](https://github.com/withAIx/agents) Python 库的配套编排系统：

| 组件 | 用途 |
|------|------|
| `agents/` Python 库 | 单个 Agent 的程序化调用（`from agents import PRDExpert`） |
| `project-orchestrator/` | 13 Agent 全生命周期编排系统（Tool Use 自动调度） |

`agents/` 库中的每个 Agent 的系统提示词，在 `project-orchestrator/agents/phase0/` 中作为 Worker 提示词被复用。

---

## 📄 License

MIT
