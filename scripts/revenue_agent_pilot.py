#!/usr/bin/env python3
"""Approval-safe revenue-agent pilot. One bounded API call; no customer actions."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

OUT = Path("runtime/revenue_agent_pilot/report.md")
LANDING = "https://mbcarbody-cmd.github.io/ai-business-factory/website/video-maker.html"
ORDER = "https://mbcarbody-cmd.github.io/ai-business-factory/website/quick-video-paid-order.html"

def page_status(url: str) -> str:
    try:
        req = Request(url, headers={"User-Agent": "RevenuePilot/1.0"})
        with urlopen(req, timeout=12) as response:
            return f"HTTP {response.status}"
    except HTTPError as exc:
        return f"HTTP {exc.code}"
    except (URLError, TimeoutError) as exc:
        return "Nepavyko patikrinti tinklo"
        
def lead_status() -> tuple[int, int]:
    path = Path("OPS/revenue_ops/lead_pipeline.json")
    if not path.exists():
        return (0, 0)
    leads = json.loads(path.read_text(encoding="utf-8")).get("leads", [])
    verified = 0
    for entry in leads:
        company = str(entry.get("company", "")).strip()
        channel = str(entry.get("contact_channel", "")).strip()
        notes = str(entry.get("notes", "")).lower()
        if company and channel and "|" not in channel and "seed" not in notes:
            verified += 1
    return len(leads), verified

def model_report(api_key: str, facts: str, instructions: str) -> str:
    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        "input": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": facts},
        ],
        "max_output_tokens": 1800,
        "store": False,
    }
    request = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
    )
    try:
        with urlopen(request, timeout=75) as response:
            result = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"OpenAI API grąžino HTTP {exc.code}; patikrink raktą, modelį ir balansą") from None
    parts = []
    for item in result.get("output", []):
        for chunk in item.get("content", []):
            if chunk.get("type") == "output_text":
                parts.append(chunk.get("text", ""))
    if not parts:
        raise RuntimeError("API negrąžino tekstinės ataskaitos")
    return "\n\n".join(parts)

def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total, verified = lead_status()
    site = page_status(LANDING)
    order = page_status(ORDER)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = (f"# Revenue agent pilot — {now}\n\n"
              f"## Patikrinti signalai\n\n"
              f"- Quick Product Video puslapis: {site}\n"
              f"- Užsakymo puslapis: {order}\n"
              f"- Įrašų potencialių klientų lentelėje: {total}; preliminariai tikrinimo kriterijus atitinka: {verified}.\n"
              f"- Pastaba: klientų skaičius nėra nepriklausomai patvirtintas; įplaukos 0 EUR, kol nėra banko/mokėjimų įrodymų.\n\n")
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        OUT.write_text(header + "## Sąranka\n\n"
                       "OPENAI_API_KEY dar nepridėtas į GitHub Actions Secrets. "
                       "Agentas nieko nesiunčia ir pinigų nenaudoja.\n", encoding="utf-8")
        print("Created setup report (API key not configured).")
        return
    readme = Path("README.md").read_text(encoding="utf-8")[:5500]
    facts = (header + "\n## Repozitorijos README ištrauka\n" + readme)
    instructions = (
        "Esi lietuviškai rašantis AI Business Factory pajamų vykdymo agentas. "
        "Tavo paskirtis ne generuoti idėjų sąrašą, o rasti vieną konkretų artimiausią kelią iki tikro mokančio kliento. "
        "Remkis tik pateiktais faktais, neišgalvok svetainių lankomumo, klientų, mokėjimų, QA įrodymų ar pelno. "
        "Repo README numato: joks klientų viliojimas ar mokėjimo prašymas, kol nėra tikro Android Chrome WEBM "
        "įrašymo, atkūrimo ir atsisiuntimo QA įrodymo. Neapeik šios taisyklės. "
        "Neturi teisės siųsti žinučių, pateikti užsakymų, keisti kainų, atlikti mokėjimų, diegti į produkciją ar "
        "rašyti į GitHub. Neprašyk prisijungimo duomenų. "
        "Atsakyk Markdown lietuviškai su: (1) tikruoju QA/pardavimo blokatoriumi, "
        "(2) vienu įvykdomu veiksmu su aiškiu proof failu, "
        "(3) iki 3 darbo juodraščių ar testų, kuriuos galima parengti nepažeidžiant apribojimų, "
        "(4) kaip patikrinti, kad tai priartino iki pajamų, "
        "(5) numatomomis ir nežinomomis API veiklos išlaidomis. "
        "Jei nėra tikrų klientų ar užsakymų, tiesiai parašyk, kad jų nepatvirtinai."
    )
    try:
        result = model_report(key, facts, instructions)
        OUT.write_text(header + "## AI veiksmų ataskaita\n\n" + result + "\n", encoding="utf-8")
        print("Created AI report artifact.")
    except RuntimeError as exc:
        OUT.write_text(header + "## API klaida\n\n" + str(exc) + "\n", encoding="utf-8")
        print(str(exc))
        raise

if __name__ == "__main__":
    main()
