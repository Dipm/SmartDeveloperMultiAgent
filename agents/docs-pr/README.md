# Docs / PR agent

Stage 7 of the SmartDeveloper ticket pipeline. Invoked only as `@docs-pr` after
`@review` issues (if any) are resolved. This stage **drafts**; opening the PR is
a required human gate on the parent, not this agent.

This package uses Cursor primitives, split by job:

| Primitive | Path | Loads when | Job |
|---|---|---|---|
| Subagent | `../docs-pr.md` | `@docs-pr` / orchestrator | Thin entry. Points here. |
| Agent prompt | `agent.md` | Always, for this stage | Identity, gates, handoff |
| Nested AGENTS.md | `AGENTS.md` | Editing files in this folder | How to change this package |
| Instructions | `instructions/` | Always, for this stage | Contract, draft loop, artifact schemas |
| Skills | `skills/*/SKILL.md` | One step at a time | Read pipeline files, docs, PR body |
| Hooks | `hooks/` | Agent lifecycle (if wired) | Review must be clear; no `gh pr create` / push; writes only `06`/`07` |

```
agents/docs-pr.md                 # Cursor subagent (keep this file; name = docs-pr)
agents/docs-pr/
  README.md
  AGENTS.md
  agent.md
  instructions/
    contract.md
    document.md
    output.md
  skills/
    gather-pipeline-artifacts/SKILL.md
    write-reviewer-docs/SKILL.md
    draft-pr-description/SKILL.md
  hooks/
    README.md
    hooks.json
    require-review-clear.py
    block-open-pr.py
```

## Invoke

From `commands/fix-ticket.md`, after `@review` is clean (or `@dev` rework landed
and review no longer has blocking / should-fix):

```
@docs-pr {ticket-id}
```

The parent must still wait for explicit go-ahead before anyone opens a PR.

## Produce

- `.dev-agent/{ticket-id}/07-docs.md`
- `.dev-agent/{ticket-id}/08-pr.md`

## Do not

- Open, push, or publish a PR
- Edit application code
- Skip unresolved review findings
