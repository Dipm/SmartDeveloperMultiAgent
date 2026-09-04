#!/usr/bin/env python3
"""Deny @triage start without a ticket id."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "triage"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    if not ph.ticket_id_from(data):
        ph.deny(
            "Triage agent blocked: no ticket id. Invoke as @triage {ticket-id}.",
            "Stop. Ticket id required.",
        )
    ph.allow()


if __name__ == "__main__":
    main()
