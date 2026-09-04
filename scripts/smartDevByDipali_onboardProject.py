#!/usr/bin/env python3
"""Onboard a project for global SmartDeveloper (two config files only)."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

DEFAULT_SD_HOME = Path.home() / ".cursor" / "smart-developer"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add per-project SmartDeveloper config (Plan A onboarding)."
    )
    parser.add_argument("target", nargs="?", default=".", help="Project root")
    parser.add_argument(
        "--sd-home",
        type=Path,
        default=DEFAULT_SD_HOME,
        help="Global SmartDeveloper install (default: ~/.cursor/smart-developer)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing config")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    sd_home = args.sd_home.resolve()
    if not target.is_dir():
        print(f"Not a directory: {target}", file=sys.stderr)
        return 1
    if not (sd_home / "INSTALL.json").is_file():
        print(
            "SmartDeveloper is not installed globally. Run scripts/smartDevByDipali_installGlobal.py first.",
            file=sys.stderr,
        )
        return 1

    checks_dst = target / ".cursor" / "skills" / "project-checks.md"
    arch_dst = target / ".cursor" / "rules" / "architecture.mdc"
    checks_src = sd_home / "skills" / "project-checks.md.template"
    arch_src = sd_home / "rules" / "architecture.mdc.template"

    created: list[str] = []
    for dst, src in ((checks_dst, checks_src), (arch_dst, arch_src)):
        if dst.exists() and not args.force:
            print(f"Skip (exists): {dst}")
            continue
        if not src.is_file():
            print(f"Missing template: {src}", file=sys.stderr)
            return 1
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        created.append(str(dst))

    gitignore = target / ".dev-agent" / ".gitignore"
    if not gitignore.exists() or args.force:
        gitignore.parent.mkdir(parents=True, exist_ok=True)
        gitignore.write_text(
            "# Ticket pipeline artifacts for this project.\n"
            "# Uncomment to ignore all ticket state:\n"
            "# *\n"
            "# !.gitignore\n",
            encoding="utf-8",
        )
        created.append(str(gitignore))

    cursorignore = target / ".cursorignore"
    if not cursorignore.exists():
        cursorignore.write_text(
            "# Optional: hide vendor/tooling from Cursor index\n"
            "# .vendor/\n",
            encoding="utf-8",
        )

    print(f"Onboarded {target}")
    for path in created:
        print(f"  created {path}")
    print()
    print("Edit these with your project's real commands and conventions:")
    print(f"  {checks_dst}")
    print(f"  {arch_dst}")
    print()
    print("Ensure Jira + GitHub MCP are connected, then run:")
    print("  /fix-ticket YOUR-TICKET-ID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
