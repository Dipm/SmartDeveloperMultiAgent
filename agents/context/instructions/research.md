# Research

Work from the triage brief. Prefer a small, high-signal set of files over a
dump of weak matches.

1. **Code** — load `skills/search-codebase/SKILL.md`. Start from names, errors,
   and modules in triage. Follow imports and call sites one hop. Stop when
   additional files would not change a plan.

2. **History** — load `skills/related-history/SKILL.md`. Same paths as step 1.
   Record what changed and why, not SHAs alone. If git/GitHub is unavailable,
   say so; do not guess.

3. **Conventions** — read `.cursor/rules/architecture.mdc` if present. Keep only
   rules that constrain this change. If the file is missing, say so.

4. **Tests** — load `skills/map-tests/SKILL.md`. Note coverage and what will
   need updating. Do not write or run tests.

Stay read-only on the application tree. Do not "prepare" files for later stages.
