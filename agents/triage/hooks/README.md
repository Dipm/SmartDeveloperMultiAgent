# Hooks for `@triage`

Merge into project `.cursor/hooks.json`.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-ticket.py` | Ticket id required (fail closed) |
| `preToolUse` | `jira-and-artifact-readonly.py` | Writes only `01-triage.md` |
| `beforeMCPExecution` | `jira-and-artifact-readonly.py` | Deny Jira writes |
| `beforeShellExecution` | `jira-and-artifact-readonly.py` | Read-only git |

```bash
chmod +x agents/triage/hooks/*.py
```
