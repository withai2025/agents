import json
from pathlib import Path
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import (
    ORCHESTRATOR_MODEL,
    AGENT_REGISTRY,
    PHASE0_ORDER,
    PROJECT_NAME,
)
from state import (
    load_state,
    save_state,
    init_state,
    get_next_phase0_agent,
    is_phase0_complete,
    mark_agent_completed,
    mark_agent_failed,
    increment_retry,
)
from worker import run_worker, save_agent_output

console = Console()
client = anthropic.Anthropic()

MAX_RETRIES = 2

# Orchestrator 系统提示词（从外部文件加载）
ORCHESTRATOR_SYSTEM = Path("agents/orchestrator.md").read_text(encoding="utf-8")

# Orchestrator 可用的 Tool 定义
ORCHESTRATOR_TOOLS = [
    {
        "name": "read_project_state",
        "description": "读取当前项目状态，返回 JSON 格式的状态数据",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "route_to_agent",
        "description": "将任务路由到指定子 Agent 执行，是 Orchestrator 的核心调度动作",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_name": {
                    "type": "string",
                    "enum": list(AGENT_REGISTRY.keys()),
                    "description": "要调用的子 Agent 名称",
                },
                "task_description": {
                    "type": "string",
                    "description": "给子 Agent 的具体任务描述（中文）",
                },
                "plan": {
                    "type": "object",
                    "description": "调度计划，包含路由理由和预期产出",
                    "properties": {
                        "reason": {"type": "string"},
                        "expected_output": {"type": "string"},
                        "parallel_tasks": {"type": "array", "items": {"type": "string"}},
                        "blockers": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["reason", "expected_output"],
                },
            },
            "required": ["agent_name", "task_description", "plan"],
        },
    },
    {
        "name": "update_state",
        "description": "更新项目状态文件",
        "input_schema": {
            "type": "object",
            "properties": {
                "updates": {"type": "object", "description": "要合并更新的状态字段"}
            },
            "required": ["updates"],
        },
    },
    {
        "name": "read_file",
        "description": "读取项目中的文件内容",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]


def execute_tool(tool_name: str, tool_input: dict, state: dict) -> tuple[str, dict]:
    """执行 Orchestrator 的 Tool 调用，返回 (结果字符串, 更新后的state)"""

    if tool_name == "read_project_state":
        return json.dumps(state, ensure_ascii=False, indent=2), state

    elif tool_name == "read_file":
        path = Path(tool_input["path"])
        if path.exists():
            return path.read_text(encoding="utf-8"), state
        return f"[文件不存在: {tool_input['path']}]", state

    elif tool_name == "update_state":
        state.update(tool_input["updates"])
        save_state(state)
        return "状态更新成功", state

    elif tool_name == "route_to_agent":
        agent_name = tool_input["agent_name"]
        task_desc = tool_input["task_description"]
        plan = tool_input["plan"]

        # 展示调度计划
        console.print(
            Panel(
                f"[bold yellow]🗺️ 调度计划[/bold yellow]\n\n"
                f"**路由到**：{AGENT_REGISTRY[agent_name]['display_name']}\n"
                f"**理由**：{plan['reason']}\n"
                f"**预期产出**：{plan['expected_output']}",
                border_style="yellow",
            )
        )

        # 执行子 Agent（带重试）
        retry_count = state["retry_counts"].get(agent_name, 0)
        result = None
        error_msg = None

        for attempt in range(MAX_RETRIES + 1):
            try:
                result = run_worker(agent_name, task_desc, stream=True)

                # 如果是 Phase 0 文档生成，保存输出文件
                saved_path = save_agent_output(agent_name, result)
                if saved_path:
                    state = mark_agent_completed(state, agent_name)

                return (
                    f"✅ {AGENT_REGISTRY[agent_name]['display_name']} 执行完成\n{result[:500]}...",
                    state,
                )

            except Exception as e:
                error_msg = str(e)
                console.print(f"[red]❌ 第 {attempt + 1} 次执行失败：{error_msg}[/red]")
                if attempt < MAX_RETRIES:
                    console.print(f"[yellow]🔄 第 {attempt + 2} 次重试...[/yellow]")
                    increment_retry(state, agent_name)

        # 全部重试失败，执行降级
        state = mark_agent_failed(state, agent_name, error_msg)
        return f"⚠️ {agent_name} 执行失败（已降级），错误：{error_msg}", state

    return f"未知 Tool: {tool_name}", state


def run_orchestrator_turn(user_input: str, state: dict) -> dict:
    """执行一轮 Orchestrator 调度循环"""

    state_summary = json.dumps(state, ensure_ascii=False, indent=2)

    messages = [
        {
            "role": "user",
            "content": f"## 当前项目状态\n```json\n{state_summary}\n```\n\n## 用户输入\n{user_input}",
        }
    ]

    console.print("[dim]🧠 Orchestrator 分析中...[/dim]")

    # Orchestrator 的 Tool Use 循环
    while True:
        response = client.messages.create(
            model=ORCHESTRATOR_MODEL,
            max_tokens=4096,
            system=ORCHESTRATOR_SYSTEM,
            tools=ORCHESTRATOR_TOOLS,
            messages=messages,
        )

        # 提取文本输出
        text_parts = [b.text for b in response.content if b.type == "text"]
        if text_parts:
            console.print(Panel("\n".join(text_parts), border_style="blue", title="📊 Orchestrator"))

        # 没有 Tool 调用则退出循环
        if response.stop_reason != "tool_use":
            break

        # 处理所有 Tool 调用
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        tool_results = []

        for tool_use in tool_uses:
            console.print(f"[dim]⚙️  调用 Tool: {tool_use.name}[/dim]")
            result_text, state = execute_tool(tool_use.name, tool_use.input, state)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result_text,
            })

        # 将结果追加到对话继续
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return state


class ProjectOrchestrator:
    def __init__(self):
        self.state = load_state()
        if not self.state.get("project_name"):
            self.state = init_state(PROJECT_NAME)
        Path("docs").mkdir(exist_ok=True)

    def print_status(self):
        """打印当前项目状态表格"""
        table = Table(title="📊 项目开发进度", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("文档", style="white")
        table.add_column("状态", style="bold")

        doc_status_map = {
            "completed": "✅ 完成",
            "in_progress": "🔄 进行中",
            "pending": "⏳ 待启动",
            "failed": "❌ 失败（降级）",
        }

        for agent_name in PHASE0_ORDER:
            doc_info = self.state["phase0_documents"].get(agent_name, {})
            status = doc_status_map.get(doc_info.get("status", "pending"), "⏳ 待启动")
            table.add_row(
                AGENT_REGISTRY[agent_name]["display_name"],
                doc_info.get("path", "-"),
                status,
            )

        console.print(table)

    def run(self, user_input: str):
        """主执行入口"""
        # Phase 0 自动推进（检查下一个待执行文档）
        if not is_phase0_complete(self.state):
            next_agent = get_next_phase0_agent(self.state)
            if next_agent:
                agent_display = AGENT_REGISTRY[next_agent]["display_name"]
                console.print(
                    f"\n[bold green]➡️  Phase 0 进行中：下一步 → {agent_display}[/bold green]"
                )

        self.state = run_orchestrator_turn(user_input, self.state)
