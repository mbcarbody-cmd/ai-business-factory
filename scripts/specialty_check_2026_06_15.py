#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'OPS/org/autonomous_product_specialties_2026_06_15.json',
    'OPS/operating_loops/specialty_router_2026_06_15.json',
    'OPS/org/specialist_closer_cohort_500_2026_06_15.json',
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file() or (ROOT / p).stat().st_size == 0]
print('SPECIALTY CHECK')
print('PASS' if not missing else 'FAIL')
for p in missing:
    print('ERROR missing:', p)
sys.exit(1 if missing else 0)
