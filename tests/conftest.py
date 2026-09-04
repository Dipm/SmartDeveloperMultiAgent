"""Test helpers for hook scripts."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_hook(script: str, payload: dict, *, agent: str | None = None) -> dict:
    env = {"FAIL_CLOSED": "0"}
    if agent:
        env["AGENT"] = agent
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / script)],
        input=json.dumps(payload).encode("utf-8"),
        capture_output=True,
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}), **env},
        check=False,
        cwd=REPO_ROOT,
    )
    assert proc.stdout, proc.stderr.decode()
    return json.loads(proc.stdout.decode())


def write_plan(ticket: str, paths: list[str]) -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    body = "# Plan\n\n```paths\n" + "\n".join(paths) + "\n```\n"
    (root / "03-plan.md").write_text(body, encoding="utf-8")


def write_artifact(ticket: str, name: str, content: str = "# ok\n") -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    (root / name).write_text(content, encoding="utf-8")
