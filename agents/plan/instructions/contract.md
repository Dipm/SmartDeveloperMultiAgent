# Contract

## In

- Ticket ID (required).
- `.dev-agent/{ticket-id}/01-triage.md` and `02-context.md` (required).

## Out

- `.dev-agent/{ticket-id}/03-plan.md`
- Parent: short summary + 2–4 decision questions

## Stop immediately

- Missing priors.
- Request to start coding or call `@dev`.
- "Just pick an approach" when a design decision is out of normal scope — still
  write the plan, but put that decision in the gate list instead of silently choosing.

## Scope

In: files, approach, order, edge cases, blast radius, extra-scope callouts.

Out: implementation, tests, PR.

## Platform and non-code scope

Follow `agents/shared/platform-and-scope.md`. Plans cover the open workspace only
unless the engineer expanded scope. Prefer a verification plan over code changes when
no client defect is found.
## On failure

- Do not write a success artifact unless the stage actually succeeded.
- Update `pipeline.json` with `status: failed` and structured `error` (see
  `agents/shared/error-handling.md`).
- Return error-card fields to the parent. Do not chain the next agent.
- Transient errors (`external_service`, `auth`, `timeout`): retry **once** inside
  this agent, then fail with `retry_count: 1`.

