# Diligence Brief

A small web app: search a company name, pick one, get a short brief written from
India's MCA register — with the record printed underneath it.

FastAPI, one HTML file, no build step.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env        # TRIJYA_API_KEY + GOOGLE_API_KEY
uvicorn app:app --reload
```

Open http://127.0.0.1:8000. Free Trijya key:
[trijya.in/account](https://trijya.in/account) → API keys. For Vertex AI instead
of AI Studio, leave `GOOGLE_API_KEY` empty and set `GOOGLE_GENAI_USE_VERTEXAI`,
`GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`.

## How it works

```
name → GET /v1/companies         → candidates
CIN  → GET /v1/companies/{cin}   → one record
       record → Gemini           → 3-5 sentences, from that record only
       record + brief → browser  → brief on top, fields underneath
```

## The part worth copying

The system prompt forbids the model from using anything it knows about the
company. Only the JSON. Ask this app about Reliance and it will not tell you it
is an Indian conglomerate, because that is not in the record — it will tell you
it is an active public company limited by shares, registered in 1973 in
Maharashtra, because that is.

Then the record is sent to the browser and rendered beneath the brief. A brief
you cannot check is just fluent text; a brief next to its source is a document
someone can act on. That layout is the feature, not a debug view.

Two smaller things:

- The candidate count comes from `total_matches`, not from the length of the
  list. A free key returns 10 rows, and "10 companies match" would be wrong.
- Both dates are shown. `knowledge_date` is what the register said,
  `capture_date` is when Trijya read it. Neither is today.

## Not included

No auth, no rate limiting, no caching, no error retry. It is a sample you can
read in one sitting, not a service. The API key stays server-side, which is the
one production habit worth keeping as-is.
