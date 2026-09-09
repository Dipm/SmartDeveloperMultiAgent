#!/usr/bin/env python3
"""Block @spec from writing application files; lean mode allows pipeline.json only."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "spec"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    if ph.tool_name(data) not in ph.WRITE_TOOLS:
        ph.allow()
        return
    path = ph.normalize_path(ph.path_of(data))
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.allow()
        return
    prefix = f".dev-agent/{ticket}/"
    if path.startswith(prefix):
        name = path.rsplit("/", 1)[-1]
        if name == ph.ARTIFACTS["manifest"]:
            ph.allow()
            return
        if not ph.use_lean_artifacts(ticket) and name in (
            ph.ARTIFACTS["triage"],
            ph.ARTIFACTS["context"],
            ph.ARTIFACTS["plan"],
        ):
            ph.allow()
            return
    ph.deny(
        f"Spec agent blocked: cannot write {path}. Update pipeline.json only (lean mode).",
        "Stop. Write only .dev-agent/{ticket}/pipeline.json unless --audit-trail.",
    )


if __name__ == "__main__":
    main()
