# Hooks for `@review`

Merge into project `.cursor/hooks.json`.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-tests.py` | Need `03-plan`, `04-dev-notes`, `05-tests` |
| `preToolUse` | `flag-only.py` | Writes only `06-review-notes.md` |
| `beforeShellExecution` | `flag-only.py` | Read-only git |

```bash
chmod +x agents/review/hooks/*.py
```
