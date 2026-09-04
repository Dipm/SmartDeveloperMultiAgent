---
name: gather-pipeline-artifacts
description: Read all prior .dev-agent ticket files and the diff so docs and the PR draft stay factual. Use when the docs-pr agent starts.
disable-model-invocation: true
---

# Gather pipeline artifacts

Read, in order if present:

1. `.dev-agent/{ticket-id}/01-triage.md`
2. `02-context.md`
3. `03-plan.md`
4. `04-dev-notes.md`
5. `05-tests.md`
6. `06-review-notes.md`
7. `09-review-log.md` if it exists

Required: 01, 03, 04, 05, review-notes. If any required file is missing or empty,
stop. Do not fill gaps from memory.

Then read the actual diff (`git diff` / `git diff --stat` against the base
branch if known). If there is no diff, say so in the parent return; still draft
from pipeline files but flag that the PR body may not match the branch.

Do not edit these files. Do not read later artifacts you are about to write
from a previous failed run as if they were source of truth — regenerate them.
