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
    list_projects,
)
from worker import run_worker, save_agent_output

console = Console()
client = anthropic.Anthropic()

MAX_RETRIES = 2

# Orchestrator system prompt (loaded from external file)
ORCHESTRATOR_SYSTEM = Path("agents/orchestrator.md").read_text(encoding="utf-8")

# Tool definitions available to Orchestrator
ORCHESTRATOR_TOOLS = [
    {
        "name": "read_project_state",
        "description": "Read current project state, returns JSON formatted state data",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "route_to_agent",
        "description": "Route a task to a specified sub-agent for execution — the core scheduling action of the Orchestrator",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_name": {
                    "type": "string",
                    "enum": list(AGENT_REGISTRY.keys()),
                    "description": "Name of the sub-agent to invoke",
                },
                "task_description": {
                    "type": "string",
                    "description": "Specific task description for the sub-agent",
                },
                "plan": {
                    "type": "object",
                    "description": "Scheduling plan containing routing rationale and expected output",
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
        "description": "Update project state file",
        "input_schema": {
            "type": "object",
            "properties": {
                "updates": {"type": "object", "description": "State fields to merge and update"}
            },
            "required": ["updates"],
        },
    },
    {
        "name": "read_file",
        "description": "Read content of a file in the project",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]


def execute_tool(tool_name: str, tool_input: dict, state: dict) -> tuple[str, dict]:
    """Execute Orchestrator Tool call, return (result string, updated state)"""

    if tool_name == "read_project_state":
        return json.dumps(state, ensure_ascii=False, indent=2), state

    elif tool_name == "read_file":
        project_dir = Path(state["_project_dir"])
        path = project_dir / tool_input["path"]
        if path.exists():
            return path.read_text(encoding="utf-8"), state
        return f"[File not found: {tool_input['path']}]", state

    elif tool_name == "update_state":
        updates = tool_input["updates"]
        old_name = state.get("project_name")
        new_name = updates.get("project_name")
        state.update(updates)
        if new_name and new_name != old_name:
            # Rename project directory to match
            old_dir = Path(state["_project_dir"])
            new_dir = old_dir.parent / new_name
            if old_dir.exists() and old_dir != new_dir:
                old_dir.rename(new_dir)
                state["_project_dir"] = str(new_dir)
        save_state(state)
        return "State updated successfully", state

    elif tool_name == "route_to_agent":
        agent_name = tool_input["agent_name"]
        task_desc = tool_input["task_description"]
        plan = tool_input["plan"]

        # Display scheduling plan
        console.print(
            Panel(
                f"[bold yellow]🗺️ Scheduling Plan[/bold yellow]\n\n"
                f"**Routing to**: {AGENT_REGISTRY[agent_name]['display_name']}\n"
                f"**Reason**: {plan['reason']}\n"
                f"**Expected output**: {plan['expected_output']}",
                border_style="yellow",
            )
        )

        # Execute sub-agent (with retries)
        retry_count = state["retry_counts"].get(agent_name, 0)
        result = None
        error_msg = None
        project_dir = Path(state["_project_dir"])

        for attempt in range(MAX_RETRIES + 1):
            try:
                result = run_worker(agent_name, task_desc, project_dir, stream=True)

                # If Phase 0 document generation, save output file
                saved_path = save_agent_output(agent_name, result, project_dir)
                if saved_path:
                    state = mark_agent_completed(state, agent_name)

                return (
                    f"✅ {AGENT_REGISTRY[agent_name]['display_name']} execution complete\n{result[:500]}...",
                    state,
                )

            except Exception as e:
                error_msg = str(e)
                console.print(f"[red]❌ Attempt {attempt + 1} failed: {error_msg}[/red]")
                if attempt < MAX_RETRIES:
                    console.print(f"[yellow]🔄 Retrying (attempt {attempt + 2})...[/yellow]")
                    increment_retry(state, agent_name)

        # All retries failed; execute degradation
        state = mark_agent_failed(state, agent_name, error_msg)
        return f"⚠️ {agent_name} execution failed (degraded), error: {error_msg}", state

    return f"Unknown Tool: {tool_name}", state


def run_orchestrator_turn(user_input: str, state: dict) -> dict:
    """Execute one round of the Orchestrator scheduling loop"""

    state_summary = json.dumps(state, ensure_ascii=False, indent=2)

    messages = [
        {
            "role": "user",
            "content": f"## Current Project State\n```json\n{state_summary}\n```\n\n## User Input\n{user_input}",
        }
    ]

    console.print("[dim]🧠 Orchestrator analyzing...[/dim]")

    # Orchestrator Tool Use loop
    while True:
        response = client.messages.create(
            model=ORCHESTRATOR_MODEL,
            max_tokens=4096,
            system=ORCHESTRATOR_SYSTEM,
            tools=ORCHESTRATOR_TOOLS,
            messages=messages,
        )

        # Extract text output
        text_parts = [b.text for b in response.content if b.type == "text"]
        if text_parts:
            console.print(Panel("\n".join(text_parts), border_style="blue", title="📊 Orchestrator"))

        # Exit loop if no Tool calls
        if response.stop_reason != "tool_use":
            break

        # Process all Tool calls
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        tool_results = []

        for tool_use in tool_uses:
            console.print(f"[dim]⚙️  Calling Tool: {tool_use.name}[/dim]")
            result_text, state = execute_tool(tool_use.name, tool_use.input, state)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result_text,
            })

        # Append results to conversation
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return state


class ProjectOrchestrator:
    def __init__(self, project_name: str | None = None):
        if project_name:
            self.state = init_state(project_name)
        else:
            # Load most recently updated project (backward compat)
            projects = list_projects()
            if projects:
                self.state = load_state(projects[0]["name"])
            else:
                self.state = init_state(PROJECT_NAME)

    def print_status(self):
        """Print current project status table"""
        table = Table(title="📊 Project Development Progress", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Document", style="white")
        table.add_column("Status", style="bold")

        doc_status_map = {
            "completed": "✅ Complete",
            "in_progress": "🔄 In Progress",
            "pending": "⏳ Pending",
            "failed": "❌ Failed (Degraded)",
        }

        for agent_name in PHASE0_ORDER:
            doc_info = self.state["phase0_documents"].get(agent_name, {})
            status = doc_status_map.get(doc_info.get("status", "pending"), "⏳ Pending")
            table.add_row(
                AGENT_REGISTRY[agent_name]["display_name"],
                doc_info.get("path", "-"),
                status,
            )

        console.print(table)

    def run(self, user_input: str):
        """Main execution entry point"""
        # Phase 0 auto-advance (check next pending document)
        if not is_phase0_complete(self.state):
            next_agent = get_next_phase0_agent(self.state)
            if next_agent:
                agent_display = AGENT_REGISTRY[next_agent]["display_name"]
                console.print(
                    f"\n[bold green]➡️  Phase 0 in progress: Next → {agent_display}[/bold green]"
                )
            elif not self.state.get("name_confirmed", False):
                console.print(
                    "\n[bold yellow]🏷️  New project — describe your app idea and I'll suggest a name[/bold yellow]"
                )
            else:
                # PRD completed but awaiting user review
                prd_status = self.state["phase0_documents"]["prd_expert"]["status"]
                if prd_status == "completed" and not self.state.get("prd_reviewed", False):
                    console.print(
                        "\n[bold yellow]📋 PRD has been generated — please review docs/PRD.md[/bold yellow]"
                    )
                    console.print(
                        "[dim]Reply 'confirmed' to proceed, or describe what you'd like to change.[/dim]"
                    )

        self.state = run_orchestrator_turn(user_input, self.state)
