# Output

Append one block to `.dev-agent/{ticket-id}/09-review-log.md`. Create the file
if it does not exist. If it exists, do not replace prior entries.

```markdown
## {iso-date} — {comment-id or short hash of the comment}

### Comment
- quoted or linked

### Classification
- trivial | replan | disagree

### Action
- what changed, or the draft reply, or "waiting on engineer"

### Confirmation
- not needed | asked | granted
```
