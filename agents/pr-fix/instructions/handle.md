# Handle

1. If the prompt contains more than one distinct review comment, stop.

2. Read the classification prefix from the invocation:
   - `trivial` — load `skills/classify-comment/SKILL.md`, treat as (a)
   - `replan` — treat as (b) needs re-plan; stop and flag
   - `disagree` — treat as (c); draft a reply, do not change code until confirmed

3. Load `skills/apply-or-reply/SKILL.md` only for `trivial`, or for `replan` /
   `disagree` after confirmation in this conversation.

4. Load `skills/append-review-log/SKILL.md`. Append classification and outcome to
   `09-review-log.md`. Never overwrite the log.
