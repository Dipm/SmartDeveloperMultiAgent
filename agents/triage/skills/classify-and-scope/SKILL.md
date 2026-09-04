---
name: classify-and-scope
description: Classify a ticket (bug/feature/chore), estimate complexity, find related work, and list wasted-work questions. Use after the ticket is fetched.
disable-model-invocation: true
---

# Classify and scope

- Classification: bug | feature | chore
- Severity/priority from the ticket; complexity: trivial / moderate / complex
- Search Jira (and GitHub if available) for duplicates or in-progress relatives
- Ambiguity: scope, AC, expected behavior

Open questions: 2–4 items most likely to cause wasted work if misunderstood.
Specific, not "does this look right?" If nothing is genuinely ambiguous, say so.

Do not grep the repo for an implementation sketch; `@context` is next.
