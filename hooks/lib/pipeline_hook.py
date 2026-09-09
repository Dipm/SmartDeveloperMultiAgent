#!/usr/bin/env python3
"""Shared primitives for SmartDeveloper pipeline hook scripts."""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PIPELINE_VERSION = "1"
PIPELINE_MODES = frozenset({"prod", "non-prod"})
DEFAULT_PIPELINE_MODE = "non-prod"

TICKET_RE = re.compile(
    r"\b([A-Z][A-Z0-9]+-\d+)\b|(?:ticket[_-]?id[:\s]+)([A-Za-z0-9._-]+)",
    re.I,
)
APPROVAL_RE = re.compile(
    r"\b(approved|go-ahead|lgtm|proceed(?:\s+with)?\s+(?:dev|implementation)|"
    r"implement\s+the\s+plan)\b",
    re.I,
)
WRITE_TOOLS = frozenset(
    {"Write", "StrReplace", "Delete", "EditNotebook", "TabWrite"}
)
BACKTICK_PATH = re.compile(r"`([^`\n]+)`")
PATHS_BLOCK = re.compile(r"```paths\s*\n([\s\S]*?)```", re.I)
FILEISH = re.compile(
    r"^[A-Za-z0-9._/@*-]+\.[A-Za-z0-9]+$|^[A-Za-z0-9._/@*-]+/[A-Za-z0-9._/@*-]+$"
)
MUTATING_SHELL_RE = re.compile(
    r"\b(git\s+(commit|push|reset|rebase|checkout|merge|add|rm|mv)|"
    r"gh\s+pr\b)\b",
    re.I,
)
SAFE_SHELL_RE = re.compile(
    r"^\s*(git\s+(log|show|blame|diff|status|rev-parse)|rg\b|grep\b|find\b|"
    r"ls\b|head\b|cat\b|npm\b|pnpm\b|yarn\b|npx\b|cargo\b|go\b|mvn\b|"
    r"gradle\b|pytest\b|make\b|lint\b|tsc\b|python\b|node\b)",
    re.I,
)
JIRA_WRITE_RE = re.compile(
    r"(createJiraIssue|editJiraIssue|transitionJiraIssue|addCommentToJiraIssue|"
    r"addWorklogToJiraIssue|createIssueLink)",
    re.I,
)
OPEN_PR_RE = re.compile(
    r"\b(gh\s+pr\s+(create|edit|merge|ready)|git\s+push|hub\s+pull-request)\b",
    re.I,
)
BATCH_COMMENT_RE = re.compile(
    r"(these comments|batch of comments|comment\s*#?\s*1[\s\S]{0,400}comment\s*#?\s*2)",
    re.I,
)
TESTISH_RE = re.compile(
    r"(^|/)(__tests__/|tests?/|test/)|(\.|/)(test|spec)\.[A-Za-z0-9]+$",
    re.I,
)

# Normalized artifact names (pipeline v1)
ARTIFACTS = {
    "triage": "01-triage.md",
    "context": "02-context.md",
    "plan": "03-plan.md",
    "dev_notes": "04-dev-notes.md",
    "tests": "05-tests.md",
    "review": "06-review-notes.md",
    "docs": "07-docs.md",
    "pr": "08-pr.md",
    "review_log": "09-review-log.md",
    "manifest": "pipeline.json",
    "plan_approved": "03-plan.approved",
}
STAGE_ARTIFACT = {
    "triage": ARTIFACTS["triage"],
    "context": ARTIFACTS["context"],
    "plan": ARTIFACTS["plan"],
    "dev": ARTIFACTS["dev_notes"],
    "test": ARTIFACTS["tests"],
    "review": ARTIFACTS["review"],
    "docs_pr": ARTIFACTS["docs"],
    "pr_draft": ARTIFACTS["pr"],
    "pr_fix": ARTIFACTS["review_log"],
    "spec": ARTIFACTS["plan"],
}

TRANSIENT_ERROR_CODES = frozenset({"external_service", "auth", "timeout"})

ARTIFACT_SIZE_WARN_BYTES = 50 * 1024


