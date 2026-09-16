---
name: fit
description: Resize one or more resume bullets to a target rendered line-count range (e.g. "keep this to 2 lines", "get these between 2 and 3 lines", "this one's too long/short"). Use when the user gives a line-count constraint for a bullet, or says a bullet overflows/is too long/too short, for resume_master.tex or a resume_<variant>.tex file.
---

# Fit Bullets to a Line-Count Range

Tighten or expand bullet wording to land within a stated rendered-line
range — check-and-iterate against a real compile, not word-count
guessing. See `AGENTS.md` for conventions (strong verbs, quantify only
with real numbers, never invent).

## 1. Target

Which bullet(s), which file (`resumes/resume_<variant>.tex` or master),
and the range Y–Z lines (a single number means Y=Z). If the user pointed
at text rather than a line number, confirm which `\resumeItem` it is via
`python3 scripts/extract_bullets.py resumes/<file>.tex`.

## 2. Rewrite

- **Over Z lines**: cut filler and redundant words first (throat-clearing
  adjectives, restating the obvious), then weaker clauses — never drop
  the metric or the core claim. Preserve all LaTeX (`\textbf{}`,
  `\href{}{}`, math mode, etc.) exactly — cutting markup instead of prose
  is the easy mistake here.
- **Under Y lines** (rarer — usually wanted for visual balance against
  neighboring bullets): add real detail already established elsewhere
  (master may have a fuller version of this bullet, or the user has more
  specifics) — never invent a number or claim to pad length. If there's
  nothing true to add, say so instead of padding with filler.

## 3. Confirm, then apply

Show the before/after wording. Apply only after the user confirms.

## 4. Verify, and iterate if needed

`python3 scripts/check_bullet_lines.py resumes/<file>.tex --min-lines Y
--max-lines Z` — the *actual* rendered line count from a real compile.
If any targeted bullet still violates the range, go back to step 2 with
that measurement in hand (e.g. "still 1 line over" tells you how much
more to cut) rather than guessing again blind. Finish with
`compile_check.py` per `AGENTS.md` — a wording change is exactly the
kind of edit that can introduce overflow elsewhere.
