# Editing the plan agent package

- **`../plan.md`** — frontmatter + load order (`name: plan`).
- **`agent.md`** — identity and gates. No file-by-file recipes.
- **`instructions/`** — contract and `03-plan.md` schema.
- **`skills/`** — one concern per skill; `disable-model-invocation: true`.
- **`hooks/`** — merge `hooks/hooks.json` into project `.cursor/hooks.json`.

Do not duplicate the plan template outside `instructions/output.md`.
Do not let this agent call `@dev`. Keep it repo-agnostic.
