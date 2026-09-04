---
name: classify-comment
description: Classify one PR review comment as trivial fix, needs re-plan, or disagreement. Use when pr-fix starts. Do not handle a batch of comments.
disable-model-invocation: true
---

# Classify comment

Read the one comment (GitHub MCP or pasted). Compare to `03-plan.md` if present.

- **(a) Trivial fix** — local, no new behavior, no new files outside the plan.
- **(b) Needs re-plan** — changes scope or approach meaningfully.
- **(c) Disagreement** — comment is mistaken, out of date, or not applicable.

If unsure between (a) and (b), choose (b). Stop after classifying (b) or (c)
until the engineer confirms.
