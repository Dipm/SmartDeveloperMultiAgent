#!/usr/bin/env python3
"""Run a hook script only when the active subagent matches AGENT env var."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_SD_HOME = Path(__file__).resolve().parent.parent
if str(_SD_HOME) not in sys.path:
    sys.path.insert(0, str(_SD_HOME))

from hooks.lib import pipeline_hook as ph  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        ph.deny("Hook wrapper misconfigured.", "Missing target script.")
    target = Path(sys.argv[1])
    if not target.is_file():
        ph.deny(f"Hook wrapper misconfigured: {target} not found.", "Missing hook script.")

    agent = os.environ.get("AGENT", "").strip().lower()
    if not agent:
        ph.deny("Hook wrapper misconfigured.", "AGENT env var is required.")

    data = ph.load_event()
    if not ph.is_target_agent(data, agent):
        ph.allow()

    result = subprocess.run(
        [sys.executable, str(target)],
        input=ph.blob(data).encode("utf-8"),
        check=False,
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
