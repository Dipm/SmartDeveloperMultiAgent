---
name: draft-pr-description
description: Draft 08-pr.md (title, summary, ticket, testing, out of scope). Use after 07-docs.md is written. Never run gh pr create or git push.
disable-model-invocation: true
---

# Draft PR description

Write `.dev-agent/{ticket-id}/08-pr.md` using `instructions/output.md`.

Include: summary, linked ticket, what changed, testing performed, explicitly
out-of-scope follow-up.

Rules:

- Title: short, ticket id if the team convention uses it. Do not promise
  "Fixes {id}" unless triage/plan said this fully closes the ticket.
- Testing: copy facts from `05-tests.md` and the manual steps in `07-docs.md`.
- Do not paste secrets, tokens, or internal URLs that are not already in the
  ticket.
- Do not open the PR. Do not run `gh pr create`, `gh pr edit`, or `git push`.

Finish by listing confirm-before-open questions (scope, wording, fix vs
partial). If nothing needs confirmation, write that explicitly.
