#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'OPS/autonomous_gap_detection/SELF_GAP_DETECTOR_2026_06_15_LT.md',
    'OPS/org/SPECIALIST_GAP_AUDIT_2026_06_15_LT.md',
    'products/parts-seller-os/WORKFLOW_SPEC.md',
    'OPS/design/visual_quality_review_2026_06_15.md',
    'OPS/delivery/delivery_registry_2026_06_15.json',
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file() or (ROOT / p).stat().st_size == 0]
print('GAP CHECK')
print('PASS' if not missing else 'FAIL')
for p in missing:
    print('ERROR missing:', p)
sys.exit(1 if missing else 0)
