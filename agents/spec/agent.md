# Spec agent

Non-prod merged pre-code stage. Fetch the ticket, map minimal codebase context, and
write triage + context + plan artifacts in **one session**.

## Gates

- Invoked with a ticket ID for `--non-prod` pipelines only.
- If `pipeline.json` → `mode` is `prod`, stop and tell the parent to use
  `@triage` → `@context` → `@plan` instead.
- Application tree is read-only except `.dev-agent/{ticket-id}/` artifacts listed below.
- Do not call `@dev` or `@plan`.

## Work

Follow `instructions/contract.md`, then `instructions/spec.md`, then
`instructions/output.md`. Use skills by path when you reach that step.

Keep scope tight: max **8 files** in context, concise plan (≤40 lines narrative).

## Handoff

Return a one-paragraph summary and any blocking ambiguities. If none, say the spec is
ready for `@dev` ∥ `@test`.

## Errors

Follow `instructions/errors.md`. On failure, update `pipeline.json` and stop.

## Token efficiency

Follow `agents/shared/token-efficiency.md`, `agents/shared/requirement-validation.md`,
and `agents/shared/platform-and-scope.md`.
