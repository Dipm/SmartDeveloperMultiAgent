Fix the Jira ticket with ID $ARGUMENTS end to end using the pipeline below.

## Options

- **Resume:** `/fix-ticket {ticket-id} --from {stage}` — skip earlier stages when
  artifacts already exist (`triage`, `context`, `plan`, `dev`, `test`, `review`,
  `docs-pr`). Still respect human gates.

## Orchestration rules

After EACH subagent finishes, present its output and any open questions it raised,
then STOP and wait for explicit go-ahead before continuing. Never chain two subagents
without the engineer responding in between.

If `@review` sends work back to `@dev` more than **3 times** for the same ticket,
stop the pipeline and ask the engineer to take over manually.

1. @triage
2. @context
3. @plan   — required human approval gate. Do not proceed without it.
4. @dev
5. @test
6. @review — if blocking or should-fix issues are found, go back to `@dev` before
   continuing; do not skip ahead.
7. @docs-pr — required human approval gate before any PR is actually opened.

For PR comments after this point, invoke `@pr-fix` once per comment with a
classification prefix: `@pr-fix {ticket-id} trivial|disagree|replan` — not in a batch.

Load `agents/orchestrator.md` for resume logic and gate checks.
