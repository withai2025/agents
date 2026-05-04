import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "claude-opus-4-7")
WORKER_MODEL_HEAVY = os.getenv("WORKER_MODEL_HEAVY", "claude-opus-4-7")
WORKER_MODEL_LIGHT = os.getenv("WORKER_MODEL_LIGHT", "claude-sonnet-4-6")
PROJECT_NAME = os.getenv("PROJECT_NAME", "my_app")

# 子 Agent 名册：agent_name -> 配置
AGENT_REGISTRY = {
    # Phase 0: 文档生成 Agent（严格串行）
    "prd_expert": {
        "phase": 0,
        "display_name": "PRD 专家",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/prd_expert.md",
        "output_doc": "docs/PRD.md",
        "requires_docs": [],
        "max_tokens": 16000,
    },
    "tech_architect": {
        "phase": 0,
        "display_name": "技术架构师",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/tech_architect.md",
        "output_doc": "docs/TECH_ARCHITECTURE.md",
        "requires_docs": ["docs/PRD.md"],
        "max_tokens": 16000,
    },
    "coding_standards": {
        "phase": 0,
        "display_name": "编码规范专家",
        "model": WORKER_MODEL_HEAVY,
        "prompt_file": "agents/phase0/coding_standards.md",
        "output_doc": "docs/CODING_STANDARDS.md",
        "requires_docs": ["docs/PRD.md", "docs/TECH_ARCHITECTURE.md"],
        "max_tokens": 16000,
    },
    "schema_architect": {
        "phase": 0,
        "display_name": "Schema 架构师",
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
        "display_name": "API 契约架构师",
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
        "display_name": "任务拆分专家",
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
    # Phase 1-N: 编码执行 Agent
    "agent_db": {
        "phase": 1,
        "display_name": "数据库迁移 Agent",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_db.md",
        "output_doc": None,
        "requires_docs": ["docs/DB_SCHEMA.md"],
        "max_tokens": 8000,
    },
    "agent_be": {
        "phase": 1,
        "display_name": "后端开发 Agent",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_be.md",
        "output_doc": None,
        "requires_docs": ["docs/API_CONTRACT.md", "docs/DB_SCHEMA.md", "docs/CODING_STANDARDS.md"],
        "max_tokens": 12000,
    },
    "agent_fe": {
        "phase": 1,
        "display_name": "前端开发 Agent",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_fe.md",
        "output_doc": None,
        "requires_docs": ["docs/CODING_STANDARDS.md", "docs/API_CONTRACT.md"],
        "max_tokens": 12000,
    },
    "agent_connect": {
        "phase": 1,
        "display_name": "联调对接 Agent",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_connect.md",
        "output_doc": None,
        "requires_docs": ["docs/API_CONTRACT.md", "docs/CODING_STANDARDS.md"],
        "max_tokens": 8000,
    },
    "agent_verify": {
        "phase": 1,
        "display_name": "验收测试 Agent",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_verify.md",
        "output_doc": None,
        "requires_docs": ["docs/TASK_BOOK.md"],
        "max_tokens": 4000,
    },
    "agent_fix": {
        "phase": 1,
        "display_name": "报错修复 Agent",
        "model": WORKER_MODEL_LIGHT,
        "prompt_file": "agents/phase1n/agent_fix.md",
        "output_doc": None,
        "requires_docs": ["docs/CODING_STANDARDS.md"],
        "max_tokens": 8000,
    },
}

# Phase 0 执行顺序（严格串行）
PHASE0_ORDER = [
    "prd_expert",
    "tech_architect",
    "coding_standards",
    "schema_architect",
    "api_contract",
    "task_decomposer",
]
