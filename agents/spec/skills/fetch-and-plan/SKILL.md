---
name: fetch-and-plan
description: Fetch Jira ticket, scan codebase minimally, write triage/context/plan artifacts. Use at start of @spec.
disable-model-invocation: true
---

# Fetch and plan (non-prod)

1. Jira MCP: fetch ticket fields.
2. `rg`/glob: locate files tied to the ticket (≤8 reads).
3. Write `01-triage.md`, `02-context.md`, `03-plan.md` under `.dev-agent/{ticket-id}/`.
4. Include a `paths` block in `03-plan.md` listing every file `@dev` and `@test` may edit.

Do not run the full test suite. Do not implement.
