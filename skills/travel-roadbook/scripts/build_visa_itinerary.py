#!/usr/bin/env python3
"""Build a concise, print-ready English visa itinerary from trip JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def build(data: dict) -> str:
    trip = data["trip"]
    stays = {stay["night"]: stay for stay in data.get("stays", [])}
    rows = []
    for day in data["days"]:
        sights = "; ".join(s["name"].split(" / ")[-1] for s in day.get("sights", []))
        title = day["title"].split(" / ")[-1]
        stay = stays.get(day["date"])
        accommodation = stay["name"] if stay else day["overnight"].split(" / ")[-1]
        rows.append(
            f"<tr><td>{esc(day['date'])}</td><td><b>{esc(title)}</b><br>{esc(sights)}</td>"
            f"<td>{esc(day['transport'].split(' / ')[-1])}</td><td>{esc(accommodation)}</td></tr>"
        )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{esc(trip["title"])} — Travel Itinerary</title><style>
@page{{size:A4;margin:14mm}}*{{box-sizing:border-box}}body{{font:10.5pt/1.42 Arial,sans-serif;color:#172825;margin:0}}
h1{{font:700 22pt/1.1 Georgia,serif;margin:0 0 4mm}}.meta{{margin-bottom:6mm;color:#4d5b57}}
table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #bdc8c3;padding:6px;vertical-align:top}}th{{background:#e8f0ec;text-align:left;font-size:9pt}}
td:first-child{{white-space:nowrap;width:19mm}}td:nth-child(3){{width:31mm}}td:nth-child(4){{width:39mm}}
.note{{margin-top:5mm;font-size:9pt;color:#53615d}}tr{{break-inside:avoid}}
</style></head><body><h1>Travel Itinerary</h1>
<div class="meta"><b>{esc(trip["title"])}</b><br>{esc(trip["start_date"])} to {esc(trip["end_date"])} · {esc(trip.get("travellers", "Travellers"))}</div>
<table><thead><tr><th>Date</th><th>Places and activities</th><th>Transport</th><th>Accommodation</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<p class="note">This itinerary is a concise summary for travel documentation. Live schedules and operating conditions remain subject to change.</p>
</body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build(data), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
