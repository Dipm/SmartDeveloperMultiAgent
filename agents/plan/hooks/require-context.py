#!/usr/bin/env python3
"""Deny @plan start unless 01-triage.md and 02-context.md exist."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "plan"
REQUIRED = (ph.ARTIFACTS["triage"], ph.ARTIFACTS["context"])


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("plan", "plan")
        return
    missing = ph.missing_prerequisites(ticket, REQUIRED)
    if missing:
        ph.deny(
            "Plan agent blocked: missing " + ", ".join(missing) + ". Run @triage and @context first.",
            "Stop. Prior stage files required.",
        )
        return
    ph.allow()


if __name__ == "__main__":
    main()
