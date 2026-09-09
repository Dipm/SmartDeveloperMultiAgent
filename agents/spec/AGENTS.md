# Editing the spec agent package

Non-prod only. Merges triage + context + plan into one `@spec` invocation.

| Primitive | Path | Job |
|---|---|---|
| Subagent | `../spec.md` | Thin entry |
| Agent prompt | `agent.md` | Identity, gates |
| Instructions | `instructions/` | Contract, work loop, output schemas |
| Skills | `skills/*/SKILL.md` | Fetch Jira + draft all three artifacts |
| Hooks | `hooks/` | Ticket required; readonly app tree |

Produces `01-triage.md`, `02-context.md`, `03-plan.md`. Plan is auto-approved on stop.