SUBAGENT_KEYS = (
    "subagent",
    "subagentName",
    "subagent_name",
    "agent",
    "agentName",
    "agent_name",
    "name",
)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    return here.parents[2]


def setup_import_path() -> None:
    root = str(repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)


def fail_closed_default() -> bool:
    return os.environ.get("FAIL_CLOSED", "1") != "0"


def load_event(*, fail_closed: bool | None = None) -> dict[str, Any]:
    closed = fail_closed_default() if fail_closed is None else fail_closed
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        if closed:
            deny(
                "Hook blocked: malformed event payload.",
                "Stop. Hook received invalid JSON.",
            )
        return {}
    if not isinstance(data, dict):
        if closed:
            deny(
                "Hook blocked: event payload must be a JSON object.",
                "Stop. Invalid hook payload shape.",
            )
        return {}
    return data


def respond(payload: dict[str, Any]) -> None:
    print(json.dumps(payload))
    raise SystemExit(0)


def allow(msg: str | None = None) -> None:
    payload: dict[str, Any] = {"permission": "allow"}
    if msg:
        payload["agent_message"] = msg
    respond(payload)


def deny(user: str, agent: str) -> None:
    respond(
        {
            "permission": "deny",
            "user_message": user,
            "agent_message": agent,
        }
    )


def blob(data: dict[str, Any]) -> str:
    return json.dumps(data)


def ticket_id_from(data: dict[str, Any]) -> str | None:
    m = TICKET_RE.search(blob(data))
    if not m:
        return None
    return next(g for g in m.groups() if g)


def subagent_name(data: dict[str, Any]) -> str | None:
    for key in SUBAGENT_KEYS:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    return None


def is_target_agent(data: dict[str, Any], agent: str) -> bool:
    name = subagent_name(data)
    if not name:
        return True
    return name == agent.lower() or name.endswith(f"/{agent.lower()}")


def require_agent(data: dict[str, Any], agent: str) -> None:
    if not is_target_agent(data, agent):
        allow()


def tool_name(data: dict[str, Any]) -> str:
    for key in ("tool_name", "toolName", "tool", "name"):
        value = data.get(key)
        if isinstance(value, str):
            return value
    return ""


def path_of(data: dict[str, Any]) -> str:
    inp = data.get("tool_input") or data.get("toolInput") or data.get("arguments") or {}
    if isinstance(inp, dict):
        for key in ("path", "file_path", "filePath", "target_notebook"):
            value = inp.get(key)
            if isinstance(value, str):
                return value.replace("\\", "/")
    return ""


def command_of(data: dict[str, Any]) -> str:
    if isinstance(data.get("command"), str):
        return data["command"]
    inp = data.get("tool_input") or data.get("toolInput") or {}
    if isinstance(inp, dict) and isinstance(inp.get("command"), str):
        return inp["command"]
    return ""


def ticket_root(ticket: str) -> Path:
    return Path(".dev-agent") / ticket


def artifact_path(ticket: str, name: str) -> Path:
    return ticket_root(ticket) / name


def missing_artifacts(ticket: str, names: tuple[str, ...]) -> list[str]:
    root = ticket_root(ticket)
    missing: list[str] = []
    for name in names:
        path = root / name
        if not path.is_file() or path.stat().st_size == 0:
            missing.append(str(path))
    return missing


def read_artifact(ticket: str, name: str) -> str:
    return artifact_path(ticket, name).read_text(encoding="utf-8", errors="replace")


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def paths_from_plan_text(text: str) -> set[str]:
    found: set[str] = set()
    block = PATHS_BLOCK.search(text)
    if block:
        for line in block.group(1).splitlines():
            p = line.strip().strip("/")
            if p and FILEISH.match(p) and not p.startswith("http"):
                found.add(p)
    for raw in BACKTICK_PATH.findall(text):
        p = raw.strip().strip("/")
        if FILEISH.match(p) and not p.startswith("http"):
            found.add(p)
    return found


def plan_paths(ticket: str) -> set[str]:
    from_manifest = manifest_plan_paths(ticket)
    if from_manifest:
        return from_manifest
    plan = artifact_path(ticket, ARTIFACTS["plan"])
    if not plan.is_file():
        return set()
    return paths_from_plan_text(plan.read_text(encoding="utf-8", errors="replace"))


