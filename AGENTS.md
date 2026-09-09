# SmartDeveloper repository guide

This repo defines the SmartDeveloper ticket pipeline for Cursor. It contains no
application runtime — only agent packages, hooks, commands, and scripts.

## Layout

| Path | Purpose |
|---|---|
| `agents/` | Subagent packages (`triage`, `context`, `plan`, `dev`, `test`, `review`, `spec`, `docs-pr`, `pr-draft`, `pr-fix`) |
| `agents/shared/` | Error handling, token-efficiency, requirement-validation, lean-artifacts, platform-and-scope |
| `agents/orchestrator.md` | Pipeline coordination contract |
| `commands/fix-ticket.md` | Slash command entry point |
| `rules/dev-agent-pipeline.mdc` | Always-on pipeline rule |
| `hooks/lib/` | Shared Python hook library |
| `hooks/smartDevByDipali_hookWrapper.py` | Agent-scoped hook dispatcher |
| `scripts/` | `smartDevByDipali_bootstrapProject.py`, `smartDevByDipali_mergeHooks.py`, `smartDevByDipali_validatePipeline.py` |
| `docs/` | Architecture and artifact reference |
| `tests/` | Hook unit tests |

## Changing an agent

1. Read the agent's `AGENTS.md` (e.g. `agents/dev/AGENTS.md`).
2. Keep each primitive in its lane: entry file, `agent.md`, `instructions/`,
   `skills/`, `hooks/`.
3. Run `python3 scripts/smartDevByDipali_validatePipeline.py` after edits.
4. Run `python3 scripts/smartDevByDipali_mergeHooks.py` if hooks changed.

## Artifact naming

Use numbered artifacts under `.dev-agent/{ticket-id}/`. Do not introduce
unnumbered stage files. See `docs/pipeline-artifacts.md`.

## Hook conventions

- Import shared code from `hooks.lib.pipeline_hook`.
- Set `AGENT = "{name}"` and call `require_agent(data, AGENT)` at the start.
- Use `load_event()` — it fails closed on malformed JSON.
- Never duplicate `tool_name` / `path_of` helpers in individual hooks.

## Installation

- **Plan A (recommended):** [docs/USAGE.md](docs/USAGE.md) — `smartDevByDipali_installGlobal.py` + `smartDevByDipali_onboardProject.py`
- **Legacy:** `scripts/smartDevByDipali_bootstrapProject.py` — full copy into a project
