#!/usr/bin/env python3
"""Deny @dev start unless 03-plan.md exists and looks approved."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "dev"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("dev", "dev")
        return

    if ph.use_lean_artifacts(ticket):
        missing = ph.missing_prerequisites(ticket, (ph.ARTIFACTS["plan"],))
        if missing:
            ph.deny(
                "Dev agent blocked: plan/spec not ready — " + ", ".join(missing),
                "Stop. Run @plan or @spec first.",
            )
            return
    else:
        plan = ph.artifact_path(ticket, ph.ARTIFACTS["plan"])
        if not plan.is_file() or plan.stat().st_size == 0:
            ph.deny(
                f"Dev agent blocked: {plan} is missing or empty. Run @plan first.",
                f"Stop. Required input {plan} was not found.",
            )
            return

    if ph.plan_is_approved(ticket, data):
        ph.allow()
        return

    ph.deny(
        f"Dev agent blocked: plan for {ticket} is not approved. "
        f"Need .dev-agent/{ticket}/03-plan.approved or completed plan stage.",
        "Stop. Do not implement an unapproved plan.",
    )


if __name__ == "__main__":
    main()
