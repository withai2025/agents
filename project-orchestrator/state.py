import json
from pathlib import Path
from datetime import datetime

STATE_FILE = "project_state.json"

DEFAULT_STATE = {
    "project_name": "",
    "orchestrator_version": "2.0",
    "created_at": "",
    "phase0_documents": {
        "prd_expert":       {"status": "pending", "path": "docs/PRD.md",               "degraded": False},
        "tech_architect":   {"status": "pending", "path": "docs/TECH_ARCHITECTURE.md", "degraded": False},
        "coding_standards": {"status": "pending", "path": "docs/CODING_STANDARDS.md",  "degraded": False},
        "schema_architect": {"status": "pending", "path": "docs/DB_SCHEMA.md",         "degraded": False},
        "api_contract":     {"status": "pending", "path": "docs/API_CONTRACT.md",      "degraded": False},
        "task_decomposer":  {"status": "pending", "path": "docs/TASK_BOOK.md",         "degraded": False},
    },
    "phase1n_tasks": {
        "completed": [],
        "in_progress": None,
        "failed": [],
        "known_issues": [],
    },
    "conflict_log": [],
    "retry_counts": {},
    "last_updated": "",
}


def load_state() -> dict:
    path = Path(STATE_FILE)
    if not path.exists():
        return DEFAULT_STATE.copy()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict) -> None:
    state["last_updated"] = datetime.now().isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def init_state(project_name: str) -> dict:
    state = DEFAULT_STATE.copy()
    state["project_name"] = project_name
    state["created_at"] = datetime.now().isoformat()
    save_state(state)
    return state


def get_next_phase0_agent(state: dict) -> str | None:
    """返回下一个待执行的 Phase 0 Agent 名称，全部完成返回 None"""
    from config import PHASE0_ORDER
    for agent_name in PHASE0_ORDER:
        doc_state = state["phase0_documents"].get(agent_name, {})
        if doc_state.get("status") != "completed":
            return agent_name
    return None


def is_phase0_complete(state: dict) -> bool:
    return get_next_phase0_agent(state) is None


def mark_agent_completed(state: dict, agent_name: str) -> dict:
    if agent_name in state["phase0_documents"]:
        state["phase0_documents"][agent_name]["status"] = "completed"
        state["phase0_documents"][agent_name]["completed_at"] = datetime.now().isoformat()
    save_state(state)
    return state


def mark_agent_failed(state: dict, agent_name: str, error: str) -> dict:
    if agent_name in state["phase0_documents"]:
        state["phase0_documents"][agent_name]["status"] = "failed"
        state["phase0_documents"][agent_name]["error"] = error
        state["phase0_documents"][agent_name]["degraded"] = True
    save_state(state)
    return state


def increment_retry(state: dict, agent_name: str) -> int:
    count = state["retry_counts"].get(agent_name, 0) + 1
    state["retry_counts"][agent_name] = count
    save_state(state)
    return count
