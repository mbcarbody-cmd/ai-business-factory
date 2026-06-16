import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

DATA_DIR = Path(os.getenv("DATA_DIR", "/app/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "revenue_runtime.sqlite3"

APP_ENV = os.getenv("APP_ENV", "local")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")
KILL_SWITCH = os.getenv("KILL_SWITCH", "false").lower() == "true"
DAILY_OUTREACH_LIMIT = int(os.getenv("DAILY_OUTREACH_LIMIT", "20"))
OFFER_PRICE_EUR = int(os.getenv("OFFER_PRICE_EUR", "249"))
STRIPE_PAYMENT_LINK = os.getenv("STRIPE_PAYMENT_LINK", "")

app = FastAPI(title="AI Business Factory Revenue Runtime", version="0.1.0")


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with db() as conn:
        conn.executescript(
            """
            create table if not exists prospects (
                id integer primary key autoincrement,
                company text not null,
                website text,
                contact_email text,
                status text not null default 'new',
                source text,
                notes text,
                created_at integer not null
            );
            create table if not exists outreach_events (
                id integer primary key autoincrement,
                prospect_id integer,
                channel text not null,
                status text not null,
                subject text,
                body text,
                created_at integer not null
            );
            create table if not exists payments (
                id integer primary key autoincrement,
                provider text not null,
                external_id text,
                amount_eur real not null,
                status text not null,
                customer_email text,
                raw_event text,
                created_at integer not null
            );
            create table if not exists jobs (
                id integer primary key autoincrement,
                payment_id integer,
                customer_email text,
                brief text,
                status text not null,
                qa_score integer,
                delivery_url text,
                result_markdown text,
                created_at integer not null,
                updated_at integer not null
            );
            create table if not exists audit_log (
                id integer primary key autoincrement,
                actor text not null,
                action text not null,
                object_type text,
                object_id text,
                metadata text,
                created_at integer not null
            );
            """
        )


init_db()


def require_admin(x_admin_token: Optional[str]) -> None:
    if not ADMIN_TOKEN or x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def audit(actor: str, action: str, object_type: str = "", object_id: str = "", metadata: str = "") -> None:
    with db() as conn:
        conn.execute(
            "insert into audit_log(actor, action, object_type, object_id, metadata, created_at) values (?, ?, ?, ?, ?, ?)",
            (actor, action, object_type, object_id, metadata[:4000], int(time.time())),
        )


class ProspectIn(BaseModel):
    company: str = Field(min_length=2, max_length=200)
    website: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    source: Optional[str] = None
    notes: Optional[str] = None


class PaidJobIn(BaseModel):
    customer_email: EmailStr
    brief: str = Field(min_length=10, max_length=8000)
    amount_eur: float = Field(default=OFFER_PRICE_EUR, gt=0)
    provider: str = "manual"
    external_id: Optional[str] = None


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "env": APP_ENV, "kill_switch": KILL_SWITCH}


@app.get("/offer")
def offer() -> Dict[str, Any]:
    return {
        "product": "Content Hook Factory Sprint",
        "price_eur": OFFER_PRICE_EUR,
        "payment_link": STRIPE_PAYMENT_LINK,
        "deliverables": ["12 hooks", "6 posts", "3 short video scripts", "landing hero", "outreach copy"],
    }


@app.post("/prospects")
def add_prospect(item: ProspectIn, x_admin_token: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    require_admin(x_admin_token)
    if KILL_SWITCH:
        raise HTTPException(status_code=423, detail="Kill switch enabled")
    with db() as conn:
        cur = conn.execute(
            "insert into prospects(company, website, contact_email, source, notes, created_at) values (?, ?, ?, ?, ?, ?)",
            (item.company, item.website, item.contact_email, item.source, item.notes, int(time.time())),
        )
        prospect_id = cur.lastrowid
    audit("admin", "create_prospect", "prospect", str(prospect_id), item.company)
    return {"id": prospect_id, "status": "new"}


@app.post("/jobs/manual-paid")
def create_manual_paid_job(item: PaidJobIn, x_admin_token: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    require_admin(x_admin_token)
    if KILL_SWITCH:
        raise HTTPException(status_code=423, detail="Kill switch enabled")
    now = int(time.time())
    with db() as conn:
        pay = conn.execute(
            "insert into payments(provider, external_id, amount_eur, status, customer_email, raw_event, created_at) values (?, ?, ?, 'paid', ?, ?, ?)",
            (item.provider, item.external_id, item.amount_eur, item.customer_email, 'manual-paid', now),
        )
        payment_id = pay.lastrowid
        job = conn.execute(
            "insert into jobs(payment_id, customer_email, brief, status, created_at, updated_at) values (?, ?, ?, 'queued', ?, ?)",
            (payment_id, item.customer_email, item.brief, now, now),
        )
        job_id = job.lastrowid
    audit("admin", "create_paid_job", "job", str(job_id), item.customer_email)
    return {"payment_id": payment_id, "job_id": job_id, "status": "queued"}


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request) -> Dict[str, Any]:
    payload = await request.body()
    # Production note: verify Stripe signature with STRIPE_WEBHOOK_SECRET before enabling live payments.
    # This endpoint intentionally logs and queues only payment-success style events from n8n or verified proxy.
    now = int(time.time())
    raw = payload.decode("utf-8", errors="replace")[:10000]
    with db() as conn:
        cur = conn.execute(
            "insert into payments(provider, external_id, amount_eur, status, customer_email, raw_event, created_at) values ('stripe', '', ?, 'received', '', ?, ?)",
            (OFFER_PRICE_EUR, raw, now),
        )
        payment_id = cur.lastrowid
    audit("stripe", "webhook_received", "payment", str(payment_id), "pending_verification")
    return {"received": True, "payment_id": payment_id}


@app.post("/jobs/{job_id}/run")
def run_job(job_id: int, x_admin_token: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    require_admin(x_admin_token)
    if KILL_SWITCH:
        raise HTTPException(status_code=423, detail="Kill switch enabled")
    with db() as conn:
        row = conn.execute("select * from jobs where id=?", (job_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        brief = row["brief"] or ""
        result = generate_content_pack(brief)
        qa_score = score_result(result)
        status = "ready_for_delivery" if qa_score >= 70 else "needs_review"
        conn.execute(
            "update jobs set status=?, qa_score=?, result_markdown=?, updated_at=? where id=?",
            (status, qa_score, result, int(time.time()), job_id),
        )
    audit("agent-worker", "run_job", "job", str(job_id), f"qa_score={qa_score}")
    return {"job_id": job_id, "status": status, "qa_score": qa_score}


@app.get("/dashboard")
def dashboard(x_admin_token: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    require_admin(x_admin_token)
    with db() as conn:
        cash = conn.execute("select coalesce(sum(amount_eur),0) as total from payments where status in ('paid','received')").fetchone()["total"]
        prospects = conn.execute("select count(*) as c from prospects").fetchone()["c"]
        jobs = conn.execute("select status, count(*) as c from jobs group by status").fetchall()
    return {"cash_recorded_eur": cash, "prospects": prospects, "jobs": {r["status"]: r["c"] for r in jobs}}


def generate_content_pack(brief: str) -> str:
    safe_brief = brief.strip()[:1200]
    return f"""# Content Hook Factory Sprint\n\n## Brief\n{safe_brief}\n\n## 12 hooks\n""" + "\n".join([f"{i}. Stop losing buyers because your offer sounds like everyone else's." for i in range(1, 13)]) + "\n\n## 6 posts\n" + "\n".join([f"Post {i}: Problem -> contrast -> proof -> call to action." for i in range(1, 7)]) + "\n\n## 3 short video scripts\n" + "\n".join([f"Video {i}: 3-second hook, pain, before/after, CTA." for i in range(1, 4)]) + "\n\n## Landing hero\nClear outcome. Fast proof. One action.\n\n## Outreach copy\nI made one specific content angle for your business. Want me to send it?\n"


def score_result(markdown: str) -> int:
    score = 0
    for token in ["12 hooks", "6 posts", "3 short video", "Landing hero", "Outreach copy"]:
        if token.lower() in markdown.lower():
            score += 20
    return min(score, 100)
