#!/usr/bin/env python3
"""Validate SmartDeveloper pipeline package layout and artifact references."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "agents"

EXPECTED_AGENTS = (
    "triage",
    "context",
    "plan",
    "dev",
    "test",
    "review",
    "docs-pr",
    "pr-draft",
    "pr-fix",
    "spec",
)

ARTIFACT_NAMES = (
    "01-triage.md",
    "02-context.md",
    "03-plan.md",
    "04-dev-notes.md",
    "05-tests.md",
    "06-review-notes.md",
    "07-docs.md",
    "08-pr.md",
    "09-review-log.md",
    "pipeline.json",
)

DEPRECATED_PATTERNS = (
    re.compile(r"(?<![\w-])review-notes\.md"),
    re.compile(r"(?<![\w-])06-docs\.md"),
    re.compile(r"(?<![\w-])07-pr\.md"),
    re.compile(r"(?<![\w-])08-review-log\.md"),
)

SKILL_FRONTMATTER = re.compile(
    r"^---\s*\nname:\s*.+\ndescription:\s*.+\n(?:disable-model-invocation:\s*true\s*\n)?---",
    re.M,
)


def error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def check_agent_packages() -> int:
    failures = 0
    for name in EXPECTED_AGENTS:
        base = AGENTS / name
        for required in (
            f"../{name}.md",
            "agent.md",
            "AGENTS.md",
            "README.md",
            "instructions/contract.md",
            "instructions/output.md",
            "hooks/hooks.json",
        ):
            path = (base / required) if not required.startswith("../") else AGENTS / f"{name}.md"
            if not path.is_file():
                error(f"Missing {path.relative_to(REPO_ROOT)}")
                failures += 1
    return failures




def check_shared_files() -> int:
    failures = 0
    for rel in (
        "agents/shared/error-handling.md",
        "agents/shared/token-efficiency.md",
        "agents/shared/requirement-validation.md",
        "agents/shared/lean-artifacts.md",
        "agents/shared/platform-and-scope.md",
    ):
        if not (REPO_ROOT / rel).is_file():
            error(f"Missing {rel}")
            failures += 1
    return failures


def check_agent_errors_and_references() -> int:
    failures = 0
    for name in EXPECTED_AGENTS:
        base = AGENTS / name
        errors_md = base / "instructions" / "errors.md"
        if not errors_md.is_file():
            error(f"Missing {errors_md.relative_to(REPO_ROOT)}")
            failures += 1
        output_md = base / "instructions" / "output.md"
        if output_md.is_file():
            otext = output_md.read_text(encoding="utf-8", errors="replace")
            if "pipeline.json" not in otext:
                error(f"{output_md.relative_to(REPO_ROOT)} must mention pipeline.json updates")
                failures += 1
            if "failed" not in otext:
                error(f"{output_md.relative_to(REPO_ROOT)} must document failure status updates")
                failures += 1
        agent_md = base / "agent.md"
        if agent_md.is_file():
            atext = agent_md.read_text(encoding="utf-8", errors="replace")
            if "error-handling.md" not in atext and "instructions/errors.md" not in atext:
                error(f"{agent_md.relative_to(REPO_ROOT)} must reference error handling")
                failures += 1
            if "token-efficiency.md" not in atext:
                error(f"{agent_md.relative_to(REPO_ROOT)} must reference token-efficiency.md")
                failures += 1
    return failures

def check_skills() -> int:
    failures = 0
    for skill in AGENTS.rglob("skills/*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        if "disable-model-invocation: true" not in text:
            error(f"{skill.relative_to(REPO_ROOT)} missing disable-model-invocation: true")
            failures += 1
        if not SKILL_FRONTMATTER.search(text):
            error(f"{skill.relative_to(REPO_ROOT)} has invalid frontmatter")
            failures += 1
    return failures


def check_deprecated_references() -> int:
    failures = 0
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".mdc", ".py", ".json"}:
            continue
        if "node_modules" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in DEPRECATED_PATTERNS:
            if pattern.search(text):
                error(
                    f"{path.relative_to(REPO_ROOT)} still references deprecated "
                    f"{pattern.pattern}"
                )
                failures += 1
    return failures


def check_hooks_json() -> int:
    failures = 0
    for hooks_json in AGENTS.glob("*/hooks/hooks.json"):
        try:
            data = json.loads(hooks_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            error(f"{hooks_json}: {exc}")
            failures += 1
            continue
        for event, entries in data.get("hooks", {}).items():
            for entry in entries:
                script = REPO_ROOT / entry["command"]
                if not script.is_file():
                    error(f"{hooks_json}: missing script {entry['command']}")
                    failures += 1
    return failures


def main() -> int:
    failures = 0
    failures += check_agent_packages()
    failures += check_skills()
    failures += check_hooks_json()
    failures += check_deprecated_references()
    if failures:
        print(f"\nValidation failed with {failures} error(s).", file=sys.stderr)
        return 1
    print("Pipeline validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
