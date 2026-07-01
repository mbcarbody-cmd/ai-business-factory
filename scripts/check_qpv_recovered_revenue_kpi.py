from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'website' / 'recovered-revenue-kpi.html'


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f'Missing {label}: {needle}')


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise AssertionError(f'Forbidden {label}: {needle}')


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
    require(text, 'id="recovered-revenue-dashboard"', 'dashboard integration panel anchor')
    require(text, 'sourceDashboardLink', 'source dashboard top navigation id')
    require(text, 'commandDashboardLink', 'command dashboard top navigation id')
    require(text, 'backToSourceDashboard', 'dashboard panel source backlink')
    require(text, 'backToCommandDashboard', 'dashboard panel command backlink')
    require(text, './source-kpi-admin.html#recovered-revenue-dashboard', 'source dashboard recovered KPI link')
    require(text, './revenue-command-center.html#recovered-revenue-dashboard', 'command dashboard recovered KPI link')
    require(text, 'dashboardIntegration', 'dashboard integration export block')
    require(text, 'dashboardIntegrationView', 'dashboard integration rendered JSON')
    require(text, 'pendingConfirmations', 'pending confirmation KPI')
    require(text, 'paidRecoveryCount', 'paid recovery count KPI')
    require(text, 'conversionRateAfterReminderPct', 'after-reminder conversion KPI alias')
    require(text, 'dashboardIntegrationRule', 'dashboard integration QA rule')
    require(text, 'dashboardIntegrationRevenueEur:0', 'dashboard integration zero revenue guard')
    require(text, 'unverifiedDashboardRevenueEur:0', 'unverified dashboard zero revenue guard')
    require(text, 'dashboard integration link is not revenue', 'dashboard link weak-pattern rejection')
    require(text, 'qpv-recovered-revenue-kpi-v2-dashboard-integration', 'version bump for integration release')

    for needle, label in [
        ('dashboardIntegrationRevenueEur:19', 'fake dashboard integration revenue'),
        ('unverifiedDashboardRevenueEur:19', 'fake unverified dashboard revenue'),
        ('pendingRevenueEur:19', 'fake pending revenue'),
        ('recoveryReminderRevenueEur:19', 'fake reminder revenue'),
        ('convertedAfterReminderRevenueEur:19', 'fake handoff revenue'),
        ('proofSubmittedRevenueEur:19', 'fake proof revenue'),
        ('paymentReferenceRevenueEur:19', 'fake payment reference revenue'),
        ('dashboard integration link counts as revenue', 'dashboard-link-as-revenue claim'),
        ('pending handoff counts as revenue', 'pending-handoff-as-revenue claim'),
    ]:
        forbid(text, needle, label)

    print('OK recovered revenue KPI regression with dashboard integration links and verified-only revenue guard')


if __name__ == '__main__':
    main()
