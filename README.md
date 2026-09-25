# Trijya Cookbook

Working samples for [Trijya](https://trijya.in) — India's public data, rebuilt
as something you can query.

## What Trijya is

India's public data is official, plentiful and almost unusable in a workflow.
It is scattered across dozens of portals in different shapes, published as
files and dashboards rather than as queries, keyed differently in every source
so nothing joins cleanly, and it shows you only what is true today — when a
register is updated, what it said last year is gone.

Trijya is that data as one layer: a REST API and an MCP server over India's
company, enterprise, geography, banking, legal and statistical registers.
Two things come with every answer.

**A date, always.** Each row carries what the register said (`knowledge_date`)
and when Trijya read it (`capture_date`). Neither is "today". A government
register refreshes on its own schedule, and anything you put in front of a user
should say which day it speaks for.

**History, not just the present.** Trijya keeps versions rather than
overwriting, so you can ask what the register said on a past date — whether a
company was active on the day a contract was signed, not merely whether it is
active now. That is the part a diligence or underwriting file actually needs,
and it is the part no portal gives you.

| Today it holds | |
| --- | --- |
| Companies | 3,740,426 |
| MSME / Udyam enterprises | 44,562,215 |
| LLPs | 514,494 |
| Villages mapped | 720,758 |
| Bank branches | 182,523 |
| Local bodies | 353,197 |
| Health facilities | 30,273 |
| Central Acts | 845 |

Plus macro and budget series, industrial classification codes, the current
criminal-code sections with their mapping from the old ones, and a hashed
archive of the source documents. `list_sources` over MCP, or
[`/v1/sources`](https://api.trijya.in/docs), returns the full catalogue.

Typical uses: KYB and vendor onboarding, lending and underwriting checks, sales
and account research, diligence, and grounding an AI agent in something it can
cite. Named for त्रिज्या, the Sanskrit word for *radius*.

## Three ways in

One per folder:

| Folder | For |
| --- | --- |
| [`mcp-samples/`](mcp-samples/) | Connecting an AI client or agent to Trijya's MCP server |
| [`api-samples/`](api-samples/) | Calling the REST API from your own code |
| [`ai-app-samples/`](ai-app-samples/) | Complete apps you can run and adapt |

## Get a key first

Sign in at [trijya.in/account](https://trijya.in/account) → API keys. Free tier:

| | |
| --- | --- |
| Calls per month | 1,000, REST and MCP together |
| Rows per response | 10 — `total_matches` still reports the true total |
| Datasets | every open and attribution-tier dataset |
| Not included | point-in-time history, document downloads, on-request datasets |

## Endpoints

| | |
| --- | --- |
| MCP | `https://mcp.trijya.in/mcp` — 32 read tools, streamable HTTP |
| REST | `https://api.trijya.in` — interactive docs at [`/docs`](https://api.trijya.in/docs) |

Both take the key in an `X-API-Key` header.

## Fastest thing to try

Point Claude Code at it and ask a question in plain English:

```bash
claude mcp add --transport http trijya https://mcp.trijya.in/mcp \
  --header "X-API-Key: YOUR_KEY"
```

Then: *"How many active companies are registered in Karnataka?"* Setup for
Claude Desktop, Cursor, Antigravity, VS Code and others is in
[`mcp-samples/connect-clients/`](mcp-samples/connect-clients/).

## One number worth knowing

A free key returns at most 10 rows, and every search also returns
`total_matches` — the real total. Search "reliance" and you get 10 rows with
`total_matches: 766`. Code that counts rows instead of reading that field will
be wrong by two orders of magnitude, quietly. Every sample here reads
`total_matches`.

## Licence

MIT — see [LICENSE](LICENSE). Fork it, adapt it, point it at your own server.
The data behind the default configuration is a Trijya service and is not
covered by this licence.
