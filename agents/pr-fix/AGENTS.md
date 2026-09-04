# Editing the pr-fix agent package

- **`../pr-fix.md`** — frontmatter + load order (`name: pr-fix`).
- **`agent.md`** — identity and gates. No GitHub reply templates beyond schema.
- **`instructions/`** — contract and `09-review-log.md` append schema.
- **`skills/`** — one concern per skill; `disable-model-invocation: true`.
- **`hooks/`** — merge into project `.cursor/hooks.json`.

Never teach this agent to batch comments. Keep the log append-only.
Keep it repo-agnostic.
