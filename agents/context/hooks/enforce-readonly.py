#!/usr/bin/env python3
"""Allow read-only research. Permit writing only 02-context.md."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "context"
ALLOWED_WRITE = ph.artifact_allowed_pattern(ph.ARTIFACTS["context"])
MUTATING_SHELL = re.compile(
    r"\b(git\s+(commit|push|reset|rebase|checkout|merge|add|rm|mv)|"
    r"rm\s+|mv\s+|mkdir\s+|chmod\s+|npm\s+install|pnpm\s+(add|remove)|"
    r"yarn\s+add)\b",
    re.I,
)
SAFE_SHELL = re.compile(
    r"^\s*(git\s+(log|show|blame|diff|status|rev-parse)|rg\b|grep\b|find\b|"
    r"ls\b|head\b|cat\b)",
    re.I,
)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    name = ph.tool_name(data)
    path = ph.path_of(data)
    cmd = ph.command_of(data)

    if name in ph.WRITE_TOOLS or path:
        if path and ALLOWED_WRITE.search(ph.normalize_path(path)):
            ph.allow()
            return
        if name in ph.WRITE_TOOLS or path:
            ph.deny(
                "Context agent may not edit application files. Only "
                ".dev-agent/{ticket-id}/02-context.md is allowed.",
                "Blocked write: stay read-only except 02-context.md.",
            )
            return

    if cmd:
        if SAFE_SHELL.search(cmd) and not MUTATING_SHELL.search(cmd):
            ph.allow()
            return
        if MUTATING_SHELL.search(cmd):
            ph.deny(
                "Context agent cannot run mutating shell commands.",
                "Blocked mutating shell. Use git log / git show / search only.",
            )
            return

    ph.allow()


if __name__ == "__main__":
    main()
