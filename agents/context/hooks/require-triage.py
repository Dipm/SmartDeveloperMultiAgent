#!/usr/bin/env python3
"""Deny @context start when 01-triage.md is missing."""
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
        ph.allow()
        return
    triage = ph.artifact_path(ticket, ph.ARTIFACTS["triage"])
    if triage.is_file() and triage.stat().st_size > 0:
        ph.allow()
        return
    ph.deny(
        f"Context agent blocked: {triage} is missing or empty. Run @triage first.",
        f"Stop. Required input {triage} was not found.",
    )


if __name__ == "__main__":
    main()
