# REST API samples

Plain `requests`. The API is at `https://api.trijya.in`, the key goes in an
`X-API-Key` header, and every route is a `GET`. Interactive docs, including
every route and parameter, are at [api.trijya.in/docs](https://api.trijya.in/docs).

## Run

```bash
pip install -r requirements.txt
cp .env.example .env          # add TRIJYA_API_KEY

python company_lookup.py "Reliance Industries"
python msme_check.py "TechTrapture" Maharashtra
python quota_and_limits.py
```

Free key: [trijya.in/account](https://trijya.in/account) → API keys.

## What each one shows

| File | |
| --- | --- |
| [`trijya.py`](trijya.py) | ~60-line client the others share. The parts worth copying are the error handling and `total_matches`. |
| [`company_lookup.py`](company_lookup.py) | Name → ranked CIN candidates → full profile. Two calls, because you should never guess a CIN from a name. |
| [`msme_check.py`](msme_check.py) | Existence check against 44.5M Udyam registrations, and why passing `state` and `registration_year` cuts the work by 40× for the same answer. |
| [`quota_and_limits.py`](quota_and_limits.py) | Quota headers, the row cap, and why 403 and 404 must not be collapsed into one error path. |

## Three things that will bite you otherwise

**`len(rows)` is not the answer.** A free key returns at most 10 rows. Every
search row carries `total_matches` with the real total — 766 for "reliance".

**403 is not 404.** 403 means Trijya holds the record and your plan does not
include it. Surfacing that as "not found" tells your user something false.

**Filters are a cost control, not just a narrowing.** On MSME, an unfiltered
all-India search reads ~12 GB; the same search with `state` and
`registration_year` reads ~0.3 GB.

## Curl, if you would rather

```bash
export TRIJYA_API_KEY=...

# Search companies
curl -s "https://api.trijya.in/v1/companies?query=reliance&limit=5" \
  -H "X-API-Key: $TRIJYA_API_KEY" | python3 -m json.tool

# One company
curl -s "https://api.trijya.in/v1/companies/L17110MH1973PLC019786" \
  -H "X-API-Key: $TRIJYA_API_KEY" | python3 -m json.tool

# See your quota, including the row cap
curl -sD - -o /dev/null "https://api.trijya.in/v1/sources" \
  -H "X-API-Key: $TRIJYA_API_KEY" | grep -i "x-quota\|x-trijya"

# IPC 302 under the new criminal code
curl -s "https://api.trijya.in/v1/legal/citations/IPC/302" \
  -H "X-API-Key: $TRIJYA_API_KEY" | python3 -m json.tool
```

## Provenance

Every row carries `knowledge_date` (what the register said) and `capture_date`
(when Trijya read it). Neither is "today" — government registers refresh on
their own schedule, and anything you show a user should say which date it is
speaking for.
