---
name: run-project-checks
description: Run lint, typecheck, and build from project-checks.md and fix failures before finishing. Use after the dev agent has applied the plan. Do not treat this as the @test stage.
disable-model-invocation: true
---

# Run project checks

Read `.cursor/skills/project-checks.md`. If it is missing, try
`skills/project-checks.md`. If both are missing or still templates (`<exact command>`),
stop and ask the parent for the real commands. Do not guess `npm test`.

Run, in this order, only the commands that exist:

1. Lint
2. Type-check / build

Do not run the full test suite here unless the approved plan says this stage
must. `@test` runs tests.

## Transient failures — one retry

If a check command fails due to network, timeout, or tool outage, retry that
command **once**. On second failure, record in `04-dev-notes.md` and fail the
stage with `error.code: external_service` if unrecoverable.

If a check fails: fix inside the plan's files when possible. If the failure is
pre-existing and outside the plan, do not expand scope — record it in
`04-dev-notes.md` and ask whether to fix it.

Iterate until lint and typecheck/build pass, or until remaining failures are
explicitly out of plan scope.

Record each command and pass/fail for `04-dev-notes.md`.
