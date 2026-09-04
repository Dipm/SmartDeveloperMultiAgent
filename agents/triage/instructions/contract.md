# Contract

## In

- Ticket ID (required).
- Jira MCP (or equivalent) for that id.

## Out

- `.dev-agent/{ticket-id}/01-triage.md`
- Parent: short summary + 2–4 wasted-work questions (or explicit "not ambiguous")

## Stop immediately

- No ticket ID.
- Jira fetch failed and there is no pasted ticket body — do not invent the ticket.
- Request to start `@context` in the same turn.

## Scope

In: classify, severity, complexity, duplicates, scope ambiguity.

Out: codebase research, implementation, Jira field edits.
