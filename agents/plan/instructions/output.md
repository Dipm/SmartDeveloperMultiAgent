# Output

**Lean mode (default):** update `pipeline.json` → `stages.plan`:
- `status: complete`
- `paths` — array of editable file paths (required for hooks)
- `summary` — one line approach

Do **not** write `03-plan.md`.

**Audit trail:** write `03-plan.md` with full plan schema including paths block.

On failure: `stages.plan.status: failed` + error.
