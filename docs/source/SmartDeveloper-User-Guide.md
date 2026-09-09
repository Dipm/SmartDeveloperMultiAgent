# SmartDeveloper — User Guide

**A simple guide for anyone using SmartDeveloper with Cursor to fix Jira tickets.**

No coding background required for setup — just follow the steps.

---

## What is SmartDeveloper?

SmartDeveloper is a **helper workflow inside Cursor** that walks you through fixing a Jira ticket step by step:

1. Understand the ticket  
2. Explore the codebase  
3. Plan the fix (you approve before any code changes)  
4. Write the code  
5. Add tests  
6. Review the work  
7. Prepare docs and a PR draft (you open the PR when ready)

Think of it as a **checklist with smart assistants** — each step is handled by a different helper (`@triage`, `@plan`, `@dev`, and so on).

---

## What you need before starting

- **Cursor** installed on your computer ([cursor.com](https://cursor.com))
- **Python 3** installed (Mac and Windows usually have it; see below if not)
- **This SmartDeveloper folder** cloned or downloaded on your machine
- **Jira** access (for reading tickets)
- **GitHub** access (for PR comments later — optional at first)

---

## Important words (simple)

| Word | Meaning |
|------|---------|
| **Global install** | Put SmartDeveloper in Cursor’s personal folder on your computer (`~/.cursor`). It works in **every project** — you don’t copy files into each app. |
| **Onboard a project** | Tell SmartDeveloper how **one app** runs tests and lint (two small config files). |
| **Ticket** | A Jira issue like `PROJ-123`. |
| **`/fix-ticket`** | A command you type in Cursor chat to start the workflow. |

---

## Part 1 — One-time setup on your computer

Do this **once per laptop/desktop**, not per project.

### Step 1 — Get the SmartDeveloper folder

Clone or copy this repository to a place you’ll remember, for example:

- **Mac:** `~/workspace/SmartDeveloperMultiAgent`
- **Windows:** `C:\Users\YourName\workspace\SmartDeveloperMultiAgent`

### Step 2 — Open Terminal and run the installer

#### On Mac

1. Open **Terminal** (Spotlight → type “Terminal”).
2. Go to the folder (change the path if yours is different):

   ```bash
   cd ~/workspace/CLI/SmartDeveloperMultiAgent
   ```

3. Run:

   ```bash
   python3 scripts/smartDevByDipali_installGlobal.py
   ```

   Or:

   ```bash
   ./scripts/smartDevByDipali_installGlobal.sh
   ```

#### On Windows

1. Open **PowerShell** or **Command Prompt**.
2. Go to the folder:

   ```powershell
   cd C:\Users\YourName\workspace\SmartDeveloperMultiAgent
   ```

3. Run:

   ```powershell
   python scripts\smartDevByDipali_installGlobal.py
   ```

   If `python` doesn’t work, try `py`:

   ```powershell
   py scripts\smartDevByDipali_installGlobal.py
   ```

**Don’t have Python?**

- **Mac:** Install from [python.org](https://www.python.org/downloads/) or run `brew install python3`
- **Windows:** Install from [python.org](https://www.python.org/downloads/) — check **“Add Python to PATH”** during install

### Step 3 — Add one rule in Cursor (manual, one time)

1. Open the file (after install):

   - **Mac:** `~/.cursor/smart-developer/rules/dev-agent-pipeline-user.mdc`
   - **Windows:** `C:\Users\YourName\.cursor\smart-developer\rules\dev-agent-pipeline-user.mdc`

2. Copy **all** the text inside.
3. In Cursor: **Settings → Rules → User Rules** → paste → save.

### Step 4 — Restart Cursor

Close Cursor completely and open it again.

### Step 5 — Check it worked

1. Open **any** project in Cursor.
2. In chat, type `@` — you should see helpers like `@triage`, `@dev`, `@plan`.
3. Open the command palette — you should see **`/fix-ticket`**.

If something is missing, re-run Step 2 and restart Cursor again.

---

## Part 2 — Setup each project (once per app)

Every app you work on needs **two small config files**. No SmartDeveloper code is copied into the app.

### Step 1 — Run onboard script

#### Mac

```bash
python3 scripts/smartDevByDipali_onboardProject.py /path/to/your-app
```

Example:

```bash
python3 ~/.cursor/smart-developer/scripts/smartDevByDipali_onboardProject.py ~/projects/my-shopping-app
```

#### Windows

```powershell
python scripts\smartDevByDipali_onboardProject.py C:\Users\YourName\projects\my-shopping-app
```

(Use the copy under your SmartDeveloper folder, or the one in `%USERPROFILE%\.cursor\smart-developer\scripts\` after global install.)

### Step 2 — Fill in test commands

Open in your project:

`.cursor/skills/project-checks.md`

Replace the placeholders with **real commands** for that app, for example:

```markdown
- **Lint:** `npm run lint`
- **Type-check / build:** `npm run build`
- **Full test suite:** `npm test`
- **Single test file:** `npm test -- {path}`
```

Use whatever that project actually uses (`gradle`, `pytest`, etc.).

### Step 3 — Fill in project rules

Open:

`.cursor/rules/architecture.mdc`

Describe in plain language:

- Where code lives (folders)
- Naming style
- Things agents should not change without asking

### Step 4 — Connect Jira and GitHub in Cursor

In Cursor settings, connect:

- **Jira** — so `@triage` can read tickets  
- **GitHub** — so `@pr-fix` can help with PR comments  

(Ask your team lead if you need MCP connection details.)

**Done.** This project is ready.

---

## Part 3 — Fix a ticket (daily work)

### Step 1 — Open the correct project

Open the app repo that the ticket belongs to — **not** the SmartDeveloper folder.

### Step 2 — Start the workflow

In Cursor chat:

```
/fix-ticket PROJ-123
```

(Replace `PROJ-123` with your real ticket ID.)

### Step 3 — Follow the stages

The assistant will go through stages **one at a time**. After each stage, **read the summary**, answer any questions, and say **“go ahead”** or **“approved”** before the next step.

| Stage | What happens | What you do |
|-------|----------------|-------------|
| **Triage** | Reads the Jira ticket | Answer unclear points |
| **Context** | Finds relevant code | Answer if something looks wrong |
| **Plan** | Writes a plan file | **Read carefully and approve** — don’t skip |
| **Dev** | Writes code | Wait; only step in if asked |
| **Test** | Runs/adds tests | Wait |
| **Review** | Checks quality | If issues found, it may loop back to Dev |
| **Docs / PR** | Drafts PR text | **You** review and open the PR |

### Step 4 — Approve the plan (important)

When `@plan` finishes, you’ll see `03-plan.md` under `.dev-agent/PROJ-123/` in your project.

**Do not rush this.** If the approach is wrong, say so before approving. Only say **“approved”** or **“go ahead with dev”** when you agree.

### Step 5 — Open the PR yourself

`@docs-pr` creates a **draft** — it does **not** open the PR for you. Review the real code diff, then open the PR in GitHub when you’re happy.

### Step 6 — PR comments (later)

For **each** review comment, run separately:

```
@pr-fix PROJ-123 trivial please rename this variable
```

Use one of: `trivial`, `disagree`, or `replan` after the ticket ID.

### Resume if you stopped halfway

```
/fix-ticket PROJ-123 --from dev
```

Starts again from the `dev` stage if earlier files already exist.

---

## Where ticket files are saved

Inside your **project** (not in SmartDeveloper):

```
.dev-agent/PROJ-123/
  01-triage.md
  02-context.md
  03-plan.md
  ...
```

These are notes from each stage. You can commit them for history or add `.dev-agent/` to `.gitignore` if your team prefers.

---

## Updating SmartDeveloper

When the team releases a new version:

1. Pull latest in the SmartDeveloper repo (or get the new zip).
2. Run the global install again:

   **Mac:**
   ```bash
   python3 scripts/smartDevByDipali_installGlobal.py
   ```

   **Windows:**
   ```powershell
   python scripts\smartDevByDipali_installGlobal.py
   ```

3. Restart Cursor.

All your projects pick up the update. You **don’t** need to re-onboard each project unless templates changed.

---

## Script names (for your reference)

All setup scripts use a unique name so they don’t clash with other tools:

| Script | What it does |
|--------|----------------|
| `smartDevByDipali_installGlobal.py` | Install once on your computer |
| `smartDevByDipali_onboardProject.py` | Setup one app project |
| `smartDevByDipali_mergeHooks.py` | Used internally when installing |
| `smartDevByDipali_validatePipeline.py` | Check the toolkit is healthy |
| `smartDevByDipali_runTests.py` | Run automated checks (developers) |
| `smartDevByDipali_bootstrapProject.py` | Old full-copy install (avoid unless told) |

---

## Troubleshooting

| Problem | Try this |
|---------|----------|
| `@triage` doesn’t appear | Re-run `smartDevByDipali_installGlobal.py`, restart Cursor |
| `/fix-ticket` not found | Same as above |
| Agent ignores steps | Paste the user rule again (Part 1, Step 3) |
| Tests fail in Dev stage | Fix `project-checks.md` for **this** project |
| “Python not found” (Windows) | Reinstall Python with “Add to PATH”, or use `py` instead of `python` |


## Pipeline error recovery

When a subagent fails or times out, the orchestrator shows a brief error card:

- **What happened** — plain-language summary
- **Impact** — what is blocked
- **Suggested fixes** — numbered recovery options

Reply with an option number (or `abort`) before the pipeline continues.

| Symptom | Likely cause | Recovery |
|---|---|---|
| Jira MCP auth error | Token expired | Re-authenticate MCP; `retry triage` |
| Stage timed out (15 min) | Large repo / slow network | `retry {stage}` or narrow scope |
| Hook blocked | Out-of-scope edit | Read hook message; fix artifact/scope |
| Review loop limit | 3+ send-backs to @dev | Engineer takes over manually |

See `agents/shared/error-handling.md` for the full contract.

| Permission error on Mac | Don’t use `sudo` — install runs in your home folder |

---

## Quick checklist

**Once on your machine:**
- [ ] Ran `smartDevByDipali_installGlobal.py`
- [ ] Pasted user rule in Cursor Settings
- [ ] Restarted Cursor
- [ ] See `@triage` and `/fix-ticket`

**Once per project:**
- [ ] Ran `smartDevByDipali_onboardProject.py`
- [ ] Filled `project-checks.md`
- [ ] Filled `architecture.mdc`
- [ ] Jira MCP connected

**Per ticket:**
- [ ] `/fix-ticket TICKET-ID`
- [ ] Approved the plan
- [ ] Reviewed PR draft before opening PR

---

*SmartDeveloper by Dipali — helper workflow for Cursor. For technical details, see `docs/architecture.md`.*
