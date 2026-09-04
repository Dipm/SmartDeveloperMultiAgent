# Contract

## In

- Ticket ID (required).
- Exactly one PR comment (required): GitHub MCP payload or pasted text.
- Optional: `03-plan.md`, `04-dev-notes.md`, `08-pr.md` to judge scope.

## Out

- Application edit only for (a) trivial fix.
- Draft reply only for (c), until the engineer confirms posting.
- Append-only `.dev-agent/{ticket-id}/09-review-log.md`
- Parent: classification + what you did or the draft reply

## Stop immediately

- Multiple comments in one invocation.
- (b) or (c) before engineer confirmation.
- Rewriting `09-review-log.md` from scratch.

## Scope

In: one comment, classified and handled.

Out: batching, silent scope expansion, `@plan` without a flag.
