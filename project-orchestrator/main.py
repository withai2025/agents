#!/usr/bin/env python3
"""
Project Orchestrator - Orchestrator-Workers APP 开发编排系统
使用方法：python main.py
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def check_env():
    """检查环境配置"""
    from dotenv import load_dotenv
    import os
    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ 请在 .env 文件中设置 ANTHROPIC_API_KEY[/red]")
        sys.exit(1)


def main():
    check_env()

    from orchestrator import ProjectOrchestrator
    orch = ProjectOrchestrator()

    console.print(
        Panel(
            "[bold blue]🚀 Project Orchestrator v2.0[/bold blue]\n"
            "Orchestrator-Workers APP 全生命周期开发编排系统\n\n"
            "命令：\n"
            "  status  → 查看当前开发进度\n"
            "  exit    → 退出系统\n"
            "  其他输入 → 交给 Orchestrator 分析并调度",
            border_style="blue",
        )
    )

    # 首次启动自动打印状态
    orch.print_status()

    while True:
        try:
            user_input = console.input("\n[bold]> [/bold]").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                console.print("再见！")
                break
            elif user_input.lower() == "status":
                orch.print_status()
            else:
                orch.run(user_input)
        except KeyboardInterrupt:
            console.print("\n\n已中断。")
            break
        except Exception as e:
            console.print(f"[red]系统错误：{e}[/red]")


if __name__ == "__main__":
    main()
