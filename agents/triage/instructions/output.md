# Output

Write `.dev-agent/{ticket-id}/01-triage.md` and update `pipeline.json` with
`stages.triage.status: "complete"`.

```markdown
# Triage — {ticket-id}

## Summary
- 2–3 sentences

## Classification
- bug | feature | chore
- severity/priority:
- complexity: trivial | moderate | complex

## Related tickets / PRs
- (or "None found.")

## Ambiguities
- (or "Nothing genuinely ambiguous.")

## Open questions (wasted-work)
1. ...
```
