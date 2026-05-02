#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "app" / "index.html"
CHANGE = ROOT / "openspec" / "changes" / "initial-cockpit"

REQUIRED_MARKERS = [
    'data-view="approvals"',
    'class="badge hot"',
    'approvals need decision',
    'OK',
    'Deny',
    'data-view="ideas"',
    'data-view="projects"',
    'data-view="tasks"',
    'Captured ideas',
    'Converted to tasks',
]
FORBIDDEN_MARKERS = [
    'data-view="architecture"',
    'SOURCECRAFT_TOKEN',
    '/home/clever',
    '/tmp/',
]


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"missing marker: {marker}")
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            errors.append(f"forbidden marker present: {marker}")

    openspec = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'validate-openspec-change.py'), str(CHANGE), '--mode', 'repo'],
        text=True,
        capture_output=True,
    )
    if openspec.returncode != 0:
        errors.append(openspec.stderr.strip() or openspec.stdout.strip())

    if errors:
        print('Validation failed:', file=sys.stderr)
        for err in errors:
            print(f'- {err}', file=sys.stderr)
        return 1
    print('Validation passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
