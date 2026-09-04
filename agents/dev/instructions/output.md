# Output

Write `.dev-agent/{ticket-id}/04-dev-notes.md` with exactly these sections.
Update `pipeline.json` with `stages.dev.status: "complete"`.

```markdown
# Dev notes — {ticket-id}

## Implemented
- what changed, mapped to plan steps

## Files touched
- `path` — one clause why

## Checks
- lint / typecheck / build: command, pass/fail, what you fixed if any

## Deviations from the plan
- (or "No deviations.")

## Assumptions the plan did not cover
- (or "None.")

## Open questions
- (or "None.")
```
