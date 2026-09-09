# Docs-PR errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Missing prior artifacts | `missing_prerequisite` | Complete earlier stages |
| Review still sends back | `validation` | Return to `@dev` first |
| Hook blocked PR open | `hook_blocked` | Draft only; engineer opens PR |
| Cursor crash | `subagent_crash` | `retry docs-pr` |
