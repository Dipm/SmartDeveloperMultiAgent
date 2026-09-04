# Contract

## In

- Ticket ID (required).
- `.dev-agent/{ticket-id}/03-plan.md` and `04-dev-notes.md` (required).

## Out

- Test files covering the change, including plan edge cases.
- `.dev-agent/{ticket-id}/05-tests.md`
- Parent: summary + uncovered edges / test-debt questions

## Stop immediately

- Missing plan or dev notes.
- Logging pass/fail without running the suite.
- Rewriting production feature code as a substitute for tests (flag first).

## Scope

In: tests + running them per project-checks.

Out: `@review`, new product behavior, full-repo cleanup of unrelated debt.
