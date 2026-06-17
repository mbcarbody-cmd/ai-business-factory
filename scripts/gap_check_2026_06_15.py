#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "OPS/autonomous_gap_detection/SELF_GAP_DETECTOR_2026_06_15_LT.md",
    "OPS/org/SPECIALIST_GAP_AUDIT_2026_06_15_LT.md",
    "OPS/org/autonomous_product_specialties_2026_06_15.json",
    "OPS/org/specialist_staffing_32x50_2026_06_17.json",
    "OPS/org/continuous_knowledge_refresh_2026_06_17.json",
    "OPS/org/specialist_router_2026_06_17.json",
    "scripts/specialist_router.py",
    "OPS/TASK_BOARD/gap_tasks_2026_06_15.json",
    "products/parts-seller-os/WORKFLOW_SPEC.md",
    "OPS/design/visual_quality_review_2026_06_15.md",
    "OPS/delivery/delivery_registry_2026_06_15.json",
    "OPS/deploy_loop/release_registry_2026_06_15.md",
    "OPS/data_intelligence/lead_review_queue_2026_06_15.json",
    "OPS/commercial/offer_acceptance_path_2026_06_15.md",
    "OPS/commercial/offer_acceptance_payment_register_2026_06_17.json",
    "OPS/commercial/external_proof_register_2026_06_15.json",
    "OPS/ci/gap_gate_manual_sop_2026_06_15.md",
    "OPS/core_status_addendum_2026_06_15.md",
    ".github/workflows/ops-gap-gate.yml",
]


def read_json(path: str, errors: list[str]) -> dict[str, Any]:
    try:
        with (ROOT / path).open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        if not isinstance(value, dict):
            errors.append(f"{path}: JSON root must be an object")
            return {}
        return value
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")


def check_specialties(errors: list[str]) -> set[str]:
    data = read_json("OPS/org/autonomous_product_specialties_2026_06_15.json", errors)
    rows = data.get("specialties", [])
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    if len(rows) != 32:
        errors.append(f"specialty catalog must contain 32 specialties, found {len(rows)}")
    if len(set(ids)) != 32 or None in ids:
        errors.append("specialty ids must be 32 unique non-empty values")
    if data.get("no_domain_before_product") is not True:
        errors.append("specialty catalog must keep no_domain_before_product=true")
    return set(ids)


def check_staffing(specialty_ids: set[str], errors: list[str]) -> None:
    data = read_json("OPS/org/specialist_staffing_32x50_2026_06_17.json", errors)
    rows = data.get("allocations", [])
    ids = {row.get("specialty_id") for row in rows if isinstance(row, dict)}
    seat_sum = sum(int(row.get("seat_count", 0)) for row in rows if isinstance(row, dict))
    if data.get("total_specialties") != 32 or len(rows) != 32:
        errors.append("staffing manifest must allocate exactly 32 specialties")
    if any(row.get("seat_count") != 50 for row in rows if isinstance(row, dict)):
        errors.append("every specialty allocation must contain exactly 50 seats")
    if data.get("seats_per_specialty") != 50 or data.get("total_specialist_seats") != 1600 or seat_sum != 1600:
        errors.append("staffing totals must equal 32 x 50 = 1600")
    if ids != specialty_ids:
        errors.append("staffing specialty ids must exactly match the specialty catalog")


def check_knowledge_refresh(errors: list[str]) -> None:
    data = read_json("OPS/org/continuous_knowledge_refresh_2026_06_17.json", errors)
    if data.get("status") != "active":
        errors.append("continuous knowledge refresh rule must be active")
    if data.get("continuous_refresh_required") is not True or data.get("refresh_on_every_execution_cycle") is not True:
        errors.append("continuous knowledge refresh must run on every execution cycle")
    if not data.get("cycle_triggers") or not data.get("refresh_sequence"):
        errors.append("continuous knowledge refresh must define triggers and sequence")


