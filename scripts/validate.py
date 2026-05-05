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
    'data-view="inbox"',
    'class="badge hot"',
    'inbox items need attention',
    'OK',
    'Deny',
    'data-view="ideas"',
    'data-view="projects"',
    'data-view="tasks"',
    'data-view="workflow"',
    'data-view="activity"',
    'data-view="schedules"',
    'Activity log',
    'activity-list',
    'schedule-list',
    'renderSchedules',
    'Idea → Project → Task lifecycle',
    'Approved idea → draft project',
    'Task = next action',
    'Schedules run by default',
    'Normal schedules run directly',
    'Captured ideas',
    'Converted to tasks',
    'STORAGE_KEY',
    'THEME_KEY',
    'currentTheme',
    'setTheme',
    'localStorage',
    'reset-demo',
    'decideApproval',
    'convertIdea',
    'data-action="idea-task"',
    'data-action="task-confirm"',
    'data-action="task-cancel"',
    '/api/state',
    '/api/approvals/decide',
    '/api/ideas/transition',
    'apiAvailable',
    'clever-cockpit-token',
]
SERVER_MARKERS = [
    'ThreadingHTTPServer',
    'sqlite3',
    'CLEVER_COCKPIT_TOKEN',
    '/api/state',
    'cron_schedules',
    'jobs-state.json',
    '/api/approvals/ready',
    '/api/approvals/complete',
    '/api/approvals',
    '/api/ideas/transition',
    'run_status',
    'payload_json',
    'redact_token',
]
RUNNER_MARKERS = [
    'handle_approval',
    'HANDLERS',
    'record_only',
    'idea_review',
    'telegram_send_and_pin_digest',
    'sourcecraft_publish',
    'digest_publish_and_send',
    '/api/approvals/ready',
    '/api/approvals/complete',
    'needs_handler',
    'resolve_path',
]
CREATE_APPROVAL_MARKERS = [
    '/api/approvals',
    'digest_publish_and_send',
    'telegram_send_and_pin_digest',
    'approval_created',
]
CREATE_IDEA_MARKERS = [
    '/api/ideas',
    '--approval',
    'idea_created',
    'idea_review',
    'approval_created',
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

    server_text = (ROOT / 'server' / 'cockpit_server.py').read_text(encoding='utf-8')
    for marker in SERVER_MARKERS:
        if marker not in server_text:
            errors.append(f'missing server marker: {marker}')
    runner_text = (ROOT / 'scripts' / 'approval_runner.py').read_text(encoding='utf-8')
    for marker in RUNNER_MARKERS:
        if marker not in runner_text:
            errors.append(f'missing runner marker: {marker}')
    create_approval_text = (ROOT / 'scripts' / 'create-cockpit-approval.py').read_text(encoding='utf-8')
    for marker in CREATE_APPROVAL_MARKERS:
        if marker not in create_approval_text:
            errors.append(f'missing create approval marker: {marker}')
    create_idea_text = (ROOT / 'scripts' / 'create-cockpit-idea.py').read_text(encoding='utf-8')
    for marker in CREATE_IDEA_MARKERS:
        if marker not in create_idea_text:
            errors.append(f'missing create idea marker: {marker}')
    py_files = [ROOT / 'server' / 'cockpit_server.py'] + sorted((ROOT / 'scripts').glob('*.py'))
    py_compile = subprocess.run([sys.executable, '-m', 'py_compile', *map(str, py_files)], cwd=ROOT, text=True, capture_output=True)
    if py_compile.returncode != 0:
        errors.append('server py_compile failed:\n' + (py_compile.stderr.strip() or py_compile.stdout.strip()))

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
