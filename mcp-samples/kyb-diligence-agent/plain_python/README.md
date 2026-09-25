# KYB agent with no framework

The `mcp` SDK for tools, the Anthropic API for the model, and nothing else.
[agent.py](agent.py) is about 120 lines, which is what an MCP agent loop costs
once you take the framework away.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
```

Fill in `TRIJYA_MCP_API_KEY` (free: [trijya.in/account](https://trijya.in/account))
and `ANTHROPIC_API_KEY`.

```bash
python agent.py "Find the CIN for Reliance Industries"
python agent.py "Is there a company called TechTrapture registered in Maharashtra?"
```

## The loop

1. Connect to the server, `list_tools()`, keep the three this agent needs.
2. Convert each tool's schema to the model's format. MCP gives
   `{name, description, inputSchema}` and Anthropic wants
   `{name, description, input_schema}`, so the converter is three lines.
3. Send the conversation with that tool list. On a tool-use response, run the
   call over the same MCP session, hand the result back as a `tool_result`, and
   loop. Stop on plain text.

Swap step 3's model client for any other tool-calling API and steps 1 and 2 do
not change. That is the whole argument for MCP.

No retries, no streaming, no session persistence — this is the minimum version
of the pattern, not a production harness.
