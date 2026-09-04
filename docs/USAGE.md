# SmartDeveloper — Usage Guide (Plan A: global install)

SmartDeveloper agents, commands, hooks, and instructions live in **one global install**
on your machine. Each application project only adds **two small config files**.

---

## What “global install” means

| Term | Meaning |
|---|---|
| **Global** | Cursor user folder: `~/.cursor/` on your machine |
| **Not global** | Not a system package (not brew/apt); not copied into every app repo |

After install:

```
~/.cursor/
  smart-developer/     ← full toolkit (private, one copy)
  agents/              ← @triage, @dev, … (entry files with absolute paths)
  commands/            ← /fix-ticket
  hooks.json           ← enforcement (optional but recommended)

my-app/                ← your project
  .cursor/skills/project-checks.md
  .cursor/rules/architecture.mdc
  .dev-agent/PROJ-123/ ← ticket artifacts
```

---

## 1. Install globally (once per machine)

From this repo:

```bash
python3 scripts/smartDevByDipali_installGlobal.py
# or
./scripts/smartDevByDipali_installGlobal.sh
```

This copies the toolkit to `~/.cursor/smart-developer/` and registers agents/commands/hooks.

### Manual step (once)

Open `~/.cursor/smart-developer/rules/dev-agent-pipeline-user.mdc` and paste its
contents into **Cursor → Settings → Rules → User Rules**.

Restart Cursor. Confirm `@triage` appears in `@`-mentions and `/fix-ticket` in the
command palette.

### Update SmartDeveloper later

Pull latest in this repo, then re-run:

```bash
python3 scripts/smartDevByDipali_installGlobal.py
```

Every project on this machine picks up the change immediately.

---

## 2. Onboard a project (once per app)

```bash
python3 scripts/smartDevByDipali_onboardProject.py /path/to/my-app
# or from my-app:
python3 ~/.cursor/smart-developer/scripts/smartDevByDipali_onboardProject.py .
```

Creates (if missing):

- `.cursor/skills/project-checks.md` — **fill in real lint/build/test commands**
- `.cursor/rules/architecture.mdc` — **fill in project conventions**
- `.dev-agent/.gitignore`

Connect **Jira MCP** (`@triage`) and **GitHub MCP** (`@pr-fix`) in Cursor.

No agents, commands, or hooks are copied into the project.

---

## 3. Run a ticket

Open the **project** the ticket belongs to:

```
/fix-ticket PROJ-123
```

| Step | Agent | Your job |
|---|---|---|
| 1–2 | `@triage`, `@context` | Answer ambiguities |
| 3 | `@plan` | **Approve** `03-plan.md` before dev |
| 4–6 | `@dev`, `@test`, `@review` | Let review loop to `@dev` if needed (max 3) |
| 7 | `@docs-pr` | Review diff + `08-pr.md`; **you** open the PR |

Resume:

```
/fix-ticket PROJ-123 --from dev
```

PR comments (one at a time):

```
@pr-fix PROJ-123 trivial rename this variable
```

---

## 4. Verify before first real ticket

```bash
python3 scripts/smartDevByDipali_validatePipeline.py
python3 scripts/smartDevByDipali_runTests.py
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Agent missing in `@`-mentions | Re-run `smartDevByDipali_installGlobal.py`; restart Cursor |
| `/fix-ticket` not found | Check `~/.cursor/commands/fix-ticket.md` exists |
| Agent ignores pipeline gates | Paste `dev-agent-pipeline-user.mdc` into **User Rules** |
| Hook doesn't fire | Check `~/.cursor/hooks.json` is valid JSON |
| `@dev` can't run checks | Fill in `.cursor/skills/project-checks.md` for **this** project |
| Agent can't find instructions | Re-run `smartDevByDipali_installGlobal.py` (paths must point to `~/.cursor/smart-developer`) |

---

## Alternative: per-project copy (legacy)

`scripts/smartDevByDipali_bootstrapProject.py` copies the full tree into a project. Prefer global install
unless you need a fully self-contained fork.
