# Output

**Lean mode (default):** implement code; update `pipeline.json` → `stages.dev`:
- `status: complete`
- `summary` — one line what changed
- `assumptions` — list if ticket validation was unclear
- `checks` — lint/typecheck pass/fail one line

Do **not** write `04-dev-notes.md`.

**Audit trail:** write `04-dev-notes.md` with full sections.

On failure: `stages.dev.status: failed` + error.
