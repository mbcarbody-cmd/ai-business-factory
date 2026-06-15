#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'OPS/autonomous_gap_detection/SELF_GAP_DETECTOR_2026_06_15_LT.md',
    'OPS/org/SPECIALIST_GAP_AUDIT_2026_06_15_LT.md',
    'OPS/org/specialist_closer_cohort_500_2026_06_15.json',
    'OPS/TASK_BOARD/gap_tasks_2026_06_15.json',
    'products/parts-seller-os/WORKFLOW_SPEC.md',
    'OPS/design/visual_quality_review_2026_06_15.md',
    'OPS/delivery/delivery_registry_2026_06_15.json',
    'OPS/deploy_loop/release_registry_2026_06_15.md',
    'OPS/data_intelligence/lead_review_queue_2026_06_15.json',
    'OPS/commercial/offer_acceptance_path_2026_06_15.md',
    'OPS/commercial/external_proof_register_2026_06_15.json',
    'OPS/ci/gap_gate_manual_sop_2026_06_15.md',
    'OPS/core_status_addendum_2026_06_15.md',
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file() or (ROOT / p).stat().st_size == 0]
print('GAP CHECK')
print('PASS' if not missing else 'FAIL')
for p in missing:
    print('ERROR missing:', p)
sys.exit(1 if missing else 0)
