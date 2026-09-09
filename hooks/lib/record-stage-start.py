#!/usr/bin/env python3
"""Record stage start in pipeline.json on subagentStart."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT_STAGE = {
    "triage": "triage",
    "context": "context",
    "plan": "plan",
    "spec": "spec",
    "dev": "dev",
    "test": "test",
    "review": "review",
    "docs-pr": "docs_pr",
    "pr-draft": "pr_draft",
    "pr-fix": "pr_fix",
}


def main() -> None:
    data = ph.load_event()
    agent = os.environ.get("AGENT", "").lower()
    if agent:
        ph.require_agent(data, agent)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.allow()
        return
    stage = AGENT_STAGE.get(agent)
    if not stage:
        ph.allow()
        return
    ph.mark_stage_running(ticket, stage)
    ph.allow()


if __name__ == "__main__":
    main()
