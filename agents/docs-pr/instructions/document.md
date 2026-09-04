# Document

1. Confirm gates in `contract.md`. If any fail, write nothing and report to parent.

2. Load `skills/gather-pipeline-artifacts/SKILL.md`. Read every prior
   `.dev-agent/{ticket-id}/*.md` file. Prefer facts from those files and the
   current diff over memory.

3. Load `skills/write-reviewer-docs/SKILL.md`. Write `07-docs.md`: what the
   issue/feature was, how it was fixed or implemented, and manual testing steps
   for a reviewer to verify.

4. Load `skills/draft-pr-description/SKILL.md`. Write `08-pr.md`: summary, linked
   ticket, what changed, testing performed, any explicitly out-of-scope follow-up.
   Draft only. Do not open the PR.

5. List 2–4 wording or scope items the engineer should confirm (ticket ID in the
   title, breaking-change language, secrets, "fixes X" vs "partial"). If nothing
   is sensitive, say so explicitly.
