#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from hooks.lib import pipeline_hook as ph
AGENT = "pr-draft"
REQUIRED_PROD = (ph.ARTIFACTS["triage"], ph.ARTIFACTS["plan"], ph.ARTIFACTS["dev_notes"], ph.ARTIFACTS["tests"], ph.ARTIFACTS["review"])
REQUIRED_NON_PROD = (ph.ARTIFACTS["plan"], ph.ARTIFACTS["dev_notes"], ph.ARTIFACTS["tests"])
def main():
    data = ph.load_event(); ph.require_agent(data, AGENT)
    ticket = ph.ticket_id_from(data)
    if not ticket: ph.deny_missing_ticket("pr-draft", "pr-draft"); return
    required = REQUIRED_NON_PROD if ph.is_non_prod(ticket) else REQUIRED_PROD
    missing = ph.missing_prerequisites(ticket, required)
    if missing:
        ph.deny("PR-draft blocked: missing " + ", ".join(missing), "Stop. Run prior stages first."); return
    if ph.is_prod(ticket) and ph.review_sends_back(ticket, blocking_only=True):
        ph.deny("PR-draft blocked: blocking review findings.", "Stop. Resolve blocking review first."); return
    ph.allow()
if __name__ == "__main__": main()
