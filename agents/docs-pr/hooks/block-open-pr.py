#!/usr/bin/env python3
"""Allow only 07-docs.md and 08-pr.md writes. Block opening or pushing a PR."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "docs-pr"
ALLOWED_WRITE = re.compile(
    rf"(?:^|/)\.dev-agent/[^/]+/({re.escape(ph.ARTIFACTS['docs'])}|"
    rf"{re.escape(ph.ARTIFACTS['pr'])})$"
)
SAFE_SHELL = re.compile(
    r"^\s*(git\s+(log|show|blame|diff|status|rev-parse|branch)|rg\b|grep\b|"
    r"ls\b|head\b|cat\b|gh\s+(pr\s+view|issue\s+view))\b",
    re.I,
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    name = ph.tool_name(data)
    path = ph.path_of(data)
    cmd = ph.command_of(data)

    if cmd:
        if ph.OPEN_PR_RE.search(cmd):
            ph.deny(
                "Docs-PR agent must not open or push a PR. Draft 08-pr.md only. "
                "The parent waits for human go-ahead before anyone opens it.",
                "Blocked gh pr create / git push.",
            )
            return
        if SAFE_SHELL.search(cmd):
            ph.allow()
            return

    if name in ph.WRITE_TOOLS or path:
        if path and ALLOWED_WRITE.search(ph.normalize_path(path)):
            ph.allow()
            return
        if name in ph.WRITE_TOOLS:
            ph.deny(
                "Docs-PR agent may only write .dev-agent/{ticket-id}/07-docs.md "
                "and 08-pr.md. Application code is out of scope.",
                "Blocked write outside docs/PR drafts.",
            )
            return

    ph.allow()


if __name__ == "__main__":
    main()
