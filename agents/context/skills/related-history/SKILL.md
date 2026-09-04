---
name: related-history
description: Find commits and PRs that touched the same files or problem as the ticket. Use when the context agent researches git/GitHub history.
disable-model-invocation: true
---

# Related history

Use the file list from codebase search as the path filter.

Prefer:

```bash
git log --oneline -n 20 -- -- {paths}
git log -n 5 -p -- {paths}
```

If GitHub MCP is available, search PRs by those paths or the ticket ID.

For each item, write: identifier, date or PR number, what changed in this area,
anything that contradicts current triage (revert, partial fix, "won't fix").

If the repo has no git remote, no GitHub auth, or no history: one line under
Related history, then stop. Do not invent PRs.
