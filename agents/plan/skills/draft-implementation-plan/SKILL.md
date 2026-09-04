---
name: draft-implementation-plan
description: Write a concrete file-by-file implementation plan with order, edge cases, and blast radius. Use after prior stages are read. Do not implement.
disable-model-invocation: true
---

# Draft implementation plan

Be concrete enough that `@dev` can execute without inventing architecture.

Must include:

- Files to touch, in order (narrative list)
- A machine-readable `paths` fenced block (see `instructions/output.md`)
- Approach (not slogans)
- Edge cases
- Risk / blast radius
- Explicit extra-scope: schema changes, new dependencies, breaking changes,
  design decisions beyond this ticket

Prefer the smallest change that meets acceptance criteria. If two approaches
are reasonable, do not pick silently — put them in Decisions for the engineer.

Do not edit application files. Do not write tests.
