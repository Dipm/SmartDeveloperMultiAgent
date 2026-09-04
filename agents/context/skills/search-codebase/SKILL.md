---
name: search-codebase
description: Find the smallest set of files, modules, and functions relevant to a triaged ticket. Use when the context agent starts codebase research.
disable-model-invocation: true
---

# Search codebase

Read `01-triage.md` first. Extract: error strings, module names, UI copy, API
paths, symbols, and file hints.

Search in this order:

1. Exact strings from triage (grep).
2. Symbol / type / function names (grep, then jump to definitions).
3. Semantic search only if exact search is thin.
4. One hop of imports and call sites from each hit that you will keep.

Keep a file only if a planner would need it. For each kept file, one clause:
what it does, why this ticket touches it.

Drop: generated code, lockfiles, unrelated fixtures, "also mentions this word"
matches.

Do not edit files. Do not open later-stage `.dev-agent/` files.
