---
name: append-review-log
description: Append one classified PR-comment outcome to 09-review-log.md. Never overwrite the file. Use when pr-fix is finishing.
disable-model-invocation: true
---

# Append review log

Append one block to `.dev-agent/{ticket-id}/09-review-log.md` using
`instructions/output.md`.

If the file exists: add below the last entry. Do not use Write to replace the
whole file. If the file does not exist: creating it once is allowed.

Record classification, action, and confirmation state even when waiting on
the engineer.
