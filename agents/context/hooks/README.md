# Hooks for `@context`

These are **templates**. Cursor only loads project `.cursor/hooks.json`. Copy or
merge this fragment there if you want the guards enforced, not just documented.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-triage.py` | Deny start when `01-triage.md` is missing for the ticket id in the prompt |
| `preToolUse` | `enforce-readonly.py` | Deny edits except `.dev-agent/**/02-context.md` |
| `beforeShellExecution` | `enforce-readonly.py` | Deny mutating shell; allow `git log` / `git show` / search |

Scripts read JSON on stdin, write JSON on stdout, exit 0. They fail open if the
payload cannot be parsed, except `require-triage.py` fails closed when it can
see a ticket id and the triage file is absent.

Make scripts executable after copy:

```bash
chmod +x agents/context/hooks/*.py
```
