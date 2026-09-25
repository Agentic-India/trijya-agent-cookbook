# Connect an AI client to Trijya

No code. Point your assistant at the MCP server and ask questions in plain
English — it picks the right lookup itself.

```
Server URL   https://mcp.trijya.in/mcp
Transport    HTTP (streamable)
Auth         X-API-Key: YOUR_KEY
```

Get a key at [trijya.in/account](https://trijya.in/account) → API keys.

Two ways to pass it. Prefer the **header**. Use the **query parameter** only
where a client has nowhere to put a header:

```
https://mcp.trijya.in/mcp?api_key=YOUR_KEY
```

A key in a URL ends up in connector config and in logs along the way. It works,
and it is the weaker of the two — rotate that key if you later move to a client
that supports headers.

---

## Claude Code

```bash
claude mcp add --transport http trijya https://mcp.trijya.in/mcp \
  --header "X-API-Key: YOUR_KEY"
```

Add `-s project` to write a shared `.mcp.json` for a repo instead of configuring
just your own machine, or `-s user` for every project you open. Check it with
`claude mcp list`, then ask:

> How many active companies are registered in Karnataka?

## Claude Desktop and claude.ai

Settings → Connectors → **Add custom connector**. The dialog takes a URL and no
headers, so use the query-parameter form:

```
https://mcp.trijya.in/mcp?api_key=YOUR_KEY
```

## Cursor

`~/.cursor/mcp.json` for every project, or `.cursor/mcp.json` inside one:

```json
{
  "mcpServers": {
    "trijya": {
      "url": "https://mcp.trijya.in/mcp",
      "headers": { "X-API-Key": "YOUR_KEY" }
    }
  }
}
```

## VS Code

`.vscode/mcp.json` in your workspace. Note VS Code calls the top-level key
`servers`, not `mcpServers`:

```json
{
  "servers": {
    "trijya": {
      "type": "http",
      "url": "https://mcp.trijya.in/mcp",
      "headers": { "X-API-Key": "YOUR_KEY" }
    }
  }
}
```

## Antigravity, Windsurf and other agent IDEs

Open the MCP settings pane and add an HTTP server with the same URL and header.
These take the `mcpServers` object shown under Cursor above; the settings UI
writes it for you, so add it there rather than hunting for the file.

## Gemini CLI

In `~/.gemini/settings.json`, under `mcpServers`. Gemini CLI names the field
`httpUrl` for streamable HTTP:

```json
{
  "mcpServers": {
    "trijya": {
      "httpUrl": "https://mcp.trijya.in/mcp",
      "headers": { "X-API-Key": "YOUR_KEY" }
    }
  }
}
```

## Check it works, without any client

```bash
npx @modelcontextprotocol/inspector
```

Choose Streamable HTTP, paste the URL, add the header, connect, and you should
see 32 tools. Or use curl:

```bash
curl -s https://mcp.trijya.in/mcp \
  -H "X-API-Key: $TRIJYA_API_KEY" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["result"]["tools"]), "tools")'
```

---

## Questions worth asking once it is connected

- How many active companies are registered in Karnataka?
- Find the CIN for Reliance Industries, then give me its registered office.
- Is there an MSME registered as TechTrapture in Maharashtra?
- What is IPC section 302 now, under the BNS?
- Which district is PIN code 411017 in?
- What was India's CPI inflation in the latest month you have?

## If it does not connect

| Symptom | Cause |
| --- | --- |
| 401 | Key missing, mistyped, or revoked. Check for a stray space, and that the header is `X-API-Key`. |
| 429 | Monthly quota used up. The response says when it resets. |
| Tool error naming a plan or feature | That dataset needs a paid plan or a grant. The message says which. |
| 10 rows when you asked for more | Free-tier row cap. `total_matches` in the rows carries the real total. |

## Verified

The Claude Code command and the `{url, headers}` config shape are what these
docs were written against. The per-product file paths for Cursor, VS Code and
Gemini CLI follow each product's own MCP documentation — if one has moved, the
settings UI in that product is the reliable route, and the URL and header stay
the same.
