# Contract

## In

- Ticket ID from the invocation (required).
- All prior `.dev-agent/{ticket-id}/*.md` files. Required:
  - `01-triage.md`
  - `03-plan.md`
  - `04-dev-notes.md`
  - `05-tests.md`
  - `06-review-notes.md`
- Optional if present: `02-context.md`, `09-review-log.md`.
- Review must not still require `@dev` (no unresolved blocking / should-fix).

## Out

- `.dev-agent/{ticket-id}/07-docs.md` — see `output.md`.
- `.dev-agent/{ticket-id}/08-pr.md` — see `output.md`.
- Parent message: short summary of both drafts + wording/scope questions.

## Stop immediately

- Missing ticket ID or any required prior file.
- Review still says go back to `@dev`.
- Request to open, push, or merge the PR.
- Request to change application code "while you're in there."

## Scope

In: pipeline docs for reviewers; PR description draft.

Out: `gh pr create`, `git push`, application edits, `@pr-fix`, merging.
## On failure

- Do not write a success artifact unless the stage actually succeeded.
- Update `pipeline.json` with `status: failed` and structured `error` (see
  `agents/shared/error-handling.md`).
- Return error-card fields to the parent. Do not chain the next agent.
- Transient errors (`external_service`, `auth`, `timeout`): retry **once** inside
  this agent, then fail with `retry_count: 1`.

