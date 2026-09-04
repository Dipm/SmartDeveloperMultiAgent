# Editing the docs-pr agent package

Keep each primitive in its lane:

- **`../docs-pr.md`** — frontmatter + load order only. Cursor discovers the
  subagent from that file (`name: docs-pr`).
- **`agent.md`** — always-on prompt. Identity, gates, handoff. No PR templates.
- **`instructions/`** — stage contract and `07-docs.md` / `08-pr.md` schemas.
- **`skills/`** — step procedures. One concern per skill. Folder name must match
  `SKILL.md` `name`. Keep `disable-model-invocation: true`; the subagent loads
  them by path.
- **`hooks/`** — deterministic allow/deny. Consuming repos merge `hooks/hooks.json`
  into project `.cursor/hooks.json`.

Do not duplicate the output templates outside `instructions/output.md`.
Do not teach this agent to run `gh pr create`; that stays a human/parent step.
Do not add application-domain advice; this agent is repo-agnostic.
