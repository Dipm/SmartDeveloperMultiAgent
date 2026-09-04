#!/usr/bin/env python3
"""Merge per-agent hook fragments into a single hooks.json."""
from __future__ import annotations

import argparse
import json
import stat
import sys
from pathlib import Path

from smartDevByDipali_names import HOOK_WRAPPER

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "agents"
DEFAULT_OUTPUT = REPO_ROOT / "hooks" / "hooks.json.example"


def agent_name_from_path(hooks_json: Path) -> str:
    return hooks_json.parent.parent.name


def wrap_command(script: Path, agent: str, sd_home: Path | None) -> str:
    wrapper_name = f"{HOOK_WRAPPER}.py"
    if sd_home:
        target = script.resolve()
        wrapper = (sd_home / "hooks" / wrapper_name).resolve()
        return (
            f"PYTHONPATH={sd_home.resolve()} AGENT={agent} FAIL_CLOSED=1 "
            f"python3 {wrapper} {target}"
        )
    rel = script.relative_to(REPO_ROOT)
    return f"AGENT={agent} FAIL_CLOSED=1 python3 hooks/{wrapper_name} {rel}"


def merge_hooks(sd_home: Path | None) -> dict:
    root = sd_home or REPO_ROOT
    agents_dir = root / "agents"
    merged: dict = {"version": 1, "hooks": {}}

    for hooks_json in sorted(agents_dir.glob("*/hooks/hooks.json")):
        agent = agent_name_from_path(hooks_json)
        fragment = json.loads(hooks_json.read_text(encoding="utf-8"))
        for event, entries in fragment.get("hooks", {}).items():
            merged["hooks"].setdefault(event, [])
            for entry in entries:
                script = root / entry["command"]
                wrapped = {
                    "command": wrap_command(script, agent, sd_home),
                    "timeout": entry.get("timeout", 10),
                    "failClosed": entry.get("failClosed", True),
                }
                merged["hooks"][event].append(wrapped)
    return merged


def make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge SmartDeveloper hook fragments.")
    parser.add_argument(
        "--sd-home",
        type=Path,
        default=None,
        help="Global install root for absolute hook paths (~/.cursor/smart-developer)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output hooks.json path",
    )
    args = parser.parse_args()

    sd_home = args.sd_home.resolve() if args.sd_home else None
    root = sd_home or REPO_ROOT
    merged = merge_hooks(sd_home)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    for script in root.rglob("agents/*/hooks/*.py"):
        make_executable(script)
    wrapper = root / "hooks" / f"{HOOK_WRAPPER}.py"
    if wrapper.is_file():
        make_executable(wrapper)

    print(f"Wrote {args.output}")
    print(f"Hook entries: {sum(len(v) for v in merged['hooks'].values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
