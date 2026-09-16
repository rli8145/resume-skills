#!/usr/bin/env python3
"""
Report each \\resumeItem's actual rendered line count, from a real
compile — reads TeX's own \\prevgraf, not a char-count estimate.

Usage:
  python3 scripts/check_bullet_lines.py resumes/resume_master.tex
  python3 scripts/check_bullet_lines.py resumes/resume_master.tex --min-lines 2 --max-lines 3

Output (JSON):
  {"file", "success", "bullet_count_ok",
   "bullets": [{"index", "section", "heading", "source_line",
                "rendered_lines", "text"}, ...],
   "violations": [...] (only with --min-lines/--max-lines)}

bullet_count_ok: false means the count didn't match extract_bullets.py's
active-bullet count -- treat results as unreliable.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_bullets import extract as extract_bullets  # noqa: E402

INJECTION = r"""
\makeatletter
\let\resumeItem@orig\resumeItem
\renewcommand{\resumeItem}[1]{%
  % \message, not \typeout: \typeout is built on \write, whose argument
  % isn't expanded until the whatsit is later processed (by then
  % \prevgraf has reset) -- \message reads \prevgraf synchronously.
  \setbox0=\hbox{\parbox{\linewidth}{\small #1\par\message{BULLETLINES:\the\prevgraf}}}%
  \resumeItem@orig{#1}%
}
\makeatother
"""

BULLETLINES_RE = re.compile(r'BULLETLINES:(\d+)')


def instrument(src_text):
    m = re.search(r'\\begin\{document\}', src_text)
    if not m:
        raise ValueError(r'no \begin{document} found')
    return src_text[:m.end()] + INJECTION + src_text[m.end():]


def compile_instrumented(tex_path, tmpdir):
    fixture_path = tmpdir / tex_path.name
    fixture_path.write_text(instrument(tex_path.read_text(encoding='utf-8')), encoding='utf-8')
    proc = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', fixture_path.name],
        cwd=tmpdir, capture_output=True, text=True, timeout=60,
    )
    log_path = tmpdir / f'{tex_path.stem}.log'
    log_text = log_path.read_text(errors='replace') if log_path.exists() else (proc.stdout + proc.stderr)
    pdf_ok = (tmpdir / f'{tex_path.stem}.pdf').exists()
    return log_text, pdf_ok


def check(tex_path, min_lines=None, max_lines=None):
    with tempfile.TemporaryDirectory() as td:
        log_text, pdf_ok = compile_instrumented(tex_path, Path(td))

    rendered = [int(c) for c in BULLETLINES_RE.findall(log_text)]
    active_bullets = [b for b in extract_bullets(str(tex_path)) if b['active']]

    bullets = [
        {
            'index': i,
            'section': b['section'],
            'heading': b['heading'],
            'source_line': b['line'],
            'rendered_lines': lines,
            'text': b['text'],
        }
        for i, (b, lines) in enumerate(zip(active_bullets, rendered))
    ]

    violations = [
        b for b in bullets
        if (max_lines is not None and b['rendered_lines'] > max_lines)
        or (min_lines is not None and b['rendered_lines'] < min_lines)
    ] if (min_lines is not None or max_lines is not None) else []

    return {
        'file': str(tex_path),
        'success': pdf_ok,
        'bullet_count_ok': len(rendered) == len(active_bullets),
        'bullets': bullets,
        'violations': violations,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('texfile', help='path to the .tex file to check')
    ap.add_argument('--max-lines', type=int, default=None, help='flag any bullet rendering to more lines than this')
    ap.add_argument('--min-lines', type=int, default=None, help='flag any bullet rendering to fewer lines than this')
    args = ap.parse_args()

    tex_path = Path(args.texfile).resolve()
    if not tex_path.exists():
        print(json.dumps({'error': f'file not found: {args.texfile}'}))
        sys.exit(1)

    try:
        result = check(tex_path, min_lines=args.min_lines, max_lines=args.max_lines)
    except ValueError as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
    except FileNotFoundError:
        print(json.dumps({'error': 'pdflatex not found on PATH'}))
        sys.exit(1)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result['success'] and not result['violations'] else 1)


if __name__ == '__main__':
    main()
