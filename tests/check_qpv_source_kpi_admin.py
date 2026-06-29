from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website" / "source-kpi-admin.html"


def read_page() -> str:
    assert PAGE.exists(), "source-kpi-admin.html must exist as a deployable admin UI"
    return PAGE.read_text(encoding="utf-8")


def test_source_kpi_admin_reads_shared_ledgers_and_filters_sources():
    html = read_page()
    assert "qpvOrderLedger" in html
    assert "qpvPaymentProofLedger" in html
    assert "qpvConversionLedger" in html
    assert "sourceFilter" in html
    assert "function sourceStats" in html
    assert "function allSources" in html
    assert "function sourceOf" in html


def test_source_kpi_admin_has_buyer_revenue_paths():
    html = read_page()
    assert "./offer.html?source=source_kpi_admin" in html
    assert "./checkout.html?source=source_kpi_admin" in html
    assert "./payment-ledger.html?source=source_kpi_admin" in html
    assert "./paid-confirmation.html" in html
    assert "Order admin" in html


def test_source_kpi_admin_preserves_zero_revenue_until_verified_paid():
    html = read_page()
    assert "Only paid/delivered order rows count confirmed EUR" in html
    assert "proofSubmittedRevenueEur:0" in html
    assert "unverifiedProofRevenueEur:0" in html
    assert "proof_submitted_manual_review is not paid" in html
    assert "paymentReference text is not revenue" in html
    assert "source visit is not revenue" in html


def test_source_kpi_admin_exposes_measurable_kpis():
    html = read_page()
    for marker in [
        "kpiSources",
        "kpiLeads",
        "kpiOrders",
        "kpiProofs",
        "kpiPaid",
        "kpiRevenue",
        "confirmedRevenueEur",
        "uniqueLeads",
        "paidRows",
    ]:
        assert marker in html


def test_source_kpi_admin_exports_source_filtered_unpaid_proof_followups():
    html = read_page()
    for marker in [
        "copyUnpaidProofs",
        "downloadUnpaidProofs",
        "unpaidProofRows",
        "toUnpaidProofCsv",
        "qpv-unpaid-proof-follow-up.csv",
        "needs_manual_payment_follow_up",
        "Source-filtered unpaid proof follow-up export",
        "Export only unpaid/unverified proof rows for buyer follow-up",
    ]:
        assert marker in html

    for csv_header in [
        "source",
        "leadId",
        "buyer",
        "proofStatus",
        "proofSubmittedAt",
        "paymentReference",
        "followUpStatus",
        "confirmedRevenueEur",
    ]:
        assert csv_header in html

    assert "orderPaidIndex" in html, "paid order rows must suppress follow-up exports"
    assert "seen=new Set" in html, "duplicate unpaid proof rows must be suppressed"
    assert "confirmedRevenueEur:0" in html, "unpaid proof export must not count revenue"


def test_source_kpi_admin_blocks_weak_patterns():
    html = read_page()
    weak_patterns = [
        "source visit is not revenue",
        "lead event is not revenue",
        "checkout order is not revenue until paid",
        "proof_submitted_manual_review is not paid",
        "paymentReference text is not revenue",
        "unpaid proof export is not revenue",
    ]
    for pattern in weak_patterns:
        assert pattern in html
