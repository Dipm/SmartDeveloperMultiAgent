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
    use_audit_trail(ticket)
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    body = "# Plan\n\n```paths\n" + "\n".join(paths) + "\n```\n"
    (root / "03-plan.md").write_text(body, encoding="utf-8")


def write_artifact(ticket: str, name: str, content: str = "# ok\n") -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    (root / name).write_text(content, encoding="utf-8")


def write_manifest(ticket: str, manifest: dict) -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    (root / "pipeline.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def use_audit_trail(ticket: str) -> None:
    """Tests that use numbered .md artifacts disable lean mode."""
    write_manifest(ticket, {
        "pipeline_version": "1",
        "ticket": ticket,
        "lean_artifacts": False,
        "stages": {},
    })


def write_plan_stage(ticket: str, paths: list[str], *, lean: bool = True) -> None:
    root = REPO_ROOT / ".dev-agent" / ticket
    root.mkdir(parents=True, exist_ok=True)
    if lean:
        manifest_path = root / "pipeline.json"
        manifest = {}
        if manifest_path.is_file():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest.setdefault("pipeline_version", "1")
        manifest.setdefault("ticket", ticket)
        manifest["lean_artifacts"] = True
        manifest.setdefault("stages", {})
        manifest["stages"]["plan"] = {
            "status": "complete",
            "paths": paths,
            "summary": "test plan",
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        write_plan(ticket, paths)
        use_audit_trail(ticket)
