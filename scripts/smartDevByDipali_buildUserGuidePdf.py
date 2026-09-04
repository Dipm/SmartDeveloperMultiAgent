#!/usr/bin/env python3
"""Build SmartDeveloper-User-Guide.md from docs/source markdown."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "docs" / "source" / "SmartDeveloper-User-Guide.md"
OUTPUT = REPO_ROOT / "SmartDeveloper-User-Guide.md"
VENDOR = REPO_ROOT / "vendor_pdf"


def load_fpdf():
    if VENDOR.is_dir():
        sys.path.insert(0, str(VENDOR))
    from fpdf import FPDF  # type: ignore

    return FPDF


class GuidePDF:
    def __init__(self) -> None:
        FPDF = load_fpdf()
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", size=11)

    def write_line(self, text: str, *, style: str = "", size: int = 11) -> None:
        self.pdf.set_font("Helvetica", style=style, size=size)
        safe = text.encode("latin-1", errors="replace").decode("latin-1")
        self.pdf.multi_cell(0, 6, safe)
        self.pdf.ln(1)

    def code_block(self, lines: list[str]) -> None:
        self.pdf.set_font("Courier", size=8)
        width = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
        for line in lines:
            safe = line.encode("latin-1", errors="replace").decode("latin-1")
            if len(safe) <= 95:
                self.pdf.multi_cell(width, 4, safe)
            else:
                while safe:
                    self.pdf.multi_cell(width, 4, safe[:95])
                    safe = safe[95:]
        self.pdf.set_font("Helvetica", size=11)
        self.pdf.ln(2)

    def build(self, md: str) -> None:
        in_code = False
        code_lines: list[str] = []
        for raw in md.splitlines():
            line = raw.rstrip()
            if line.strip().startswith("```"):
                if in_code:
                    self.code_block(code_lines)
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue
            if in_code:
                code_lines.append(line)
                continue
            if not line.strip():
                self.pdf.ln(3)
                continue
            if line.startswith("# "):
                self.write_line(line[2:].strip(), style="B", size=16)
                continue
            if line.startswith("## "):
                self.write_line(line[3:].strip(), style="B", size=13)
                continue
            if line.startswith("### "):
                self.write_line(line[4:].strip(), style="B", size=11)
                continue
            if line.startswith("- [ ] "):
                self.write_line("[ ] " + line[6:].strip())
                continue
            if line.startswith("- [x] ") or line.startswith("- [X] "):
                self.write_line("[x] " + line[6:].strip())
                continue
            if line.startswith("- "):
                self.write_line("  * " + line[2:].strip())
                continue
            if line.startswith("|") and "---" not in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                self.write_line("  " + " | ".join(cells))
                continue
            if line.startswith("---"):
                self.pdf.ln(2)
                continue
            text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
            text = text.replace("**", "")
            text = text.replace("`", "")
            self.write_line(text)

    def save(self, path: Path) -> None:
        self.pdf.output(str(path))


def main() -> int:
    if not SOURCE.is_file():
        print(f"Missing source: {SOURCE}", file=sys.stderr)
        return 1
    md = SOURCE.read_text(encoding="utf-8")
    guide = GuidePDF()
    guide.build(md)
    guide.save(OUTPUT)
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
