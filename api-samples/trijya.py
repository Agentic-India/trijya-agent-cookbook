"""Minimal Trijya REST client shared by the samples in this folder.

Everything here is one `requests.get` with a key header. The only parts worth
copying into your own code are the error handling and `total_matches`.
"""
from __future__ import annotations

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.environ.get("TRIJYA_API_URL", "https://api.trijya.in").rstrip("/")
KEY = os.environ.get("TRIJYA_API_KEY", "")


class TrijyaError(RuntimeError):
    pass


def get(path: str, **params):
    """GET a Trijya route. Returns parsed JSON: a list for searches, an object
    for single-record lookups."""
    if not KEY:
        raise TrijyaError("Set TRIJYA_API_KEY — copy .env.example to .env. Free key: https://trijya.in/account")

    r = requests.get(
        f"{BASE}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"X-API-Key": KEY, "Accept": "application/json"},
        timeout=60,
    )

    if r.status_code == 401:
        raise TrijyaError("401 — key missing, mistyped or revoked.")
    if r.status_code == 403:
        # Not "does not exist". Trijya holds it, your plan may not include it.
        raise TrijyaError(f"403 — your plan does not include this: {_detail(r)}")
    if r.status_code == 404:
        return None
    if r.status_code == 429:
        raise TrijyaError(f"429 — monthly quota used up, resets {r.headers.get('X-Quota-Resets', 'soon')}.")
    r.raise_for_status()
    return r.json()


def quota(path: str = "/v1/sources", **params) -> dict:
    """The quota headers Trijya returns on every call."""
    r = requests.get(f"{BASE}{path}", params=params,
                     headers={"X-API-Key": KEY}, timeout=60)
    return {
        "limit": r.headers.get("X-Quota-Limit"),
        "used": r.headers.get("X-Quota-Used"),
        "resets": r.headers.get("X-Quota-Resets"),
        "row_cap": r.headers.get("X-Trijya-Row-Cap"),
    }


def total_matches(rows: list) -> int:
    """The real number of matches, which is NOT len(rows).

    A free key receives at most 10 rows. Every search row carries the full
    count, so read it from there and never from the list you were handed.
    """
    return rows[0].get("total_matches", len(rows)) if rows else 0


def _detail(r) -> str:
    try:
        return r.json().get("detail", r.text[:120])
    except Exception:
        return r.text[:120]


def die(msg: str):
    print(msg, file=sys.stderr)
    raise SystemExit(1)
