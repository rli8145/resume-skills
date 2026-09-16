---
name: tailor
description: Adapt a resume to a specific job posting — select and reword bullets from resume_master.tex to match a pasted or linked job posting, producing/updating a resume_<variant>.tex. Use when the user pastes a job posting/description, links to a job listing, or asks to tailor/adapt/customize their resume for a specific role or company.
---

# Tailor Resume to a Job Posting

Deliberate selection from the full bullet pool plus truthful rewording
toward the posting's language — not a generic rewrite. See `AGENTS.md`
for conventions.

## 1. Get the posting

Pasted text, or fetch a URL (web fetch, or `gh`/GitHub MCP if
GitHub-hosted) and pull just the role title, responsibilities,
requirements. Extract: level, must-have vs. nice-to-have skills,
emphasized domain, ATS keywords — and explicitly which requirements the
candidate's material does *not* support.

## 2. Pick a starting point

An existing variant close to the role family, if one is — it's already
curated. Otherwise `resumes/resume_master.tex` (the complete pool); never
start from a poor-match variant just because it exists. Ask whether the
result overwrites an existing variant or is a new file.

## 3. Select bullets

`python3 scripts/extract_bullets.py resumes/resume_master.tex` for the
full pool — check `active: false` bullets too, master has commented-out
content that may still fit this posting. Prioritize: matches a must-have
> quantified > recent. Stay within template density (~2 bullets/entry)
and the one-page target — but the target is a *filled* page, not just
one that doesn't overflow: cutting too aggressively leaves visible
blank space at the bottom, which reads as thin as a spilling-over
second page reads as bloated. When in doubt between including a
reasonably-relevant bullet or leaving space empty, include it — `render`
(step 4b) catches an underfilled result at the end regardless.

## 4. Reword

Mirror the posting's language. Add applicable tools and technologies listed in the posting to the Technical Skills section and to Projects and Experience bullets. To keep a reworded bullet within a target line count, use the `fit` skill (`.agents/skills/fit/SKILL.md`).

## 5. Write, then review

Preserve the shared template/preamble. Run `review`
(`.agents/skills/review/SKILL.md`) on the output — don't duplicate its
compile/overflow/bullet-quality checks here.

## 6. Report

Which bullets were included/excluded and why, any requirement not covered, and the output path.
