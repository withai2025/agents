import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "claude-opus-4-7")
WORKER_MODEL_HEAVY = os.getenv("WORKER_MODEL_HEAVY", "claude-opus-4-7")
WORKER_MODEL_LIGHT = os.getenv("WORKER_MODEL_LIGHT", "claude-sonnet-4-6")
PROJECT_NAME = os.getenv("PROJECT_NAME", "my_app")

# Agent registry: agent_name -> config
AGENT_REGISTRY = {
    # Phase 0: Document generation agents (strict serial)
    "prd_expert": {
        "phase": 0,
        "display_name": "PRD Expert",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/prd_expert.md",
        "output_doc": "docs/PRD.md",
        "requires_docs": [],
        "max_tokens": 16000,
    },
    "tech_architect": {
        "phase": 0,
        "display_name": "Tech Architect",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/tech_architect.md",
        "output_doc": "docs/TECH_ARCHITECTURE.md",
        "requires_docs": ["docs/PRD.md"],
        "max_tokens": 16000,
    },
    "coding_standards": {
        "phase": 0,
        "display_name": "Coding Standards Expert",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/coding_standards.md",
        "output_doc": "docs/CODING_STANDARDS.md",
        "requires_docs": ["docs/PRD.md", "docs/TECH_ARCHITECTURE.md"],
        "max_tokens": 16000,
    },
    "schema_architect": {
        "phase": 0,
        "display_name": "Schema Architect",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/schema_architect.md",
        "output_doc": "docs/DB_SCHEMA.md",
        "requires_docs": [
            "docs/PRD.md",
            "docs/TECH_ARCHITECTURE.md",
            "docs/CODING_STANDARDS.md",
        ],
        "max_tokens": 20000,
    },
    "api_contract": {
        "phase": 0,
        "display_name": "API Contract Architect",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/api_contract.md",
        "output_doc": "docs/API_CONTRACT.md",
        "requires_docs": [
            "docs/PRD.md",
            "docs/TECH_ARCHITECTURE.md",
            "docs/CODING_STANDARDS.md",
            "docs/DB_SCHEMA.md",
        ],
        "max_tokens": 24000,
    },
    "task_decomposer": {
        "phase": 0,
        "display_name": "Task Decomposer",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/task_decomposer.md",
        "output_doc": "docs/TASK_BOOK.md",
        "requires_docs": [
            "docs/PRD.md",
            "docs/TECH_ARCHITECTURE.md",
            "docs/CODING_STANDARDS.md",
            "docs/DB_SCHEMA.md",
            "docs/API_CONTRACT.md",
        ],
        "max_tokens": 32000,
    },
    # Phase 1-N: Coding execution agents
    "agent_db": {
        "phase": 1,
        "display_name": "Agent-DB",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_db.md",
        "output_doc": None,
        "requires_docs": ["docs/DB_SCHEMA.md"],
        "max_tokens": 8000,
    },
    "agent_be": {
        "phase": 1,
        "display_name": "Agent-BE",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_be.md",
        "output_doc": None,
        "requires_docs": ["docs/API_CONTRACT.md", "docs/DB_SCHEMA.md", "docs/CODING_STANDARDS.md"],
        "max_tokens": 12000,
    },
    "agent_fe": {
        "phase": 1,
        "display_name": "Agent-FE",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_fe.md",
        "output_doc": None,
        "requires_docs": ["docs/CODING_STANDARDS.md", "docs/API_CONTRACT.md"],
        "max_tokens": 12000,
    },
    "agent_connect": {
        "phase": 1,
        "display_name": "Agent-CONNECT",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_connect.md",
        "output_doc": None,
        "requires_docs": ["docs/API_CONTRACT.md", "docs/CODING_STANDARDS.md"],
        "max_tokens": 8000,
    },
    "agent_verify": {
        "phase": 1,
        "display_name": "Agent-VERIFY",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_verify.md",
        "output_doc": None,
        "requires_docs": ["docs/TASK_BOOK.md"],
        "max_tokens": 4000,
    },
    "agent_fix": {
        "phase": 1,
        "display_name": "Agent-FIX",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_fix.md",
        "output_doc": None,
        "requires_docs": ["docs/CODING_STANDARDS.md"],
        "max_tokens": 8000,
    },
}

# Phase 0 execution order (strict serial)
PHASE0_ORDER = [
    "prd_expert",
    "tech_architect",
    "coding_standards",
    "schema_architect",
    "api_contract",
    "task_decomposer",
]
