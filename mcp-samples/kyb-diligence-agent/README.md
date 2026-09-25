# KYB / Corporate Diligence Agent

The checks a lending, KYB or vendor-onboarding workflow runs before approving a
counterparty:

- Find the CIN for a company name, and disambiguate when several match.
- Is this CIN active, and when was it incorporated?
- Is this business in the MSME (Udyam) register, and where?

Two implementations, same behaviour — [`google_adk/`](google_adk/) (Google ADK,
Gemini) and [`plain_python/`](plain_python/) (the `mcp` SDK, no framework,
Claude).

## Tools

| Tool | Input → output |
| --- | --- |
| `search_companies` | name → candidate CINs, over 3.7M MCA-registered companies. Identity and status only. |
| `get_company` | CIN → full profile: status, incorporation date, authorised and paid-up capital, registered office, RoC, NIC code. |
| `search_msme` | name, state, year → Udyam enterprises, 44.5M of them. Name, registration date, state, district, PIN. |

Three of the 32 tools the server offers. The rest — geography, banking, legal
codes, statistics — are filtered out, so the model cannot reach for the wrong
lookup.

`search_msme` returns no address and no activity list, so an MSME answer here
confirms existence, date and location. Not more.

## The rules it follows

**Only state what a tool returned.** No lookup, no answer. For a diligence
check a plausible guess is worse than "I couldn't verify that", so the agent
says the latter.

**Never guess a CIN from a name.** `search_companies` first. "Tata" matches
hundreds of entities; the agent lists candidates and asks.

**Count from `total_matches`, not from rows.** A free key returns at most 10
rows, and `total_matches` carries the real total — 766 for "reliance", where 10
rows come back. Both system prompts state this with the number in them.

**Dates are the record's, not today's.** Government registers refresh on their
own schedule, and the agent reports the date the data carries.

## Run it

Pick a folder and follow its README. Both need a free Trijya key from
[trijya.in/account](https://trijya.in/account) — all three tools are on the
free tier, so a free key runs this end to end.

## Limits

No point-in-time lookups — "was this CIN active on 1 March 2024?" is answered by
Trijya over REST at `/v1/companies/{cin}/as-of/{date}`, but there is no MCP tool
for it, so this agent cannot reach it. It is also a paid feature, so a free key
would get a 403 where these three return rows.

This is not a credit decision. It reports what the register says on the date the
register says it.
