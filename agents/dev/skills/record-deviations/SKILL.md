---
name: record-deviations
description: Write 04-dev-notes.md with what shipped, check results, and any plan deviations or uncovered assumptions. Use when the dev agent is finishing.
disable-model-invocation: true
---

# Record deviations

Write `.dev-agent/{ticket-id}/04-dev-notes.md` using `instructions/output.md`.

A deviation is any of:

- File not in the plan (only after it was flagged)
- Approach different from the plan
- Planned step skipped
- Extra refactor or dependency
- Check failure left unfixed

If none: write `No deviations.` Do not invent nits.

Assumptions: anything you decided that the plan did not specify (defaults, error
strings, names). If none: `None.`

Open questions go to the parent as well as the file. Ask about deviations and
uncovered assumptions; do not ask a generic "does this look right?"
