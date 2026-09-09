# Output

**Lean mode (default):** update `.dev-agent/{ticket-id}/pipeline.json` only. Do **not**
create `01-triage.md`, `02-context.md`, or `03-plan.md`.

Set in one pass:
- `stages.triage`, `stages.context`, `stages.plan`, `stages.spec` → `status: complete`
- `stages.spec.paths` — array of files `@dev` and `@test` may edit
- `stages.spec.summary` — one line
- Optional: `validation_verdict`, `assumptions` on spec stage

On failure: `stages.spec.status: failed` + structured `error`.

**Audit trail (`--audit-trail`):** also write numbered `.md` files per legacy schemas.
