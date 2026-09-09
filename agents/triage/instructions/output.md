# Output

**Lean mode (default):** update `pipeline.json` only (`stages.triage`: status, summary,
validation_verdict, assumptions). No `01-triage.md`.

On failure: `stages.triage.status: failed` + error object.

**Audit trail (`--audit-trail`):** write `01-triage.md` with Summary, Pipeline mode,
Expected behavior validation, Classification, Open questions sections.