def dev_notes_paths(ticket: str) -> set[str]:
    notes = artifact_path(ticket, ARTIFACTS["dev_notes"])
    if not notes.is_file():
        return set()
    return paths_from_plan_text(notes.read_text(encoding="utf-8", errors="replace"))


def in_path_set(path: str, allowed: set[str]) -> bool:
    norm = normalize_path(path)
    for item in allowed:
        if norm == item or norm.endswith("/" + item) or item.endswith("/" + norm):
            return True
        if norm.endswith(item) and (
            len(norm) == len(item) or norm[: -len(item)].endswith("/")
        ):
            return True
    return False


def review_verdict(ticket: str) -> str | None:
    review = artifact_path(ticket, ARTIFACTS["review"])
    if not review.is_file():
        return None
    text = review.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("## verdict"):
            continue
        if stripped.startswith("- "):
            value = stripped[2:].strip().lower()
            if "send back" in value or value == "send back to @dev":
                return "send_back"
            if value == "clean":
                return "clean"
    manifest = load_manifest(ticket)
    review_stage = manifest.get("stages", {}).get("review", {})
    verdict = review_stage.get("verdict")
    if isinstance(verdict, str):
        return verdict.lower()
    return None


def _review_section_has_items(text: str, heading: str) -> bool:
    section = re.search(
        rf"## {heading}\s*\n([\s\S]*?)(?=\n## |\Z)", text, re.I
    )
    if not section:
        return False
    body = section.group(1).strip().lower()
    return bool(body and body not in ("none.", "none", "- none."))


def review_sends_back(ticket: str, *, blocking_only: bool | None = None) -> bool:
    if blocking_only is None:
        blocking_only = True
    if use_lean_artifacts(ticket):
        manifest = load_manifest(ticket)
        review = manifest.get("stages", {}).get("review", {})
        if isinstance(review, dict):
            verdict = review.get("verdict")
            if isinstance(verdict, str) and verdict.lower() == "clean":
                return False
            blocking = review.get("blocking")
            if isinstance(blocking, list) and any(str(x).strip() for x in blocking):
                return True
            if not blocking_only:
                should_fix = review.get("should_fix")
                if isinstance(should_fix, list) and any(str(x).strip() for x in should_fix):
                    return True
        return False
    verdict = review_verdict(ticket)
    if verdict == "clean":
        return False
    if verdict == "send_back" and blocking_only:
        return True
    review = artifact_path(ticket, ARTIFACTS["review"])
    if not review.is_file():
        return blocking_only
    text = review.read_text(encoding="utf-8", errors="replace")
    if _review_section_has_items(text, "Blocking"):
        return True
    if not blocking_only and _review_section_has_items(text, "Should-fix"):
        return True
    return False



def use_lean_artifacts(ticket: str) -> bool:
    """When True (default), stages record state in pipeline.json only — no numbered .md files."""
    manifest = load_manifest(ticket)
    if "lean_artifacts" in manifest:
        return bool(manifest["lean_artifacts"])
    return True


def set_lean_artifacts(ticket: str, lean: bool) -> None:
    manifest = load_manifest(ticket)
    manifest["lean_artifacts"] = lean
    save_manifest(ticket, manifest)


def stage_is_complete(ticket: str, stage: str) -> bool:
    status = stage_status(ticket, stage)
    return status in ("complete", "approved")


STAGE_FOR_ARTIFACT = {
    ARTIFACTS["triage"]: "triage",
    ARTIFACTS["context"]: "context",
    ARTIFACTS["plan"]: "plan",
    ARTIFACTS["dev_notes"]: "dev",
    ARTIFACTS["tests"]: "test",
    ARTIFACTS["review"]: "review",
    ARTIFACTS["docs"]: "docs_pr",
    ARTIFACTS["pr"]: "pr_draft",
}


