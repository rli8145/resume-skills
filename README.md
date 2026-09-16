some claude skills and accompanying python scripts I find useful for writing and tweaking $\LaTeX$ resumes

### skills (`.agents/skills/`)

- **review** - critique a resume (ATS parsability, bullet strength, ...)
- **xyz** - reword bullets with XYZ method
- **tailor** - adapt bullets to a job posting into a `resume_<variant>.tex`.
- **fit** - resize a bullet to a target line count
- **proj-to-bullets** - draft Projects bullets from a GitHub repo link
- **render** - compile to PDF and enforce a filled single page

### scripts (`scripts/`)

- **compile_check.py** - compile a `.tex` and report errors/overflow/page fill as JSON
- **extract_bullets.py** - dump every `\resumeItem` as JSON
- **check_bullet_lines.py** - report each bullet's exact rendered line count
