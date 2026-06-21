# QA evidence — AI asistento architektas — 2026-06-21

Product path: website/ai-assistant-architect.html
Primary path: index.html redirects to the product through a meta refresh.

Executable test path: tests/test_ai_assistant_architect.py
Workflow path: .github/workflows/assistant-architect-qa.yml

Static critical-path checks confirmed from repository contents:
- Form exists: id="architectForm"
- Generator exists: function buildBlueprint(d)
- Download controls exist: id="downloadMd" and id="downloadJson"
- Offer CTA exists: mailto:mbcarbody@gmail.com with 149 EUR offer
- ROI math matches the browser formula: 40 weekly uses x 12 minutes x 20 EUR/h x 70 percent automation = 24.2 h/month and about 485 EUR/month value
- Payback formula: 149 / 485 ~= 0.31 months
- No external runtime script dependency is used
- The page says calculation is local and form data is not sent to a server

Public URL smoke note: direct URL verification through the available browser tool was not possible because the URL was not indexed in search results. Therefore, the public URL is recorded as configured, not independently smoke-proven in this run.

Result: functional repository artifact remains valid; revenue state advanced by adding 20 outreach-ready rows and updating the canonical product board.
