---
name: run-test-suite
description: Run tests from project-checks.md and iterate until passing. Use after writing tests. Do not skip execution.
disable-model-invocation: true
---

# Run test suite

Read `.cursor/skills/project-checks.md` (fallback `skills/project-checks.md`).
If commands are still `<exact command>`, stop and ask. Do not guess.

Run **Single test file** for what you added, then **Full test suite** if that
command exists.

## Transient failures — one retry

If a test run fails due to network, timeout, or flaky infrastructure, retry
**once**. On second failure, distinguish flake vs real failure in `05-tests.md`.
If still failing, fail the stage with `error.code: validation` or
`external_service` as appropriate.

Iterate until passing. If a failure is unrelated pre-existing debt, do not
expand scope to rewrite the repo — record it and ask if it is in scope.

Actually execute. A written test that never ran is a failed stage.
