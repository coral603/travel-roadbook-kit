#!/usr/bin/env python3
"""Build a responsive, offline, single-file travel roadbook."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def link(url: str, label: str) -> str:
    if not url:
        return ""
    return f'<a class="button" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)} ↗</a>'


def build(data: dict) -> str:
    trip = data["trip"]
    days = data["days"]
    flights = data.get("flights", [])
    stays = {item["night"]: item for item in data.get("stays", [])}
    sources = data.get("sources", [])

    day_cards = []
    overview_rows = []
    for index, day in enumerate(days, 1):
        stay = stays.get(day["date"])
        sights = "".join(
            f"""<li><strong>{esc(sight["name"])}</strong>
            <span>{esc(sight.get("description", ""))}</span>
            {f'<small>{esc(sight["note"])}</small>' if sight.get("note") else ""}</li>"""
            for sight in day.get("sights", [])
        )
        stay_html = ""
        if stay:
            stay_html = f"""<div class="stay">
              <span class="eyebrow">当晚住宿 / Stay</span>
              <strong>{esc(stay["name"])}</strong>
              <span>{esc(stay["area"])}</span>
              {f'<small>{esc(stay["note"])}</small>' if stay.get("note") else ""}
              {link(stay.get("map_url", ""), "住宿导航 / Navigate")}
            </div>"""
        day_cards.append(f"""<article class="day-card" id="day-{index}">
          <header><span class="day-number">{index:02d}</span><div>
            <p>{esc(day["date"])}</p><h3>{esc(day["title"])}</h3>
          </div></header>
          <p class="summary">{esc(day["summary"])}</p>
          <dl><div><dt>交通 / Transport</dt><dd>{esc(day["transport"])}</dd></div>
          <div><dt>住宿区域 / Overnight</dt><dd>{esc(day["overnight"])}</dd></div></dl>
          <ul class="sights">{sights}</ul>
          <div class="notes">
            {f'<p><b>预订 / Booking</b>{esc(day["booking"])}</p>' if day.get("booking") else ""}
            {f'<p><b>备选 / Fallback</b>{esc(day["fallback"])}</p>' if day.get("fallback") else ""}
          </div>
          <div class="actions">{link(day.get("map_url", ""), "路线地图 / Route map")}</div>
          {stay_html}
        </article>""")
        overview_rows.append(
            f"<tr><td>{esc(day['date'][5:])}</td><td>{esc(day['title'])}</td>"
            f"<td>{esc(day['overnight'])}</td></tr>"
        )

    flight_cards = "".join(
        f"""<div class="mini-card"><b>{esc(item["date"])}</b>
        <span>{esc(item["route"])}</span><small>{esc(item.get("time", ""))} · {esc(item.get("note", ""))}</small></div>"""
        for item in flights
    ) or '<p class="muted">No fixed transport recorded.</p>'
    source_items = "".join(
        f'<li><a href="{esc(item["url"])}" target="_blank" rel="noopener">{esc(item["label"])}</a>'
        f'<small>checked {esc(item.get("checked_on", "date not recorded"))}</small></li>'
        for item in sources
    ) or "<li>No verification sources recorded.</li>"

    return f"""<!doctype html>
