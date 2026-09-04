---
name: implement-from-plan
description: Apply an approved 03-plan.md in listed file order without expanding scope. Use when the dev agent starts implementation.
disable-model-invocation: true
---

# Implement from plan

Read `.dev-agent/{ticket-id}/03-plan.md`. Extract: files to touch, order, approach,
edge cases, explicit non-goals.

For each planned file, in the plan's order:

1. Read the current file (or confirm it must be created).
2. Make only the change the plan describes.
3. Do not refactor, rename, or "clean up" unless the plan says to.

If you need a file not in the plan: stop, name the file and why, wait for the
parent. Do not edit it first.

If a planned step is already done in the tree: record that under deviations as
"already present," do not redo it.

Do not author a test suite unless those test paths are in the plan. `@test` owns
coverage after this stage.
