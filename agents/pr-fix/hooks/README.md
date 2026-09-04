# Hooks for `@pr-fix`

Merge into project `.cursor/hooks.json`.

| Event | Script | Effect |
|---|---|---|
| `subagentStart` | `require-single-comment.py` | Deny batches / missing ticket |
| `preToolUse` | `append-only-log.py` | Do not overwrite existing `09-review-log.md` |
| `beforeShellExecution` | `append-only-log.py` | No `git push` / `gh pr merge` |

```bash
chmod +x agents/pr-fix/hooks/*.py
```
