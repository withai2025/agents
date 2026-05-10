import anthropic
from pathlib import Path
from config import AGENT_REGISTRY
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
client = anthropic.Anthropic()


def load_agent_prompt(agent_name: str) -> str:
    """Load sub-agent system prompt."""
    config = AGENT_REGISTRY[agent_name]
    prompt_path = Path(config["prompt_file"])
    if not prompt_path.exists():
        raise FileNotFoundError(f"Agent prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def load_context_docs(doc_paths: list[str], project_dir: Path) -> str:
    """Load context documents and merge into a single string.

    Paths are resolved relative to the project directory so each project's
    documents are isolated.
    """
    parts = []
    for path in doc_paths:
        p = project_dir / path
        if p.exists():
            content = p.read_text(encoding="utf-8")
            parts.append(f"\n\n---\n# Document: {path}\n\n{content}")
        else:
            parts.append(f"\n\n---\n# Document: {path}\n\n[File does not exist. Please complete prerequisite tasks first.]")
    return "".join(parts)


def run_worker(
    agent_name: str,
    task_description: str,
    project_dir: Path,
    extra_context: str = "",
    stream: bool = True,
) -> str:
    """Execute sub-agent and return complete output."""
    config = AGENT_REGISTRY[agent_name]
    system_prompt = load_agent_prompt(agent_name)

    # Assemble context documents from this project's directory
    context = load_context_docs(config.get("requires_docs", []), project_dir)
    if extra_context:
        context += f"\n\n---\n# Extra Context\n\n{extra_context}"

    user_message = f"""## Task Description
{task_description}

## Available Document Context
{context if context else "(No prerequisite documents)"}
"""

    console.print(
        Panel(
            f"[bold cyan]🤖 {config['display_name']} starting up...[/bold cyan]\n"
            f"Model: {config['model']}",
            border_style="cyan",
        )
    )

    full_response = ""

    if stream:
        with client.messages.stream(
            model=config["model"],
            max_tokens=config["max_tokens"],
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        ) as stream_obj:
            for text in stream_obj.text_stream:
                print(text, end="", flush=True)
                full_response += text
        print()  # newline
    else:
        response = client.messages.create(
            model=config["model"],
            max_tokens=config["max_tokens"],
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        full_response = response.content[0].text
        console.print(Markdown(full_response))

    return full_response


def save_agent_output(agent_name: str, content: str, project_dir: Path) -> str | None:
    """Save agent output to the project's docs directory. Returns saved path."""
    config = AGENT_REGISTRY[agent_name]
    output_path = config.get("output_doc")
    if not output_path:
        return None

    p = project_dir / output_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    console.print(f"[green]✅ Document saved: {output_path}[/green]")
    return str(output_path)
