"""Diligence Brief — a small web app that writes a company brief you can check.

One lookup against Trijya, then one model call that may use nothing but the JSON
that lookup returned. The record is sent back to the browser beside the brief,
so every sentence can be checked against the field it came from.

    pip install -r requirements.txt
    cp .env.example .env        # TRIJYA_API_KEY + GOOGLE_API_KEY
    uvicorn app:app --reload    # http://127.0.0.1:8000
"""
from __future__ import annotations

import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from pydantic import BaseModel

load_dotenv()

API = os.environ.get("TRIJYA_API_URL", "https://api.trijya.in").rstrip("/")
KEY = os.environ.get("TRIJYA_API_KEY", "")
MODEL = os.environ.get("MODEL", "gemini-2.5-flash")

if not KEY:
    raise RuntimeError("Set TRIJYA_API_KEY — copy .env.example to .env. Free key: https://trijya.in/account")

# Reads GOOGLE_API_KEY, or GOOGLE_GENAI_USE_VERTEXAI + project/location.
model = genai.Client()

app = FastAPI(title="Diligence Brief")
app.mount("/static", StaticFiles(directory="static"), name="static")

# The whole discipline of this app is in one instruction: the model gets a
# record and may not go beyond it. No "as a large language model I know that
# Reliance is an Indian conglomerate" — if it is not in the JSON, it is not in
# the brief.
PROMPT = """You write short factual briefs about Indian companies for someone doing
a counterparty check.

You are given one company record from India's MCA register as JSON. Use ONLY the
fields in that JSON. You may not add history, industry context, financial
commentary, reputation, subsidiaries, or anything else you happen to know about
this company — not one clause of it. If a field is absent, it is not in the
brief.

Write 3 to 5 sentences of plain prose. State the company's status and what it
is registered as, when it was incorporated, where it is registered, and its
capital if present. End with the date the register is current to.

No headings, no bullet points, no preamble, no advice about whether to trade
with them."""


class Ask(BaseModel):
    name: str


def trijya(path: str, **params):
    r = requests.get(f"{API}{path}", params={k: v for k, v in params.items() if v is not None},
                     headers={"X-API-Key": KEY}, timeout=60)
    if r.status_code == 401:
        raise HTTPException(502, "Trijya rejected the API key.")
    if r.status_code == 429:
        raise HTTPException(429, "Trijya monthly quota used up.")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/search")
def search(q: str):
    """Candidate companies for a name. Returned as-is, plus the real total."""
    rows = trijya("/v1/companies", query=q, limit=10) or []
    return {
        "candidates": rows,
        # NOT len(rows) — a free key caps the response at 10 rows.
        "total_matches": rows[0].get("total_matches", len(rows)) if rows else 0,
    }


CAPITAL_FIELDS = ("authorized_capital", "paidup_capital")


def readable(record: dict) -> dict:
    """Format capital in crore before anyone sees it.

    The register stores rupees as a float, so a raw record reads
    "500000000000.0". Do this here, not in the prompt — a model asked to
    reformat numbers is a model given a chance to get them wrong.
    """
    out = dict(record)
    for key in CAPITAL_FIELDS:
        v = out.get(key)
        if isinstance(v, (int, float)) and v:
            out[key] = (f"Rs {v / 1e7:,.0f} crore" if v >= 1e7 else f"Rs {v:,.0f}")
    return out


@app.post("/api/brief")
def brief(ask: Ask):
    """Look up one CIN, then have the model write from that record alone."""
    raw = trijya(f"/v1/companies/{ask.name}")
    if raw is None:
        raise HTTPException(404, "No company with that CIN in the current snapshot.")
    record = readable(raw)

    result = model.models.generate_content(
        model=MODEL,
        contents=f"Company record:\n{record}",
        config={"system_instruction": PROMPT, "temperature": 0.2},
    )

    return {
        "brief": (result.text or "").strip(),
        # The record travels with the brief. That is what makes the brief
        # checkable rather than merely fluent.
        "record": record,
        "knowledge_date": record.get("knowledge_date"),
        "capture_date": record.get("capture_date"),
    }


@app.get("/health")
def health():
    return {"ok": True}
