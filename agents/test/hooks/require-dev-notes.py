#!/usr/bin/env python3
"""Deny @test start unless plan exists; dev notes required only in prod sequential mode."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "test"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("test", "test")
        return

    missing = ph.missing_prerequisites(ticket, (ph.ARTIFACTS["plan"],))
    if missing:
        ph.deny(
            "Test agent blocked: missing " + ", ".join(missing) + ". Run @plan or @spec first.",
            "Stop. Plan required before @test.",
        )
        return

    if ph.is_prod(ticket):
        missing_notes = ph.missing_prerequisites(ticket, (ph.ARTIFACTS["dev_notes"],))
        if missing_notes:
            ph.deny(
                "Test agent blocked: missing " + ", ".join(missing_notes) + ". Run @dev first.",
                "Stop. Dev notes required in prod sequential mode.",
            )
            return

    ph.allow()


if __name__ == "__main__":
    main()
