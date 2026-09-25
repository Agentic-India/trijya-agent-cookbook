# MCP samples

Trijya's MCP server lives at `https://mcp.trijya.in/mcp` — streamable HTTP, 32
read tools, key in an `X-API-Key` header.

| | |
| --- | --- |
| [`connect-clients/`](connect-clients/) | Point Claude Code, Claude Desktop, Cursor, Antigravity, VS Code or Gemini CLI at it. No code. |
| [`kyb-diligence-agent/`](kyb-diligence-agent/) | An agent you run yourself, built twice — on Google ADK and on plain Python with no framework. |

## What the tools cover

Companies (3.7M MCA registrations) · MSME/Udyam (44.5M) · LLPs · geography
(villages, districts, PIN codes, local bodies) · banking (IFSC, insurers) ·
hospitals · legal (Central Acts, BNS/BNSS/BSA sections, IPC→BNS citation
mapping) · macro and budget series · NIC classification · a hashed
source-document archive.

`list_sources` returns the catalogue with each dataset's tier. Some tools need
a paid plan or an explicit grant and return an error naming what is missing,
rather than failing obscurely.
