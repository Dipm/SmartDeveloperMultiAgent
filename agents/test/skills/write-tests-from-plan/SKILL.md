---
name: write-tests-from-plan
description: Add tests for the shipped change, including plan edge cases. Use when the test agent starts. Do not re-implement the feature.
disable-model-invocation: true
---

# Write tests from plan

Read `03-plan.md` and `04-dev-notes.md`. Cover the behavior that shipped,
including edge cases in the plan.

Match existing test layout and helpers. Do not introduce a new test framework.

If a test needs a production seam the plan did not allow: flag it, do not
refactor the feature quietly.

Do not "complete" unfinished `@dev` work inside tests.
