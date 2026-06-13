#!/usr/bin/env python3
"""Dependency-free local OPS audit for ai-business-factory."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    ".claude/settings.json",
    "OPS/CORE_OS_STATUS.md",
    "OPS/task_board.json",
    "OPS/task_board_v2.json",
    "OPS/agent_memory/README.md",
    "OPS/competitor_intelligence/competitors.json",
    "OPS/product_gates/product_stages.json",
    "OPS/deploy_loop/deploy_sop.md",
    "OPS/qa/bug_board.json",
    "OPS/cfo/costs.json",
    "OPS/revenue_ops/lead_pipeline.json",
    "OPS/delivery/72h_delivery_playbook.md",
    "OPS/marketplace/roadmap.md",
    "OPS/marketplace/parts_os_mvp_data_model.json",
    "OPS/data_intelligence/PUBLIC_DATA_COLLECTION_PLAYBOOK.md",
    "OPS/data_intelligence/source_registry.json",
    "OPS/data_intelligence/verification_queue.json",
    "OPS/model_council/CLAUDE_CODE_EXECUTION_PLAYBOOK_LT.md",
]

TASK_REQUIRED_FIELDS = [
    "id", "title", "layer", "owner", "status", "priority",
    "next_role", "next_action", "output_path", "done_proof"
]

TASK_V2_REQUIRED_FIELDS = [
    "id", "title", "layer", "owner", "status", "priority", "deadline",
    "money_path_or_strategic_reason", "next_role", "next_action", "blocker",
    "fallback_next_task", "output_path", "done_proof", "proof_status",
    "proof_verified_by"
]

BUG_REQUIRED_FIELDS = [
    "id", "product", "workflow", "severity", "status", "owner",
    "expected", "actual", "next_action", "proof_path"
]


def load_json(path: str) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def has_value(record: dict[str, Any], field: str) -> bool:
    value = record.get(field)
    return value is not None and value != "" and value != [] and value != {}


def audit_required_files(errors: list[str]) -> None:
    for rel_path in REQUIRED_FILES:
        if not (ROOT / rel_path).exists():
            errors.append(f"missing required file: {rel_path}")


def audit_task_board(errors: list[str], warnings: list[str]) -> None:
    board = load_json("OPS/task_board.json")
    for task in board.get("tasks", []):
        missing = [field for field in TASK_REQUIRED_FIELDS if not has_value(task, field)]
        if missing:
            errors.append(f"task {task.get('id', '<unknown>')} missing fields: {', '.join(missing)}")
        if task.get("status") == "blocked" and not task.get("next_action"):
            errors.append(f"task {task.get('id')} blocked without next_action")
        if task.get("status") == "done" and not task.get("done_proof"):
            errors.append(f"task {task.get('id')} done without done_proof")
        if task.get("status") in {"ready", "in_progress"} and not task.get("output_path"):
            warnings.append(f"task {task.get('id')} has no output_path")


def audit_task_board_v2(errors: list[str]) -> None:
    board = load_json("OPS/task_board_v2.json")
    for task in board.get("tasks", []):
        missing = [field for field in TASK_V2_REQUIRED_FIELDS if not has_value(task, field)]
        if missing:
            errors.append(f"task_v2 {task.get('id', '<unknown>')} missing fields: {', '.join(missing)}")
        if task.get("status") == "blocked" and not task.get("fallback_next_task"):
            errors.append(f"task_v2 {task.get('id')} blocked without fallback_next_task")
        if task.get("status") == "done" and task.get("proof_status") in {None, "", "missing"}:
            errors.append(f"task_v2 {task.get('id')} done with missing proof_status")


def audit_bug_board(errors: list[str], warnings: list[str]) -> None:
    board = load_json("OPS/qa/bug_board.json")
    open_high = []
    for bug in board.get("bugs", []):
        missing = [field for field in BUG_REQUIRED_FIELDS if not has_value(bug, field)]
        if missing:
            errors.append(f"bug {bug.get('id', '<unknown>')} missing fields: {', '.join(missing)}")
        if bug.get("status") in {"open", "in_progress"} and bug.get("severity") in {"critical", "high"}:
            open_high.append(bug.get("id"))
    if open_high:
        warnings.append("open critical/high QA items require Judge approval before delivery: " + ", ".join(open_high))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    audit_required_files(errors)

    for fn in (audit_task_board, audit_bug_board):
        try:
            fn(errors, warnings)
        except Exception as exc:
            errors.append(f"audit failed in {fn.__name__}: {exc}")

    try:
        audit_task_board_v2(errors)
    except Exception as exc:
        errors.append(f"audit failed in audit_task_board_v2: {exc}")

    print("OPS AUDIT RESULT")
    print("================")
    print("FAIL" if errors else "PASS")

    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
