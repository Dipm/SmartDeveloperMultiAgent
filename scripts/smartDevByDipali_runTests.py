#!/usr/bin/env python3
"""Run hook tests without pytest (stdlib only)."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def run_hook(script: str, payload: dict, *, agent: str | None = None) -> dict:
    env = {**__import__("os").environ, "FAIL_CLOSED": "0"}
    if agent:
        env["AGENT"] = agent
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / script)],
        input=json.dumps(payload).encode("utf-8"),
        capture_output=True,
        env=env,
        check=False,
        cwd=REPO_ROOT,
    )
    assert proc.stdout, proc.stderr.decode()
    return json.loads(proc.stdout.decode())


def use_audit_trail(ticket: str) -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    (root / "pipeline.json").write_text(
        json.dumps({
            "pipeline_version": "1",
            "ticket": ticket,
            "lean_artifacts": False,
            "stages": {},
        }) + "\n",
        encoding="utf-8",
    )


def write_plan(ticket: str, paths: list[str]) -> None:
    use_audit_trail(ticket)
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    body = "# Plan\n\n```paths\n" + "\n".join(paths) + "\n```\n"
    (root / "03-plan.md").write_text(body, encoding="utf-8")


def write_artifact(ticket: str, name: str, content: str = "# ok\n") -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    (root / name).write_text(content, encoding="utf-8")


class HookTests(unittest.TestCase):
    ticket = "TEST-1"

    def setUp(self) -> None:
        self.root = REPO_ROOT / ".dev-agent" / self.ticket
        if self.root.exists():
            shutil.rmtree(self.root)
        self.root.mkdir(parents=True)

    def tearDown(self) -> None:
        if self.root.exists():
            shutil.rmtree(self.root)

    def test_triage_requires_ticket_id(self) -> None:
        result = run_hook("agents/triage/hooks/require-ticket.py", {}, agent="triage")
        self.assertEqual(result["permission"], "deny")

    def test_dev_blocks_unapproved_plan(self) -> None:
        write_plan(self.ticket, ["src/foo.ts"])
        result = run_hook(
            "agents/dev/hooks/require-approved-plan.py",
            {"subagent": "dev", "prompt": f"@dev {self.ticket}"},
            agent="dev",
        )
        self.assertEqual(result["permission"], "deny")

    def test_dev_allows_approved_plan(self) -> None:
        write_plan(self.ticket, ["src/foo.ts"])
        write_artifact(self.ticket, "03-plan.approved", "")
        result = run_hook(
            "agents/dev/hooks/require-approved-plan.py",
            {"subagent": "dev", "prompt": f"@dev {self.ticket}"},
            agent="dev",
        )
        self.assertEqual(result["permission"], "allow")

    def test_docs_pr_blocks_when_review_sends_back(self) -> None:
        for name in ("01-triage.md", "03-plan.md", "04-dev-notes.md", "05-tests.md"):
            write_artifact(self.ticket, name)
        write_artifact(
            self.ticket,
            "06-review-notes.md",
            "# Review\n\n## Verdict\n- send back to @dev\n\n## Blocking\n- bug\n",
        )
        result = run_hook(
            "agents/docs-pr/hooks/require-review-clear.py",
            {"subagent": "docs-pr", "prompt": f"@docs-pr {self.ticket}"},
            agent="docs-pr",
        )
        self.assertEqual(result["permission"], "deny")


class LibraryTests(unittest.TestCase):
    def test_paths_from_plan_block(self) -> None:
        from hooks.lib import pipeline_hook as ph

        text = "# Plan\n```paths\nsrc/a.ts\nsrc/b.test.ts\n```\n"
        self.assertEqual(ph.paths_from_plan_text(text), {"src/a.ts", "src/b.test.ts"})


if __name__ == "__main__":
    raise SystemExit(unittest.main(verbosity=2))
