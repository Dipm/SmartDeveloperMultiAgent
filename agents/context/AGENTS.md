# Editing the context agent package

Keep each primitive in its lane:

- **`../context.md`** — frontmatter + load order only. Cursor discovers the
  subagent from that file (`name: context`).
- **`agent.md`** — always-on prompt. Identity, gates, handoff. No search recipes.
- **`instructions/`** — stage contract and output schema. Change these when the
  pipeline artifact changes.
- **`skills/`** — step procedures. One concern per skill. Folder name must match
  `SKILL.md` `name`. Keep `disable-model-invocation: true`; the subagent loads
  them by path.
- **`hooks/`** — deterministic allow/deny. No prose policy here; if it can be a
  script, it is a hook. Consuming repos merge `hooks/hooks.json` into project
  `.cursor/hooks.json`.

Do not duplicate the `02-context.md` template in more than `instructions/output.md`.
Do not add application-domain advice; this agent is repo-agnostic.
