# Test errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Missing plan/dev notes | `missing_prerequisite` | Run `@dev` first |
| Tests fail after retry | `validation` | Record flake vs real failure in `05-tests.md` |
| project-checks missing | `user_input_needed` | Ask parent for test commands |
| Cursor crash | `subagent_crash` | `retry test` |
