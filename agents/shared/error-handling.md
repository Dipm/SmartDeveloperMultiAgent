# Shared error handling

All pipeline agents and the orchestrator follow this contract. Failures must be
**structured**, **brief**, and **actionable**.

## pipeline.json stage status

Each stage uses one of: `running`, `complete`, `failed`.

```json
{
  "pipeline_version": "1",
  "ticket": "PROJ-123",
  "stages": {
    "triage": {
      "status": "failed",
      "artifact": "01-triage.md",
      "started_at": "2026-09-04T12:00:00Z",
      "completed_at": "2026-09-04T12:02:00Z",
      "error": {
        "code": "external_service",
        "message": "Jira MCP returned auth error",
        "recoverable": true,
        "retry_count": 1,
        "suggestions": [
          "Re-authenticate Jira MCP, then reply 'retry triage'",
          "Paste ticket body in chat, then reply 'retry triage with pasted body'"
        ]
      }
    }
  }
}
```

On success: set `status: complete`, `completed_at`, and omit `error`.

On failure: set `status: failed`, `completed_at`, and populate `error`.

## Error codes

| Code | When | Recoverable |
|---|---|---|
| `missing_prerequisite` | Prior artifact or gate missing | yes |
| `external_service` | Jira/MCP/network down | yes |
| `auth` | Token or API key expired | yes |
| `hook_blocked` | Python hook denied a tool | yes |
| `timeout` | Stage exceeded 15 min budget | yes |
| `subagent_crash` | Cursor stopped with error | yes |
| `validation` | Artifact empty or malformed | yes |
| `user_input_needed` | Ambiguous ticket, no data | yes |

## Transient errors — one auto-retry

For `external_service`, `auth`, and `timeout`: retry **once** inside the agent.
On second failure, set `retry_count: 1` in the error object and stop.

## Agent failure protocol

1. Do **not** write a success artifact unless the stage actually succeeded.
2. Update `pipeline.json` with `status: failed` and the structured `error` object.
3. Return error-card fields to the parent (see below). Do **not** chain the next agent.
4. Do **not** auto-retry after the user-visible failure — wait for user confirmation.

## Error card (parent / orchestrator emits)

```markdown
## Stage failed: @{stage} ({ticket-id})
**What happened:** {one sentence}
**Impact:** {what is blocked}
**Suggested fixes:**
1. {option} → reply `{recovery command}`
2. {option} → reply `{recovery command}`
**Confirm:** Reply with option number (or `abort`) before I continue.
```

## Recovery commands (user-confirmed only)

| User says | Action |
|---|---|
| `retry {stage}` | Re-invoke same subagent |
| `retry {stage} with pasted body` | Re-invoke with pasted context |
| `/fix-ticket {id} --from {stage}` | Resume per orchestrator rules |
| `abort` | Mark pipeline aborted; stop |

## Time budgets (orchestrator)

- **5 min:** warn user the stage is still running.
- **15 min:** treat as `timeout` failure; write manifest error; emit error card.
- Never auto-retry a timeout without user confirmation.
