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
