#!/usr/bin/env python3
"""Validate AI agent outcome *evidence*, not story-like progress reports.

A bank transaction export must be provided independently before money is counted.
This is a schema/proof gate, NOT a verifier of external websites or authenticity.
Never commit bank exports or personal buyer data to GitHub.
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit


def valid_url(value):
    if not isinstance(value, str):
        return False
    try:
        p = urlsplit(value)
        return p.scheme == "https" and bool(p.netloc)
    except ValueError:
        return False


def _amount(value):
    try:
        n = round(float(value), 2)
    except (TypeError, ValueError, OverflowError):
        return None
    return n if n >= 0 and n < 1e12 else None


def evaluate(events, bank_transactions=()):
    """Returns evidence statuses and confirmed cash, requiring exact bank matches."""
    bank_by_ref = {}
    for t in bank_transactions:
        if not isinstance(t, dict):
            continue
        ref, amount = str(t.get("reference", "")).strip(), _amount(t.get("amount_eur"))
        if ref and amount is not None and t.get("received") is True:
            # Ambiguous duplicate references are never accepted as evidence.
            if ref in bank_by_ref:
                bank_by_ref[ref] = None
            else:
                bank_by_ref[ref] = amount
    rows, seen_ids, used_bank_refs = [], set(), set()
    gross, expenses = 0.0, 0.0
    for e in events:
        if not isinstance(e, dict):
            rows.append({"status": "REJECTED", "reason": "not_object"})
            continue
        event_id = str(e.get("id", "")).strip()
        kind = str(e.get("kind", "")).strip()
        row = {"id": event_id, "kind": kind}
        if not event_id or event_id in seen_ids:
            row.update(status="REJECTED", reason="missing_or_duplicate_id")
            rows.append(row)
            continue
        seen_ids.add(event_id)
        if kind == "published_listing":
            row.update(
                status="EVIDENCE_ONLY_NOT_LIVE_VERIFIED" if valid_url(e.get("public_url")) else "REJECTED",
                reason="url_must_be_checked_live_by_agent" if valid_url(e.get("public_url")) else "missing_https_url",
            )
        elif kind == "media_file":
            f = Path(str(e.get("local_path", "")))
            exists = bool(str(e.get("local_path", "")).strip()) and f.is_file() and f.stat().st_size > 0
            row.update(status="FILE_EXISTS_NOT_QA" if exists else "REJECTED",
                       reason="media_file_needs_manual_qa" if exists else "missing_or_empty_file")
        elif kind == "buyer_lead":
            ok = valid_url(e.get("source_url")) and bool(str(e.get("inbound_message_ref", "")).strip())
            row.update(status="LEAD_EVIDENCE_REQUIRES_CONTACT_CHECK" if ok else "REJECTED",
                       reason="not_a_paid_sale" if ok else "needs_source_url_and_inbound_message_ref")
        elif kind == "paid_sale":
            ref = str(e.get("payment_reference", "")).strip()
            expected = _amount(e.get("gross_eur"))
            cost = _amount(e.get("expenses_eur"))
            bank_amount = bank_by_ref.get(ref)
            matched = bool(ref) and ref not in used_bank_refs and expected is not None and cost is not None and bank_amount is not None and abs(bank_amount - expected) < 0.005
            if matched:
                used_bank_refs.add(ref)
                gross += expected
                expenses += cost
                row.update(status="BANK_ROW_MATCHED", amount_eur=expected,
                           net_after_recorded_expenses_eur=round(expected-cost, 2),
                           reason="bank_row_match_only_verify_export_is_authentic")
            else:
                row.update(status="UNCONFIRMED_NO_REVENUE_COUNTED",
                           reason="no_exact_unique_received_bank_transaction_match")
        else:
            row.update(status="REJECTED", reason="unsupported_kind")
        rows.append(row)
    return {
        "events": rows,
        "bank_row_matched_gross_eur": round(gross, 2),
        "bank_row_matched_net_after_recorded_expenses_eur": round(gross-expenses, 2),
        "warning": "Bank rows and expenses must come from authentic external records; this script cannot authenticate their source or completeness.",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("events", type=Path, help="JSON file containing {'events':[...]} (no secrets)")
    p.add_argument("--bank-rows", type=Path, help="Independent PRIVATE JSON export: {'transactions':[...]} (never commit)")
    p.add_argument("--output", type=Path, help="Optional output JSON path")
    args = p.parse_args()
    data = json.loads(args.events.read_text(encoding="utf-8"))
    bank = json.loads(args.bank_rows.read_text(encoding="utf-8")) if args.bank_rows else {"transactions": []}
    result = evaluate(data["events"], bank["transactions"])
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
