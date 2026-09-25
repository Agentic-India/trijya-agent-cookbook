# Trijya Cookbook — India public data API and MCP server samples

Working samples for [Trijya](https://trijya.in): search Indian companies by
name or CIN, check MSME/Udyam registrations, resolve PIN codes and districts,
look up IFSC bank branches, and map an old IPC section to its BNS replacement —
from a REST API, from an MCP server, or from an AI agent you run yourself.

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

## What you can look up

- **Find a company's CIN by name** — ranked matches across 3.7M registered Indian companies, with status and incorporation date.
- **Check whether a company is active** — full profile by CIN: status, class, authorised and paid-up capital, registered office, RoC.
- **Was a company active on a past date** — point-in-time company history, rather than only its state today.
- **Check if a business is a registered MSME** — search 44M Udyam registrations by name, state and registration year.
- **Search Indian LLPs by name** — the LLP register, keyed by LLPIN.
- **Resolve a PIN code to its district and state** — plus villages, subdistricts and local bodies across India.
- **Find a bank branch by IFSC code** — and search the insurer registry.
- **Map IPC to BNS** — what an old Indian Penal Code section is now, under the Bharatiya Nyaya Sanhita, with the section text.
- **Search Central Acts** — the Indian Central Act registry, with statutory section text.
- **Query India's macro and Union Budget series** — CPI, WPI, IIP, national accounts and budget headline figures.
- **Look up NIC industrial classification codes** — including the concordance between vintages.

Each of these is one REST call or one MCP tool. Interactive API docs:
[api.trijya.in/docs](https://api.trijya.in/docs).

Point-in-time history is the exception: REST only, on a paid plan. Everything
else on this list works on a free key.

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

## FAQ

**Is there an API for Indian company data (MCA / CIN lookup)?**
Yes — `GET /v1/companies?query=…` to search by name, `GET /v1/companies/{cin}`
for the full profile. See [`api-samples/`](api-samples/).

**Is there an MCP server for Indian government data?**
`https://mcp.trijya.in/mcp`, 32 read tools, streamable HTTP. Setup for Claude
Code, Claude Desktop, Cursor, VS Code, Antigravity and Gemini CLI is in
[`mcp-samples/connect-clients/`](mcp-samples/connect-clients/).

**Is it free?**
There is a free tier — 1,000 calls a month, 10 rows per response. Sign up at
[trijya.in/account](https://trijya.in/account).

**Can I use this for KYB or lending checks?**
That is what the [KYB agent](mcp-samples/kyb-diligence-agent/) is built for. It
reports what the register says on the date the register says it; what you do
with that is your decision, not the API's.

**Which Indian datasets are covered?**
Companies, MSME/Udyam, LLPs, geography and PIN codes, bank branches and
insurers, health facilities, Central Acts and criminal-code sections, NIC
classification, macro and budget series. `list_sources` returns the catalogue.

**Does it work with Claude, Gemini and OpenAI models?**
The MCP server is model-agnostic. The samples here use Gemini via Google ADK
and Claude via the Anthropic API; the REST API works with anything.

## Licence

MIT — see [LICENSE](LICENSE). Fork it, adapt it, point it at your own server.
The data behind the default configuration is a Trijya service and is not
covered by this licence.
