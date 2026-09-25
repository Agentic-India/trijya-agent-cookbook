"""What your key is allowed to do, and how the limits show up.

    python quota_and_limits.py

Three things every integration should handle, and none of them are exceptions
you can ignore:

  1. Quota headers on every response — read them, don't count calls yourself.
  2. The free-tier row cap — announced in X-Trijya-Row-Cap, and the reason
     total_matches exists.
  3. 403 vs 404 — 403 means Trijya holds the data and your plan does not cover
     it. That is a different fact from "does not exist", and worth surfacing
     differently to whoever is waiting on the answer.
"""
from trijya import TrijyaError, get, quota, total_matches


def main():
    q = quota()
    print("Quota (from response headers)")
    print(f"  limit   {q['limit'] or 'unmetered'}")
    print(f"  used    {q['used'] or '-'}")
    print(f"  resets  {q['resets'] or '-'}")
    print(f"  rows    {q['row_cap'] or 'no cap on this plan'}\n")

    # Ask for 50, see what the plan actually allows through.
    rows = get("/v1/companies", query="reliance", limit=50)
    print(f"Asked for 50 rows, received {len(rows)}, "
          f"total_matches says {total_matches(rows)}.")
    if len(rows) < total_matches(rows):
        print("  -> Report total_matches. Counting rows would understate this "
              f"by {total_matches(rows) - len(rows)}.\n")

    # A Pro-only route on a free key: 403, not 404. The record exists.
    print("Point-in-time history (a paid feature):")
    try:
        c = get("/v1/companies/L17110MH1973PLC019786/as-of/2024-03-01")
        print(f"  {c['company_name']} was {c['company_status']} on 2024-03-01.")
    except TrijyaError as e:
        print(f"  {e}")
        print("  -> 403 means it exists and your plan excludes it. Do not "
              "report that to a user as 'not found'.")


if __name__ == "__main__":
    try:
        main()
    except TrijyaError as e:
        raise SystemExit(str(e))
