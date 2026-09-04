#!/usr/bin/env python3
"""PR-fix: append-only 09-review-log.md; no push/merge."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph  # noqa: E402

AGENT = "pr-fix"
LOG = ph.artifact_allowed_pattern(ph.ARTIFACTS["review_log"])
PUSH = re.compile(r"\b(git\s+push|gh\s+pr\s+(merge|create|ready))\b", re.I)


def main() -> None:
    data = ph.load_event()
    ph.require_agent(data, AGENT)
    name, path, cmd = ph.tool_name(data), ph.path_of(data), ph.command_of(data)

    if cmd and PUSH.search(cmd):
        ph.deny(
            "PR-fix cannot push or merge. Handle one comment; leave publishing to humans.",
            "Blocked push/merge.",
        )
        return

    if path and LOG.search(ph.normalize_path(path)) and name in {"Write", "Delete"}:
        file_path = Path(path)
        if file_path.is_file() and file_path.stat().st_size > 0:
            ph.deny(
                "09-review-log.md is append-only. Use StrReplace to add an entry; "
                "do not overwrite.",
                "Blocked overwrite of review log.",
            )
            return
    ph.allow()


if __name__ == "__main__":
    main()
