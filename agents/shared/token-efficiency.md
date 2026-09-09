# Token efficiency

Minimize reads and writes. Quality over verbosity.

## Read order

1. `instructions/contract.md`
2. Stage work file (`triage.md`, `research.md`, etc.)
3. `instructions/output.md`
4. **One** skill at a time — only when that step starts

Do not preload all skills. Do not re-read the full repo.

## Search discipline

- Use targeted `rg` / glob for specific symbols or paths.
- Read only files relevant to the current ticket.
- Prior-stage artifacts: read once, cite briefly — do not paste them wholesale.

## Artifact caps

- Lists (files, tickets, commits): max **15 items**, then "…and N more".
- Summarize tool output in ≤5 lines; never paste large logs into artifacts.
- Bullet summaries, not prose dumps.

## Per-stage caps

| Stage | Cap |
|---|---|
| context | Max 15 files in `02-context.md`; 2-line summary per file |
| plan | `paths` block = only files to edit; narrative ≤ 80 lines |
| dev | Only read plan `paths` + direct imports |
| review | Diff-focused; do not re-read entire context artifact |
| docs-pr | Pull from artifacts; do not re-research codebase |

## Artifact size

Keep each artifact under **50 KB**. If larger, trim lists and move detail to
referenced file paths instead of inline content.
