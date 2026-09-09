# Output

**Lean mode (default):** update `pipeline.json` → `stages.review`:
- `status: complete`
- `verdict`: clean | send_back
- `blocking`: [] or list of strings
- `should_fix`: [] optional

Do **not** write `06-review-notes.md`.

**Audit trail:** write `06-review-notes.md`.

On failure: `stages.review.status: failed` + error.
