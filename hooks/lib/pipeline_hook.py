#!/usr/bin/env python3
"""Shared primitives for SmartDeveloper pipeline hook scripts."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

PIPELINE_VERSION = "1"

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


def review_sends_back(ticket: str) -> bool:
    verdict = review_verdict(ticket)
    if verdict == "clean":
        return False
    if verdict == "send_back":
        return True
    review = artifact_path(ticket, ARTIFACTS["review"])
    if not review.is_file():
        return True
    text = review.read_text(encoding="utf-8", errors="replace")
    blocking = re.search(
        r"## Blocking\s*\n([\s\S]*?)(?=\n## |\Z)", text, re.I
    )
    should_fix = re.search(
        r"## Should-fix\s*\n([\s\S]*?)(?=\n## |\Z)", text, re.I
    )
    for section in (blocking, should_fix):
        if not section:
            continue
        body = section.group(1).strip().lower()
        if body and body not in ("none.", "none", "- none."):
            return True
    return False


def plan_is_approved(ticket: str, data: dict[str, Any]) -> bool:
    sidecar = artifact_path(ticket, ARTIFACTS["plan_approved"])
    if sidecar.is_file():
        return True
    if APPROVAL_RE.search(blob(data)):
        return True
    manifest = load_manifest(ticket)
    plan = manifest.get("stages", {}).get("plan", {})
    return plan.get("status") == "approved"


def load_manifest(ticket: str) -> dict[str, Any]:
    path = artifact_path(ticket, ARTIFACTS["manifest"])
    if not path.is_file():
        return {"pipeline_version": PIPELINE_VERSION, "ticket": ticket, "stages": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
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
