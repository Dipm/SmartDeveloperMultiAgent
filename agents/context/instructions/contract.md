# Contract

## In

- Ticket ID from the invocation (required).
- `.dev-agent/{ticket-id}/01-triage.md` (required). Read it fully. Use its
  summary, classification, related tickets, and open questions as the search brief.

## Out

- `.dev-agent/{ticket-id}/02-context.md` — see `output.md`.
- Parent message: 3–6 sentence summary + open questions.

## Stop immediately

- Missing ticket ID.
- Missing or empty `01-triage.md`.
- Request to implement, refactor, or "just start the plan."
- Pressure to skip human go-ahead and invoke `@plan`.

## Scope

In: files, history, conventions, tests that affect this ticket.

Out: classification (triage), implementation plan (plan), code edits, new tests.
