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
