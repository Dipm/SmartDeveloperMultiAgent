# Requirement validation

Before implementing, verify ticket **expected behavior** against the **current codebase**.
QA or Jira text may describe outdated, wrong, or ambiguous expectations.

## Mode default

If the user did not pass `--prod` / `--non-prod` and the ticket does not clearly
require production-grade handling (prod deploy, compliance, security incident,
explicit "production" / P0-prod labels), treat the run as **`non-prod`**. Only use
`--prod` when the user or ticket explicitly demands it.

## Quick validation (always — budget ≤3 min)

1. Read ticket expected behavior / acceptance criteria.
2. Locate the relevant code path (targeted search, ≤5 files).
3. Decide one of:
   - **Confirmed** — code matches ticket; proceed.
   - **Ticket wrong** — code already behaves correctly; QA/ticket misunderstanding.
   - **Code wrong** — ticket expectation matches product intent; fix code.
   - **Unclear** — not enough signal in ≤3 min.

Record the verdict in the stage artifact under `## Expected behavior validation`.

## Annotation (optional — do not block pipeline)

When validation is quick, add a short note in the artifact:

```markdown
## Expected behavior validation
- Ticket says: ...
- Code does: ... (file:line or path)
- Verdict: confirmed | ticket-wrong | code-wrong | unclear
- Notes: ...
```

If annotating Jira would help QA, mention it in the artifact — **do not** spend time
opening/editing Jira unless the user asked. Prefer artifact notes.

## When code looks correct or the issue may be out of scope

If validation suggests the client code is already correct, or the symptom points to
backend/API, test environment, QA repro, or network/proxy — follow
`agents/shared/platform-and-scope.md`. Do not proceed to `@dev` with a fabricated fix;
record findings and suggest concrete next checks for the engineer.

## When validation is time-consuming

Do **not** stall the pipeline. Instead:

1. Record `verdict: unclear` or partial findings in the artifact.
2. Add a **User verification guide** section with concrete steps for the engineer/QA
   to confirm expected vs actual behavior.
3. Proceed with the most likely correct fix, or a minimal safe change.
4. Document every assumption in `## Assumptions` (spec/plan/dev notes).

## Assumptions and review ask (mandatory when proceeding on unclear tickets)

In `04-dev-notes.md` (and PR draft summary), include:

```markdown
## Assumptions made
- ...

## Please review
- Confirm whether expected behavior is X (ticket) or Y (what code did).
- Steps to verify: ...
```

At the **PR gate**, the orchestrator must surface assumptions and ask the user to
review before opening the PR.

## Prod vs non-prod

| Signal | Mode |
|---|---|
| No flag, ticket silent on environment | `non-prod` |
| "staging", "dev", "QA", internal tool | `non-prod` |
| "production", "prod hotfix", compliance, security P0 | `prod` |
| User says `--prod` | `prod` |

When in doubt, **`non-prod`** and note the assumption in triage/spec.
