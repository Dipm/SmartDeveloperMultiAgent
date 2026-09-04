#!/usr/bin/env python3
"""Install SmartDeveloper pipeline files into a target repository."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

COPY_ITEMS = (
    "agents",
    "commands",
    "rules",
    "skills",
    "hooks",
    "scripts",
    "docs",
)

OPTIONAL_ITEMS = (
    "hooks/hooks.json.example",
    "rules/architecture.mdc.template",
)


def copy_tree(src: Path, dst: Path, *, force: bool) -> None:
    if dst.exists() and not force:
        raise FileExistsError(f"{dst} already exists (use --force to overwrite)")
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=force)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Legacy: copy SmartDeveloper into a target repo. Prefer smartDevByDipali_installGlobal.py."
    )
    parser.add_argument("target", nargs="?", default=".", help="Target repository path")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"Target not found: {target}", file=sys.stderr)
        return 1

    for item in COPY_ITEMS:
        copy_tree(REPO_ROOT / item, target / item, force=args.force)

    for item in OPTIONAL_ITEMS:
        src = REPO_ROOT / item
        if src.is_file():
            copy_tree(src, target / item, force=args.force)

    # project-checks template
    checks_dst = target / ".cursor" / "skills" / "project-checks.md"
    checks_src = REPO_ROOT / "skills" / "project-checks.md.template"
    if not checks_dst.exists() or args.force:
        checks_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(checks_src, checks_dst)

    arch_dst = target / ".cursor" / "rules" / "architecture.mdc"
    arch_src = REPO_ROOT / "rules" / "architecture.mdc.template"
    if not arch_dst.exists() or args.force:
        arch_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(arch_src, arch_dst)

    merge = subprocess.run(
        [sys.executable, str(target / "scripts" / "smartDevByDipali_mergeHooks.py")],
        cwd=target,
        check=False,
    )
    if merge.returncode != 0:
        print("Warning: smartDevByDipali_mergeHooks.py failed.", file=sys.stderr)

    gitignore = target / ".dev-agent" / ".gitignore"
    if not gitignore.exists() or args.force:
        gitignore.parent.mkdir(parents=True, exist_ok=True)
        gitignore.write_text(
            "# Keep pipeline artifacts for audit trail, or uncomment to ignore:\n"
            "# *\n"
            "# !.gitignore\n",
            encoding="utf-8",
        )

    print(f"SmartDeveloper installed into {target}")
    print("Note: global install is recommended — see docs/USAGE.md")
    print("Next steps:")
    print("  1. Fill in .cursor/skills/project-checks.md")
    print("  2. Copy hooks/hooks.json.example to .cursor/hooks.json")
    print("  3. Run /fix-ticket {ticket-id} in Cursor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
