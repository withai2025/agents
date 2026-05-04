# Agents

A collection of well-crafted AI agents powered by Claude. Each agent features a meticulously designed system prompt, supports both programmatic invocation and Claude Code Skill format, and is ready to drop into your projects.

## Installation

```bash
pip install -e .
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

### Programmatic

```python
from agents import PromptEngineer

agent = PromptEngineer()
result = agent.run("帮我写一个代码审查的提示词")
print(result)
```

### CLI

```bash
python -m agents.cli run prompt-engineer "帮我写一个代码审查的提示词"
```

### As Claude Code Skill

Copy the corresponding `.md` file from `skills/` into your Claude Code skills directory.

## Agents

| # | Agent | Description |
|---|-------|-------------|
| 1 | PromptEngineer | 提示词工程专家，根据需求设计高质量结构化提示词 |
| 2 | ProductResearcher | AI产品调研专家，1小时内完成竞品快调研与机会发现 |
| 3 | UXDesigner | AI产品UX全链路设计专家，Mobile-First覆盖交互/UI/设计系统 |
| 4 | PRDExpert | APP PRD 专家助手，将模糊产品构想转化为开发团队可直接执行的需求文档 |
| 5 | MobileArchitect | 移动端技术架构师，从 PRD 到可执行技术方案，涵盖技术选型/数据库/AI集成 |
| 6 | CodingStandards | 编码规范专家，从 PRD+技术方案生成 CODING_STANDARDS.md 与 Cursor Prompt 模板 |
| 7 | DBSchemaArchitect | 数据库 Schema 架构师，生成 PostgreSQL/SQLite/ER图/RLS/同步策略完整设计 |
| 8 | APIContractArchitect | API 接口契约架构师，生成完整 API 契约文档含 TypeScript 类型/SSE/幂等/请求函数模板 |
| 9 | TaskDecomposer | 编码任务拆分专家，将全套文档拆解为分阶段任务书含依赖图/Claude Code指令/验收标准 |

## License

MIT
