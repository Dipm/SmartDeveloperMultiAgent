---
name: inspect-diff
description: Read plan, dev notes, tests, and the actual diff for an independent review. Use when the review agent starts. Do not edit code.
disable-model-invocation: true
---

# Inspect diff

Read `03-plan.md`, `04-dev-notes.md`, `05-tests.md`, then `git diff` (and
`git diff --stat`) against the base branch if known.

Check:

- Correctness against the plan
- Missed edge cases (plan + tests)
- Unused or dead code
- Scope creep beyond the plan
- Security: injection, hardcoded secrets, unsafe deserialization
- Style vs `.cursor/rules/architecture.mdc` if present

You are not the author. Do not give the implementation the benefit of the doubt
on blocking issues.
