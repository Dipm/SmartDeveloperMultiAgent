# Lean artifacts (default)

Developers care about **code**, not stage markdown logs. By default the pipeline
writes **only `pipeline.json`** under `.dev-agent/{ticket-id}/` — no numbered
`01-triage.md` … `07-docs.md` files.

## Default

`pipeline.json` includes:

```json
{
  "pipeline_version": "1",
  "ticket": "PROJ-123",
  "mode": "non-prod",
  "lean_artifacts": true,
  "stages": {
    "spec": {
      "status": "complete",
      "paths": ["src/foo.ts", "src/foo.test.ts"],
      "summary": "One-line stage outcome",
      "validation_verdict": "confirmed"
    },
    "dev": { "status": "complete", "summary": "Implemented X" },
    "test": { "status": "complete", "summary": "Tests pass" },
    "pr_draft": {
      "status": "complete",
      "title": "...",
      "body": "..."
    }
  }
}
```

Keep `summary` to **one line** per stage. Put assumptions in `dev.summary` or
`dev.assumptions` (string or list). Do not write prose dumps.

## What agents write

| Stage | Lean output |
|---|---|
| spec / triage / context / plan | Update `pipeline.json` stages + `paths` for plan/spec |
| dev | Code + `stages.dev` in pipeline.json |
| test | Tests + `stages.test` in pipeline.json |
| review | `stages.review.verdict`, `blocking`, `should_fix` arrays |
| docs-pr | `stages.docs_pr.summary` (optional one line) |
| pr-draft | `stages.pr_draft.title`, `body` — **no `08-pr.md` required** |

Return brief text to the parent chat; that is enough for the engineer.

## Audit trail (optional)

Pass `--audit-trail` on `/fix-ticket` to also write numbered `.md` files
(compliance, post-mortems). Sets `"lean_artifacts": false`.

## Hooks

In lean mode, hooks check `pipeline.json` stage status and `paths` — not `.md` files.
