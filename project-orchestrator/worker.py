import anthropic
from pathlib import Path
from config import AGENT_REGISTRY
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
client = anthropic.Anthropic()


def load_agent_prompt(agent_name: str) -> str:
    """加载子 Agent 的系统提示词"""
    config = AGENT_REGISTRY[agent_name]
    prompt_path = Path(config["prompt_file"])
    if not prompt_path.exists():
        raise FileNotFoundError(f"Agent 提示词文件不存在: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def load_context_docs(doc_paths: list[str]) -> str:
    """加载上下文文档，合并为字符串"""
    parts = []
    for path in doc_paths:
        p = Path(path)
        if p.exists():
            content = p.read_text(encoding="utf-8")
            parts.append(f"\n\n---\n# 文档：{path}\n\n{content}")
        else:
            parts.append(f"\n\n---\n# 文档：{path}\n\n[文件不存在，请先完成前置任务]")
    return "".join(parts)


def run_worker(
    agent_name: str,
    task_description: str,
    extra_context: str = "",
    stream: bool = True,
) -> str:
    """执行子 Agent，返回完整输出内容"""
    config = AGENT_REGISTRY[agent_name]
    system_prompt = load_agent_prompt(agent_name)

    # 组装上下文文档
    context = load_context_docs(config.get("requires_docs", []))
    if extra_context:
        context += f"\n\n---\n# 额外上下文\n\n{extra_context}"

    user_message = f"""## 任务要求
{task_description}

## 可用文档上下文
{context if context else "（无前置文档）"}
"""

    console.print(
        Panel(
            f"[bold cyan]🤖 {config['display_name']} 启动中...[/bold cyan]\n"
            f"模型：{config['model']}",
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
        print()  # 换行
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


def save_agent_output(agent_name: str, content: str) -> str | None:
    """将 Agent 输出保存到对应文档路径，返回保存路径"""
    config = AGENT_REGISTRY[agent_name]
    output_path = config.get("output_doc")
    if not output_path:
        return None

    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    console.print(f"[green]✅ 文档已保存：{output_path}[/green]")
    return output_path
