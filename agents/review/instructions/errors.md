# Review errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Missing test notes / diff | `missing_prerequisite` | Run `@test` first |
| Review iteration > 3 | `validation` | Escalate to engineer; do not send back again |
| Cursor crash | `subagent_crash` | `retry review` |
