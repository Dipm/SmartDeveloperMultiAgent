#!/usr/bin/env python3
"""Deny @review start unless required prior artifacts exist."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "review"
REQUIRED = (
    ph.ARTIFACTS["plan"],
    ph.ARTIFACTS["dev_notes"],
    ph.ARTIFACTS["tests"],
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("review", "review")
        return
    missing = ph.missing_prerequisites(ticket, REQUIRED)
    if missing:
        ph.deny(
            "Review agent blocked: missing " + ", ".join(missing) + ". Run @test first.",
            "Stop. Prior stage files required.",
        )
        return
    ph.allow()


if __name__ == "__main__":
    main()