<html lang="{esc(trip.get("language", "en"))}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(trip["title"])}</title>
<style>
:root{{--ink:#18322f;--muted:#61716d;--cream:#f4f1ea;--paper:#fffdf8;--line:#d8ddd7;--accent:#e85d3f;--mint:#dcebe4;--nav-h:58px}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:calc(var(--nav-h) + 18px)}}
body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Noto Sans SC","PingFang SC",sans-serif}}
a{{color:inherit}}.wrap{{width:min(1040px,calc(100% - 32px));margin:auto}}
.hero{{padding:72px 0 58px;background:linear-gradient(135deg,#18322f,#315b52);color:white}}
.kicker,.eyebrow{{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;font-weight:750}}
h1{{font-family:Georgia,"Noto Serif SC",serif;font-size:clamp(2.35rem,7vw,5rem);line-height:1;margin:.18em 0}}
.hero p{{max-width:720px;color:#d8e5df;font-size:1.08rem}}.meta{{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}}
.meta span{{border:1px solid #ffffff40;border-radius:999px;padding:7px 12px}}
.nav{{position:sticky;top:0;z-index:20;background:#fffdf8ed;backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
.nav .wrap{{display:flex;overflow:auto;scrollbar-width:none}}.nav a{{min-height:var(--nav-h);display:grid;place-items:center;padding:0 18px;text-decoration:none;color:var(--muted);white-space:nowrap;border-bottom:3px solid transparent}}
.nav a.active{{color:var(--ink);border-bottom-color:var(--accent);font-weight:750}}
section{{padding:58px 0}}section h2{{font-family:Georgia,"Noto Serif SC",serif;font-size:clamp(1.8rem,5vw,3rem);line-height:1.1;margin:0 0 24px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.mini-card,.day-card,.panel{{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 8px 24px #18322f0a}}
.mini-card{{display:grid;gap:3px}}.mini-card span{{font-weight:700}}small,.muted{{color:var(--muted)}}
.table-wrap{{overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:18px}}table{{border-collapse:collapse;width:100%;min-width:620px}}td,th{{padding:13px 16px;text-align:left;border-bottom:1px solid var(--line)}}th{{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em}}
.days{{display:grid;gap:20px}}.day-card{{padding:clamp(18px,4vw,30px)}}.day-card header{{display:flex;gap:16px;align-items:center}}.day-card header p{{margin:0;color:var(--muted)}}.day-card h3{{font-size:clamp(1.25rem,4vw,1.75rem);line-height:1.25;margin:0}}
.day-number{{display:grid;place-items:center;flex:none;width:48px;height:48px;border-radius:50%;background:var(--accent);color:white;font-weight:800}}.summary{{font-size:1.06rem}}
dl{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}dl div,.stay{{display:grid;gap:3px;background:var(--mint);border-radius:13px;padding:14px}}dt{{color:var(--muted);font-size:.78rem;font-weight:700}}dd{{margin:0;font-weight:700}}
.sights{{padding:0;list-style:none;display:grid;gap:12px}}.sights li{{display:grid;gap:3px;border-left:3px solid var(--accent);padding-left:13px}}.notes b{{display:block;font-size:.78rem;color:var(--muted)}}.actions{{margin:18px 0}}
.button{{display:inline-flex;min-height:44px;align-items:center;padding:9px 14px;border-radius:999px;background:var(--ink);color:white;text-decoration:none;font-weight:700}}.stay .button{{justify-self:start;margin-top:8px}}
.sources{{display:grid;gap:10px;padding-left:20px}}.sources li small{{display:block}}footer{{padding:28px 0 80px;color:var(--muted);border-top:1px solid var(--line)}}
@media(max-width:650px){{.grid,dl{{grid-template-columns:1fr}}.wrap{{width:min(100% - 22px,1040px)}}section{{padding:42px 0}}.hero{{padding:52px 0 42px}}}}
@media print{{.nav,.button{{display:none!important}}body{{background:white;font-size:10pt}}.hero{{background:white;color:var(--ink);padding:20px 0}}.hero p{{color:var(--muted)}}section{{padding:20px 0}}.day-card,.mini-card,.panel{{box-shadow:none;break-inside:avoid}}}}
</style>
</head>
<body>
<header class="hero" id="top"><div class="wrap"><span class="kicker">Independent travel roadbook</span>
<h1>{esc(trip["title"])}</h1><p>{esc(trip.get("subtitle", ""))}</p>
<div class="meta"><span>{esc(trip["start_date"])} → {esc(trip["end_date"])}</span><span>{esc(trip.get("travellers", ""))}</span></div></div></header>
<nav class="nav" aria-label="Roadbook sections"><div class="wrap">
<a href="#overview">总览 / Overview</a><a href="#transport">交通 / Transport</a>
<a href="#days">每日 / Days</a><a href="#sources">核验 / Sources</a>
</div></nav>
<main>
<section id="overview" data-section><div class="wrap"><span class="eyebrow">At a glance</span><h2>每日要点 / Daily overview</h2>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Plan</th><th>Overnight</th></tr></thead><tbody>{''.join(overview_rows)}</tbody></table></div></div></section>
<section id="transport" data-section><div class="wrap"><span class="eyebrow">Fixed legs</span><h2>交通 / Transport</h2><div class="grid">{flight_cards}</div></div></section>
<section id="days" data-section><div class="wrap"><span class="eyebrow">Day by day</span><h2>每日行程 / Daily itinerary</h2><div class="days">{''.join(day_cards)}</div></div></section>
<section id="sources" data-section><div class="wrap"><span class="eyebrow">Verification log</span><h2>核验来源 / Sources</h2><div class="panel"><ul class="sources">{source_items}</ul></div></div></section>
</main><footer><div class="wrap">Generated with Travel Roadbook Kit. Recheck live schedules, access and weather before departure.</div></footer>
<script>
const links=[...document.querySelectorAll('.nav a')], sections=[...document.querySelectorAll('[data-section]')];
function setActive(id){{links.forEach(a=>{{const on=a.hash==='#'+id;a.classList.toggle('active',on);if(on)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')}});const active=links.find(a=>a.classList.contains('active'));active?.scrollIntoView({{block:'nearest',inline:'center'}})}}
links.forEach(a=>a.addEventListener('click',()=>setActive(a.hash.slice(1))));
let scheduled=false;
function updateFromScroll(){{scheduled=false;const marker=document.querySelector('.nav').offsetHeight+28;let current=sections[0];for(const section of sections){{if(section.getBoundingClientRect().top<=marker)current=section}}if(innerHeight+scrollY>=document.documentElement.scrollHeight-4)current=sections[sections.length-1];setActive(current.id)}}
addEventListener('scroll',()=>{{if(!scheduled){{scheduled=true;requestAnimationFrame(updateFromScroll)}}}},{{passive:true}});
addEventListener('hashchange',()=>{{const id=location.hash.slice(1);if(sections.some(s=>s.id===id))setActive(id)}});
setActive(location.hash.slice(1)||'overview');updateFromScroll();
</script></body></html>"""


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
