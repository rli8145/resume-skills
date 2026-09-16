#!/usr/bin/env python3
"""
Extract every \\resumeItem{...} from a resume .tex, brace-balanced (so
nested \\textbf{}/\\href{}{} don't truncate one early), as JSON.

Usage:
  python3 scripts/extract_bullets.py resumes/resume_master.tex

Output:
  {"file", "count", "bullets": [{"line", "section", "heading", "active", "text"}, ...]}

active: false = inside \\iffalse or %-commented -- draft/cut, not rendered.
"""
import bisect
import json
import re
import sys
from pathlib import Path

TOKEN_RE = re.compile(
    r'\\section\{'
    r'|\\resumeSubheading\b'
    r'|\\resumeProjectHeading\b'
    r'|\\resumeItem\{'
    r'|\\iffalse\b'
    r'|\\fi\b'
)


def find_matching_brace(text, open_idx):
    """text[open_idx] must be '{'. Return the index of its matching '}', or -1."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        c = text[i]
        if c == '\\' and i + 1 < n:
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def extract(path):
    src = Path(path).read_text(encoding='utf-8')

    # Only scan the document body. The preamble defines these same macros
    # (\newcommand{\resumeSubItem}[1]{\resumeItem{#1}...} etc.) and those
    # definitions would otherwise be mistaken for real bullets/headings.
    body_start_match = re.search(r'\\begin\{document\}', src)
    body_offset = body_start_match.end() if body_start_match else 0

    line_starts = [0]
    for m in re.finditer('\n', src):
        line_starts.append(m.end())

    def line_number(char_offset):
        return bisect.bisect_right(line_starts, char_offset)

    bullets = []
    current_section = None
    current_heading = None
    iffalse_depth = 0

    for m in TOKEN_RE.finditer(src):
        start = m.start()
        if start < body_offset:
            continue  # preamble macro definitions, not real content
        tok = m.group()

        line_start = src.rfind('\n', 0, start) + 1
        line_prefix = src[line_start:start]
        is_percent_commented = line_prefix.lstrip().startswith('%')

        if tok == '\\iffalse':
            iffalse_depth += 1
            continue
        if tok == '\\fi':
            if iffalse_depth > 0:
                iffalse_depth -= 1
            continue

        if tok == '\\section{':
            close = find_matching_brace(src, m.end() - 1)
            if close != -1:
                current_section = src[m.end():close]
                current_heading = None
            continue

        if tok in ('\\resumeSubheading', '\\resumeProjectHeading'):
            brace_start = src.find('{', m.end())
            if brace_start != -1:
                close = find_matching_brace(src, brace_start)
                if close != -1:
                    current_heading = src[brace_start + 1:close].strip()
            continue

        if tok == '\\resumeItem{':
            open_idx = m.end() - 1
            close = find_matching_brace(src, open_idx)
            if close == -1:
                continue
            text = src[open_idx + 1:close]
            bullets.append({
                'line': line_number(start),
                'section': current_section,
                'heading': current_heading,
                'active': iffalse_depth == 0 and not is_percent_commented,
                'text': text.strip(),
            })

    return bullets


def main():
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'usage: extract_bullets.py <file.tex>'}))
        sys.exit(2)

    path = sys.argv[1]
    if not Path(path).exists():
        print(json.dumps({'error': f'file not found: {path}'}))
        sys.exit(1)

    bullets = extract(path)
    print(json.dumps({'file': path, 'count': len(bullets), 'bullets': bullets}, indent=2))


if __name__ == '__main__':
    main()
