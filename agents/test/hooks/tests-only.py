#!/usr/bin/env python3
"""Test agent: write test files and 05-tests.md only; no git commit/push."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "test"
NOTES = ph.artifact_allowed_pattern(ph.ARTIFACTS["tests"])
MUTATING = re.compile(
    r"\b(git\s+(commit|push|reset|rebase|checkout|merge|add)|gh\s+pr\b)", re.I
)
SAFE = re.compile(
    r"^\s*(git\s+(log|show|diff|status)|rg\b|npm\b|pnpm\b|yarn\b|npx\b|pytest\b|"
    r"cargo\b|go\s+test\b|mvn\b|gradle\b|make\b|python\b|node\b)",
    re.I,
)


def allowed_test_path(ticket: str, path: str) -> bool:
    norm = ph.normalize_path(path)
    if NOTES.search(norm):
        return True
    if not ph.TESTISH_RE.search(norm):
        return False
    allowed = ph.plan_paths(ticket) | ph.dev_notes_paths(ticket)
    if not allowed:
        return True
    return ph.in_path_set(norm, allowed) or any(
        ph.TESTISH_RE.search(item) and (norm.endswith(item) or item in norm)
        for item in allowed
    )


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    name, path, cmd = ph.tool_name(data), ph.path_of(data), ph.command_of(data)
    ticket = ph.ticket_id_from(data)

    if cmd:
        if MUTATING.search(cmd):
            ph.deny("Test agent cannot commit or open a PR.", "Blocked mutating git.")
            return
        if SAFE.search(cmd):
            ph.allow()
            return

    if name in ph.WRITE_TOOLS or path:
        if path and ticket and allowed_test_path(ticket, path):
            ph.allow()
            return
        if path and not ticket and (NOTES.search(ph.normalize_path(path)) or ph.TESTISH_RE.search(path)):
            ph.allow()
            return
        if name in ph.WRITE_TOOLS:
            ph.deny(
                "Test agent may write test files listed in the plan/dev notes and "
                ".dev-agent/{ticket-id}/05-tests.md only.",
                "Blocked non-test write.",
            )
            return
    ph.allow()


if __name__ == "__main__":
    main()
