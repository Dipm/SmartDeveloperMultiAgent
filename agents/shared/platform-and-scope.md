# Platform and scope boundaries

Agents work in the **current Cursor workspace** only. Tickets often span multiple
platforms or repos — scope must stay tight and escalations must be explicit.

## Multi-platform tickets (Android / iOS / web / etc.)

When a ticket mentions more than one platform or client repo:

1. **Detect the open project** from the workspace (Gradle/Android, Xcode/Swift,
   React Native monorepo subfolder, etc.).
2. **Limit research, planning, and fixes** to that open project unless the engineer
   explicitly expands scope.
3. **Record in the stage artifact** (or `pipeline.json` summary fields):
   - `active_platform` / `active_repo` — what you are working in now
   - `ticket_platforms_mentioned` — platforms named in Jira/ticket text
   - `out_of_scope_platforms` — platforms mentioned but not in this workspace
4. **Do not** silently clone, open, or edit other platform repos.
5. **Ask the engineer** before expanding:
   > This ticket mentions [platforms]. I'm working in [current repo/platform].
   > Should I also fix [other platform(s)]? If yes, please open that workspace or
   > share the repo path/branch.

If the engineer confirms another platform, collect repo info (path, branch, how it
relates to this ticket) and update the plan before `@dev` touches code there.

Pre-code stages (`@triage`, `@context`, `@plan`, `@spec`) should flag multi-platform
scope in open questions. `@dev` and `@pr-fix` must not cross repos without explicit
confirmation.

## Non-code root causes

The defect may not live in client code. Common out-of-scope causes:

| Area | Examples |
|---|---|
| Backend / API | Wrong payload, 4xx/5xx, stale cache, feature-flag server side |
| Environment | Staging vs prod config, bad test data, expired tokens |
| QA / process | Incorrect repro steps, wrong build, account state |
| Network / proxy | Charles/mitm/proxy logs, CDN, certificate pinning, VPN |
| Remote config | Firebase/LaunchDarkly flags, A/B buckets, kill switches |
| Third party | SDK outage, payment gateway, maps/analytics provider |

### When no plausible client defect is found

After a **targeted** search (same budget as requirement validation — do not burn
hours grep-ing):

1. **Do not** ship a speculative code change just to close the ticket.
2. Record verdict: `no_client_code_issue_found` (or `unclear` with findings) in the
   artifact / `pipeline.json`.
3. **Stop `@dev`** and tell the parent/engineer what to check next, for example:
   - API response body and status for the failing call (backend logs)
   - Proxy/network capture during repro
   - QA repro on a known-good build vs the reported build
   - Environment-specific config or test account setup
   - Whether backend or QA owns the next step
4. Pre-code stages may proceed with a **verification plan** instead of an
   implementation plan when code looks correct.

Use `error.code: user_input_needed` when the pipeline cannot proceed without
engineer/QA/backend confirmation.

## Handoff wording (template)

```markdown
## Scope note
- Working in: {repo / platform}
- Ticket also mentions: {other platforms} — not touched unless you confirm

## No code fix found
- Searched: {paths / areas}
- Client code appears: {correct / inconclusive}
- Suggested next checks: {backend logs / proxy / QA repro / env config}
- Out of agent scope: {what you cannot verify from this workspace}
```
