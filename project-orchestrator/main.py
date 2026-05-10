#!/usr/bin/env python3
"""
Project Orchestrator - Orchestrator-Workers APP Development Orchestration System
Usage: python main.py
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def show_welcome():
    """Show project introduction — works without API key"""
    console.print(
        Panel(
            "[bold blue]🚀 Project Orchestrator v2.0[/bold blue]\n"
            "Orchestrator-Workers — full lifecycle APP development system\n\n"
            "[bold]Powered by Anthropic Claude[/bold]\n"
            "13 specialized AI agents turn your app idea into a complete, runnable application.\n\n"
            "[dim]Phase 0: 6 planning agents design every detail of your app[/dim]\n"
            "[dim]Phase 1-N: 6 coding agents build, connect, verify, and fix[/dim]\n\n"
            "Type [bold]help[/bold] to see available commands.",
            border_style="blue",
        )
    )


def setup_api_key():
    """Guide the user to configure their Anthropic API key.

    Returns True if the key was configured, False if the user wants to exit.
    """
    from dotenv import load_dotenv

    load_dotenv()
    if os.getenv("ANTHROPIC_API_KEY"):
        return True

    console.print()
    console.print(
        Panel(
            "[bold yellow]⚡ This project needs an Anthropic API key to work.[/bold yellow]\n\n"
            "The orchestrator calls the Anthropic API to power 13 AI agents that\n"
            "turn your app idea into a complete, runnable application.\n\n"
            "[bold]Security note:[/bold]\n"
            "  • Your key is stored [bold]only in the local .env file[/bold] on your machine\n"
            "  • The .env file is [bold]gitignored[/bold] — it will never be committed or pushed\n"
            "  • The key is sent [bold]only to api.anthropic.com[/bold] — nowhere else\n"
            "  • No telemetry, no third-party servers, no uploads\n"
            "  • You can inspect [bold]every line of source code[/bold] to verify",
            border_style="yellow",
        )
    )

    console.print(
        "\n[bold]To get your key:[/bold] [link=https://console.anthropic.com/settings/keys]https://console.anthropic.com/settings/keys[/link]\n"
    )

    while True:
        key = console.input("[bold]Enter your Anthropic API key[/bold] (or 'q' to quit): ").strip()
        if key.lower() == "q":
            return False
        if key:
            _write_env_file(key)
            return True
        console.print("[yellow]Please enter a valid key[/yellow]")


def _write_env_file(key: str):
    """Write the API key to .env, creating it from .env.example if it doesn't exist."""
    env_path = Path(".env")
    env_example = Path(".env.example")

    lines = []
    if env_example.exists():
        lines = env_example.read_text().splitlines()
    else:
        lines = [
            "ANTHROPIC_API_KEY=your_api_key_here",
            "ORCHESTRATOR_MODEL=claude-opus-4-7",
            "WORKER_MODEL_HEAVY=claude-opus-4-7",
            "WORKER_MODEL_LIGHT=claude-sonnet-4-6",
            "PROJECT_NAME=my_app",
        ]

    new_lines = []
    for line in lines:
        if line.startswith("ANTHROPIC_API_KEY="):
            new_lines.append(f"ANTHROPIC_API_KEY={key}")
        else:
            new_lines.append(line)

    env_path.write_text("\n".join(new_lines) + "\n")

    # Reload so the new key is picked up immediately
    from dotenv import load_dotenv
    load_dotenv(override=True)

    console.print("[green]✅ API key saved to .env (local only, never uploaded)[/green]\n")


def show_help():
    """Show commands available without an API key."""
    table = Table(title="Available Commands", border_style="dim")
    table.add_column("Command", style="bold cyan")
    table.add_column("Description")
    table.add_row("help", "Show this help message")
    table.add_row("intro", "Show project introduction")
    table.add_row("setup", "Configure or change your API key")
    table.add_row("status", "View current development progress")
    table.add_row("exit", "Exit the system")
    table.add_row("<your app idea>", "Send to Orchestrator for analysis and scheduling")
    console.print()
    console.print(table)
    console.print()


def main():
    show_welcome()

    if not setup_api_key():
        console.print("\n[yellow]No API key configured. You can run [bold]setup[/bold] later to configure one.[/yellow]")
        console.print("[dim]Running in preview mode — type [bold]help[/bold] for available commands.[/dim]\n")

    from orchestrator import ProjectOrchestrator
    orch = ProjectOrchestrator()

    # Print status if key is configured
    if os.getenv("ANTHROPIC_API_KEY"):
        orch.print_status()

    while True:
        try:
            user_input = console.input("[bold]> [/bold]").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                console.print("Goodbye!")
                break
            elif user_input.lower() == "help":
                show_help()
            elif user_input.lower() == "intro":
                show_welcome()
            elif user_input.lower() == "setup":
                if setup_api_key():
                    console.print("[green]Orchestrator is ready — type your app idea to begin![/green]")
            elif user_input.lower() == "status":
                if not os.getenv("ANTHROPIC_API_KEY"):
                    console.print("[yellow]Status requires an API key. Type [bold]setup[/bold] to configure one.[/yellow]")
                else:
                    orch.print_status()
            else:
                if not os.getenv("ANTHROPIC_API_KEY"):
                    console.print("[yellow]This command requires an API key. Type [bold]setup[/bold] to configure one.[/yellow]")
                else:
                    orch.run(user_input)
        except KeyboardInterrupt:
            console.print("\n\nInterrupted.")
            break
        except Exception as e:
            console.print(f"[red]System error: {e}[/red]")


if __name__ == "__main__":
    main()
