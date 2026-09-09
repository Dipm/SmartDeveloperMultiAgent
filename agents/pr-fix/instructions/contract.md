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

## Platform and non-code scope

Follow `agents/shared/platform-and-scope.md`. Limit fixes to the open workspace;
ask before touching other platform repos. If the comment implies a backend/QA/env
issue and client code looks correct, draft a reply suggesting those checks instead
of changing code.
## On failure

- Do not write a success artifact unless the stage actually succeeded.
- Update `pipeline.json` with `status: failed` and structured `error` (see
  `agents/shared/error-handling.md`).
- Return error-card fields to the parent. Do not chain the next agent.
- Transient errors (`external_service`, `auth`, `timeout`): retry **once** inside
  this agent, then fail with `retry_count: 1`.

