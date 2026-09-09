#!/usr/bin/env python3
"""Deny @dev start when review loop limit (3) is reached."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "dev"
MAX_ITERATIONS = 3


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket(AGENT, "dev")
        return

    if ph.review_iteration(ticket) >= MAX_ITERATIONS:
        ph.deny(
            f"Dev agent blocked: review loop limit ({MAX_ITERATIONS}) reached for {ticket}. "
            "Engineer must take over manually.",
            "Stop. Review loop limit exceeded. Escalate to engineer.",
        )
        return
    ph.allow()


if __name__ == "__main__":
    main()
