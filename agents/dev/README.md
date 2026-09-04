# Dev agent

Stage 4 of the SmartDeveloper ticket pipeline. Invoked only as `@dev` after the
human has approved `.dev-agent/{ticket-id}/03-plan.md`.

This package uses Cursor primitives, split by job:

| Primitive | Path | Loads when | Job |
|---|---|---|---|
| Subagent | `../dev.md` | `@dev` / orchestrator | Thin entry. Points here. |
| Agent prompt | `agent.md` | Always, for this stage | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | Editing files in this folder | How to change this package |
| Instructions | `instructions/` | Always, for this stage | Contract, implement loop, notes schema |
| Skills | `skills/*/SKILL.md` | One step at a time | Plan execution, checks, deviation log |
| Hooks | `hooks/` | Agent lifecycle (if wired) | Plan present + approved; writes scoped to the plan |

```
agents/dev.md                     # Cursor subagent (keep this file; name = dev)
agents/dev/
  README.md
  AGENTS.md
  agent.md
  instructions/
    contract.md
    implement.md
    output.md
  skills/
    implement-from-plan/SKILL.md
    run-project-checks/SKILL.md
    record-deviations/SKILL.md
  hooks/
    README.md
    hooks.json
    require-approved-plan.py
    enforce-plan-scope.py
```

## Invoke

From `commands/fix-ticket.md`, after `@plan` and explicit human go-ahead:

```
@dev {ticket-id}
```

Approval is the conversation go-ahead, or a sidecar
`.dev-agent/{ticket-id}/03-plan.approved`. Do not treat a written plan as
approved by default.

## Produce

`.dev-agent/{ticket-id}/04-dev-notes.md` plus the application edits the plan lists.

## Do not

- Implement without an approved plan
- Touch files the plan does not list (flag first)
- Chain into `@test` or `@review`
