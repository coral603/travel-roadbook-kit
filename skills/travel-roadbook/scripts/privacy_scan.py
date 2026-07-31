#!/usr/bin/env python3
"""Scan shareable text files and filenames for common privacy leaks."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


TEXT_EXTENSIONS = {
    ".css", ".csv", ".html", ".js", ".json", ".md", ".py", ".svg",
    ".toml", ".ts", ".txt", ".yaml", ".yml",
}
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", "dist"}
PATTERNS = [
    (re.compile("/" + r"Users/[^/\s\"'<]+/"), "local macOS user path"),
    (re.compile(r"(?i)\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), "AWS access key"),
    (re.compile(r"(?i)\b(?:api[_ -]?key|token|secret|password|passwd|pin)\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{6,}"), "secret-like assignment"),
    (re.compile(r"\b1[3-9]\d{9}\b"), "possible mainland China phone number"),
    (re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"), "email address"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
]
SENSITIVE_NAMES = re.compile(
    r"(?i)(passport|confirmation|booking[_ -]?proof|voucher|invoice|receipt|private|secret|credential|订单|护照|确认单)"
)


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            yield Path(base) / name


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_files(root):
        relative = path.relative_to(root) if root.is_dir() else Path(path.name)
        if SENSITIVE_NAMES.search(path.name):
            findings.append(f"{relative}: sensitive filename")
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > 5_000_000:
                continue
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(content.splitlines(), 1):
            for pattern, label in PATTERNS:
                if pattern.search(line):
                    findings.append(f"{relative}:{line_number}: {label}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="File or folder to scan")
    args = parser.parse_args()
    findings = scan(args.path.resolve())
    if findings:
        print(f"FAILED: {len(findings)} possible privacy leak(s)")
        for finding in findings:
            print(f"- {finding}")
        print("Review every finding. False positives may be allowlisted only after manual inspection.")
        return 1
    print(f"OK: no common privacy patterns found in {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
