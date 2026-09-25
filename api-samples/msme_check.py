"""Is this business in the MSME (Udyam) register?

    python msme_check.py "TechTrapture" Maharashtra
    python msme_check.py "" Goa 2025        # count a state and year, no name

Pass state and year whenever you know them. They are not just filters: the
warehouse is partitioned and clustered on them, so an all-India unfiltered
search reads ~12 GB where Maharashtra-plus-2025 reads ~0.3 GB. Same answer,
a fraction of the work.
"""
import sys

from trijya import TrijyaError, die, get, total_matches


def main(name: str, state: str | None, year: int | None):
    rows = get("/v1/msme", query=name or None, state=state,
               registration_year=year, limit=10)

    scope = " · ".join(x for x in [name and repr(name), state, year and str(year)] if x)
    if not rows:
        return print(f"No MSME registration found for {scope}.")

    # total_matches is the whole answer to "how many". len(rows) is the page.
    n = total_matches(rows)
    print(f"{n} registration{'' if n == 1 else 's'} match {scope}. Showing {len(rows)}:\n")
    for m in rows:
        print(f"  {m['enterprise_name']}")
        print(f"    registered {m['registration_date']} · {m['district_name'].title()}, "
              f"{m['state_name'].title()} · PIN {m['pincode']}")

    print(f"\n  Register current to {rows[0]['knowledge_date']}.")
    print("  Confirms existence, date and location. No address or activity list "
          "is served for MSME records.")


if __name__ == "__main__":
    args = sys.argv[1:] or ["TechTrapture", "Maharashtra"]
    name = args[0] if args else ""
    state = args[1] if len(args) > 1 else None
    year = int(args[2]) if len(args) > 2 else None
    try:
        main(name, state, year)
    except TrijyaError as e:
        die(str(e))
