# Hooks for `@dev`

These are **templates**. Cursor only loads project `.cursor/hooks.json`. Copy or
merge this fragment there if you want the guards enforced, not just documented.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-approved-plan.py` | Deny start when `03-plan.md` is missing or unapproved |
| `preToolUse` | `enforce-plan-scope.py` | Deny writes outside plan paths; always allow `04-dev-notes.md` |
| `beforeShellExecution` | `enforce-plan-scope.py` | Deny git commit/push/reset; allow checks and read-only git |

Scripts read JSON on stdin, write JSON on stdout, exit 0.

Make scripts executable after copy:

```bash
chmod +x agents/dev/hooks/*.py
```
