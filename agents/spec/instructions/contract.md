# Contract

## In

- Ticket ID (required).
- `pipeline.json` with `"mode": "non-prod"` (or orchestrator flag).

## Out

- `.dev-agent/{ticket-id}/01-triage.md`
- `.dev-agent/{ticket-id}/02-context.md`
- `.dev-agent/{ticket-id}/03-plan.md`
- Update `pipeline.json` stages: triage, context, plan, spec → `complete`

## Stop immediately

- Pipeline mode is `prod`.
- Missing ticket ID.
- Request to implement code.

## Scope

In: Jira fetch, minimal repo scan, concise plan with `paths` block.

Out: implementation, tests, PR.
