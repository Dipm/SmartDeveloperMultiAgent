# Test agent

Stage 5 of the SmartDeveloper ticket pipeline. Invoked only as `@test` after
`@dev` has written `.dev-agent/{ticket-id}/04-dev-notes.md`.

| Primitive | Path | Job |
|---|---|---|
| Subagent | `../test.md` | Thin entry |
| Agent prompt | `agent.md` | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | How to change this package |
| Instructions | `instructions/` | Contract, write/run loop, `05-tests.md` schema |
| Skills | `skills/*/SKILL.md` | Author tests, run suite, log gaps |
| Hooks | `hooks/` | Dev notes present; writes limited to tests + `05-tests.md` |

## Invoke

```
@test {ticket-id}
```

## Produce

Tests covering the change, plus `.dev-agent/{ticket-id}/05-tests.md`.

## Do not

- Re-implement the feature
- Log results without actually running the suite
- Chain into `@review`
