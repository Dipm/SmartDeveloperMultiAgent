# Triage

When invoked with a ticket ID:

1. Load `skills/fetch-jira-ticket/SKILL.md`.
## Jira fetch — transient failures (one retry)

If Jira MCP fails with network, timeout, or auth errors, wait briefly and retry
**once**. On second failure, stop and update `pipeline.json` with `status: failed`:
- `error.code`: `auth` or `external_service`
- `error.retry_count`: 1
- `error.suggestions`: re-auth MCP; paste ticket body; `retry triage with pasted body`

If no ticket data after retry, use pasted body from parent or stop with
`error.code: user_input_needed`.

 Pull title, description, acceptance
   criteria, linked tickets, comments.

2. Load `agents/shared/requirement-validation.md` and `agents/shared/platform-and-scope.md`.
   Quick-check ticket expected behavior vs current code (≤3 min, targeted search).
   Note active platform vs platforms mentioned in the ticket. Do not block on long analysis.

3. Load `skills/classify-and-scope/SKILL.md`.
   - Classify: bug, feature, or chore.
   - Severity/priority and complexity: trivial / moderate / complex.
   - Duplicate or already-in-progress related tickets.
   - Anything ambiguous about scope, acceptance criteria, or expected behavior.

4. Write `01-triage.md`.

5. Ask the 2–4 misunderstandings most likely to waste work — not "does this
   look right?" If nothing is genuinely ambiguous, say so explicitly.
