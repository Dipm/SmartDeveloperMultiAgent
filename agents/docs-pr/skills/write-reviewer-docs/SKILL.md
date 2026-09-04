---
name: write-reviewer-docs
description: Write 07-docs.md with problem, change, and manual test steps for a human reviewer. Use after pipeline artifacts are gathered. Do not open a PR.
disable-model-invocation: true
---

# Write reviewer docs

Write `.dev-agent/{ticket-id}/07-docs.md` using `instructions/output.md`.

- **What it was** — from triage, not a restatement of the diff.
- **What changed** — from plan + `04-dev-notes.md`. Include deviations that
  shipped. Do not list every file.
- **Manual testing** — concrete steps (data, UI path, command) a reviewer can
  follow. Pull from `05-tests.md` plus anything the plan called out that tests
  did not automate. Do not claim a step was run if notes say it was not.
- **Out of scope** — only what prior stages marked out of scope. Do not invent
  a roadmap.

Do not update product README or architecture docs unless those paths were in
the approved plan and already changed by `@dev`. This skill writes `07-docs.md`
only.
