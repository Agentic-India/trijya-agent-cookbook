# KYB agent on Google ADK

`LlmAgent` + `McpToolset`. Tools come from the server at startup and are
narrowed to three with `tool_filter`. [agent.py](agent.py) is under 60 lines.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
```

Fill in `TRIJYA_MCP_API_KEY` (free: [trijya.in/account](https://trijya.in/account))
and `GOOGLE_API_KEY`. For Vertex AI instead of AI Studio, set
`GOOGLE_GENAI_USE_VERTEXAI=TRUE`, `GOOGLE_CLOUD_PROJECT` and
`GOOGLE_CLOUD_LOCATION`, and leave `GOOGLE_API_KEY` empty.

```bash
adk web .     # chat UI on localhost:8000
adk run .     # terminal
```

## Why `tool_filter`

The server offers 32 tools; this agent needs three. `tool_filter` means the
model never sees the other 29. A short, correct tool list is a reliability
lever, not tidiness — fewer tools to confuse means fewer wrong calls.

The folder name has an underscore because ADK imports an agent directory as a
Python package, and `google-adk` is not a valid module name.
