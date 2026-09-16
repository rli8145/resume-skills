# Resume Editor

Agentic workspace for maintaining/tailoring LaTeX resumes. "Correct"
means: compiles cleanly, fills one page (not visibly underfilled), and
is honest. Read this file first (see "Working across agents" below).

## Setup

`scripts/` is pure Python 3 stdlib but shells out to:

- **A TeX distribution** (`latexmk`, `pdflatex`) — macOS:
  `brew install --cask mactex-no-gui` (or smaller `basictex` +
  `tlmgr install <pkg>` as needed).
- **Poppler** (`pdftotext -bbox`, for page-fill measurement) —
  `brew install poppler`.

Verify: `latexmk -v && pdflatex -v && pdftotext -v`.

## Layout

- `resumes/` — sources and PDFs, side by side.
  - `resume_master.tex` — every bullet ever written; source of truth
    for content, not meant to ship as-is.
  - `resume_<variant>.tex` (`ml`, `quant`, `swe`) — hand-forked subsets
    of master, reworded per role. Can drift from master — check when
    fixing a shared typo.
  - `reviews/` — dated reports from the `review` skill.
  - Template: "Jake's Resume" (`\resumeItem`, `\resumeSubheading`,
    `\resumeProjectHeading`). Section order: Education, Technical
    Skills, Honors & Awards, Experience, Projects.
- `docs/` — supporting docs, not resumes.
- `.agents/skills/<name>/SKILL.md` — capability definitions.
- `scripts/` — deterministic helpers; use these instead of freehanding
  `latexmk` or eyeballing `.tex` (nested braces make that error-prone):
  - `compile_check.py <file>.tex` — errors/overfull/page_count/
    `bottom_whitespace_pt` as JSON, measured from the real PDF (not
    estimated). ~44pt = filled one-pager; >~72pt means real slack.
  - `extract_bullets.py <file>.tex` — every `\resumeItem` → JSON.
  - `check_bullet_lines.py` — rendered line count per bullet via TeX's
    `\prevgraf`; `--min-lines`/`--max-lines` for violations.
  - `fit` chains these: write → measure → reword → re-measure.

  Judgment calls (weak verbs, posting match, what to cut) stay in the
  skills — only the mechanical parts are scripted.

## Conventions

- Don't touch the shared preamble/macros for non-formatting changes.
- Past tense for past roles, present for ongoing ones. Strong verbs —
  no "responsible for"/"helped"/"worked on". Real numbers only, never
  invented.
- After any `.tex` edit, run `compile_check.py` (and `extract_bullets.py`
  to read bullets back) rather than hand-checking.
- For GitHub, prefer `gh` (authenticated, portable) over the `github`
  MCP server (fine, but session-bound); web fetch is last resort.
- Commit logical chunks with clear messages.

## Capabilities

Read `.agents/skills/<name>/SKILL.md` before acting on one — don't
improvise from memory:

- **`review`** — critique a resume (ATS, bullet strength,
  quantification, consistency, compile/overflow).
- **`xyz`** — reword bullets into XYZ (accomplishment/metric/method);
  asks for a real number rather than inventing one.
- **`tailor`** — select + reword bullets against a job posting into a
  `resume_<variant>.tex`.
- **`fit`** — resize a bullet to a target line-count range.
- **`proj-to-bullets`** — draft Projects bullets from a GitHub repo.
- **`render`** — compile to a target directory, enforce a filled single
  page, propose ranked cuts/additions.

The other five reuse `review`'s compile-check step instead of
duplicating it.

## Working across agents

Only two cross-tool formats are kept: `AGENTS.md` (native to Codex CLI,
Cursor, Copilot, Windsurf) and `.agents/skills/` (open `SKILL.md`
format, also Codex-native). No per-tool adapters (`CLAUDE.md`,
`.claude/`) — an unsupported tool can just be told to read these
directly.

If skills are ever symlinked elsewhere, symlink at the **file** level
only (`SKILL.md -> ...`), never a whole `skills` directory — a
directory symlink once caused a recursive clean of `.claude/` to delete
the real files.

To add a capability: write `.agents/skills/<name>/SKILL.md` and list it
above. Nothing else required.
