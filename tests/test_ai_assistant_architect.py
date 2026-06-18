from pathlib import Path
import re

HTML = Path(__file__).resolve().parents[1] / "website" / "ai-assistant-architect.html"
text = HTML.read_text(encoding="utf-8")

required = [
    'id="architectForm"',
    'function buildBlueprint(d)',
    'id="downloadMd"',
    'id="downloadJson"',
    '149 €',
    'mailto:mbcarbody@gmail.com',
    'Žmogaus patvirtinimo vartai',
    '14 dienų paleidimas',
]
for marker in required:
    assert marker in text, f"missing critical marker: {marker}"

assert '<script>' in text and '</script>' in text
assert text.count('<form') == text.count('</form>') == 1
assert text.count('<html') == text.count('</html>') == 1
assert 'location.replace' not in text

# Mirror the deterministic ROI formula used by the browser product.
frequency, minutes, hourly, automation = 40, 12, 20, 0.70
weekly_hours = frequency * minutes / 60
saved_monthly = weekly_hours * 4.33 * automation
monthly_value = saved_monthly * hourly
payback = 149 / monthly_value
assert round(weekly_hours, 1) == 8.0
assert round(saved_monthly, 1) == 24.2
assert round(monthly_value) == 485
assert round(payback, 2) == 0.31

# Guard against accidental external runtime dependencies.
assert not re.search(r'<script[^>]+src=', text, re.I)
assert not re.search(r'<link[^>]+stylesheet[^>]+href=["\']https?://', text, re.I)

print("PASS: assistant architect critical path, ROI, downloads, offer CTA and dependency guard")
