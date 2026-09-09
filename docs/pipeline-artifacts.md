# SmartDeveloper pipeline artifacts

Each ticket gets a directory: `.dev-agent/{ticket-id}/`

| File | Stage | Description |
|---|---|---|
| `pipeline.json` | all | Machine-readable stage status |
| `01-triage.md` | triage | Classification and ambiguities |
| `02-context.md` | context | Codebase mapping |
| `03-plan.md` | plan | Implementation plan |
| `03-plan.approved` | gate | Sidecar marking plan approval |
| `04-dev-notes.md` | dev | What shipped, deviations |
| `05-tests.md` | test | Test results and gaps |
| `06-review-notes.md` | review | Review verdict |
| `07-docs.md` | docs-pr | Reviewer documentation |
| `08-pr.md` | pr-draft | PR draft (not published; ship wave) |
| `09-review-log.md` | pr-fix | Append-only PR comment log |

## pipeline.json schema (v1)

Stage `status` values: `running`, `complete`, `failed`.

```json
{
  "pipeline_version": "1",
  "ticket": "PROJ-123",
  "stages": {
    "triage": {
      "status": "complete",
      "artifact": "01-triage.md",
      "started_at": "2026-09-04T12:00:00Z",
      "completed_at": "2026-09-04T12:01:30Z"
    },
    "plan": {
      "status": "approved",
      "artifact": "03-plan.md"
    },
    "review": {
      "status": "complete",
      "verdict": "clean",
      "iteration": 1
    }
  }
}
```

### Failure shape

When a stage fails, set `status: failed` and add an `error` object:

```json
{
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
      "Re-authenticate Jira MCP, then reply 'retry triage'"
    ]
  }
}
```

Error codes: `missing_prerequisite`, `external_service`, `auth`, `hook_blocked`,
`timeout`, `subagent_crash`, `validation`, `user_input_needed`.

See `agents/shared/error-handling.md` for the full contract.

## .gitignore

See `.dev-agent/.gitignore`. Default keeps artifacts for audit trail.


## Pipeline modes

Set `mode` in `pipeline.json` (`prod` or `non-prod`; default `non-prod`).

| Mode | Pre-code | Implement | Ship | Review |
|---|---|---|---|---|
| prod | triage→context→plan | dev∥test | docs-pr∥pr-draft | review |
| non-prod | spec | dev∥test | docs-pr∥pr-draft | skipped |

## Requirement validation

Triage/spec artifacts include `## Expected behavior validation` and optional
`## User verification guide`. Dev notes include `## Assumptions made` and
`## Please review` content surfaced at the PR gate. See
`agents/shared/requirement-validation.md`.

## Lean artifacts (default)

`lean_artifacts: true` — only `pipeline.json` is required. Stage summaries, paths,
review verdict, and PR draft text live in `stages.*` fields. Numbered `.md` files are
**not** created unless `--audit-trail`. See `agents/shared/lean-artifacts.md`.
