# Triage errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| No ticket ID | `missing_prerequisite` | Invoke as `@triage {ticket-id}` |
| Jira MCP down / network | `external_service` | Retry once; re-auth MCP; paste ticket body |
| Jira auth expired | `auth` | Re-authenticate Jira MCP; retry |
| No ticket data after retry | `user_input_needed` | Paste title/description; `retry triage with pasted body` |
| Hook blocked write | `hook_blocked` | Only write `01-triage.md` under `.dev-agent/` |
| Cursor crash | `subagent_crash` | `retry triage`; check partial artifact |
