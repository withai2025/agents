# Contributing to AppForge

Thanks for your interest in contributing! AppForge is an AI-driven app development pipeline that turns your idea into a working product with 13 AI agents.

## Development Setup

```bash
git clone https://github.com/withAIx/AppForge.git
cd AppForge

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Environment

Copy `.env.example` to `.env` and set your API key:

```bash
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY or DEEPSEEK_API_KEY
```

## Project Structure

- `src/agents/` — Python library: 10 individual agent implementations
- `project-orchestrator/` — Orchestration system with Tool Use scheduler
- `project-orchestrator/agents/` — 13 system prompt `.md` files
- `skills/` — Claude Code skill files

## How to Contribute

### Reporting Bugs

Use the Bug Report issue template. Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, API provider)

### Feature Requests

Use the Feature Request template. Describe:
- The problem you're solving
- Your proposed solution
- Alternatives you've considered

### Pull Requests

1. Fork the repo and create a branch from `main`
2. Make your changes, following existing code style
3. Run existing tests to verify nothing is broken
4. Submit a PR with a clear description of changes

### Code Style

- Python 3.11+, type hints encouraged
- Keep diffs minimal — prefer editing existing files over creating new ones
- Agent system prompts are in Chinese; code comments may be in English or Chinese
- No half-finished implementations

## Testing

```bash
# Verify imports
python -c "from agents._base import BaseAgent, AgentConfig; print('OK')"

# Verify orchestrator config
cd project-orchestrator
python -c "from config import AGENT_REGISTRY; print(len(AGENT_REGISTRY), 'agents registered')"
```

## Questions?

Start a [Discussion](https://github.com/withAIx/AppForge/discussions) or open an issue.
