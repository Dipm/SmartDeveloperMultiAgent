# Editing the triage agent package

- **`../triage.md`** — frontmatter + load order (`name: triage`).
- **`agent.md`** — identity and gates. No Jira field maps beyond the skill.
- **`instructions/`** — contract and `01-triage.md` schema.
- **`skills/`** — fetch vs classify; `disable-model-invocation: true`.
- **`hooks/`** — merge into project `.cursor/hooks.json`.

Do not pull codebase search into this agent (`@context` owns that).
Do not add Jira write operations. Keep it tracker-field agnostic except title,
description, AC, links, comments.
