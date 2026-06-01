#!/usr/bin/env python3
import os
import sys
from docx import Document


def convert(readme_path, out_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    doc = Document()
    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            doc.add_paragraph('')
            continue
        if stripped.startswith('#'):
            # count heading level (#, ##, ### ...)
            level = len(stripped) - len(stripped.lstrip('#'))
            text = stripped.lstrip('#').strip()
            doc.add_heading(text, level=min(level, 4))
        else:
            doc.add_paragraph(stripped)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    readme = os.path.join(repo_root, 'README.md')
    out = os.path.join(repo_root, 'reports', 'README.docx')

    if not os.path.exists(readme):
        print(f"README not found at {readme}")
        sys.exit(2)

    convert(readme, out)
