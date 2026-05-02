#!/usr/bin/env python3
"""Validate required files/headings for OpenSpec cross-repo changes."""
from __future__ import annotations
import argparse
import pathlib
import re
import sys

PRODUCT_REQUIRED = {
    "intake.md": ["Raw request", "Problem hypothesis", "Unknowns"],
    "analysis.md": ["Problem", "Users / actors", "Current behavior", "Desired outcome", "Assumptions", "Open questions"],
    "options.md": ["Option A", "Option B", "Recommendation", "Tradeoffs"],
    "decision.md": ["Selected option", "Rationale", "Confidence"],
    "proposal.md": ["Why", "What changes", "Non-goals", "Success criteria"],
    "repo-impact.md": ["protobuf-repo", "server-backend", "server-frontend", "agent", "Cross-repo order", "Compatibility"],
    "tasks.md": ["Product gates", "Repo slices", "Integration"],
    "validation.md": ["End-to-end scenarios", "Compatibility checks", "Archive readiness"],
}

REPO_REQUIRED = {
    "proposal.md": ["Parent product change", "Implements requirements", "Local scope", "Out of scope", "Dependencies"],
    "design.md": ["Approach", "Code areas", "Contract dependencies", "Compatibility", "Tests", "Risks"],
    "tasks.md": ["Read parent product change", "Implement changes", "Add/update tests"],
    "validation.md": ["Unit tests", "Integration tests", "Evidence", "Archive readiness"],
}


def has_heading(text: str, heading: str) -> bool:
    pattern = r"^#{1,6}\s+" + re.escape(heading) + r"\s*$"
    return re.search(pattern, text, re.MULTILINE | re.IGNORECASE) is not None


def has_required_text(text: str, needle: str) -> bool:
    return has_heading(text, needle) or needle.lower() in text.lower()


def validate(root: pathlib.Path, mode: str) -> list[str]:
    required = PRODUCT_REQUIRED if mode == "product" else REPO_REQUIRED
    errors: list[str] = []
    for rel, headings in required.items():
        path = root / rel
        if not path.exists():
            errors.append(f"missing file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"empty file: {rel}")
            continue
        for heading in headings:
            if not has_required_text(text, heading):
                errors.append(f"{rel}: missing required text/heading '{heading}'")
    specs = root / "specs"
    if not specs.exists() or not list(specs.rglob("*.md")):
        errors.append("missing specs/**/*.md")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="OpenSpec change directory")
    ap.add_argument("--mode", choices=["product", "repo"], default="product")
    args = ap.parse_args()
    errors = validate(pathlib.Path(args.path), args.mode)
    if errors:
        print("OpenSpec validation failed:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1
    print("OpenSpec validation passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