def missing_prerequisites(ticket: str, artifact_names: tuple[str, ...]) -> list[str]:
    """Return missing artifact paths or stage names depending on lean mode."""
    if not use_lean_artifacts(ticket):
        return missing_artifacts(ticket, artifact_names)
    missing: list[str] = []
    for name in artifact_names:
        stage = STAGE_FOR_ARTIFACT.get(name)
        if not stage:
            path = artifact_path(ticket, name)
            if not path.is_file() or path.stat().st_size == 0:
                missing.append(str(path))
            continue
        if name == ARTIFACTS["plan"]:
            if stage_is_complete(ticket, "spec") or stage_is_complete(ticket, "plan"):
                if not plan_paths(ticket):
                    missing.append("pipeline.json: stages.plan.paths or stages.spec.paths")
                continue
        if not stage_is_complete(ticket, stage):
            missing.append(f"pipeline.json: stages.{stage}.status != complete")
    return missing


def manifest_plan_paths(ticket: str) -> set[str]:
    manifest = load_manifest(ticket)
    found: set[str] = set()
    for key in ("spec", "plan"):
        stage = manifest.get("stages", {}).get(key, {})
        if not isinstance(stage, dict):
            continue
        paths = stage.get("paths")
        if isinstance(paths, list):
            for item in paths:
                if isinstance(item, str) and item.strip():
                    found.add(item.strip().strip("/"))
    return found


def pipeline_mode(ticket: str) -> str:
    manifest = load_manifest(ticket)
    mode = manifest.get("mode")
    if isinstance(mode, str) and mode in PIPELINE_MODES:
        return mode
    return DEFAULT_PIPELINE_MODE


def is_non_prod(ticket: str) -> bool:
    return pipeline_mode(ticket) == "non-prod"


def is_prod(ticket: str) -> bool:
    return pipeline_mode(ticket) == "prod"


def set_pipeline_mode(ticket: str, mode: str) -> None:
    if mode not in PIPELINE_MODES:
        raise ValueError(f"invalid pipeline mode: {mode}")
    manifest = load_manifest(ticket)
    manifest["mode"] = mode
    save_manifest(ticket, manifest)


def auto_approve_plan(ticket: str) -> None:
    sidecar = artifact_path(ticket, ARTIFACTS["plan_approved"])
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    if not sidecar.is_file():
        sidecar.write_text("auto-approved\n", encoding="utf-8")
    manifest = load_manifest(ticket)
    plan = manifest.setdefault("stages", {}).setdefault("plan", {})
    plan["status"] = "approved"
    plan["artifact"] = ARTIFACTS["plan"]
    plan.setdefault("approved_at", utc_now_iso())
    save_manifest(ticket, manifest)



def plan_is_approved(ticket: str, data: dict[str, Any]) -> bool:
    sidecar = artifact_path(ticket, ARTIFACTS["plan_approved"])
    if sidecar.is_file():
        return True
    if APPROVAL_RE.search(blob(data)):
        return True
    manifest = load_manifest(ticket)
    plan = manifest.get("stages", {}).get("plan", {})
    status = plan.get("status")
    if status == "approved":
        return True
    if status == "complete":
        if artifact_path(ticket, ARTIFACTS["plan"]).is_file():
            return True
        if use_lean_artifacts(ticket) and plan_paths(ticket):
            return True
    return False


