"""Name -> CIN -> full company profile.

    python company_lookup.py "Reliance Industries"

Two calls on purpose. /v1/companies ranks candidates for a name and returns
identity only; /v1/companies/{cin} returns the full profile for the one you
picked. Never guess a CIN from a name — "Tata" matches hundreds of entities.
"""
import sys

from trijya import TrijyaError, die, get, total_matches


def main(name: str):
    rows = get("/v1/companies", query=name, limit=10)
    if not rows:
        return print(f"No company matches {name!r}.")

    print(f"{total_matches(rows)} companies match {name!r}. Showing {len(rows)}:\n")
    for i, c in enumerate(rows, 1):
        print(f"  {i}. {c['company_name']}")
        print(f"     {c['cin']} · {c['company_status']} · {c['company_class']}"
              f" · registered {c['date_of_registration']} · {c['registered_state']}")

    cin = rows[0]["cin"]
    print(f"\nFull profile for the top match ({cin}):\n")
    c = get(f"/v1/companies/{cin}")
    if c is None:
        return print("  Not in the current snapshot.")

    for label, key in [
        ("Name", "company_name"), ("Status", "company_status"),
        ("Registered", "date_of_registration"), ("Category", "company_category"),
        ("Authorised capital", "authorized_capital"), ("Paid-up capital", "paidup_capital"),
        ("Registered office", "registered_office_address"), ("RoC", "registrar_of_companies"),
        ("NIC code", "nic_code"), ("Activity", "industrial_classification"),
    ]:
        v = c.get(key)
        if v in (None, ""):
            continue
        # Capital comes back as a number; print it readably in rupees.
        if "capital" in key:
            v = f"Rs {v:,.0f}"
        print(f"  {label + ':':<20} {v}")

    # Provenance: what the register said, and when we read it. Not "today".
    print(f"\n  Register current to {c['knowledge_date']}, captured {c['capture_date']}.")


if __name__ == "__main__":
    try:
        main(" ".join(sys.argv[1:]) or "Reliance Industries")
    except TrijyaError as e:
        die(str(e))
