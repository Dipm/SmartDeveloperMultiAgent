# Hooks for `@docs-pr`

These are **templates**. Cursor only loads project `.cursor/hooks.json`. Copy or
merge this fragment there if you want the guards enforced, not just documented.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-review-clear.py` | Deny if required pipeline files are missing or review still sends work to `@dev` |
| `preToolUse` | `block-open-pr.py` | Allow writes only to `07-docs.md` and `08-pr.md` |
| `beforeShellExecution` | `block-open-pr.py` | Deny `gh pr create` / `git push`; allow read-only git |

Scripts read JSON on stdin, write JSON on stdout, exit 0.

```bash
chmod +x agents/docs-pr/hooks/*.py
```
