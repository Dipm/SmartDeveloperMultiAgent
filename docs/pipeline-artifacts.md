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
| `08-pr.md` | docs-pr | PR draft (not published) |
| `09-review-log.md` | pr-fix | Append-only PR comment log |

## pipeline.json example

```json
{
  "pipeline_version": "1",
  "ticket": "PROJ-123",
  "stages": {
    "triage": { "status": "complete", "artifact": "01-triage.md" },
    "plan": { "status": "approved", "artifact": "03-plan.md" },
    "review": { "status": "complete", "verdict": "clean", "iteration": 1 }
  }
}
```

## .gitignore

See `.dev-agent/.gitignore`. Default keeps artifacts for audit trail.
