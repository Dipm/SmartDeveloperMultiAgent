# SmartDeveloper architecture

SmartDeveloper is a **staged multi-agent pipeline** for Cursor that turns Jira
tickets into reviewed, tested, documented pull requests with human gates.

## Design principles

1. **One agent, one stage** — each subagent has a narrow mandate.
2. **Artifact handoffs** — stages communicate through `.dev-agent/{ticket-id}/`
   files, not conversation memory.
3. **Defense in depth** — prompts, contracts, and Python hooks all enforce boundaries.
4. **Human gates** — only PR opening requires explicit engineer consent; plans auto-approve on success.

## Pipeline flow

```
/fix-ticket PROJ-123 --prod
  → @triage → @context → @plan → @dev ∥ @test → @review
  → (loop to @dev if needed, max 3) → @docs-pr ∥ @pr-draft → human opens PR
  → @pr-fix per comment

/fix-ticket PROJ-123 --non-prod
  → @spec → @dev ∥ @test → @docs-pr ∥ @pr-draft → human opens PR
```

See `agents/orchestrator.md` for resume (`--from`) and gate logic.

## Package layout

```
agents/{name}/
  agent.md           # Identity, gates, handoff
  instructions/      # contract.md, work.md, output.md
  skills/*/SKILL.md  # Step procedures
  hooks/             # Deterministic guards
agents/{name}.md     # Cursor subagent entry (frontmatter)
```

Shared hook library: `hooks/lib/pipeline_hook.py`

## Hook enforcement

Per-agent hooks are merged by `scripts/smartDevByDipali_mergeHooks.py` into
`.cursor/hooks.json.example`. The wrapper (`hooks/smartDevByDipali_hookWrapper.py`) scopes each hook
to its agent via the `AGENT` env var.

Hooks **fail closed** on malformed JSON by default (`FAIL_CLOSED=1`).

## Extending the pipeline

1. Add a new directory under `agents/`.
2. Follow the package layout in any existing `AGENTS.md`.
3. Register hooks in `hooks/hooks.json`.
4. Run `python3 scripts/smartDevByDipali_mergeHooks.py`.
5. Add the stage to `agents/orchestrator.md` and `commands/fix-ticket.md`.

## Validation

```bash
python3 scripts/smartDevByDipali_validatePipeline.py
python3 -m pytest tests/
```

## Error handling

Failures are structured in `pipeline.json` (`status: failed` + `error` object).
The orchestrator presents an error card and waits for user confirmation before
retry or resume. See `agents/shared/error-handling.md`.

```
subagent error → read pipeline.json + artifacts
              → emit error card (what / impact / fixes)
              → user confirms recovery → retry | resume | abort
```

Time budgets: warn at 5 min, timeout at 15 min (orchestrator instructions).

Hooks record stage start (`subagentStart`) and verify artifacts on stop
(`subagentStop`). Review loop capped at 3 iterations via `enforce-review-loop.py`.

