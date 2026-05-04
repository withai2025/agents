"""
CLI entry point for agents.

Usage:
    python -m agents.cli list                         # list all agents
    python -m agents.cli run <name> "<input>"          # run an agent
    python -m agents.cli run-stream <name> "<input>"   # stream output
"""

from __future__ import annotations

import click

from agents import APIContractArchitect, CodingStandards, DBSchemaArchitect, MobileArchitect, PRDExpert, ProductResearcher, PromptEngineer, TaskDecomposer, UXDesigner

_REGISTRY = {
    "task-decomposer": TaskDecomposer,
    "api-contract-architect": APIContractArchitect,
    "db-schema-architect": DBSchemaArchitect,
    "coding-standards": CodingStandards,
    "mobile-architect": MobileArchitect,
    "prd-expert": PRDExpert,
    "prompt-engineer": PromptEngineer,
    "product-researcher": ProductResearcher,
    "ux-designer": UXDesigner,
}


@click.group()
def main():
    """AI Agents CLI — run well-crafted Claude-powered agents from the command line."""


@main.command()
def list():
    """List all available agents."""
    for name, cls in _REGISTRY.items():
        agent = cls()
        click.echo(f"  {name:30s}  {agent.description}")


@main.command()
@click.argument("name")
@click.argument("input_text")
@click.option("--model", default=None, help="Override model")
@click.option("--temperature", type=float, default=None, help="Override temperature")
def run(name, input_text, model, temperature):
    """Run an agent with the given input."""
    cls = _REGISTRY.get(name)
    if cls is None:
        click.echo(f"Unknown agent: {name}. Use 'agents list' to see available agents.")
        raise SystemExit(1)

    agent = cls()
    kwargs = {}
    if model:
        kwargs["model"] = model
    if temperature is not None:
        kwargs["temperature"] = temperature

    result = agent.run(input_text, **kwargs)
    click.echo(result)


@main.command()
@click.argument("name")
@click.argument("input_text")
@click.option("--model", default=None, help="Override model")
@click.option("--temperature", type=float, default=None, help="Override temperature")
def run_stream(name, input_text, model, temperature):
    """Run an agent with streaming output."""
    cls = _REGISTRY.get(name)
    if cls is None:
        click.echo(f"Unknown agent: {name}. Use 'agents list' to see available agents.")
        raise SystemExit(1)

    agent = cls()
    kwargs = {}
    if model:
        kwargs["model"] = model
    if temperature is not None:
        kwargs["temperature"] = temperature

    for chunk in agent.run_stream(input_text, **kwargs):
        click.echo(chunk, nl=False)


if __name__ == "__main__":
    main()
