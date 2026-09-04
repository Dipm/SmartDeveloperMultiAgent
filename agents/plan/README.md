# Plan agent

Stage 3 of the SmartDeveloper ticket pipeline. Invoked only as `@plan` after
`@context` has written `.dev-agent/{ticket-id}/02-context.md`. Highest-leverage
gate: the parent must get explicit human approval before `@dev`.

| Primitive | Path | Job |
|---|---|---|
| Subagent | `../plan.md` | Thin entry |
| Agent prompt | `agent.md` | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | How to change this package |
| Instructions | `instructions/` | Contract, planning loop, `03-plan.md` schema |
| Skills | `skills/*/SKILL.md` | Read priors, draft plan, decision list |
| Hooks | `hooks/` | Priors present; no implementation; write only `03-plan.md` |

## Invoke

```
@plan {ticket-id}
```

## Produce

`.dev-agent/{ticket-id}/03-plan.md`

## Do not

- Implement
- Treat a written plan as approved (parent + human own that)
