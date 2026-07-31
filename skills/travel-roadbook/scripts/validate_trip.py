#!/usr/bin/env python3
"""Validate Travel Roadbook JSON without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse


PRIVATE_PATTERNS = [
    (re.compile("/" + r"Users/[^/\s]+/"), "local macOS user path"),
    (re.compile(r"(?i)\b(?:pin|password|passwd|secret|api[_ -]?key)\s*[:=]\s*\S+"), "secret-like field"),
    (re.compile(r"\b1[3-9]\d{9}\b"), "possible mainland China phone number"),
    (re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"), "email address"),
]


def parse_day(value: str, field: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        errors.append(f"{field} must be an ISO date (YYYY-MM-DD): {value!r}")
        return None


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def scan_strings(value: object, location: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            scan_strings(item, f"{location}.{key}", errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_strings(item, f"{location}[{index}]", errors)
    elif isinstance(value, str):
        for pattern, label in PRIVATE_PATTERNS:
            if pattern.search(value):
                errors.append(f"{location} contains {label}")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    trip = data.get("trip")
    days = data.get("days")
    if not isinstance(trip, dict):
        return ["trip must be an object"]
    if not isinstance(days, list) or not days:
        return ["days must be a non-empty array"]

    for field in ("title", "start_date", "end_date"):
        if not trip.get(field):
            errors.append(f"trip.{field} is required")

    start = parse_day(trip.get("start_date"), "trip.start_date", errors)
    end = parse_day(trip.get("end_date"), "trip.end_date", errors)
    if start and end and end < start:
        errors.append("trip.end_date must not be earlier than trip.start_date")

    seen_dates: list[date] = []
    for index, item in enumerate(days):
        path = f"days[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object")
            continue
        for field in ("date", "title", "overnight", "transport", "summary"):
            if not item.get(field):
                errors.append(f"{path}.{field} is required")
        parsed = parse_day(item.get("date"), f"{path}.date", errors)
        if parsed:
            seen_dates.append(parsed)
        if "map_url" in item and item["map_url"] and not valid_url(item["map_url"]):
            errors.append(f"{path}.map_url must be an http(s) URL")
        sights = item.get("sights", [])
        if not isinstance(sights, list):
            errors.append(f"{path}.sights must be an array")
        else:
            for sight_index, sight in enumerate(sights):
                if not isinstance(sight, dict) or not sight.get("name"):
                    errors.append(f"{path}.sights[{sight_index}].name is required")

    if seen_dates != sorted(seen_dates):
        errors.append("days must be sorted by date")
    if len(seen_dates) != len(set(seen_dates)):
        errors.append("days contain duplicate dates")
    if start and end:
        expected = []
        current = start
        while current <= end:
            expected.append(current)
            current += timedelta(days=1)
        missing = sorted(set(expected) - set(seen_dates))
        extra = sorted(set(seen_dates) - set(expected))
        if missing:
            errors.append("missing days: " + ", ".join(map(str, missing)))
        if extra:
            errors.append("days outside trip range: " + ", ".join(map(str, extra)))

    stays = data.get("stays", [])
    if not isinstance(stays, list):
        errors.append("stays must be an array")
    else:
        stay_nights: list[date] = []
        for index, stay in enumerate(stays):
            path = f"stays[{index}]"
            if not isinstance(stay, dict):
                errors.append(f"{path} must be an object")
                continue
            for field in ("night", "name", "area"):
                if not stay.get(field):
                    errors.append(f"{path}.{field} is required")
            parsed = parse_day(stay.get("night"), f"{path}.night", errors)
            if parsed:
                stay_nights.append(parsed)
            if stay.get("map_url") and not valid_url(stay["map_url"]):
                errors.append(f"{path}.map_url must be an http(s) URL")
        if len(stay_nights) != len(set(stay_nights)):
            errors.append("stays contain duplicate nights")

    for index, source in enumerate(data.get("sources", [])):
        if not isinstance(source, dict) or not valid_url(source.get("url", "")):
            errors.append(f"sources[{index}].url must be an http(s) URL")

    scan_strings(data, "$", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Trip JSON file")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {args.input} is structurally valid and passed basic privacy checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
