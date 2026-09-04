from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tests.conftest import REPO_ROOT, run_hook, write_artifact, write_plan


@pytest.fixture
def ticket_dir():
    ticket = "TEST-1"
    root = REPO_ROOT / ".dev-agent" / ticket
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    yield ticket
    if root.exists():
        shutil.rmtree(root)


def test_triage_requires_ticket_id():
    result = run_hook("agents/triage/hooks/require-ticket.py", {}, agent="triage")
    assert result["permission"] == "deny"


def test_triage_allows_with_ticket(ticket_dir):
    result = run_hook(
        "agents/triage/hooks/require-ticket.py",
        {"subagent": "triage", "prompt": f"@triage {ticket_dir}"},
        agent="triage",
    )
    assert result["permission"] == "allow"


def test_dev_blocks_without_plan(ticket_dir):
    result = run_hook(
        "agents/dev/hooks/require-approved-plan.py",
        {"subagent": "dev", "prompt": f"@dev {ticket_dir}"},
        agent="dev",
    )
    assert result["permission"] == "deny"


def test_dev_blocks_unapproved_plan(ticket_dir):
    write_plan(ticket_dir, ["src/foo.ts"])
    result = run_hook(
        "agents/dev/hooks/require-approved-plan.py",
        {"subagent": "dev", "prompt": f"@dev {ticket_dir}"},
        agent="dev",
    )
    assert result["permission"] == "deny"


def test_dev_allows_approved_plan(ticket_dir):
    write_plan(ticket_dir, ["src/foo.ts"])
    write_artifact(ticket_dir, "03-plan.approved", "")
    result = run_hook(
        "agents/dev/hooks/require-approved-plan.py",
        {"subagent": "dev", "prompt": f"@dev {ticket_dir}"},
        agent="dev",
    )
    assert result["permission"] == "allow"


def test_dev_blocks_out_of_plan_write(ticket_dir):
    write_plan(ticket_dir, ["src/foo.ts"])
    write_artifact(ticket_dir, "03-plan.approved", "")
    result = run_hook(
        "agents/dev/hooks/enforce-plan-scope.py",
        {
            "subagent": "dev",
            "prompt": f"@dev {ticket_dir}",
            "tool_name": "Write",
            "tool_input": {"path": "src/other.ts"},
        },
        agent="dev",
    )
    assert result["permission"] == "deny"


def test_dev_allows_plan_path_write(ticket_dir):
    write_plan(ticket_dir, ["src/foo.ts"])
    write_artifact(ticket_dir, "03-plan.approved", "")
    result = run_hook(
        "agents/dev/hooks/enforce-plan-scope.py",
        {
            "subagent": "dev",
            "prompt": f"@dev {ticket_dir}",
            "tool_name": "Write",
            "tool_input": {"path": "src/foo.ts"},
        },
        agent="dev",
    )
    assert result["permission"] == "allow"


def test_docs_pr_blocks_when_review_sends_back(ticket_dir):
    for name in (
        "01-triage.md",
        "03-plan.md",
        "04-dev-notes.md",
        "05-tests.md",
    ):
        write_artifact(ticket_dir, name)
    write_artifact(
        ticket_dir,
        "06-review-notes.md",
        "# Review\n\n## Verdict\n- send back to @dev\n\n## Blocking\n- bug\n",
    )
    result = run_hook(
        "agents/docs-pr/hooks/require-review-clear.py",
        {"subagent": "docs-pr", "prompt": f"@docs-pr {ticket_dir}"},
        agent="docs-pr",
    )
    assert result["permission"] == "deny"


def test_docs_pr_allows_clean_review(ticket_dir):
    for name in (
        "01-triage.md",
        "03-plan.md",
        "04-dev-notes.md",
        "05-tests.md",
    ):
        write_artifact(ticket_dir, name)
    write_artifact(
        ticket_dir,
        "06-review-notes.md",
        "# Review\n\n## Verdict\n- clean\n\n## Blocking\n- None.\n",
    )
    result = run_hook(
        "agents/docs-pr/hooks/require-review-clear.py",
        {"subagent": "docs-pr", "prompt": f"@docs-pr {ticket_dir}"},
        agent="docs-pr",
    )
    assert result["permission"] == "allow"


def test_pr_fix_requires_classification(ticket_dir):
    result = run_hook(
        "agents/pr-fix/hooks/require-single-comment.py",
        {"subagent": "pr-fix", "prompt": f"@pr-fix {ticket_dir} fix this"},
        agent="pr-fix",
    )
    assert result["permission"] == "deny"


def test_pr_fix_allows_with_classification(ticket_dir):
    result = run_hook(
        "agents/pr-fix/hooks/require-single-comment.py",
        {
            "subagent": "pr-fix",
            "prompt": f"@pr-fix {ticket_dir} trivial please rename variable",
        },
        agent="pr-fix",
    )
    assert result["permission"] == "allow"


def test_hook_fails_closed_on_bad_json():
    import json
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "agents/triage/hooks/require-ticket.py")],
        input=b"not-json",
        capture_output=True,
        env={**__import__("os").environ, "FAIL_CLOSED": "1", "AGENT": "triage"},
        cwd=REPO_ROOT,
    )
    result = json.loads(proc.stdout.decode())
    assert result["permission"] == "deny"
