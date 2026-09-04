# Contract

## In

- Ticket ID (required).
- `.dev-agent/{ticket-id}/03-plan.md`, `04-dev-notes.md`, `05-tests.md` (required).
- The actual diff (required).

## Out

- `.dev-agent/{ticket-id}/06-review-notes.md`
- Parent: ranked summary; explicit "go back to `@dev`" if blocking/should-fix

## Stop immediately

- Missing tests notes or empty diff when a change was expected.
- Request to "just fix it while you review."

## Scope

In: correctness vs plan, edge cases, dead code, scope creep, security smells,
style vs `.cursor/rules/architecture.mdc`.

Out: patches, nits invented for thoroughness, `@docs-pr`.
