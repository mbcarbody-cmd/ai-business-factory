# OPS Gap Gate SOP

Date: 2026-06-17  
Owner: SPEC-011 QA Automation Engineer + SPEC-013 Release Engineer  
Status: automated_ci_connected

The previous workflow-write blocker is resolved. The automated gate is stored at `.github/workflows/ops-gap-gate.yml` and runs on relevant pull requests, pushes to `main`, and manual dispatch.

The automated gate executes:

```bash
python3 scripts/gap_check_2026_06_15.py
python3 scripts/ops_audit.py
```

It also smoke-tests `scripts/specialist_router.py` with a deterministic QA task.

The default gap check validates repository integrity: the 32-specialty catalog, 32x50 staffing manifest, continuous knowledge-refresh rule, specialist router, outreach-ready lead rows, offer and payment path, no-domain rule and required files.

External business evidence is checked separately. Run this strict command when testing paid-pilot and real-delivery proof:

```bash
python3 scripts/gap_check_2026_06_15.py --require-external-proof
```

The strict command remains failed until genuine external evidence exists. Templates and internal dry runs do not qualify.

## Manual fallback

Run the same commands locally after meaningful repository changes. Every failure becomes a task with an owner, output path, next action and fallback.

## Done condition

CI connection is complete when the workflow exists and a pull-request run reports its actual result. Repository integrity and external business proof are reported separately.
