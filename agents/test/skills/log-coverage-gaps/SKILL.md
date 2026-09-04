---
name: log-coverage-gaps
description: Write 05-tests.md with commands, pass/fail, uncovered edges, and test debt. Use when the test agent finishes.
disable-model-invocation: true
---

# Log coverage gaps

Write `.dev-agent/{ticket-id}/05-tests.md` using `instructions/output.md`.

Flag:

- Plan edge cases you could not cover (and why)
- Pre-existing test debt in this area
- Whether those are in scope to address (ask, do not silently fix)

If everything planned is covered and green, say so explicitly.
