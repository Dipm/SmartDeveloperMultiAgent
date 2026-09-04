# Output

Write `.dev-agent/{ticket-id}/06-review-notes.md` and update `pipeline.json`:

- `stages.review.status`: `"complete"`
- `stages.review.verdict`: `"clean"` or `"send_back"`
- `stages.review.iteration`: increment from prior review (start at 1)

```markdown
# Review — {ticket-id}

## Verdict
- clean | send back to @dev

## Review iteration
- N

## Blocking
- (or "None.")

## Should-fix
- (or "None.")

## Nit
- (or "None. Not inventing nits.")

## Notes
- vs plan, tests, security, style — only if they affect the verdict
```

If Blocking or Should-fix is not empty, Verdict must be `send back to @dev`.

If `Review iteration` exceeds 3, state in Notes that the engineer should take over.
