#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph
AGENT = "pr-draft"
ALLOWED = re.compile(rf"(?:^|/)\.dev-agent/[^/]+/{re.escape(ph.ARTIFACTS['pr'])}$")
def main():
    data = ph.load_event(); ph.require_agent(data, AGENT)
    name = ph.tool_name(data); path = ph.path_of(data); cmd = ph.command_of(data)
    if cmd and ph.OPEN_PR_RE.search(cmd):
        ph.deny("PR-draft must not publish. Draft artifact only.", "Blocked publish command."); return
    if name in ph.WRITE_TOOLS:
        if path and ALLOWED.search(ph.normalize_path(path)): ph.allow(); return
        ph.deny("PR-draft may only write 08-pr.md.", "Blocked write."); return
    ph.allow()
if __name__ == "__main__": main()
