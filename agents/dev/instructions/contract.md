# Contract

## In

- Ticket ID from the invocation (required).
- `.dev-agent/{ticket-id}/03-plan.md` (required). Read it fully.
- Explicit human approval of that plan (required). If the plan exists but was
  not approved, stop and report rather than proceeding.
- Optional: `.dev-agent/{ticket-id}/01-triage.md` and `02-context.md` only to
  resolve a plan ambiguity. The plan wins if they disagree; flag the disagreement.

## Out

- Application edits listed in the plan, in the order the plan gives.
- `.dev-agent/{ticket-id}/04-dev-notes.md` — see `output.md`.
- Parent message: short summary + open questions (deviations, uncovered
  assumptions).

## Stop immediately

- Missing ticket ID.
- Missing or empty `03-plan.md`.
- Plan not approved.
- Need to edit a file the plan does not list — flag first, do not silently expand.
- Request to skip checks, open a PR, or write the `@test` suite unprompted.

## Scope

In: implement the approved plan; run lint / typecheck / build; record deviations.

Out: re-planning, new product decisions, test-suite authorship (`@test`), review,
docs/PR (`@docs-pr`).

## Platform and non-code scope

Follow `agents/shared/platform-and-scope.md`.

- Fix only the **open workspace** when the ticket names multiple platforms; ask before
  editing other repos and collect repo info if the engineer wants them included.
- If targeted search finds no plausible client defect, **stop** — do not ship speculative
  fixes. Report suggested backend/proxy/QA/env checks to the parent.
## On failure

- Do not write a success artifact unless the stage actually succeeded.
- Update `pipeline.json` with `status: failed` and structured `error` (see
  `agents/shared/error-handling.md`).
- Return error-card fields to the parent. Do not chain the next agent.
- Transient errors (`external_service`, `auth`, `timeout`): retry **once** inside
  this agent, then fail with `retry_count: 1`.

