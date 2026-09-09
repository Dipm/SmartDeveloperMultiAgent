# Implement

1. Confirm gates in `contract.md`. If any fail, write nothing and report to parent.

   Load `agents/shared/platform-and-scope.md`. If the ticket spans platforms, confirm
   you are fixing the open project only. If no client-code issue is found after targeted
   search, stop and escalate per that doc — do not implement a guess.

2. Load `skills/implement-from-plan/SKILL.md`. Implement strictly according to
   the plan: files, approach, order of changes. Do not "improve" adjacent code.

3. If the plan is wrong in a way that blocks the ticket, stop. Do not invent a
   new approach. Ask the parent; `@plan` is a separate agent.

4. After implementing, load `skills/run-project-checks/SKILL.md`. Run project
   checks per `.cursor/skills/project-checks.md` (lint, typecheck, build) and
   fix issues before finishing. Prefer fixes that stay inside the plan's files.

5. Load `skills/record-deviations/SKILL.md`. Write `04-dev-notes.md` even when
   there were no deviations (say so explicitly).
