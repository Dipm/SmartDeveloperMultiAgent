# Output

**Lean mode (default):** update `pipeline.json` → `stages.pr_draft`:
- `status: complete`
- `title`, `body` — PR draft text
- `assumptions_review` — pull from dev assumptions for user review

Do **not** write `08-pr.md`. Orchestrator presents `body` at PR gate.

**Audit trail:** write `08-pr.md`.

On failure: `stages.pr_draft.status: failed` + error.
