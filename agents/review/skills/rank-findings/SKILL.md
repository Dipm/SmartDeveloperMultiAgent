---
name: rank-findings
description: Rank review issues as blocking, should-fix, or nit. Use after inspecting the diff. Do not fix code. Do not invent nits.
disable-model-invocation: true
---

# Rank findings

- **blocking** — wrong vs plan/AC, security, data loss, tests that do not
  prove the change
- **should-fix** — real defect or scope creep; should return to `@dev`
- **nit** — optional style. Use sparingly.

If any blocking or should-fix: verdict is send back to `@dev`. Do not soften
this.

If you found nothing: write that. Do not invent nitpicks to seem thorough.
