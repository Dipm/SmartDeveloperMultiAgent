# Triage

When invoked with a ticket ID:

1. Load `skills/fetch-jira-ticket/SKILL.md`. Pull title, description, acceptance
   criteria, linked tickets, comments.

2. Load `skills/classify-and-scope/SKILL.md`.
   - Classify: bug, feature, or chore.
   - Severity/priority and complexity: trivial / moderate / complex.
   - Duplicate or already-in-progress related tickets.
   - Anything ambiguous about scope, acceptance criteria, or expected behavior.

3. Write `01-triage.md`.

4. Ask the 2–4 misunderstandings most likely to waste work — not "does this
   look right?" If nothing is genuinely ambiguous, say so explicitly.
