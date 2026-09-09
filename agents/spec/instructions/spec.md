# Spec work loop

Load `agents/shared/requirement-validation.md` and `agents/shared/platform-and-scope.md` first.

1. **Mode:** If user did not pass `--prod` and ticket does not clearly require prod,
   set `pipeline.json` → `"mode": "non-prod"`.
2. Fetch ticket via Jira MCP (title, description, acceptance criteria).
3. **Validate expected behavior** (≤3 min): compare ticket claims to current code
   (targeted search, ≤8 files). Record verdict in triage section.
4. Write `01-triage.md` — include classification, mode assumption, and validation.
5. Write `02-context.md` — file map tied to validated behavior (≤8 files).
6. Write `03-plan.md` with `paths` block and an `## Assumptions` section if validation
   was unclear.
7. Mark stages complete in `pipeline.json`.

If validation is inconclusive, add **User verification guide** to `01-triage.md` — do
not block. Prefer proceeding with the most likely fix and documenting assumptions.

Prefer defaults over questions. Only stop for blocking ambiguities.
