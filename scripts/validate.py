#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HTML = ROOT / "app" / "index.html"

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
    'STORAGE_KEY',
    'localStorage',
    'reset-demo',
    'decideApproval',
    'convertIdea',
    'data-action="idea-task"',
]
FORBIDDEN_MARKERS = [
    'data-view="architecture"',
    'SOURCECRAFT_TOKEN',
    '/home/clever',
    '/tmp/',
]


def openspec_cmd() -> list[str]:
    found = shutil.which('openspec')
    if found:
        return [found]
    return ['npx', '-y', '@fission-ai/openspec@latest']


def main() -> int:
    errors: list[str] = []

    text = HTML.read_text(encoding='utf-8')
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f'missing marker: {marker}')
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            errors.append(f'forbidden marker present: {marker}')

    cmd = openspec_cmd() + ['validate', '--changes', '--json']
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        errors.append('OpenSpec validation failed:\n' + (result.stderr.strip() or result.stdout.strip()))
    else:
        # Ensure JSON is parseable; OpenSpec may print a telemetry notice before JSON on first run,
        # so parse from the first object brace.
        out = result.stdout.strip()
        idx = out.find('{')
        if idx >= 0:
            try:
                data = json.loads(out[idx:])
                summary = data.get('summary', {})
                if summary.get('totals', {}).get('failed', 0):
                    errors.append('OpenSpec reported failed items')
            except Exception as exc:
                errors.append(f'OpenSpec JSON output was not parseable: {exc}')

    if errors:
        print('Validation failed:', file=sys.stderr)
        for err in errors:
            print(f'- {err}', file=sys.stderr)
        return 1
    print('Validation passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
