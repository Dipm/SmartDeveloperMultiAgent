# Output

Write `.dev-agent/{ticket-id}/02-context.md` with exactly these sections.
Omit speculation. Empty sections get one factual line (e.g. "Git history not
available in this environment."). Update `pipeline.json` with
`stages.context.status: "complete"`.

```markdown
# Context — {ticket-id}

## Relevant files
- `path` — purpose; why it matters for this ticket

## Related history
- commit/PR — what it changed in this area

## Applicable conventions
- rule from architecture.mdc and how it applies here

## Existing tests
- `path` — what it covers; likely need update: yes/no

## Dependencies needed
- new packages or services the plan may need to add (or "None identified.")

## Contradictions / complications vs triage
- (or "Context is straightforward; nothing contradicts triage.")
```
