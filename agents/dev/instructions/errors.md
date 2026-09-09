# Dev errors

See `agents/shared/error-handling.md`.

| Failure | Code | Suggestion |
|---|---|---|
| Plan missing/unapproved | `missing_prerequisite` | Approve plan; create `03-plan.approved` |
| Out-of-plan file edit blocked | `hook_blocked` | Update plan first or flag deviation |
| Checks fail in-plan | `validation` | Fix in plan files; record in `04-dev-notes.md` |
| Checks fail out-of-scope | `user_input_needed` | Ask engineer if fix is in scope |
| Cursor crash | `subagent_crash` | `retry dev` |
