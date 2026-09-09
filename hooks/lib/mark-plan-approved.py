#!/usr/bin/env python3
"""Auto-approve plan when @plan or @spec completes with a valid artifact."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

PLAN_AGENTS = frozenset({"plan", "spec"})


def main() -> None:
    data = ph.load_event()
    agent = os.environ.get("AGENT", "").lower()
    if agent:
        ph.require_agent(data, agent)
    if agent not in PLAN_AGENTS:
        ph.allow()
        return
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.allow()
        return

    stage = "spec" if agent == "spec" else "plan"
    status = ph.stage_status(ticket, stage)
    if status != "complete":
        ph.allow()
        return

    if ph.use_lean_artifacts(ticket):
        if not ph.plan_paths(ticket):
            ph.allow()
            return
    else:
        plan = ph.artifact_path(ticket, ph.ARTIFACTS["plan"])
        if not plan.is_file() or plan.stat().st_size == 0:
            ph.allow()
            return

    ph.auto_approve_plan(ticket)
    ph.allow()


if __name__ == "__main__":
    main()
