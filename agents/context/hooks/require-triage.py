#!/usr/bin/env python3
"""Deny @context start when triage stage is incomplete."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "context"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("context", "context")
        return
    missing = ph.missing_prerequisites(ticket, (ph.ARTIFACTS["triage"],))
    if missing:
        ph.deny(
            "Context agent blocked: triage not complete — " + ", ".join(missing),
            "Stop. Run @triage first.",
        )
        return
    ph.allow()


if __name__ == "__main__":
    main()
