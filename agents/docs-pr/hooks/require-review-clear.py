#!/usr/bin/env python3
"""Deny @docs-pr start unless prior artifacts exist and review is clear (prod only)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "docs-pr"
REQUIRED_PROD = (
    ph.ARTIFACTS["triage"],
    ph.ARTIFACTS["plan"],
    ph.ARTIFACTS["dev_notes"],
    ph.ARTIFACTS["tests"],
    ph.ARTIFACTS["review"],
)
REQUIRED_NON_PROD = (
    ph.ARTIFACTS["plan"],
    ph.ARTIFACTS["dev_notes"],
    ph.ARTIFACTS["tests"],
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket:
        ph.deny_missing_ticket("docs-pr", "docs-pr")
        return

    required = REQUIRED_NON_PROD if ph.is_non_prod(ticket) else REQUIRED_PROD
    missing = ph.missing_prerequisites(ticket, required)
    if missing:
        ph.deny(
            "Docs-PR agent blocked: missing required pipeline files: "
            + ", ".join(missing),
            "Stop. Run prior stages first.",
        )
        return

    if ph.is_prod(ticket) and ph.review_sends_back(ticket, blocking_only=True):
        review_path = ph.artifact_path(ticket, ph.ARTIFACTS["review"])
        ph.deny(
            f"Docs-PR agent blocked: {review_path} has blocking findings. "
            "Resolve blocking items before drafting docs.",
            "Stop. Unresolved blocking review findings.",
        )
        return

    ph.allow()


if __name__ == "__main__":
    main()
