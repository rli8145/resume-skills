---
name: proj-to-bullets
description: Draft resume project bullets from a GitHub repository. Use when the user pastes/links a GitHub repo URL (or owner/repo) and wants project bullets, a Projects-section entry, or portfolio copy drafted from it for a resume.
---

# GitHub Repo → Resume Bullets

1-3 `\resumeItem` bullets in this project's voice and template, grounded
only in what the repo actually shows. See `AGENTS.md` for conventions.

## 1. Gather repo data

Use `gh` (`gh repo view`, `gh api repos/<owner>/<repo>/languages`,
`.../readme`, `.../commits` — commits only to gauge scale/recency, not to
manufacture a metric): it's already authenticated and works the same in
any environment. If a `github` MCP server happens to be connected, it's
fine to use for the same data — a nice-to-have, not a dependency. Last
resort: a plain web fetch of the repo page (lower fidelity — say so).

## 2. Extract what's resume-worthy

From the README, manifests (`package.json`, `pyproject.toml`,
`requirements.txt`), and metadata: what it does (one sentence), the real
stack (from manifests/imports/languages API, not guessed), any metric the
README/benchmarks *explicitly state* (none stated → none used, ever), and
scale/effort signals (size, commits, solo vs. team) as phrasing context
only — never a bullet's actual metric.

## 3. Draft bullets

Match the existing macro pattern exactly (see any `\resumeProjectHeading`
in `resumes/resume_master.tex`):

```
\resumeProjectHeading
  {\href{<repo url>}
  {\textbf{<Project Name>}} $|$ \emph{<Language, Framework, Tool, ...>}}
  {}
        \resumeItemListStart
    \resumeItem{<bullet 1>}
    \resumeItem{<bullet 2, optional>}
        \resumeItemListEnd
```

Same bullet rules as `review`: strong verb, active voice, quantify only
with a real number from step 2 — no metric found means the bullet ships
without one, plus a note on what number would strengthen it.

## 4. Where it goes

Ask which file(s) (`resume_master.tex`, a variant, or both) and whether
it replaces or sits alongside an existing entry — check
`python3 scripts/extract_bullets.py resumes/<file>.tex` for an
`active: false` draft of this same project already there. Insert
following existing `\section{Projects}` ordering, then apply.

## 5. Compile-check

Run `review`'s compile-check (`.agents/skills/review/SKILL.md` step 2) —
a new entry is exactly the kind of change that pushes a variant past one
page.
