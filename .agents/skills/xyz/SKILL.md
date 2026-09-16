---
name: xyz
description: Reword resume bullets to follow the XYZ method ("Accomplished X, as measured by Y, by doing Z"). Use when the user asks to rewrite/reword/tighten bullets, apply the XYZ method/formula, or make bullets more results-oriented, for resume_master.tex or a resume_<variant>.tex file.
---

# XYZ-Method Bullet Rewriting

Rewrite bullets into X (accomplishment) / Y (metric proving it) / Z
(method used) — without inventing anything the bullet or user didn't
already establish. Unlike `review`, this applies edits, not just flags.
See `AGENTS.md` for conventions.

## 1. Target

Named file, role → `resumes/resume_<role>.tex`, or ask if ambiguous. If
the user pointed at specific bullets, touch only those.

## 2. Decompose into X / Y / Z

`python3 scripts/extract_bullets.py resumes/<file>.tex`. For each
**active** bullet in scope:

- **X**: the actual outcome, not the task ("reduced latency", not "worked
  on latency").
- **Y**: the number proving X mattered (%, time, scale, rank, $) — usually
  the missing piece.
- **Z**: the technique/tool used — usually already well covered.

Note what's present, weak, or absent before touching anything.

## 3. Rewrite with real material only

- All three present/recoverable: restructure into a tight sentence in
  house style (lead with a strong verb — "Reduced X by Y% via Z" is
  functionally XYZ; don't force the literal "Accomplished X, as measured
  by Y, by doing Z" wording onto every bullet). Preserve all LaTeX.
- **Y missing** (common): never invent a metric. Propose the rewrite with
  a bracketed placeholder and ask for the real number; offer to leave it
  unquantified if there isn't one.
- **X vague** ("helped with", "worked on"): name the actual outcome using
  only what's already stated in the bullet or elsewhere in the project
  (e.g. master may have a fuller version) — don't guess at scope.
- **Z missing/generic**: only add specifics already stated for that
  role/project; ask rather than guess a tool.
- **Line-length target** (e.g. "keep this to 2 lines"): that's the `fit`
  skill (`.agents/skills/fit/SKILL.md`) — use it directly, or apply it
  after this rewrite if the result still isn't the right length.

## 4. Confirm, then apply

Show before/after with a one-line reason. Apply only after the user
confirms (whole file or per-bullet) — don't rewrite unasked.

## 5. Compile-check

Follow `review`'s compile-check (`.agents/skills/review/SKILL.md` step
2) on the changed file — a rewrite is exactly the kind of edit that can
introduce overflow.