def check_router(specialty_ids: set[str], errors: list[str]) -> None:
    data = read_json("OPS/org/specialist_router_2026_06_17.json", errors)
    if data.get("status") != "active":
        errors.append("specialist router must be active")
    if data.get("executable") != "scripts/specialist_router.py":
        errors.append("specialist router must point to scripts/specialist_router.py")
    routed_ids = set(data.get("keyword_routes", {}).values())
    if routed_ids != specialty_ids:
        errors.append("specialist router keyword routes must cover all 32 specialties")
    required_fields = set(data.get("required_task_fields", []))
    if not {"task_id", "title", "description", "priority", "output_path", "done_proof"}.issubset(required_fields):
        errors.append("specialist router is missing required ownership/proof task fields")


def check_outreach_queue(errors: list[str]) -> None:
    data = read_json("OPS/data_intelligence/lead_review_queue_2026_06_15.json", errors)
    rows = data.get("rows", [])
    if not rows:
        errors.append("lead review queue must contain at least one row")
        return
    for row in rows:
        if row.get("state") != "outreach_ready":
            errors.append(f"lead {row.get('id')} is not outreach_ready")
        for field in ("relevance_verdict", "allowed_contact_route", "route_source", "reviewed_at", "reviewed_by"):
            if not row.get(field):
                errors.append(f"lead {row.get('id')} missing {field}")
    if data.get("outreach_ready_count") != len(rows):
        errors.append("outreach_ready_count must equal the number of verified rows")


def check_offer_and_payment(errors: list[str], strict_external: bool) -> None:
    offer_text = (ROOT / "OPS/commercial/offer_acceptance_path_2026_06_15.md").read_text(encoding="utf-8").lower()
    for term in ("accepted", "invoice_issued", "payment_pending", "paid", "payment evidence"):
        if term not in offer_text:
            errors.append(f"offer acceptance path missing term: {term}")

    register = read_json("OPS/commercial/offer_acceptance_payment_register_2026_06_17.json", errors)
    allowed = set(register.get("allowed_states", []))
    if not {"accepted", "invoice_issued", "payment_pending", "paid", "started", "delivered"}.issubset(allowed):
        errors.append("payment register is missing required commercial states")
    paid_state = register.get("first_paid_pilot", {}).get("state")
    if strict_external and paid_state != "done":
        errors.append("strict external proof: first paid pilot evidence is not done")


def check_external_proof(errors: list[str], strict_external: bool) -> None:
    data = read_json("OPS/commercial/external_proof_register_2026_06_15.json", errors)
    items = {item.get("id"): item for item in data.get("items", []) if isinstance(item, dict)}
    public_address = items.get("EXT-003", {})
    if public_address.get("state") != "blocked_until_functional_product":
        errors.append("no-domain-before-functional-product rule is not intact")
    for item_id in ("EXT-001", "EXT-002"):
        item = items.get(item_id, {})
        if item.get("state") == "done" and not item.get("evidence_reference"):
            errors.append(f"{item_id} cannot be done without evidence_reference")
        if strict_external and item.get("state") != "done":
            errors.append(f"strict external proof: {item_id} is not done")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-external-proof", action="store_true", help="Fail until paid-pilot and real-delivery evidence exist.")
    args = parser.parse_args()

    errors: list[str] = []
    check_required(errors)
    specialty_ids = check_specialties(errors)
    check_staffing(specialty_ids, errors)
    check_knowledge_refresh(errors)
    check_router(specialty_ids, errors)
    check_outreach_queue(errors)
    check_offer_and_payment(errors, args.require_external_proof)
    check_external_proof(errors, args.require_external_proof)

    print("OPS GAP CHECK")
    print("PASS" if not errors else "FAIL")
    print(f"mode={'strict_external' if args.require_external_proof else 'repo_integrity'}")
    for error in errors:
        print(f"ERROR: {error}")
    if not args.require_external_proof:
        print("INFO: external paid-pilot and real-delivery proof remain business-event gates and are not fabricated by CI.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
