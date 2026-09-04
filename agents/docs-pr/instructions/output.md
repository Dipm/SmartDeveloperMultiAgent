# Output

Write both files. Do not invent testing that `05-tests.md` does not support.
Update `pipeline.json` with `stages.docs_pr.status: "complete"`.

## `.dev-agent/{ticket-id}/07-docs.md`

```markdown
# Docs — {ticket-id}

## What it was
- issue/feature in 2–4 sentences from triage + plan

## What changed
- how it was fixed or implemented (from plan + dev notes, not a file dump)

## Manual testing
- numbered steps a reviewer can run without the agent

## Out of scope / follow-up
- (or "None recorded.")
```

## `.dev-agent/{ticket-id}/08-pr.md`

```markdown
# PR draft — {ticket-id}

## Title
{short title}

## Body

### Summary
- 1–3 bullets

### Ticket
- {ticket-id} (link if the tracker URL is known; otherwise the id only)

### What changed
- bullets mapped to the diff / plan

### Testing
- what `@test` ran and the manual steps from 07-docs

### Out of scope
- explicitly out-of-scope follow-up (or "None.")

## Confirm before open
- wording/scope questions for the engineer
```
