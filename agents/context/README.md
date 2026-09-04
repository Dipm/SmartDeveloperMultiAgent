# Context agent

Stage 2 of the SmartDeveloper ticket pipeline. Invoked only as `@context` after
`@triage` has written `.dev-agent/{ticket-id}/01-triage.md`.

This package uses Cursor primitives, split by job:

| Primitive | Path | Loads when | Job |
|---|---|---|---|
| Subagent | `../context.md` | `@context` / orchestrator | Thin entry. Points here. |
| Agent prompt | `agent.md` | Always, for this stage | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | Editing files in this folder | How to change this package |
| Instructions | `instructions/` | Always, for this stage | Contract, research loop, output schema |
| Skills | `skills/*/SKILL.md` | One step at a time | Procedures that should not sit in the always-on prompt |
| Hooks | `hooks/` | Agent lifecycle (if wired) | Non-negotiable: triage present, no app-code writes |

```
agents/context.md                 # Cursor subagent (keep this file; name = context)
agents/context/
  README.md
  AGENTS.md
  agent.md
  instructions/
    contract.md
    research.md
    output.md
  skills/
    search-codebase/SKILL.md
    related-history/SKILL.md
    map-tests/SKILL.md
  hooks/
    README.md
    hooks.json
    enforce-readonly.py
    require-triage.py
```

## Invoke

From `commands/fix-ticket.md`, after triage and human go-ahead:

```
@context {ticket-id}
```

## Produce

`.dev-agent/{ticket-id}/02-context.md`

If `readonly: true` blocks that write, return the full markdown to the parent and
ask it to save the file. Do not write anywhere else.

## Do not

- Skip missing triage
- Plan or implement
- Chain into `@plan`
