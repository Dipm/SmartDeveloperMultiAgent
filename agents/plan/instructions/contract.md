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
