# Editing the review agent package

- **`../review.md`** — frontmatter + load order (`name: review`).
- **`agent.md`** — identity and gates. Reviewer stance lives here.
- **`instructions/`** — checklist and `06-review-notes.md` schema.
- **`skills/`** — inspect vs rank; `disable-model-invocation: true`.
- **`hooks/`** — merge into project `.cursor/hooks.json`.

Do not add auto-fix guidance. Keep findings ranked blocking / should-fix / nit.
Keep it repo-agnostic; style comes from `.cursor/rules/architecture.mdc`.
