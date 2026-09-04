#!/usr/bin/env python3
"""Deny @test start unless 03-plan.md and 04-dev-notes.md exist."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "test"
REQUIRED = (ph.ARTIFACTS["plan"], ph.ARTIFACTS["dev_notes"])


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.allow()
        return
    missing = ph.missing_artifacts(ticket, REQUIRED)
    if missing:
        ph.deny(
            "Test agent blocked: missing " + ", ".join(missing) + ". Run @dev first.",
            "Stop. Plan and dev notes required.",
        )
        return
    ph.allow()


if __name__ == "__main__":
    main()
