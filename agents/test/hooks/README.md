# Hooks for `@test`

Merge into project `.cursor/hooks.json`.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-dev-notes.py` | Need `03-plan.md` and `04-dev-notes.md` |
| `preToolUse` | `tests-only.py` | Writes: test files + `05-tests.md` |
| `beforeShellExecution` | `tests-only.py` | No commit/push; allow test runners |

```bash
chmod +x agents/test/hooks/*.py
```
