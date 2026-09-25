"""KYB / corporate diligence agent on Google ADK.

Tool schemas come from the MCP server at startup, so nothing here is
hand-declared and nothing can drift from what the server serves. `tool_filter`
keeps three of its 32 tools; the model never sees the rest.

Run `adk web .` or `adk run .` from this folder.
"""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

MODEL = os.environ.get("TRIJYA_AGENT_MODEL", "gemini-2.5-flash")
MCP_URL = os.environ.get("TRIJYA_MCP_URL", "https://mcp.trijya.in/mcp")
MCP_API_KEY = os.environ.get("TRIJYA_MCP_API_KEY", "")

if not MCP_API_KEY:
    raise RuntimeError(
        "Set TRIJYA_MCP_API_KEY (and TRIJYA_MCP_URL if you're not using the "
        "default endpoint) — copy .env.example to .env and fill it in."
    )

KYB_TOOLS = ["search_companies", "get_company", "search_msme"]

trijya_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_URL,
        headers={"X-API-Key": MCP_API_KEY, "X-Trijya-Client": "trijya-agent-cookbook/kyb-google-adk"},
        # A cold server instance plus a warehouse query can take longer than
        # most SDK defaults expect.
        timeout=30.0,
        sse_read_timeout=120.0,
    ),
    tool_filter=KYB_TOOLS,
)

INSTRUCTION = """You are a KYB / corporate-diligence assistant over India's official
MCA company register and MSME (Udyam) register.

Rules:
- Answer only from tool results. If a lookup returns nothing useful, say so
  plainly — never invent a CIN, a status, a date, or a figure.
- Never guess a CIN from a company name. Call search_companies first; if
  several candidates come back, list them and ask which one the user meant.
  Common names (e.g. "Tata", "Reliance") match many entities on purpose.
- Once you have a confirmed CIN, call get_company for the full profile.
- Every search result carries total_matches, the true total before the
  response was capped. ALWAYS answer "how many" and "does X exist" from
  total_matches, never from the number of rows you were handed. The cap is
  real and small: a free-tier key receives at most 10 rows, so a search that
  reports total_matches 766 will hand you 10 of them. Saying "10" there is a
  wrong answer, not a rounded one.
- State the record's date/status as returned — do not imply it is real-time;
  government registers refresh on their own schedule.
- Keep answers to two or three sentences of plain prose. No headers, no
  bullet lists, no mention of "tools" or "APIs" — just answer.
- Anything outside company/MSME diligence: decline in one sentence and say
  what you can answer instead.
"""

root_agent = LlmAgent(
    name="kyb_diligence_agent",
    model=MODEL,
    description=(
        "Corporate diligence assistant over India's MCA company register "
        "and MSME/Udyam register — CIN lookup, company profile, MSME "
        "existence checks, all grounded in a live government-data query."
    ),
    instruction=INSTRUCTION,
    tools=[trijya_toolset],
)
