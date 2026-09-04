#!/usr/bin/env python3
"""Deny @docs-pr start unless prior artifacts exist and review is clear."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "docs-pr"
REQUIRED = (
    ph.ARTIFACTS["triage"],
    ph.ARTIFACTS["plan"],
    ph.ARTIFACTS["dev_notes"],
    ph.ARTIFACTS["tests"],
    ph.ARTIFACTS["review"],
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.allow()
        return

    missing = ph.missing_artifacts(ticket, REQUIRED)
    if missing:
        ph.deny(
            "Docs-PR agent blocked: missing required pipeline files: "
            + ", ".join(missing),
            "Stop. Run prior stages through @review first.",
        )
        return

    if ph.review_sends_back(ticket):
        review_path = ph.artifact_path(ticket, ph.ARTIFACTS["review"])
        ph.deny(
            f"Docs-PR agent blocked: {review_path} still sends work back to @dev. "
            "Resolve blocking/should-fix before drafting a PR.",
            "Stop. Unresolved review findings.",
        )
        return

    ph.allow()


if __name__ == "__main__":
    main()
