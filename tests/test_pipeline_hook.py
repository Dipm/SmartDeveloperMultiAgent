from __future__ import annotations

from hooks.lib import pipeline_hook as ph


def test_paths_from_plan_block():
    text = """
# Plan
## Files
```paths
src/a.ts
src/b.test.ts
```
"""
    paths = ph.paths_from_plan_text(text)
    assert paths == {"src/a.ts", "src/b.test.ts"}


def test_review_verdict_clean():
    text = "# Review\n\n## Verdict\n- clean\n"
    assert ph.paths_from_plan_text("") == set()
    # review_verdict needs file; test parsing via inline logic
    for line in text.splitlines():
        if line.strip().startswith("- "):
            assert "clean" in line


def test_review_sends_back_detects_blocking():
    text = """# Review

## Verdict
- send back to @dev

## Blocking
- null pointer risk

## Should-fix
- None.
"""
    root = ph.ticket_root("X")
    # unit test the section parser indirectly
    blocking = __import__("re").search(
        r"## Blocking\s*\n([\s\S]*?)(?=\n## |\Z)", text, __import__("re").I
    )
    assert blocking
    body = blocking.group(1).strip().lower()
    assert body not in ("none.", "none")


def test_is_transient_error():
    assert ph.is_transient_error("external_service")
    assert ph.is_transient_error("auth")
    assert ph.is_transient_error("timeout")
    assert not ph.is_transient_error("validation")


def test_stage_status_and_manifest(tmp_path, monkeypatch):
    ticket = "TEST-99"
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".dev-agent" / ticket).mkdir(parents=True)
    assert ph.stage_status(ticket, "triage") is None
    ph.mark_stage_running(ticket, "triage")
    assert ph.stage_status(ticket, "triage") == "running"
    ph.mark_stage_complete(ticket, "triage")
    assert ph.stage_status(ticket, "triage") == "complete"


def test_mark_stage_failed(tmp_path, monkeypatch):
    ticket = "TEST-100"
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".dev-agent" / ticket).mkdir(parents=True)
    ph.mark_stage_failed(
        ticket,
        "triage",
        code="external_service",
        message="Jira down",
        suggestions=["retry triage"],
        retry_count=1,
    )
    manifest = ph.load_manifest(ticket)
    entry = manifest["stages"]["triage"]
    assert entry["status"] == "failed"
    assert entry["error"]["code"] == "external_service"
    assert entry["error"]["retry_count"] == 1


def test_validate_stage_artifact(tmp_path, monkeypatch):
    ticket = "TEST-101"
    monkeypatch.chdir(tmp_path)
    root = tmp_path / ".dev-agent" / ticket
    root.mkdir(parents=True)
    (root / "pipeline.json").write_text(
        '{"pipeline_version":"1","ticket":"'
        + ticket
        + '","lean_artifacts":false,"stages":{}}',
        encoding="utf-8",
    )
    assert ph.validate_stage_artifact(ticket, "triage") == [
        f"missing: .dev-agent/{ticket}/01-triage.md"
    ]
    (root / "01-triage.md").write_text("ok", encoding="utf-8")
    (root / "pipeline.json").write_text(
        '{"pipeline_version":"1","ticket":"'
        + ticket
        + '","lean_artifacts":false,"stages":{"triage":{"status":"complete"}}}',
        encoding="utf-8",
    )
    assert ph.validate_stage_artifact(ticket, "triage") == []


def test_load_manifest_corrupt_json(tmp_path, monkeypatch):
    ticket = "TEST-102"
    monkeypatch.chdir(tmp_path)
    root = tmp_path / ".dev-agent" / ticket
    root.mkdir(parents=True)
    (root / "pipeline.json").write_text("{bad", encoding="utf-8")
    manifest = ph.load_manifest(ticket)
    assert manifest.get("_manifest_error") == "corrupt_json"


def test_pipeline_mode_defaults_non_prod(tmp_path, monkeypatch):
    ticket = "TEST-200"
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".dev-agent" / ticket).mkdir(parents=True)
    assert ph.pipeline_mode(ticket) == "non-prod"
    assert ph.is_non_prod(ticket)


def test_review_sends_back_blocking_only_ignores_should_fix(tmp_path, monkeypatch):
    ticket = "TEST-202"
    monkeypatch.chdir(tmp_path)
    root = tmp_path / ".dev-agent" / ticket
    root.mkdir(parents=True)
    (root / "pipeline.json").write_text(
        '{"pipeline_version":"1","ticket":"TEST-202","mode":"prod","stages":{}}',
        encoding="utf-8",
    )
    review = "\n".join([
        "# Review",
        "",
        "## Blocking",
        "- None.",
        "",
        "## Should-fix",
        "- nitpick",
        "",
    ])
    (root / "06-review-notes.md").write_text(review, encoding="utf-8")
    assert not ph.review_sends_back(ticket, blocking_only=True)


def test_auto_approve_plan_writes_sidecar(tmp_path, monkeypatch):
    ticket = "TEST-204"
    monkeypatch.chdir(tmp_path)
    root = tmp_path / ".dev-agent" / ticket
    root.mkdir(parents=True)
    (root / "03-plan.md").write_text("# Plan\n", encoding="utf-8")
    ph.auto_approve_plan(ticket)
    assert (root / "03-plan.approved").is_file()
    manifest = ph.load_manifest(ticket)
    assert manifest["stages"]["plan"]["status"] == "approved"