def load_manifest(ticket: str) -> dict[str, Any]:
    path = artifact_path(ticket, ARTIFACTS["manifest"])
    if not path.is_file():
        return {"pipeline_version": PIPELINE_VERSION, "ticket": ticket, "stages": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        return {
            "pipeline_version": PIPELINE_VERSION,
            "ticket": ticket,
            "stages": {},
            "_manifest_error": "corrupt_json",
        }
    return {"pipeline_version": PIPELINE_VERSION, "ticket": ticket, "stages": {}}


def save_manifest(ticket: str, manifest: dict[str, Any]) -> None:
    root = ticket_root(ticket)
    root.mkdir(parents=True, exist_ok=True)
    manifest.setdefault("pipeline_version", PIPELINE_VERSION)
    manifest.setdefault("ticket", ticket)
    manifest.setdefault("stages", {})
    path = artifact_path(ticket, ARTIFACTS["manifest"])
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def update_stage(
    ticket: str,
    stage: str,
    *,
    status: str,
    artifact: str | None = None,
    **extra: Any,
) -> None:
    manifest = load_manifest(ticket)
    entry: dict[str, Any] = {"status": status}
    if artifact:
        entry["artifact"] = artifact
    entry.update(extra)
    manifest.setdefault("stages", {})[stage] = entry
    save_manifest(ticket, manifest)


def review_iteration(ticket: str) -> int:
    manifest = load_manifest(ticket)
    review = manifest.get("stages", {}).get("review", {})
    iteration = review.get("iteration", 0)
    return int(iteration) if isinstance(iteration, (int, float, str)) else 0


def artifact_allowed_pattern(artifact: str) -> re.Pattern[str]:
    escaped = re.escape(artifact)
    return re.compile(rf"(?:^|/)\.dev-agent/[^/]+/{escaped}$")


def is_dev_agent_notes(path: str) -> bool:
    return bool(artifact_allowed_pattern(ARTIFACTS["dev_notes"]).search(normalize_path(path)))

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stage_status(ticket: str, stage: str) -> str | None:
    manifest = load_manifest(ticket)
    stage_entry = manifest.get("stages", {}).get(stage, {})
    if isinstance(stage_entry, dict):
        status = stage_entry.get("status")
        if isinstance(status, str):
            return status
    return None


def is_transient_error(code: str) -> bool:
    return code in TRANSIENT_ERROR_CODES


def validate_stage_artifact(ticket: str, stage: str) -> list[str]:
    if use_lean_artifacts(ticket):
        if not stage_is_complete(ticket, stage):
            return [f"pipeline.json: stages.{stage}.status not complete"]
        if stage in ("plan", "spec") and not plan_paths(ticket):
            return ["pipeline.json: missing stages.plan.paths or stages.spec.paths"]
        return []
    issues: list[str] = []
    artifact_name = STAGE_ARTIFACT.get(stage)
    if not artifact_name:
        return issues
    path = artifact_path(ticket, artifact_name)
    if not path.is_file():
        issues.append(f"missing: {path}")
    elif path.stat().st_size == 0:
        issues.append(f"empty: {path}")
    elif path.stat().st_size > ARTIFACT_SIZE_WARN_BYTES:
        issues.append(f"oversized: {path} ({path.stat().st_size} bytes)")
    return issues


def mark_stage_running(ticket: str, stage: str, *, artifact: str | None = None) -> None:
    if artifact is None and use_lean_artifacts(ticket):
        artifact_name = ARTIFACTS["manifest"]
    else:
        artifact_name = artifact or STAGE_ARTIFACT.get(stage)
    update_stage(
        ticket,
        stage,
        status="running",
        artifact=artifact_name,
        started_at=utc_now_iso(),
    )


def mark_stage_complete(
    ticket: str,
    stage: str,
    artifact: str | None = None,
    **extra: Any,
) -> None:
    if artifact is None and use_lean_artifacts(ticket):
        artifact_name = ARTIFACTS["manifest"]
    else:
        artifact_name = artifact or STAGE_ARTIFACT.get(stage)
    update_stage(
        ticket,
        stage,
        status="complete",
        artifact=artifact_name,
        completed_at=utc_now_iso(),
        **extra,
    )


def mark_stage_failed(
    ticket: str,
    stage: str,
    *,
    code: str,
    message: str,
    recoverable: bool = True,
    suggestions: list[str] | None = None,
    retry_count: int = 0,
    artifact: str | None = None,
) -> None:
    artifact_name = artifact or STAGE_ARTIFACT.get(stage)
    error: dict[str, Any] = {
        "code": code,
        "message": message,
        "recoverable": recoverable,
        "retry_count": retry_count,
        "suggestions": suggestions or [],
    }
    update_stage(
        ticket,
        stage,
        status="failed",
        artifact=artifact_name,
        completed_at=utc_now_iso(),
        error=error,
    )


def deny_missing_ticket(agent: str, stage: str) -> None:
    deny(
        f"{agent} blocked: no ticket id. Invoke as @{stage} {{ticket-id}}.",
        f"Stop. Ticket id required for @{stage}.",
    )
