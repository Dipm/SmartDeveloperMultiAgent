#!/usr/bin/env python3
"""Review agent: flag only. Write 06-review-notes.md; no code edits."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "review"
ALLOWED = ph.artifact_allowed_pattern(ph.ARTIFACTS["review"])
MUTATING = re.compile(r"\b(git\s+(commit|push|reset|add)|gh\s+pr\b)", re.I)
SAFE = re.compile(
    r"^\s*(git\s+(log|show|blame|diff|status|rev-parse)|rg\b|grep\b|ls\b|head\b|cat\b)",
    re.I,
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    name, path, cmd = ph.tool_name(data), ph.path_of(data), ph.command_of(data)

    if cmd:
        if MUTATING.search(cmd):
            ph.deny("Review agent cannot fix or publish. Flag only.", "Blocked mutating shell.")
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
                "Review agent may only write .dev-agent/{ticket-id}/06-review-notes.md. "
                "Do not fix code.",
                "Blocked review-time edit.",
            )
            return
    ph.allow()


if __name__ == "__main__":
    main()
