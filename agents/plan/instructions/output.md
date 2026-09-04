# Output

Write `.dev-agent/{ticket-id}/03-plan.md` and update `pipeline.json` (create if
missing) with `stages.plan.status: "complete"`.

Use this schema for `03-plan.md`:

# Plan — {ticket-id}

## Approach
- how, in enough detail that `@dev` does not have to invent architecture

## Files to touch (in order)
- `path` — what changes and why

## Files to touch (machine-readable)

Include a fenced `paths` block listing every file `@dev` or `@test` may edit
(one path per line). Example:

    ```paths
    src/foo.ts
    src/foo.test.ts
    ```

## Edge cases
- cases the implementation must handle

## Risk / blast radius
- what else this can break

## Outside normal scope
- schema, new deps, breaking changes, extra design decisions
- (or "None.")

## Decisions for the engineer
1. ...
2. ...

The `paths` block is parsed by hooks. Keep it in sync with the narrative file list.
