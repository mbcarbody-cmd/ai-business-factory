from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'website' / 'recovered-revenue-kpi.html'


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f'Missing {label}: {needle}')


def main() -> None:
    text = PAGE.read_text(encoding='utf-8')
    require(text, 'qpvRecoveryConversionHandoffLedger', 'recovery conversion handoff ledger binding')
    require(text, 'paid_confirmed', 'paid confirmed status gate')
    require(text, 'paidEventId', 'verified paid event id requirement')
    require(text, 'dedupePaid', 'duplicate suppression function')
    require(text, 'blockedDuplicatePaidHandoffs', 'duplicate paid handoff KPI')
    require(text, 'recoveredRevenueEur', 'verified recovered revenue KPI')
    require(text, 'afterReminderConversionRatePct', 'after-reminder conversion KPI')
    require(text, 'pendingRevenueEur:0', 'pending rows zero-revenue guard')
    require(text, 'recoveryReminderRevenueEur:0', 'recovery reminder zero-revenue guard')
    require(text, 'convertedAfterReminderRevenueEur:0', 'handoff zero-revenue guard')
    require(text, 'proofSubmittedRevenueEur:0', 'proof zero-revenue guard')
    require(text, 'paymentReferenceRevenueEur:0', 'payment reference zero-revenue guard')
    require(text, 'pending handoff is not revenue', 'weak-pattern rejection for pending handoff')
    require(text, 'duplicate paid click is not revenue', 'weak-pattern rejection for duplicate paid click')
    require(text, './paid-confirmation.html?source=recovered_revenue_kpi', 'paid gate navigation')
    require(text, './payment-recovery-queue.html?source=recovered_revenue_kpi', 'recovery queue navigation')
    print('OK recovered revenue KPI regression')


if __name__ == '__main__':
    main()
