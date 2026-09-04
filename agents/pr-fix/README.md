# PR-fix agent

Post-PR stage. Invoked as `@pr-fix` by the orchestrator **once per reviewer
comment**, never as a batch.

| Primitive | Path | Job |
|---|---|---|
| Subagent | `../pr-fix.md` | Thin entry |
| Agent prompt | `agent.md` | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | How to change this package |
| Instructions | `instructions/` | Contract, classify/act, append-only log |
| Skills | `skills/*/SKILL.md` | Classify, apply or reply, append log |
| Hooks | `hooks/` | One comment; append-only `09-review-log.md` |

## Invoke

```
@pr-fix {ticket-id} — comment: {one comment}
```

## Produce

Append to `.dev-agent/{ticket-id}/09-review-log.md`. Application edits only for
classification (a) trivial fix.

## Do not

- Handle multiple comments in one run
- Expand scope or push back on a reviewer without engineer confirmation
