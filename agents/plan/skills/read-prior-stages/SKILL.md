---
name: read-prior-stages
description: Read 01-triage.md and 02-context.md as the only inputs to planning. Use when the plan agent starts.
disable-model-invocation: true
---

# Read prior stages

Read `.dev-agent/{ticket-id}/01-triage.md` and `02-context.md` fully.

Treat contradictions between them as plan risks: call them out in Outside
normal scope / Decisions, do not quietly pick a side.

Do not open `04-dev-notes.md` or later. Do not start a codebase rewrite of
context; if context is thin, say so in the plan instead of re-doing `@context`.
