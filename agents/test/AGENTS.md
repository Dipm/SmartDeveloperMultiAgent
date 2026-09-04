# Editing the test agent package

- **`../test.md`** — frontmatter + load order (`name: test`).
- **`agent.md`** — identity and gates. No project-specific commands.
- **`instructions/`** — contract and `05-tests.md` schema.
- **`skills/`** — write vs run vs log; `disable-model-invocation: true`.
- **`hooks/`** — merge into project `.cursor/hooks.json`.

Commands live in `.cursor/skills/project-checks.md` (see
`skills/project-checks.md.template`). Do not guess `npm test`.
Keep it repo-agnostic.
