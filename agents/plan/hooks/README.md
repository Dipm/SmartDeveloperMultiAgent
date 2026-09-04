# Hooks for `@plan`

Merge into project `.cursor/hooks.json`.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-context.py` | Deny if `01-triage.md` or `02-context.md` missing |
| `preToolUse` | `block-implementation.py` | Writes only `03-plan.md` |
| `beforeShellExecution` | `block-implementation.py` | No mutating git |

```bash
chmod +x agents/plan/hooks/*.py
```
