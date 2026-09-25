"""KYB / corporate diligence agent with no agent framework.

The `mcp` SDK talks to the server, the Anthropic API drives the model. Connect,
list tools, convert each schema to the model's format, then loop: send the
conversation, run any tool call over the same MCP session, feed the result back,
stop on plain text.

Swap the model client and the MCP half is unchanged.

Run: python agent.py "Find the CIN for Reliance Industries"
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

MCP_URL = os.environ.get("TRIJYA_MCP_URL", "https://mcp.trijya.in/mcp")
MCP_API_KEY = os.environ.get("TRIJYA_MCP_API_KEY", "")
MODEL = os.environ.get("TRIJYA_AGENT_MODEL", "claude-sonnet-5")
KYB_TOOLS = {"search_companies", "get_company", "search_msme"}

SYSTEM_PROMPT = """You are a KYB / corporate-diligence assistant over India's official
MCA company register and MSME (Udyam) register.

Rules:
- Answer only from tool results. If a lookup returns nothing useful, say so
  plainly — never invent a CIN, a status, a date, or a figure.
- Never guess a CIN from a company name. Call search_companies first; if
  several candidates come back, list them and ask which one the user meant.
- Once you have a confirmed CIN, call get_company for the full profile.
- Every search result carries total_matches, the true total before the
  response was capped. ALWAYS answer "how many" and "does X exist" from
  total_matches, never from the row count you were shown. The cap is real and
  small: a free-tier key receives at most 10 rows, so a search reporting
  total_matches 766 hands you 10 of them. Saying "10" there is a wrong
  answer, not a rounded one.
- Keep answers to two or three sentences of plain prose. No mention of
  "tools" or "APIs" — just answer.
"""

anthropic = Anthropic()  # reads ANTHROPIC_API_KEY from the environment


def _mcp_tool_to_anthropic(tool) -> dict:
    """MCP and Anthropic both describe a tool as {name, description,
    input JSON Schema} — only the key names differ."""
    return {
        "name": tool.name,
        "description": tool.description or "",
        "input_schema": tool.inputSchema,
    }


def _tool_result_text(result) -> str:
    """MCP tool results come back as a list of content blocks; this server
    returns one text block per row. Anthropic just wants a string back."""
    parts = [block.text for block in result.content if getattr(block, "text", None)]
    return "\n".join(parts) if parts else json.dumps({"rows": []})


async def ask(question: str) -> str:
    async with streamablehttp_client(
        MCP_URL,
        headers={"X-API-Key": MCP_API_KEY, "X-Trijya-Client": "trijya-agent-cookbook/kyb-plain-python"},
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            available = await session.list_tools()
            tools = [_mcp_tool_to_anthropic(t) for t in available.tools if t.name in KYB_TOOLS]

            messages = [{"role": "user", "content": question}]
            for _ in range(6):  # a diligence answer should never need more than a couple of lookups
                response = anthropic.messages.create(
                    model=MODEL, max_tokens=1024, system=SYSTEM_PROMPT,
                    tools=tools, messages=messages,
                )
                messages.append({"role": "assistant", "content": response.content})

                if response.stop_reason != "tool_use":
                    return "".join(b.text for b in response.content if b.type == "text").strip()

                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    result = await session.call_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": _tool_result_text(result),
                    })
                messages.append({"role": "user", "content": tool_results})

            return "I couldn't reach a verified answer in a reasonable number of lookups."


def main() -> None:
    if not MCP_API_KEY:
        raise SystemExit("Set TRIJYA_MCP_API_KEY — copy .env.example to .env and fill it in.")
    question = " ".join(sys.argv[1:]) or "Is there a company called TechTrapture registered in Maharashtra?"
    print(asyncio.run(ask(question)))


if __name__ == "__main__":
    main()
