# ⚒️ AppForge

> **用 13 个 AI 智能体，将你的 APP 构想锻造成可运行的完整产品。**
>
> 一句话输入 → 完整 APP 输出。零人工编码。

<p align="center">
  <a href="https://github.com/withAIx/DeepSeek-AppForge/stargazers"><img src="https://img.shields.io/github/stars/withAIx/DeepSeek-AppForge?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/withAIx/DeepSeek-AppForge/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python 3.11+"></a>
  <a href="https://github.com/openai/openai-python"><img src="https://img.shields.io/badge/OpenAI%20SDK-1.0+-green.svg" alt="OpenAI SDK (DeepSeek compatible)"></a>
  <a href="https://github.com/withAIx/DeepSeek-AppForge/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

<p align="center">
  <a href="README.md">English</a> · <b>中文</b>
</p>

> 💡 **寻找 Claude（Anthropic）版本？** → [AppForge](https://github.com/withAIx/AppForge)

---

## 🤔 AppForge 是什么？

AppForge 是一条 **AI 驱动的 APP 开发流水线**。你用日常语言描述想要什么——剩下的事情交给 13 个 AI 智能体，它们自动完成从产品构想到可运行 APP 的全过程。

不再是零敲碎打地用 AI 写代码。AppForge 管理整个**产品生命周期**：

```
你说：                              AppForge 自动产出：
"我想做一个跑步打卡APP，              ✅ docs/PRD.md          （9 章节产品需求文档）
 可以记录路线、配速、                  ✅ docs/TECH_ARCHITECTURE （技术选型 + 目录结构）
 消耗卡路里，加好友PK"                ✅ docs/CODING_STANDARDS  （编码规范，DO/DON'T 示例）
                                      ✅ docs/DB_SCHEMA         （ER 图 + 建表 SQL + RLS）
                                      ✅ docs/API_CONTRACT      （接口定义 + TS 类型 + 错误码）
                                      ✅ docs/TASK_BOOK         （分阶段任务书 + Mock 方案）
                                      ✅ 完整可运行的 React Native APP
```

> **想象你雇了一个 13 人的全栈团队**——1 个 Tech Lead + 6 个架构师 + 6 个工程师。他们不睡觉、不抱怨、端到端交付。

---

## 🎯 为什么选择 AppForge？

| 以前你需要... | AppForge 替你... |
|-------------|-----------------|
| 手写 PRD、技术方案、编码规范 | **6 个规划智能体**严格串行生成全部 6 份文档，每份自动校验 |
| 自己想"下一步该干什么" | **Orchestrator** 读取项目状态，自动判断并调度正确的智能体 |
| 在 5 个 AI 工具之间来回切换 | **一条流水线**：一次对话，13 个智能体，零上下文切换 |
| 祈祷代码质量别崩 | **CODING_STANDARDS.md** 首先生成，后续每个编码智能体强制执行 |
| 手动追踪项目进度 | **project_state.json** 追踪每个任务、重试次数、降级状态 |
| 项目半途而废 | **优雅降级**：失败的智能体产出简化版，不阻塞流水线 |

---

## 🚀 基于 DeepSeek V4 深度优化

AppForge 全部 13 个智能体基于 **DeepSeek V4 模型家族**构建，以极低成本提供超强性能。

### 为什么选择 DeepSeek？

| 能力 | DeepSeek V4 Pro | Claude Opus 4 | 优势 |
|------|----------------|---------------|------|
| 上下文窗口 | **1,000,000 tokens** | 200,000 tokens | 5 倍大——可一次性加载全部 6 份规划文档 |
| 输入价格（每百万 token） | **$1.74** | $15.00 | 便宜 8.6 倍 |
| 输出价格（每百万 token） | **$3.48** | $75.00 | 便宜 21.5 倍 |
| 思考模式 | **thinking / thinking_max** | Extended thinking | 按 Agent 粒度精细控制 |
| 前缀缓存 | **自动（80-92% 折扣）** | 手动 | Phase 0 串行链节省约 60% 成本 |
| 中文能力 | **母语级** | 良好 | 系统提示词全部为中文 |

### 智能模型路由

不是所有任务都需要最强大脑。AppForge 按任务复杂度自动分配模型：

| 层级 | 模型 | 思考模式 | 智能体 | 适用场景 |
|------|------|---------|--------|----------|
| 重量级 | `deepseek-v4-pro` | `thinking_max` | PRD 专家、Schema 架构师、API 契约、任务拆分 | 复杂推理，多文档综合 |
| 标准级 | `deepseek-v4-pro` | `thinking` | Orchestrator、技术架构师、编码规范、Agent-BE、Agent-FE、Agent-FIX | 架构决策，代码生成 |
| 轻量级 | `deepseek-v4-flash` | `non-thinking` | Agent-DB、Agent-CONNECT、Agent-VERIFY | 机械性 SQL/字段映射/验证 |

### DeepSeek 独占特性

**100 万上下文跨文档审查**
Phase 0 全部 6 份文档完成后，`cross_doc_checker.py` 将**所有文档一次性加载到单个 API 调用**中进行整体一致性审查——捕获字段名不匹配、Schema-API 不一致、跨文档逻辑矛盾等问题。这在 200K 上下文窗口下无法实现。

**自动前缀缓存**
DeepSeek 自动在块边界缓存重复的 prompt 前缀。Phase 0 串行链（每个 Agent 加载前序 Agent 的输出）中前缀缓存命中率高达 **80-92%**，削减约 60% 的 prompt 成本。`prefix_cache_utils.py` 辅助构建最大化缓存重叠的消息结构。

**思考过程流式展示**
启用 `thinking` 模式后，DeepSeek 同时返回 `delta.reasoning_content`（模型内部思考链）和 `delta.content`（可见输出）。Orchestrator 展示推理过程，让你理解每一步调度决策背后的原因。

---

## 🏗️ 架构总览

### 两阶段流水线

```
                         ⚒️ AppForge
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
     ┌─────────────────────────────────────────────────┐
     │              🧠 Orchestrator（总调度器）           │
     │         DeepSeek V4 Pro + Function Calling             │
     │                                                 │
     │   读取 project_state.json → 判断下一步 →          │
     │   路由到正确的子 Agent → 更新进度                  │
     └──────────────────────┬──────────────────────────┘
                            │
          ┌─────────────────┴──────────────────┐
          ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│  Phase 0：文档生成     │          │  Phase 1-N：编码执行   │
│  （严格串行 6 步）     │          │  （混合串并行）         │
│  ①→②→③→④→⑤→⑥      │          │  DB │ FE║BE │ CONNECT │
│  六份规划文档自动产出   │          │  VERIFY → FIX → 交付   │
└──────────────────────┘          └──────────────────────┘
```

### Phase 0 详解：文档生成串行链

每一步的输出是下一步的输入，严格有序，不可并行——每份文档是下一份的基石。

```
用户构想  "我想做一个跑步打卡 APP..."
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ① 📝 PRD 专家                                                    │
│    输入：用户构想（哪怕只有一句话）                                  │
│    产出：docs/PRD.md — 9 章节，Given-When-Then 验收标准            │
│    校验：✅ 无模糊禁用词  ✅ P0 功能 ≤ 全部功能的 40%               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ② 🏗️ 技术架构师                                                  │
│    输入：docs/PRD.md                                             │
│    产出：docs/TECH_ARCHITECTURE.md                               │
│    内容：每项技术选型 2+ 备选方案对比 / 完整目录结构 /              │
│          MVP 阶段划分 / 零经验环境搭建步骤                        │
│    校验：✅ 选型有对比表格  ✅ 无「性能较好」「适当缓存」等禁用词    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ③ 📏 编码规范专家                                                │
│    输入：PRD + 技术方案                                           │
│    产出：docs/CODING_STANDARDS.md — 13 章节                       │
│    内容：命名规范 / 组件规范 / Store 规范 / Service 规范 /         │
│          Git 规范 / Cursor AI 编码规范 Prompt 模板               │
│    校验：✅ DO/DON'T 代码示例  ✅ 目录结构与技术方案完全一致       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ④ 🗄️ Schema 架构师                                               │
│    输入：PRD + 技术方案 + 编码规范（3 份文档）                      │
│    产出：docs/DB_SCHEMA.md                                       │
│    内容：Mermaid ER 图 / PostgreSQL DDL / SQLite DDL /            │
│          RLS 策略 / 索引策略 / 同步策略 / Redis 缓存键            │
│    校验：✅ 每张表可追溯 PRD 原文  ✅ SQL 无占位符，可直接执行     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ⑤ 🔌 API 契约架构师                                              │
│    输入：PRD + 技术方案 + 编码规范 + Schema（4 份文档）             │
│    产出：docs/API_CONTRACT.md                                    │
│    内容：错误码体系 / 鉴权分级 / TypeScript 类型 /                 │
│          分页规范 / 文件上传规范 / 弱网容错方案 / 请求函数模板       │
│    校验：✅ PRD 每项用户操作有对应接口  ✅ 字段名与 Schema 完全一致 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ ⑥ 📋 任务拆分专家                                                │
│    输入：上述全部五份文档                                          │
│    产出：docs/TASK_BOOK.md                                       │
│    内容：Mermaid 依赖图 / 每任务文件清单 / Mock 数据方案 /          │
│          可直接复制的 Claude Code 完整指令                         │
│    校验：✅ PRD 每页面有对应前端任务  ✅ 验收标准全是终端命令       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 独立审查（新对话，零上下文偏见）                                 │
│    跨文档一致性 → 可操作性 → 完整性                                │
│    输出：必须修复项 / 建议修复项 / 可忽略项 / 评分（1-10）           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    审查通过 ✅
                             │
                             ▼
              Phase 1-N 编码执行开始
```

### Phase 1-N 详解：编码执行混合串并行

```
docs/TASK_BOOK.md
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1：基础设施链（强制串行——依赖关系不可打破）                    │
│                                                                 │
│ T00 ──▶ T01 ──▶ T02 ──▶ T03 ──▶ T04                            │
│ 项目     基础     全局     请求     基础                           │
│ 初始化   配置     类型     封装     UI 组件                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2：认证模块                                                 │
│                                                                 │
│ T05（Auth Store）──▶ T06（注册页）║ T07（登录页）← 可并行         │
│                           │                                      │
│                           ▼                                      │
│                   T08（Auth Edge Function）                       │
│                           │                                      │
│                           ▼                                      │
│                T06 + T07：Mock 替换为真实 API                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3+：核心功能（前端 ║ 后端允许并行，最多 2-3 个）              │
│                                                                 │
│                 ┌──────────────┐                                 │
│                 │  🗃️ Agent-DB  │   执行数据库迁移                 │
│                 └──────┬───────┘                                 │
│                        │                                         │
│          ┌─────────────┼─────────────┐                           │
│          ▼             ▼             ▼                           │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│   │ 🎨 FE    │ │ 🔧 BE    │ │ 🎨 FE    │  ← 最多 3 个并行        │
│   │ 首页Feed │ │ Post接口  │ │ 发帖页面  │                        │
│   │ +Mock    │ │          │ │ +Mock    │                        │
│   └────┬─────┘ └────┬─────┘ └────┬─────┘                        │
│        │            │            │                                │
│        └────────────┼────────────┘                                │
│                     ▼                                            │
│             ┌──────────────┐                                     │
│             │ 🔗 CONNECT    │  Mock → 真实 API 联调               │
│             └──────┬───────┘                                     │
│                    ▼                                             │
│             ┌──────────────┐                                     │
│             │ ✅ VERIFY     │  逐条验收                           │
│             └──┬───────┬───┘                                     │
│                │       │                                         │
│           通过 ✅   失败 ❌                                       │
│                │       ▼                                         │
│                │  ┌──────────┐                                    │
│                │  │ 🩹 FIX    │  修复 → 重新验收                  │
│                │  └────┬─────┘                                    │
│                ▼       │                                         │
│            下一任务 ◀──┘                                          │
└─────────────────────────────────────────────────────────────────┘
                             │
                    所有任务完成
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 里程碑审查（新对话，全新视角）                                   │
│    无"必须修复"项 → 🎉 完整可运行的 APP                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 13 智能体全名册

### 🎛️ 总调度器

| 智能体 | 模型 | 职责 |
|-------|------|------|
| 🧠 **Orchestrator** | DeepSeek V4 Pro + thinking | 读取项目状态 → 判断下一步 → Function Calling 动态路由 → 更新进度 |

### 📋 Phase 0：规划团队（严格串行，6 人）

| # | 智能体 | 产出文档 | 前置依赖 | 一句话职责 |
|---|-------|---------|---------|-----------|
| 1 | 📝 **PRD 专家** | `docs/PRD.md` | 用户构想 | 模糊想法 → 9 章节结构化 PRD，Given-When-Then 验收标准 |
| 2 | 🏗️ **技术架构师** | `docs/TECH_ARCHITECTURE.md` | PRD | 技术选型对比论证 + 目录结构 + MVP 路径 + 环境配置 |
| 3 | 📏 **编码规范专家** | `docs/CODING_STANDARDS.md` | 技术方案 | 13 章编码规范，DO/DON'T 示例，Cursor Prompt 模板 |
| 4 | 🗄️ **Schema 架构师** | `docs/DB_SCHEMA.md` | 编码规范 | Mermaid ER 图 + PostgreSQL/SQLite DDL + RLS + 同步策略 |
| 5 | 🔌 **API 契约架构师** | `docs/API_CONTRACT.md` | Schema | API 定义 + TS 类型 + 错误码体系 + 鉴权分级 + 弱网容错 |
| 6 | 📋 **任务拆分专家** | `docs/TASK_BOOK.md` | 全部五文档 | 分阶段任务书 + 依赖图 + Mock 策略 + 可直接复制的 Claude Code 指令 |

### 💻 Phase 1-N：编码执行团队（混合串并行，6 人）

| 智能体 | 触发条件 | 产出 |
|-------|---------|------|
| 🗃️ **Agent-DB** | 任务书中有数据库迁移任务 | Supabase 建表 SQL + RLS 策略 |
| 🔧 **Agent-BE** | 后端 Edge Function 任务 | TypeScript Deno Edge Function 代码 |
| 🎨 **Agent-FE** | 前端页面/组件任务 | React Native 页面 + 内置 Mock 数据 + `// TODO: TXX` 标记 |
| 🔗 **Agent-CONNECT** | 前后端均已完成 | Mock → 真实 API，snake_case/camelCase 字段映射 |
| ✅ **Agent-VERIFY** | 任意编码任务完成后 | 逐条验收报告（✅ 通过 / ❌ 未通过，不用抽象的"功能正常"） |
| 🩹 **Agent-FIX** | 编译报错、验收失败 | 精确到文件路径 + 行号的修复方案，最小改动 |

---

## 🎛️ Orchestrator 调度机制

Orchestrator 通过 DeepSeek **Function Calling** 实现全自动调度决策，无需人工判断下一步做什么。

### 四个调度工具

```
┌──────────────────────────────────────────────────────────────────┐
│                        🧠 Orchestrator                            │
│                                                                  │
│  ┌─────────────────────┐          ┌─────────────────────┐        │
│  │ read_project_state   │          │ read_file            │        │
│  │ 读取项目状态 JSON     │          │ 读取项目文件内容      │        │
│  │ "每个智能体的状态是   │          │ "这份文档/代码写了    │        │
│  │  什么？完成了哪些？"  │          │  什么？"             │        │
│  └─────────────────────┘          └─────────────────────┘        │
│                                                                  │
│  ┌─────────────────────┐          ┌─────────────────────┐        │
│  │ route_to_agent       │          │ update_state         │        │
│  │ 调度子智能体执行       │          │ 更新项目状态          │        │
│  │ "调用 Agent-X 执行    │          │ "标记任务完成 /       │        │
│  │  这个任务，带上这些    │          │  记录失败原因 /       │        │
│  │  前置文档"           │          │  更新重试次数"        │        │
│  └─────────────────────┘          └─────────────────────┘        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 一轮完整的调度循环

```
用户输入："我想做一个跑步打卡 APP..."
                │
                ▼
┌──────────────────────────────┐
│ Orchestrator 读取状态         │
│ → PRD.md 不存在              │
│ → Phase 0，需要第 1 步        │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Orchestrator 输出：           │
│ 📊 状态：Phase 0，第 1 步     │
│ 🗺️ 计划：调度 PRD 专家        │
│    无需前置文档，只需用户的    │
│    产品构想                   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Function Calling 调用：         │
│ route_to_agent(              │
│   agent="prd_expert",        │
│   task="为跑步打卡APP生成     │
│         完整PRD文档...",      │
│   plan={reason: "...",       │
│         expected_output:     │
│         "docs/PRD.md"}       │
│ )                            │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Worker 执行：                 │
│ 1. 加载 prd_expert.md 提示词  │
│ 2. 流式输出 PRD 到终端        │
│ 3. 保存到 docs/PRD.md        │
│ 4. 标记状态：completed        │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Orchestrator: update_state() │
│ ➡️ 下一步预告：技术架构师      │
│   （输入：docs/PRD.md）       │
└──────────────────────────────┘
```

---

## ⚡ 快速开始

### 完整流水线（推荐）

```bash
git clone https://github.com/withAIx/DeepSeek-AppForge.git
cd AppForge/project-orchestrator

pip install -r requirements.txt
cp .env.example .env   # 编辑填入 DEEPSEEK_API_KEY

python main.py
```

```text
> 我想做一个卡路里追踪APP，可以扫码识别食物、记录每餐摄入...

Orchestrator 自动依次调度：
  Agent-PRD → Agent-ARCH → Agent-STANDARDS → Agent-SCHEMA
  → Agent-API → Agent-DECOMP → 进入编码执行阶段...
```

### 国内用户注意事项

GitHub 克隆慢可使用镜像：
```bash
git clone https://ghproxy.com/https://github.com/withAIx/DeepSeek-AppForge.git
```

DeepSeek API 在国内需要代理访问，运行前设置：
```bash
export HTTPS_PROXY=http://127.0.0.1:7890   # 替换为你的代理地址
python main.py
```

### 程序化调用单个 Agent（Python 库）

```bash
pip install -e .
```

```python
from agents import PRDExpert, MobileArchitect, TaskDecomposer

prd = PRDExpert()
result = prd.run("我想做一个面向大学生的校园外卖APP...")
print(result)
```

### CLI 命令行

```bash
python -m agents.cli run prd-expert "帮我写一个宠物领养APP的PRD"
python -m agents.cli list                          # 列出全部 10 个 Agent
python -m agents.cli run-stream task-decomposer "..."  # 流式输出模式
```

### Claude Code Skill

将 `skills/` 目录下的 `.md` 文件复制到你的 Claude Code skills 目录，对话中激活：

```
/activate prd-expert
```

---

## 🛡️ 容错机制：优雅降级

每个智能体最多重试 **2 次**。全部失败后流水线不停止，执行降级策略：

| 智能体 | 降级策略 |
|-------|---------|
| PRD 专家 | 最小 PRD：产品概述 + P0 功能列表 |
| 技术架构师 | 默认技术栈：Expo + Supabase + Zustand + NativeWind |
| 编码规范专家 | 最小规范集：命名规范 + 目录结构 + 禁用词列表 |
| Schema 架构师 | 只产出核心表：profiles + 1-2 张业务表 |
| API 契约架构师 | 认证模块接口 + 最核心的 1 个业务接口 |
| 任务拆分专家 | 简化任务书：任务 ID + 名称 + 依赖关系，省略 Claude Code 指令 |

降级版本在 `project_state.json` 中标记 `"degraded": true`。后续智能体基于降级版继续——流水线不停。

---

## 🚦 冲突解决优先级

当多份文档之间出现矛盾时（常见场景：Schema 与 API 契约中的字段名不一致）：

```
第一优先级：PRD 文档        ← 功能行为的最终裁决
第二优先级：技术方案文档     ← 架构选型不可被下游覆盖
第三优先级：编码规范文档     ← 命名风格以此为准
第四优先级：Schema 文档     ← 字段名以此为准
第五优先级：API 契约文档     ← 接口格式服从上层定义
```

处理流程：识别冲突 → 查阅更高层级文档确认业务意图 → 修正低层级文档 → 决策记录到 `project_state.json`。不允许 LLM 自行判断"哪边看起来更合理"。

---

## 📂 项目结构

```
AppForge/                                  # ← 你现在的位置
│
├── README.md                              # English README
├── README_CN.md                           # 中文 README（本页）
├── pyproject.toml                         # Python 包配置
│
├── 📦 src/agents/                         # Python 库（程序化调用）
│   ├── _base.py                           # Agent 基类
│   ├── prd_expert.py .. orchestrator.py   # 10 个 Agent 实现
│   └── cli.py                             # click CLI 入口
│
├── ⚒️ project-orchestrator/               # 编排系统（全生命周期调度）
│   ├── README.md                          # 编排系统详细文档
│   ├── main.py                            # 交互式 REPL 入口
│   ├── orchestrator.py                    # Function Calling 调度循环
│   ├── worker.py                          # 子 Agent 执行封装
│   ├── state.py                           # JSON 状态机
│   ├── config.py                          # 12 Agent 注册表 + 依赖图
│   ├── agents/                            # 13 个系统提示词 .md 文件
│   │   ├── orchestrator.md
│   │   ├── phase0/                        # 6 个文档生成专家提示词
│   │   └── phase1n/                       # 6 个编码执行 Agent 提示词
│   └── docs/                              # 文档输出目录（自动创建）
│
└── 📋 skills/                             # Claude Code Skill 文件（10 个）
    ├── prd-expert.md
    ├── mobile-architect.md
    └── ...
```

---

## 📄 License

MIT — 锻造不止，交付不息。
