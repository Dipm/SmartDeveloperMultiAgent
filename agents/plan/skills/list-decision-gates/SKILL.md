---
name: list-decision-gates
description: List the 2-4 plan decisions the engineer must approve before @dev. Use when finishing the plan. Do not start implementation.
disable-model-invocation: true
---

# List decision gates

This is the highest-leverage gate — do not be brief.

List 2–4 decisions: approach trade-offs, scope calls, anything from
triage/context that changes the plan. Ask those explicitly.

If there is truly only one responsible approach and no scope ambiguity, say
that and still name the residual risk the engineer should accept.

Do not call `@dev`. Approval is the parent's human gate.
