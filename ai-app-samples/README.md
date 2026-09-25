# AI app samples

Complete apps, not snippets. Clone, add a key, run.

| App | |
| --- | --- |
| [`diligence-brief/`](diligence-brief/) | Search a company, get an AI-written brief from India's MCA register with the source record printed beside it. FastAPI + one HTML file, no build step. |

## The rule these apps follow

The model may only use what a lookup returned. Not what it remembers about the
company, not what sounds plausible — the record, and nothing else. When an app
puts the record next to the answer, that rule becomes something a user can
check rather than something you promise in a README.

That is the difference between a demo and a tool someone will put in front of a
credit committee.
