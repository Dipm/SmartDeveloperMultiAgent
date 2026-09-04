#!/usr/bin/env python3
"""Deny @pr-fix if ticket id missing or the prompt looks like a comment batch."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "pr-fix"
CLASSIFICATION = re.compile(
    r"\b(pr-fix|@pr-fix)\s+\S+\s+(trivial|disagree|replan)\b",
    re.I,
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    blob = ph.blob(data)

    if not ph.ticket_id_from(data):
        ph.deny(
            "PR-fix agent blocked: no ticket id. "
            "Invoke as @pr-fix {ticket-id} trivial|disagree|replan.",
            "Stop. Ticket id required.",
        )
        return

    if ph.BATCH_COMMENT_RE.search(blob):
        ph.deny(
            "PR-fix agent blocked: looks like multiple comments. Invoke once per comment.",
            "Stop. No batching.",
        )
        return

    if not CLASSIFICATION.search(blob):
        ph.deny(
            "PR-fix agent blocked: missing classification prefix. "
            "Invoke as @pr-fix {ticket-id} trivial|disagree|replan.",
            "Stop. Add classification prefix before the comment.",
        )
        return

    ph.allow()


if __name__ == "__main__":
    main()
