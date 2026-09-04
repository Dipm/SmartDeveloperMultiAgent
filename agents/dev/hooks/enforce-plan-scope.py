#!/usr/bin/env python3
"""Allow writes listed in 03-plan.md plus 04-dev-notes.md. Block mutating git."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "dev"


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    name = ph.tool_name(data)
    path = ph.path_of(data)
    cmd = ph.command_of(data)
    ticket = ph.ticket_id_from(data)

    if cmd:
        if ph.MUTATING_SHELL_RE.search(cmd):
            ph.deny(
                "Dev agent cannot commit, push, or open a PR. That is a later stage.",
                "Blocked mutating git / gh pr.",
            )
            return
        if ph.SAFE_SHELL_RE.search(cmd):
            ph.allow()
            return

    if name in ph.WRITE_TOOLS or path:
        norm = ph.normalize_path(path) if path else ""
        if path and ph.is_dev_agent_notes(norm):
            ph.allow()
            return
        if ticket:
            allowed = ph.plan_paths(ticket)
            if path and ph.in_path_set(norm, allowed):
                ph.allow()
                return
            if name in ph.WRITE_TOOLS and path:
                ph.deny(
                    f"Dev agent may not edit {path}; it is not listed in "
                    f".dev-agent/{ticket}/03-plan.md. Flag the extra file first.",
                    "Blocked out-of-plan write.",
                )
                return
        if name in ph.WRITE_TOOLS and path and not ticket:
            ph.deny(
                f"Dev agent blocked: cannot write {path} without a ticket id in context.",
                "Blocked write without ticket id.",
            )
            return

    ph.allow()


if __name__ == "__main__":
    main()
