# SmartDeveloper Multi-Agent Pipeline

A Cursor-native, staged pipeline for fixing Jira tickets end to end: triage →
context → plan → dev → test → review → docs/PR, with human gates and
deterministic hook guards.

**New users:** start with [SmartDeveloper-User-Guide.pdf](SmartDeveloper-User-Guide.pdf) — simple step-by-step setup (Mac & Windows).

## Recommended: global install (Plan A)

Install **once per machine**. Each project only adds two config files.

### 1. Install globally

```bash
python3 scripts/smartDevByDipali_installGlobal.py
```

Then paste `rules/dev-agent-pipeline-user.mdc` into **Cursor → Settings → Rules →
User Rules** and restart Cursor.

### 2. Onboard each project

```bash
python3 scripts/smartDevByDipali_onboardProject.py /path/to/your-app
```

Edit in that project:

- `.cursor/skills/project-checks.md` — lint, build, test commands
- `.cursor/rules/architecture.mdc` — naming, layering, conventions

Connect Jira + GitHub MCP in Cursor.

### 3. Run a ticket

```
/fix-ticket PROJ-123
```

Full guide: [docs/USAGE.md](docs/USAGE.md)

---

## What gets installed where

| Location | Contents |
|---|---|
| `~/.cursor/smart-developer/` | Full toolkit (agents, hooks, skills, scripts) |
| `~/.cursor/agents/` | Subagent entry files (`@triage`, `@dev`, …) |
| `~/.cursor/commands/` | `/fix-ticket` |
| `~/.cursor/hooks.json` | Hook enforcement |
| **Each project** | `project-checks.md`, `architecture.mdc`, `.dev-agent/` |

---

## Pipeline stages

| Stage | Subagent | Output |
|---|---|---|
| 1 | `@triage` | `01-triage.md` |
| 2 | `@context` | `02-context.md` |
| 3 | `@plan` | `03-plan.md` (**approval gate**) |
| 4 | `@dev` | code + `04-dev-notes.md` |
| 5 | `@test` | `05-tests.md` |
| 6 | `@review` | `06-review-notes.md` |
| 7 | `@docs-pr` | `07-docs.md`, `08-pr.md` (**PR gate**) |
| post-PR | `@pr-fix` | `09-review-log.md` |

---

## Development (this repo)

```bash
python3 scripts/smartDevByDipali_validatePipeline.py
python3 scripts/smartDevByDipali_mergeHooks.py
python3 scripts/smartDevByDipali_runTests.py
```

After changes, re-run `smartDevByDipali_installGlobal.py` on your machine to refresh `~/.cursor/`.

## Legacy: per-project copy

```bash
python3 scripts/smartDevByDipali_bootstrapProject.py /path/to/your/repo
```

Copies the full tree into the project. Use only for forks or air-gapped installs.

## Documentation

- [Usage guide (Plan A)](docs/USAGE.md)
- [Architecture](docs/architecture.md)
- [Pipeline artifacts](docs/pipeline-artifacts.md)
- [Orchestrator contract](agents/orchestrator.md)
