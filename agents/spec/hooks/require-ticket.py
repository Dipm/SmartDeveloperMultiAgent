#!/usr/bin/env python3
"""Deny @spec start without ticket id; block in prod mode."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "spec"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("spec", "spec")
        return
    if ph.is_prod(ticket):
        ph.deny(
            f"Spec agent blocked: pipeline mode is prod for {ticket}. "
            "Use @triage → @context → @plan instead.",
            "Stop. @spec is non-prod only.",
        )
        return
    ph.allow()


if __name__ == "__main__":
    main()
