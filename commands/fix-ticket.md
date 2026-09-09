Fix the Jira ticket with ID $ARGUMENTS end to end using the pipeline below.

## Options

- **Mode:** `/fix-ticket {ticket-id}` defaults to **`--non-prod`**. Add `--prod` only when
  the user or ticket explicitly requires production-grade handling (prod deploy,
  compliance, security incident, or clear "production" / P0-prod labels).
  - **`--non-prod` (default):** Fast path — `@spec` → dev ∥ test → docs ∥ pr.
  - **`--prod`:** Full pipeline — triage → context → plan → dev ∥ test → review → docs ∥ pr.
- **Resume:** `/fix-ticket {ticket-id} --from {stage} [--prod|--non-prod]` — skip earlier
  stages when artifacts already exist. Stages with `status: failed` in `pipeline.json`
  must be retried before resuming past them.

On first run, write `pipeline.json` with `"mode"`, `"lean_artifacts": true` (default), and stage entries.

- **`--audit-trail`:** also write numbered `.md` files (`01-triage.md` …) for compliance.
  Default is **lean** — state lives in `pipeline.json` only; no per-stage markdown logs.

## Mode selection

**Default is `non-prod`.** Use `--prod` only when explicitly requested or clearly
required by the ticket. If ambiguous, set `"mode": "non-prod"` in `pipeline.json`
and note the assumption in triage/spec.

## Requirement validation

Load `agents/shared/lean-artifacts.md` — **do not create numbered .md files** unless `--audit-trail`.
Load `agents/shared/requirement-validation.md`. Before implementing:

1. Compare ticket **expected behavior** to the **current codebase** (quick check, ≤3 min).
2. Flag QA/ticket misunderstandings vs real code bugs in the triage/spec artifact.
3. Annotate requirements in the artifact when cheap; **do not block** on long analysis.
4. If validation is inconclusive, add a **User verification guide** for the engineer/QA,
   proceed on reasonable assumptions, and document them in dev notes.
5. At the **PR gate**, list assumptions and what was fixed based on them — **ask the user to review**.

## Platform and scope

Load `agents/shared/platform-and-scope.md`.

- Multi-platform tickets (Android/iOS, etc.): fix only the **open workspace**; ask before
  other repos and collect path/branch info.
- If no client-code defect is found, escalate (backend logs, proxy capture, QA repro, env
  config) — do not force a speculative code change.


## Orchestration rules (speed-first)

**Chain stages automatically.** Do not stop between stages unless:

1. A subagent raises **open questions** that block progress, or
2. A subagent **fails** (error card + wait for recovery), or
3. The pipeline reaches the **PR gate** (see below).

The only required human gate is **before opening a PR**. After `@docs-pr` / `@pr-draft`
finish, present the PR draft (`08-pr.md`) and **STOP** until the engineer confirms
they want to open/push the PR.

Plan approval is **automatic** when `@plan` or `@spec` completes successfully
(sidecar `03-plan.approved` is written by hooks). Do not wait for manual plan sign-off.

### Parallel waves

Launch subagents in the **same message** when a wave lists multiple agents:

| Wave | `--prod` | `--non-prod` |
|---|---|---|
| Pre-code | `@triage` → `@context` → `@plan` (sequential) | `@spec` |
| Implement | `@dev` **and** `@test` in parallel | `@dev` **and** `@test` in parallel |
| Review | `@review` (sequential) | *(skipped)* |
| Ship docs | `@docs-pr` **and** `@pr-draft` in parallel | `@docs-pr` **and** `@pr-draft` in parallel |

**Dev ∥ test:** `@dev` owns production paths from the plan `paths` block; `@test` owns
test paths only. Both may start together — `@test` reads `03-plan.md`, not `04-dev-notes.md`.

**Docs ∥ PR:** `@docs-pr` writes only `07-docs.md`. `@pr-draft` writes only `08-pr.md`.
Both read the same prior artifacts. Wait for both before the PR gate.

### Failure handling

If a subagent stops with an error:

1. Read `.dev-agent/{ticket-id}/pipeline.json` and partial artifacts.
2. Present a brief **error card** (what happened, impact, suggested fixes).
3. **Stop.** Wait for the user to confirm a recovery option before retrying or continuing.

Recovery options: `retry {stage}`, `retry {stage} with pasted body`,
`/fix-ticket {id} --from {stage}`, or `abort`.

See `agents/shared/error-handling.md` for the full contract.

### Progress and timeout

- Warn the user at **5 minutes** if a subagent is still running.
- At **15 minutes**, treat the stage as timed out, record `error.code: timeout` in
  `pipeline.json`, and present the error card. Do not auto-retry.

If `@review` sends work back to `@dev` more than **3 times** for the same ticket,
stop the pipeline and ask the engineer to take over manually.

## `--prod` pipeline

1. `@triage`
2. `@context`
3. `@plan` — auto-approved on success; chain to dev immediately
4. `@dev` ∥ `@test` — parallel wave
5. `@review` — **blocking** findings loop to `@dev`; should-fix notes go in PR only
6. `@docs-pr` ∥ `@pr-draft` — parallel wave
7. **PR gate** — present `08-pr.md`; engineer opens PR manually

## `--non-prod` pipeline

1. `@spec` — writes triage + context + plan artifacts in one pass; auto-approved
2. `@dev` ∥ `@test` — parallel wave
3. `@docs-pr` ∥ `@pr-draft` — parallel wave (no `@review`)
4. **PR gate** — present `08-pr.md`; engineer opens PR manually

For PR comments after this point, invoke `@pr-fix` once per comment with a
classification prefix: `@pr-fix {ticket-id} trivial|disagree|replan` — not in a batch.

Load `agents/orchestrator.md` for resume logic and gate checks.
