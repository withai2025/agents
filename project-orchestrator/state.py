import json
from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path("projects")

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
    "prd_reviewed": False,
    "last_updated": "",
}


def _state_path(project_dir: Path) -> Path:
    return project_dir / "project_state.json"


def list_projects() -> list[dict]:
    """Return list of existing project summaries sorted by last updated."""
    if not PROJECTS_DIR.exists():
        return []
    projects = []
    for d in sorted(PROJECTS_DIR.iterdir(), reverse=True):
        if not d.is_dir():
            continue
        sp = _state_path(d)
        if not sp.exists():
            continue
        try:
            state = json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        # Count completed Phase 0 docs
        completed = sum(
            1 for v in state.get("phase0_documents", {}).values()
            if v.get("status") == "completed"
        )
        total = len(state.get("phase0_documents", {}))
        projects.append({
            "name": d.name,
            "created_at": state.get("created_at", ""),
            "phase0_progress": f"{completed}/{total}",
            "last_updated": state.get("last_updated", ""),
        })
    return projects


def load_state(project_name: str) -> dict:
    """Load state for a specific project."""
    project_dir = PROJECTS_DIR / project_name
    sp = _state_path(project_dir)
    if not sp.exists():
        state = DEFAULT_STATE.copy()
        state["project_name"] = project_name
        state["_project_dir"] = str(project_dir)
        return state
    state = json.loads(sp.read_text(encoding="utf-8"))
    state["_project_dir"] = str(project_dir)
    return state


def save_state(state: dict) -> None:
    """Persist state to the project's directory."""
    state["last_updated"] = datetime.now().isoformat()
    project_dir = Path(state["_project_dir"])
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    sp = _state_path(project_dir)
    sp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def init_state(project_name: str) -> dict:
    """Create a new project with the given name."""
    project_dir = PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    state = DEFAULT_STATE.copy()
    state["project_name"] = project_name
    state["_project_dir"] = str(project_dir)
    state["created_at"] = datetime.now().isoformat()
    save_state(state)
    return state


def get_next_phase0_agent(state: dict) -> str | None:
    """Return the name of the next pending Phase 0 agent, or None if all complete.

    If PRD is complete but the user hasn't reviewed it yet, block and return None
    so the orchestrator waits for confirmation before proceeding.
    """
    from config import PHASE0_ORDER

    # PRD review gate: block further progress until user confirms the PRD
    prd_status = state["phase0_documents"].get("prd_expert", {}).get("status")
    if prd_status == "completed" and not state.get("prd_reviewed", False):
        return None

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
