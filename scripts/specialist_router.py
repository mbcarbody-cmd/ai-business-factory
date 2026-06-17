#!/usr/bin/env python3
"""Deterministic specialist router for the 32x50 staffing model."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "OPS/org/specialist_router_2026_06_17.json"
STAFFING_PATH = ROOT / "OPS/org/specialist_staffing_32x50_2026_06_17.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def route_task(task: dict[str, Any]) -> dict[str, Any]:
    router = load_json(ROUTER_PATH)
    staffing = load_json(STAFFING_PATH)

    missing = [field for field in router["required_task_fields"] if not task.get(field)]
    if missing:
        raise ValueError(f"missing required task fields: {', '.join(missing)}")

    text = " ".join(
        str(task.get(field, ""))
        for field in ("title", "description", "money_path", "risk_domains", "keywords")
    ).lower()

    domain_request = any(term in text for term in ("buy domain", "purchase domain", "public address"))
    if domain_request and not task.get("functional_product_proof", False):
        return {
            "task_id": task["task_id"],
            "status": "blocked_by_no_domain_before_functional_product",
            "owner_specialty_id": "SPEC-013",
            "owner_seat_id": "SPEC-013-A001",
            "reviewer_specialty_ids": ["SPEC-001", "SPEC-012"],
            "rationale": "Public-address work is blocked until functional-product proof exists.",
            "output_path": task["output_path"],
            "done_proof": task["done_proof"],
            "fallback_next_task": task.get("fallback_next_task", "Continue the highest-value functional product task."),
        }

    freshness_terms = ("current", "latest", "price", "law", "api", "competitor", "contact route", "payment")
    freshness_sensitive = any(term in text for term in freshness_terms)
    if freshness_sensitive and not task.get("knowledge_refresh_complete", False):
        return {
            "task_id": task["task_id"],
            "status": "blocked_pending_knowledge_refresh",
            "owner_specialty_id": "SPEC-030",
            "owner_seat_id": "SPEC-030-A001",
            "reviewer_specialty_ids": [],
            "rationale": "Freshness-sensitive work must complete the continuous knowledge refresh rule first.",
            "output_path": task["output_path"],
            "done_proof": task["done_proof"],
            "fallback_next_task": task.get("fallback_next_task", "Run the knowledge refresh cycle."),
        }

    scores: dict[str, int] = {}
    matched: dict[str, list[str]] = {}
    for phrase, specialty_id in router["keyword_routes"].items():
        terms = phrase.split()
        hits = [term for term in terms if term in text]
        if hits:
            scores[specialty_id] = scores.get(specialty_id, 0) + len(hits)
            matched.setdefault(specialty_id, []).extend(hits)

    owner = max(scores, key=lambda item: (scores[item], item)) if scores else "SPEC-032"
    allocation_ids = {row["specialty_id"] for row in staffing["allocations"]}
    if owner not in allocation_ids:
        raise ValueError(f"router selected unstaffed specialty: {owner}")

    seat_number = int(hashlib.sha256(str(task["task_id"]).encode("utf-8")).hexdigest(), 16) % 50 + 1
    owner_seat = f"{owner}-A{seat_number:03d}"

    reviewers: list[str] = []
    reviewer_map = {
        "security": "SPEC-014",
        "privacy": "SPEC-015",
        "payment": "SPEC-025",
        "invoice": "SPEC-025",
        "release": "SPEC-011",
        "ci": "SPEC-011",
        "delivery": "SPEC-026",
        "client": "SPEC-026",
    }
    for term, specialty_id in reviewer_map.items():
        if term in text and specialty_id != owner and specialty_id not in reviewers:
            reviewers.append(specialty_id)
    reviewers = reviewers[:3]

    if task.get("blocked_by") and "SPEC-031" not in reviewers and owner != "SPEC-031":
        reviewers.append("SPEC-031")

    return {
        "task_id": task["task_id"],
        "status": "routed",
        "owner_specialty_id": owner,
        "owner_seat_id": owner_seat,
        "reviewer_specialty_ids": reviewers[:3],
        "routing_score": scores.get(owner, 0),
        "rationale": f"Matched terms: {sorted(set(matched.get(owner, [])))}" if scores else "No stronger domain match; routed to Build Orchestrator.",
        "output_path": task["output_path"],
        "done_proof": task["done_proof"],
        "fallback_next_task": task.get("fallback_next_task", "Route blocker to SPEC-031 and execute the next highest-value unblocked task."),
    }


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: specialist_router.py [task.json]", file=sys.stderr)
        return 2
    try:
        if len(sys.argv) == 2:
            task = load_json(Path(sys.argv[1]))
        else:
            task = json.load(sys.stdin)
        print(json.dumps(route_task(task), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ROUTER ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
