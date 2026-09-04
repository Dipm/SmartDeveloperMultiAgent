# Review agent

Stage 6 of the SmartDeveloper ticket pipeline. Invoked only as `@review` after
`@test`. Reviews the diff; never edits application code.

| Primitive | Path | Job |
|---|---|---|
| Subagent | `../review.md` | Thin entry |
| Agent prompt | `agent.md` | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | How to change this package |
| Instructions | `instructions/` | Contract, checklist, `06-review-notes.md` schema |
| Skills | `skills/*/SKILL.md` | Inspect diff, rank findings |
| Hooks | `hooks/` | Tests present; flag-only writes to `06-review-notes.md` |

## Invoke

```
@review {ticket-id}
```

## Produce

`.dev-agent/{ticket-id}/06-review-notes.md`

## Do not

- Fix code
- Soften blocking / should-fix into nits
- Invent nits when you found nothing
