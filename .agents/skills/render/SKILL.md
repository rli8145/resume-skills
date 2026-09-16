---
name: render
description: Compile a resume .tex to PDF, verify it fills exactly one page (warn and suggest specific cuts if it overflows, or specific additions if it leaves the page underfilled), and place the output PDF in the designated directory. Use when asked to render, compile, build, export, or generate a PDF from a resume file, or to check whether a resume fits/fills one page.
---

# Render Resume

Compile and enforce the one-page target — not just "does it fit under a
page" but "does it fill it," in both directions: not just "did it
compile" but "does it fit, and if not, here's what to cut" — or "here's
what's missing," if it's short. See `AGENTS.md` for conventions.

## 1. Target and destination

Target: named file, role → `resumes/resume_<role>.tex`, or ask. Default
destination is `resumes/` (side by side with the source); use whatever
directory the user names instead, creating it if needed.

## 2. Compile

`python3 scripts/compile_check.py resumes/<file>.tex --output-dir
<destination>` (omit `--output-dir` for the `resumes/` default). Same
script `review` uses — JSON `errors`/`overfull`/`page_count`/
`bottom_whitespace_pt`, PDF copied to the destination, build junk
cleaned. Non-empty `errors` → stop and report; don't give a page verdict
on a broken compile.

## 3. Check page count and fill

- **>1 page** (or an oddly near-empty extra page): warn with the actual
  count, go to step 4a.
- **1 page, `bottom_whitespace_pt` > ~72** (an inch or more — the
  template's own bottom margin on a fully-packed page is ~44pt, so this
  is real slack, not just margin): warn with the actual value, go to
  step 4b.
- **1 page, `bottom_whitespace_pt` roughly ≤72**: report success with
  `pdf_path`.

## 4a. Over a page: propose specific cuts

Ranked, not generic advice:

1. **Overflow, not content**: each `overfull` entry names a source line
   range — usually one long bullet forcing an extra line. Cross-reference
   against `extract_bullets.py` to name it; a tightened reword may reclaim
   the page without cutting content.
2. **Weakest bullets** (`review`'s checklist, step 3): unquantified, weak
   verb, or redundant with a stronger neighbor — cheapest to cut/merge.
   Least-relevant/oldest if entries compete for space.
3. **Last resort**: spacing/margin tweaks (`\vspace`, `itemsep`) — flag,
   don't apply silently; cramped margins read worse than an honest cut.

Quote the actual bullet for each candidate.

## 4b. Underfilled: propose specific additions

The inverse — never pad with filler or invented claims:

1. **Restore commented-out content**: `extract_bullets.py` reports
   `active: false` bullets — master often has real, true bullets that
   were cut for a different variant; check if any apply here first.
2. **Add a second/third bullet to a thin entry**: an entry under the
   template's usual ~2 bullets while master has more true material for
   it.
3. **Widen scope slightly**: an older role/project in master that was
   left out only for space, not relevance.
4. **Last resort**: spacing tweaks in the other direction (`\vspace`,
   `itemsep`) — flag, don't apply silently; stretched spacing reads worse
   than genuine content.

If none of these have real material to add, say so explicitly rather
than inventing content or padding wording — an honestly short resume beats
a padded one.

## 5. Apply and confirm

Apply on confirmation (or the top-ranked minimal set if the user just
says "fix it"), recompile, and confirm it actually lands on a filled
single page — don't guess-and-stop.

## 6. Report

Final page count, `bottom_whitespace_pt`, output path(s), and what
changed if a cut or fill pass ran.
