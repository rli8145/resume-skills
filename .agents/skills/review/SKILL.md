---
name: review
description: Critique a resume .tex file in this project (master or a role variant) for ATS parsability, bullet strength, quantification, consistency with other variants, and compile/overflow issues. Use when the user asks to review, critique, check, or grade a resume file, or asks "is this resume good", before/after tailoring a variant, or wants typos/inconsistencies caught across resume_*.tex files.
---

# Resume Review

A brutally honest, specific critique — a line-by-line pass over what's actually
written, not generic resume advice. See `AGENTS.md` for layout/conventions.

## 1. Target

Named file, or map a role mention to `resumes/resume_<role>.tex`; default
to `resumes/resume_master.tex` if that's the obvious meaning; ask if not.
If the target is a variant, also read `resumes/resume_master.tex` (needed
for step 4).

## 2. Compile check

`python3 scripts/compile_check.py resumes/<file>.tex` → JSON: `errors`
(must-fix), `overfull` (each `Overfull \hbox`/`\vbox` with its source line
range), `page_count`, `bottom_whitespace_pt`. Flag over 1 page unless the
content justifies it — a judgment call, not an automatic fail. Also flag
1 page with `bottom_whitespace_pt` well over ~72 (the template's own
bottom margin on a fully-packed page is ~44pt) — an underfilled page is
as much an issue as an overflowing one here. If the user wants either
actually fixed, that's the `render` skill's job (step 4a/4b). Every skill
that compiles a resume uses this script — never freehand `latexmk` or
hand-parse a `.log`.

## 3. Bullet-by-bullet

`python3 scripts/extract_bullets.py resumes/<file>.tex` → each
`\resumeItem` (brace-balanced) with line, section, heading, and `active`
(`false` = commented-out/`\iffalse` — draft content, not a live issue).
For each **active** bullet, and across the set, check:

- **Weak verbs/filler**: "responsible for", "worked on", "helped with",
  "involved in", "in charge of", "participated in" → should be a concrete
  action verb (Built, Reduced, Shipped, Led, Optimized, ...).
- **Passive voice** where active would be stronger.
- **Missing quantification**: no number (%, time, scale, latency,
  accuracy)? Flag it — ask the user for a real metric, never suggest
  inventing one.
- **Verb repetition**: same leading verb 3+ times → flag, suggest variety.
- **Tense**: past for past roles, present only for genuinely ongoing ones;
  flag mixing within a role.
- **Jargon**: dense with unexplained acronyms a recruiter skim won't
  parse — flag, don't auto-rewrite.
- **Length outliers**: a bullet much longer than its neighbors (often the
  same one flagged `overfull` in step 2). For exact rendered line counts
  per bullet — not just the rare overfull case — run
  `python3 scripts/check_bullet_lines.py resumes/<file>.tex` (add
  `--min-lines`/`--max-lines` for an explicit violations list). The `fit`
  skill (`.agents/skills/fit/SKILL.md`) can then resize a flagged bullet
  toward a target — this skill reviews, it doesn't fix.
- **Typos**: read closely — this project has typos that got fixed in some
  variants but not others (e.g. "contexual" → "contextual"). For a
  variant, diff its bullets against master's for fixes present in one but
  not the other, either direction.

## 4. Cross-file consistency (variants only)

Vs. `resumes/resume_master.tex` and sibling variants: same fact (company,
dates, metric) stated differently — flag, or fix if it's an obvious typo;
formatting drift (dates, header order, capitalization) with no reason.

## 5. ATS check

Already reasonably safe (plain sections, no tables, `\pdfgentounicode=1`).
Confirm: no content relies purely on an icon/glyph for meaning; contact
info is real text not an image; section headers use conventional names.

## 6. Output

Grouped by severity — **must-fix** (errors, factual inconsistencies,
typos), **should-fix** (weak verbs, missing metrics, tense, overflow),
**consider** (verb variety, jargon, length). Quote the specific bullet for
each, give a concrete fix or the question to ask if a fact/metric is
missing. Don't rewrite the file — this skill reviews, it doesn't edit.

Offer to save to `resumes/reviews/<basename>-<YYYY-MM-DD>.md` (only if the
user says yes).
