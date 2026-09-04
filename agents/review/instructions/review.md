# Review

1. Confirm gates.

2. Load `skills/inspect-diff/SKILL.md`. Read plan, dev notes, tests, and the diff.
   Check: correctness against the plan, missed edge cases, unused or dead code,
   scope creep beyond the plan, security smells (injection, hardcoded secrets,
   unsafe deserialization), style consistency with architecture.mdc.

3. Load `skills/rank-findings/SKILL.md`. Rank: blocking / should-fix / nit.
   Do not fix anything — flag only.

4. Write `06-review-notes.md`. If blocking or should-fix: state this should go back
   to `@dev` before proceeding. If nothing: say so explicitly.
