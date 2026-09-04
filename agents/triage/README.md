# Triage agent

Stage 1 of the SmartDeveloper ticket pipeline. Invoked only as `@triage` with a
ticket ID. Classifies the ticket; does not research the codebase in depth.

| Primitive | Path | Job |
|---|---|---|
| Subagent | `../triage.md` | Thin entry |
| Agent prompt | `agent.md` | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | How to change this package |
| Instructions | `instructions/` | Contract, triage loop, `01-triage.md` schema |
| Skills | `skills/*/SKILL.md` | Fetch Jira, classify and probe scope |
| Hooks | `hooks/` | Ticket id required; Jira read-only; write only `01-triage.md` |

## Invoke

```
@triage {ticket-id}
```

## Produce

`.dev-agent/{ticket-id}/01-triage.md`

## Do not

- Implement or plan
- Edit the Jira ticket
- Ask a generic "does this look right?"
