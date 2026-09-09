# Plan errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Missing triage/context | `missing_prerequisite` | Run earlier stages |
| Plan too complex / timeout | `timeout` | Narrow scope; `retry plan` |
| Hook blocked implementation | `hook_blocked` | Do not edit application code in plan stage |
| Cursor crash | `subagent_crash` | `retry plan` |
