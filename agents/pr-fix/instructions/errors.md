# PR-fix errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Multiple comments | `validation` | Invoke once per comment |
| replan/disagree without confirm | `user_input_needed` | Wait for engineer confirmation |
| Cursor crash | `subagent_crash` | `retry pr-fix` with same comment |
