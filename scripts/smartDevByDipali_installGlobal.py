#!/usr/bin/env python3
"""Install SmartDeveloper globally for Cursor (Plan A)."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from smartDevByDipali_names import MERGE_HOOKS, ONBOARD_PROJECT

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SD_HOME = Path.home() / ".cursor" / "smart-developer"
CURSOR_DIR = Path.home() / ".cursor"

SYNC_DIRS = ("agents", "commands", "hooks", "rules", "skills", "scripts", "docs")
AGENT_ENTRIES = (
    "triage",
    "context",
    "plan",
    "dev",
    "test",
    "review",
    "docs-pr",
    "pr-fix",
)
SKIP_NAMES = {".git", "__pycache__", ".pytest_cache", "node_modules"}


def rewrite_paths(text: str, sd_home: Path) -> str:
    home = str(sd_home)
    text = text.replace("`agents/", f"`{home}/agents/")
    text = text.replace("Load `agents/", f"Load `{home}/agents/")
    text = text.replace("agents/orchestrator.md", f"{home}/agents/orchestrator.md")
    return text


def sync_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in SKIP_NAMES:
            continue
        target = dst / item.name
        if item.is_dir():
            sync_tree(item, target)
        else:
            shutil.copy2(item, target)


def make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_payload(source: Path, sd_home: Path) -> None:
    for name in SYNC_DIRS:
        src = source / name
        if src.is_dir():
            sync_tree(src, sd_home / name)

    for script in sd_home.rglob("agents/*/hooks/*.py"):
        make_executable(script)
    make_executable(sd_home / "hooks" / "smartDevByDipali_hookWrapper.py")
    for script in (sd_home / "scripts").glob("smartDevByDipali_*.py"):
        make_executable(script)


def install_agents(source: Path, sd_home: Path, cursor_agents: Path) -> int:
    cursor_agents.mkdir(parents=True, exist_ok=True)
    count = 0
    for name in AGENT_ENTRIES:
        src = source / "agents" / f"{name}.md"
        if not src.is_file():
            continue
        body = rewrite_paths(src.read_text(encoding="utf-8"), sd_home)
        (cursor_agents / f"{name}.md").write_text(body, encoding="utf-8")
        count += 1
    return count


def install_commands(source: Path, sd_home: Path, cursor_commands: Path) -> None:
    cursor_commands.mkdir(parents=True, exist_ok=True)
    src = source / "commands" / "fix-ticket.md"
    body = rewrite_paths(src.read_text(encoding="utf-8"), sd_home)
    (cursor_commands / "fix-ticket.md").write_text(body, encoding="utf-8")


def install_hooks(sd_home: Path, hooks_dst: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(sd_home / "scripts" / "smartDevByDipali_mergeHooks.py"),
            "--sd-home",
            str(sd_home),
            "--output",
            str(hooks_dst),
        ],
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("smartDevByDipali_mergeHooks.py failed during global install")


def write_manifest(sd_home: Path, source: Path) -> None:
    manifest = {
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source.resolve()),
        "sd_home": str(sd_home.resolve()),
        "pipeline_version": "1",
    }
    (sd_home / "INSTALL.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install SmartDeveloper globally under ~/.cursor/ (Plan A)."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=REPO_ROOT,
        help="SmartDeveloper repo root (default: this repo)",
    )
    parser.add_argument(
        "--sd-home",
        type=Path,
        default=DEFAULT_SD_HOME,
        help="Global install root (default: ~/.cursor/smart-developer)",
    )
    parser.add_argument(
        "--skip-hooks",
        action="store_true",
        help="Skip writing ~/.cursor/hooks.json",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    sd_home = args.sd_home.resolve()
    if not (source / "agents").is_dir():
        print(f"Invalid source (missing agents/): {source}", file=sys.stderr)
        return 1

    print(f"Installing SmartDeveloper from {source}")
    print(f"  → {sd_home}")

    install_payload(source, sd_home)
    agent_count = install_agents(source, sd_home, CURSOR_DIR / "agents")
    install_commands(source, sd_home, CURSOR_DIR / "commands")

    if not args.skip_hooks:
        install_hooks(sd_home, CURSOR_DIR / "hooks.json")
        print(f"  → {CURSOR_DIR / 'hooks.json'}")

    write_manifest(sd_home, source)

    print(f"Installed {agent_count} agents → {CURSOR_DIR / 'agents'}")
    print(f"Installed /fix-ticket → {CURSOR_DIR / 'commands' / 'fix-ticket.md'}")
    print()
    print("Manual step (once):")
    print("  Paste rules/dev-agent-pipeline-user.mdc into Cursor → Settings → Rules → User Rules")
    print(f"  File: {sd_home / 'rules' / 'dev-agent-pipeline-user.mdc'}")
    print()
    print("Per project, run:")
    print("  python3 scripts/smartDevByDipali_onboardProject.py /path/to/your-app")
    print()
    print("Restart Cursor, then confirm @triage and /fix-ticket appear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
