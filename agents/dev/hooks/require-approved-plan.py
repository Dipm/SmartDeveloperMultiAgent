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
        ph.allow()
        return

    plan = ph.artifact_path(ticket, ph.ARTIFACTS["plan"])
    if not plan.is_file() or plan.stat().st_size == 0:
        ph.deny(
            f"Dev agent blocked: {plan} is missing or empty. Run @plan and wait for approval.",
            f"Stop. Required input {plan} was not found.",
        )
        return

    if ph.plan_is_approved(ticket, data):
        ph.allow()
        return

    ph.deny(
        f"Dev agent blocked: {plan} exists but is not approved. "
        f"Need explicit go-ahead or .dev-agent/{ticket}/03-plan.approved.",
        "Stop. Do not implement an unapproved plan.",
    )


if __name__ == "__main__":
    main()
