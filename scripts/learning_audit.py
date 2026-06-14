#!/usr/bin/env python3
"""Dependency-free learning layer audit for ai-business-factory."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_LEARNING_FILES = [
    "OPS/org/TEN_THOUSAND_LEARNING_WORKFORCE_2026_06_14.json",
    "OPS/learning/GLOBAL_KNOWLEDGE_CORE_LT.md",
    "OPS/learning/AI_BUSINESS_FACTORY_LEARNING_ACADEMY_LT.md",
    "OPS/learning/worker_exam_matrix.json",
    "OPS/learning/knowledge_sync_bus.json",
    "OPS/learning/parts_seller_os_training_matrix.json",
    "OPS/learning/learning_metrics_2026_06_14.json",
    "OPS/TASK_BOARD/learning_scale_tasks_2026_06_14.json",
]


def load_json(path: str) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def has_value(record: dict[str, Any], field: str) -> bool:
    value = record.get(field)
    return value is not None and value != "" and value != [] and value != {}


def audit_required_files(errors: list[str]) -> None:
    for rel_path in REQUIRED_LEARNING_FILES:
        if not (ROOT / rel_path).exists():
            errors.append(f"missing learning file: {rel_path}")


def audit_workforce_directive(errors: list[str], warnings: list[str]) -> None:
    directive = load_json("OPS/org/TEN_THOUSAND_LEARNING_WORKFORCE_2026_06_14.json")
    if directive.get("status") != "active":
        errors.append("10k learning directive must be active")
    if directive.get("total_units") != 10000:
        errors.append("10k learning directive total_units must be 10000")
    allocation = directive.get("allocation", [])
    units = sum(int(cohort.get("units", 0)) for cohort in allocation)
    if units != 10000:
        errors.append(f"10k learning allocation must sum to 10000, got {units}")
    if len(allocation) != 10:
        warnings.append(f"expected 10 learning cohorts, got {len(allocation)}")
    for cohort in allocation:
        for field in ["cohort_id", "name", "units", "mission", "canonical_output_path", "done_proof"]:
            if not has_value(cohort, field):
                errors.append(f"learning cohort {cohort.get('cohort_id', '<unknown>')} missing {field}")


def audit_exam_matrix(errors: list[str], warnings: list[str]) -> None:
    matrix = load_json("OPS/learning/worker_exam_matrix.json")
    if matrix.get("minimum_passing_score", 0) < 85:
        errors.append("minimum passing score must be at least 85")
    modules = matrix.get("global_exam_modules", [])
    if len(modules) < 10:
        errors.append("exam matrix must define at least 10 global exam modules")
    module_ids = {module.get("module_id") for module in modules}
    for module in modules:
        for field in ["module_id", "name", "required_for", "source", "pass_condition"]:
            if not has_value(module, field):
                errors.append(f"exam module {module.get('module_id', '<unknown>')} missing {field}")
    for requirement in matrix.get("cohort_exam_requirements", []):
        for module_id in requirement.get("required_modules", []):
            if module_id not in module_ids:
                errors.append(f"cohort {requirement.get('cohort_id')} references unknown exam module {module_id}")


def audit_knowledge_sync(errors: list[str], warnings: list[str]) -> None:
    bus = load_json("OPS/learning/knowledge_sync_bus.json")
    lessons = bus.get("lessons", [])
    if not lessons:
        errors.append("knowledge sync bus must contain at least one lesson")
    for lesson in lessons:
        for field in ["id", "source_project", "source_output_path", "lesson_type", "lesson", "reusable_rule", "affected_projects", "owner", "sync_status", "proof_path", "next_action"]:
            if not has_value(lesson, field):
                errors.append(f"lesson {lesson.get('id', '<unknown>')} missing {field}")
        if lesson.get("sync_status") == "blocked" and not has_value(lesson, "next_action"):
            errors.append(f"lesson {lesson.get('id')} blocked without next_action")
    if not any(lesson.get("sync_status") in {"queued_for_sync", "synced"} for lesson in lessons):
        warnings.append("no lessons are queued_for_sync or synced")


def audit_parts_training(errors: list[str], warnings: list[str]) -> None:
    matrix = load_json("OPS/learning/parts_seller_os_training_matrix.json")
    modules = matrix.get("workflow_modules", [])
    required_modules = {
        "add_part",
        "categorize",
        "fitment",
        "suggest_location",
        "set_price_and_floor",
        "listing_readiness",
        "reserve_order_delivery",
        "ageing_dead_stock",
    }
    found = {module.get("module") for module in modules}
    missing = required_modules - found
    if missing:
        errors.append("parts seller training missing modules: " + ", ".join(sorted(missing)))
    for module in modules:
        for field in ["module", "what_workers_must_know", "rules_to_apply", "test_case"]:
            if not has_value(module, field):
                errors.append(f"parts training module {module.get('module', '<unknown>')} missing {field}")


def audit_learning_task_manifest(errors: list[str]) -> None:
    manifest = load_json("OPS/TASK_BOARD/learning_scale_tasks_2026_06_14.json")
    tasks = manifest.get("tasks", [])
    if len(tasks) < 7:
        errors.append("learning task manifest must define at least 7 tasks")
    for task in tasks:
        for field in ["id", "title", "layer", "owner", "status", "priority", "next_role", "next_action", "output_path", "done_proof"]:
            if not has_value(task, field):
                errors.append(f"learning task {task.get('id', '<unknown>')} missing {field}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    audit_required_files(errors)
    for fn in (audit_workforce_directive, audit_exam_matrix, audit_knowledge_sync, audit_parts_training):
        try:
            fn(errors, warnings)
        except Exception as exc:
            errors.append(f"audit failed in {fn.__name__}: {exc}")
    try:
        audit_learning_task_manifest(errors)
    except Exception as exc:
        errors.append(f"audit failed in audit_learning_task_manifest: {exc}")

    print("LEARNING AUDIT RESULT")
    print("=====================")
    print("FAIL" if errors else "PASS")
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
