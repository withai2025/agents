#!/usr/bin/env python3
"""Update Python agent files: English SYSTEM_PROMPT + Chinese SYSTEM_PROMPT_CN."""
from __future__ import annotations

import ast
import os
import textwrap

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "agents")
PHASE0_DIR = os.path.join(os.path.dirname(__file__), "..", "project-orchestrator", "agents")
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")

# Map Python file → (English .md source, Chinese .md source)
MAPPING = {
    "prd_expert.py": (
        f"{PHASE0_DIR}/phase0/prd_expert.md",
        f"{PHASE0_DIR}/phase0/prd_expert_cn.md",
    ),
    "mobile_architect.py": (
        f"{PHASE0_DIR}/phase0/tech_architect.md",
        f"{PHASE0_DIR}/phase0/tech_architect_cn.md",
    ),
    "coding_standards.py": (
        f"{PHASE0_DIR}/phase0/coding_standards.md",
        f"{PHASE0_DIR}/phase0/coding_standards_cn.md",
    ),
    "db_schema_architect.py": (
        f"{PHASE0_DIR}/phase0/schema_architect.md",
        f"{PHASE0_DIR}/phase0/schema_architect_cn.md",
    ),
    "api_contract_architect.py": (
        f"{PHASE0_DIR}/phase0/api_contract.md",
        f"{PHASE0_DIR}/phase0/api_contract_cn.md",
    ),
    "task_decomposer.py": (
        f"{PHASE0_DIR}/phase0/task_decomposer.md",
        f"{PHASE0_DIR}/phase0/task_decomposer_cn.md",
    ),
    "project_orchestrator.py": (
        f"{PHASE0_DIR}/orchestrator.md",
        f"{PHASE0_DIR}/orchestrator_cn.md",
    ),
}

# Files whose English source is a skills/ file (has YAML front-matter to strip)
SKILLS_SOURCE = {"product_researcher.py", "prompt_engineer.py", "ux_designer.py"}


def read_md(path: str, strip_frontmatter: bool = False) -> str:
    """Read .md file, optionally stripping YAML front-matter."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if strip_frontmatter and content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
    return content.strip()


def escape_for_python_str(s: str) -> str:
    """Escape a string for use inside a Python triple-quoted string."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"""', '\\"\\"\\"')
    return s


def find_system_prompt_span(file_content: str) -> tuple[int, int] | None:
    """Find the start and end positions of the SYSTEM_PROMPT string in Python source.

    Returns (start_pos, end_pos) where start is the position of 'SYSTEM_PROMPT ='
    and end is the position after the closing '\"\"\"'.
    """
    marker = "SYSTEM_PROMPT = "
    idx = file_content.find(marker)
    if idx == -1:
        return None

    # Find the opening triple quote
    start = idx + len(marker)
    if file_content[start:start+3] != '"""':
        return None

    # Find the closing triple quote
    content_start = start + 3
    end = file_content.find('"""', content_start)
    while end != -1:
        # Make sure this isn't an escaped triple quote
        if end > 0 and file_content[end-1:end] == '\\':
            # Count backslashes before the """
            bs_count = 0
            i = end - 1
            while i >= 0 and file_content[i] == '\\':
                bs_count += 1
                i -= 1
            if bs_count % 2 == 1:  # odd number = escaped
                end = file_content.find('"""', end + 3)
                continue
        break

    if end == -1:
        return None

    return (idx, end + 3)


def update_agent_file(py_path: str, en_md_path: str, cn_md_path: str,
                      is_skills_source: bool = False) -> bool:
    """Update a Python agent file with English + Chinese system prompts."""
    en_prompt = read_md(en_md_path, strip_frontmatter=is_skills_source)
    cn_prompt = read_md(cn_md_path, strip_frontmatter=is_skills_source)

    en_escaped = escape_for_python_str(en_prompt)
    cn_escaped = escape_for_python_str(cn_prompt)

    with open(py_path, encoding="utf-8") as f:
        original = f.read()

    # Remove existing SYSTEM_PROMPT_CN if present
    cn_marker = "SYSTEM_PROMPT_CN = "
    if cn_marker in original:
        span = find_system_prompt_span(original)
        if span is None:
            print(f"  WARNING: SYSTEM_PROMPT_CN exists but can't find SYSTEM_PROMPT span in {os.path.basename(py_path)}")
            return False
        # Find end of SYSTEM_PROMPT_CN
        cn_idx = original.find(cn_marker)
        cn_span = find_system_prompt_span(original[cn_idx:])
        if cn_span:
            original = original[:span[0]] + original[cn_idx + cn_span[1]:]

    span = find_system_prompt_span(original)
    if span is None:
        print(f"  WARNING: Can't find SYSTEM_PROMPT span in {os.path.basename(py_path)}")
        return False

    new_block = (
        f'SYSTEM_PROMPT = """\n{en_escaped}\n"""\n\n'
        f'SYSTEM_PROMPT_CN = """\n{cn_escaped}\n"""\n'
    )

    new_content = original[:span[0]] + new_block + original[span[1]:]

    with open(py_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    for py_file, (en_src, cn_src) in MAPPING.items():
        py_path = os.path.join(AGENTS_DIR, py_file)
        if not os.path.exists(py_path):
            print(f"  ✗ File not found: {py_file}")
            continue
        if not os.path.exists(en_src):
            print(f"  ✗ EN source not found: {en_src}")
            continue
        if not os.path.exists(cn_src):
            print(f"  ✗ CN source not found: {cn_src}")
            continue
        if update_agent_file(py_path, en_src, cn_src):
            print(f"  ✓ Updated {py_file}")

    # Handle skills-sourced files separately
    for py_file in sorted(SKILLS_SOURCE):
        py_path = os.path.join(AGENTS_DIR, py_file)
        base_name = py_file.replace(".py", "").replace("_", "-")
        en_src = os.path.join(SKILLS_DIR, f"{base_name}.md")
        cn_src = os.path.join(SKILLS_DIR, f"{base_name}_cn.md")
        if not os.path.exists(py_path):
            print(f"  ✗ File not found: {py_file}")
            continue
        if not os.path.exists(en_src):
            print(f"  ✗ EN skills source not found: {en_src}")
            continue
        if not os.path.exists(cn_src):
            print(f"  ✗ CN skills source not found: {cn_src}")
            continue
        if update_agent_file(py_path, en_src, cn_src, is_skills_source=True):
            print(f"  ✓ Updated {py_file} (skills source)")


if __name__ == "__main__":
    main()
