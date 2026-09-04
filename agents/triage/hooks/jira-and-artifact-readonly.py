#!/usr/bin/env python3
"""Triage: write only 01-triage.md; Jira and git stay read-only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "triage"
ALLOWED = ph.artifact_allowed_pattern(ph.ARTIFACTS["triage"])
MUTATING = re.compile(r"\b(git\s+(commit|push|reset|add)|gh\s+pr\b)", re.I)
SAFE = re.compile(
    r"^\s*(git\s+(log|show|diff|status)|rg\b|grep\b|ls\b|head\b|cat\b)", re.I
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    blob = ph.blob(data)
    name, path, cmd = ph.tool_name(data), ph.path_of(data), ph.command_of(data)

    if ph.JIRA_WRITE_RE.search(blob) or ph.JIRA_WRITE_RE.search(name):
        ph.deny("Triage agent cannot edit Jira. Read the ticket only.", "Blocked Jira write.")
        return

    if cmd:
        if MUTATING.search(cmd):
            ph.deny("Triage agent cannot commit or open a PR.", "Blocked mutating git.")
            return
        if SAFE.search(cmd):
            ph.allow()
            return

    if name in ph.WRITE_TOOLS or path:
        if path and ALLOWED.search(ph.normalize_path(path)):
            ph.allow()
            return
        if name in ph.WRITE_TOOLS:
            ph.deny(
                "Triage agent may only write .dev-agent/{ticket-id}/01-triage.md.",
                "Blocked extra write.",
            )
            return
    ph.allow()


if __name__ == "__main__":
    main()
