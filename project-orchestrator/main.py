#!/usr/bin/env python3
"""
Project Orchestrator - Orchestrator-Workers APP Development Orchestration System
Usage: python main.py
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def check_env():
    """Check environment configuration"""
    from dotenv import load_dotenv
    import os
    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ Please set ANTHROPIC_API_KEY in your .env file[/red]")
        sys.exit(1)


def main():
    check_env()

    from orchestrator import ProjectOrchestrator
    orch = ProjectOrchestrator()

    console.print(
        Panel(
            "[bold blue]🚀 Project Orchestrator v2.0[/bold blue]\n"
            "Orchestrator-Workers Full-Lifecycle APP Development Orchestration System\n\n"
            "Commands:\n"
            "  status  → View current development progress\n"
            "  exit    → Exit the system\n"
            "  anything else → Send to Orchestrator for analysis and scheduling",
            border_style="blue",
        )
    )

    # Auto-print status on first launch
    orch.print_status()

    while True:
        try:
            user_input = console.input("\n[bold]> [/bold]").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                console.print("Goodbye!")
                break
            elif user_input.lower() == "status":
                orch.print_status()
            else:
                orch.run(user_input)
        except KeyboardInterrupt:
            console.print("\n\nInterrupted.")
            break
        except Exception as e:
            console.print(f"[red]System error: {e}[/red]")


if __name__ == "__main__":
    main()
