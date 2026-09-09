# Context errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Missing `01-triage.md` | `missing_prerequisite` | Run `@triage` first |
| Readonly write blocked | `validation` | Return full markdown to parent; do not claim success |
| Repo too large / timeout | `timeout` | Narrow search scope; `retry context` |
| Hook blocked | `hook_blocked` | Only write `02-context.md` |
| Cursor crash | `subagent_crash` | `retry context` |
