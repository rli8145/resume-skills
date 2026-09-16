#!/usr/bin/env python3
"""
Compile a resume with latexmk; report errors, overfull warnings, page
count, and bottom-of-page whitespace as JSON. Cleans build junk unless
--keep-junk.

Usage:
  python3 scripts/compile_check.py resumes/resume_master.tex
  python3 scripts/compile_check.py resumes/resume_swe.tex --output-dir ~/Desktop

Output:
  {"file", "success", "page_count", "errors": [...],
   "overfull": [{"detail", "lines": [start, end]}],
   "page_height_pt", "content_bottom_pt", "bottom_whitespace_pt", "pdf_path"}

bottom_whitespace_pt: blank space below the last line on the last page,
measured from the real PDF (~44pt is a fully-packed page's own margin;
much more means the page is underfilled).

Exit 0 on success (PDF produced, no errors) -- page count/whitespace are
reported here, not judged; that's the render skill's job.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ERROR_RE = re.compile(r'^! (.+)$', re.MULTILINE)
OVERFULL_RE = re.compile(
    r'Overfull \\[hv]box \(([^)]+)\) in paragraph at lines (\d+)--(\d+)'
)
PAGE_COUNT_RE = re.compile(r'Output written on .*?\((\d+) pages?')
BBOX_PAGE_RE = re.compile(r'<page width="[\d.]+" height="([\d.]+)">(.*?)</page>', re.DOTALL)
YMAX_RE = re.compile(r'yMax="([\d.]+)"')


def measure_page_fill(pdf_path):
    """How much blank space is below the last line of text on the last
    page, from the real PDF's own word bounding boxes — not estimated."""
    try:
        out = subprocess.run(
            ['pdftotext', '-bbox', str(pdf_path), '-'],
            capture_output=True, text=True, timeout=30,
        ).stdout
    except FileNotFoundError:
        return None
    pages = BBOX_PAGE_RE.findall(out)
    if not pages:
        return None
    page_height, last_page_body = pages[-1]
    ymaxes = [float(y) for y in YMAX_RE.findall(last_page_body)]
    if not ymaxes:
        return None
    content_bottom = max(ymaxes)
    page_height = float(page_height)
    return {
        'page_height_pt': round(page_height, 1),
        'content_bottom_pt': round(content_bottom, 1),
        'bottom_whitespace_pt': round(page_height - content_bottom, 1),
    }


def compile_and_check(tex_path, output_dir, keep_junk):
    src_dir = tex_path.parent
    stem = tex_path.stem

    try:
        proc = subprocess.run(
            ['latexmk', '-pdf', '-interaction=nonstopmode', tex_path.name],
            cwd=src_dir, capture_output=True, text=True, timeout=120,
        )
        combined_out = f'{proc.stdout}\n{proc.stderr}'
    except FileNotFoundError:
        return {'error': 'latexmk not found on PATH — is a TeX distribution installed?'}
    except subprocess.TimeoutExpired:
        return {'error': 'latexmk timed out after 120s'}

    log_path = src_dir / f'{stem}.log'
    log_text = log_path.read_text(errors='replace') if log_path.exists() else combined_out

    errors = [m.group(1).strip() for m in ERROR_RE.finditer(log_text)]
    overfull = [
        {'detail': m.group(1), 'lines': [int(m.group(2)), int(m.group(3))]}
        for m in OVERFULL_RE.finditer(log_text)
    ]
    page_match = PAGE_COUNT_RE.search(log_text)
    page_count = int(page_match.group(1)) if page_match else None

    pdf_path = src_dir / f'{stem}.pdf'
    pdf_exists = pdf_path.exists()
    success = pdf_exists and not errors
    result_pdf_path = str(pdf_path) if pdf_exists else None
    page_fill = measure_page_fill(pdf_path) if pdf_exists else None

    if pdf_exists and output_dir:
        out_dir = Path(output_dir).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / pdf_path.name
        if dest.resolve() != pdf_path.resolve():
            shutil.copy2(pdf_path, dest)
        result_pdf_path = str(dest)

    if not keep_junk:
        subprocess.run(
            ['latexmk', '-c', tex_path.name],
            cwd=src_dir, capture_output=True, text=True,
        )

    return {
        'file': str(tex_path),
        'success': success,
        'page_count': page_count,
        'errors': errors,
        'overfull': overfull,
        'page_height_pt': page_fill['page_height_pt'] if page_fill else None,
        'content_bottom_pt': page_fill['content_bottom_pt'] if page_fill else None,
        'bottom_whitespace_pt': page_fill['bottom_whitespace_pt'] if page_fill else None,
        'pdf_path': result_pdf_path,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('texfile', help='path to the .tex file to compile')
    ap.add_argument('--output-dir', default=None, help='copy the resulting PDF here too (default: leave it next to the .tex)')
    ap.add_argument('--keep-junk', action='store_true', help="don't clean .aux/.log/etc after compiling")
    args = ap.parse_args()

    tex_path = Path(args.texfile).resolve()
    if not tex_path.exists():
        print(json.dumps({'error': f'file not found: {args.texfile}'}))
        sys.exit(1)

    result = compile_and_check(tex_path, args.output_dir, args.keep_junk)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
