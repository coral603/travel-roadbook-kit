---
name: travel-roadbook
description: Plan, verify, revise, and publish executable independent-travel roadbooks from flights, traveller preferences, route ideas, and bookings. Use for multi-city or self-drive itinerary design, route-option comparison, real-map and seasonal feasibility checks, booking-location audits, bilingual daily plans, offline mobile roadbooks, print-ready visa itineraries, or privacy-safe trip handoffs.
---

# Travel Roadbook

Turn a rough travel idea into a decision-ready plan and then into an operational roadbook. Keep facts, assumptions, recommendations, and unverified items visibly separate.

## Choose the current stage

Identify the earliest unfinished stage and do not jump ahead:

1. **Intake** — essential constraints or fixed bookings are missing.
2. **Options** — travellers need to compare materially different route structures.
3. **Feasibility** — a preferred route exists but transport, maps, seasonality, or fatigue need checking.
4. **Booking-ready** — dates and overnight bases are stable enough to specify bookable legs.
5. **Booked-trip audit** — confirmations exist and must be reconciled with the itinerary.
6. **Publication** — content is approved and needs web, offline, print, or visa outputs.

If the user asks only for analysis, stop after the analysis. Do not edit or publish an existing roadbook until the user confirms the proposed changes.

## 1. Collect only decision-relevant inputs

Read [references/intake-questionnaire.md](references/intake-questionnaire.md). Ask a compact set of questions only for facts that could change the route: dates, entry/exit points, group, driving capacity, luggage, must-dos, walking level, budget, fixed bookings, and risk tolerance.

Extract dates and times from supplied tickets or confirmations, but label OCR-derived details as needing confirmation when the image is unclear. Never expose booking numbers, PINs, phone numbers, passport data, or private addresses in shared outputs.

## 2. Build route options around real trade-offs

Read [references/decision-framework.md](references/decision-framework.md). Create two or three genuinely different route structures, not cosmetic variations. For each option:

- define the transport logic and overnight bases;
- estimate transit load and difficult days;
- state what is gained and what is sacrificed;
- identify the main failure mode;
- recommend one option with reasons.

Use a comparison table or one-page visual when several people must decide together. Avoid false precision before live prices and schedules are checked.

## 3. Verify before calling a route feasible

Read [references/route-validation.md](references/route-validation.md). Use live primary sources and a real routing service whenever the answer depends on current schedules, seasonal roads, ferries, rental policies, or closures.

Verify each critical leg separately:

- map route and realistic driving time;
- ferry, train, flight, or cruise operating date;
- seasonal road status and daylight;
- trail conditions and weather fallback;
- pickup/return opening hours and one-way restrictions;
- enough buffer between separately booked services.

Record the check date, source link, confirmed fact, and remaining uncertainty. Do not describe a route as “verified” merely because the geography looks plausible.

## 4. Convert the preferred route into a bookable plan

Build one row per calendar day with:

- date and overnight base;
- transport mode and route;
- primary sights in visit order;
- approximate active time and transit time;
- meal or resupply constraints when relevant;
- weather fallback;
- booking action and deadline;
- risks or special notes.

Use bilingual labels when the travellers discuss the trip in one language but local navigation uses another. Preserve local spellings in map links.

For structured generation, copy `assets/trip-template.json` and complete it. Run:

```bash
python3 scripts/validate_trip.py path/to/trip.json
python3 scripts/build_roadbook.py path/to/trip.json --output roadbook.html
```

The roadbook generator creates a responsive, single-file HTML page with sticky navigation, active-section tracking, print styles, daily cards, and text map links. It does not fetch or embed third-party images.

## 5. Audit booked accommodation

Read [references/booking-audit.md](references/booking-audit.md). Reconcile every night against the daily plan. Check dates, city/area, arrival feasibility, cancellation deadline, room capacity, parking, late check-in, and route direction.

Keep the following layers separate:

- **private source pack** — original confirmations and personal details;
- **working register** — minimum booking data needed by the group;
- **public/shareable roadbook** — property name or area, navigation link, and operational notes only.

Never commit the private source pack to a repository.

## 6. Produce the right deliverable

Choose the smallest format that solves the need:

- **Decision brief** — compare route options before bookings.
- **Mobile roadbook** — operational daily reference for the travelling group.
- **Offline HTML** — resilient single-file copy for weak connectivity.
- **Print/PDF** — discussion, backup, or visa application.
- **Visa itinerary** — concise English table with dates, places, transport modes, sights, and accommodation; omit unnecessary rental and booking identifiers.

For a concise print-ready English itinerary, run:

```bash
python3 scripts/build_visa_itinerary.py path/to/trip.json --output visa-itinerary.html
```

Open the HTML in a browser and print to PDF. Keep claims consistent with actual tickets and accommodation confirmations.

## 7. Run QA and privacy checks

Read [references/roadbook-qa.md](references/roadbook-qa.md) and [references/privacy-rules.md](references/privacy-rules.md). Before handoff:

```bash
python3 scripts/privacy_scan.py path/to/shareable/folder
python3 scripts/validate_trip.py path/to/trip.json
```

Then manually test:

- sticky navigation remains visible;
- clicking a nav item updates its selected state;
- scrolling updates the selected state;
- every map link opens the intended place or route;
- every day has distinct, relevant content;
- mobile text is readable without horizontal scrolling;
- print/PDF has no clipped cards or blank pages;
- dates, overnight bases, and transport legs are continuous.

If publishing to GitHub, scan both the working tree and staged files. Treat Git history as public: removing a secret in a later commit is not sufficient.

## Resource routing

- Use [references/intake-questionnaire.md](references/intake-questionnaire.md) for first-contact questions.
- Use [references/decision-framework.md](references/decision-framework.md) for route comparisons.
- Use [references/route-validation.md](references/route-validation.md) for map, schedule, weather, and seasonal checks.
- Use [references/booking-audit.md](references/booking-audit.md) after bookings are supplied.
- Use [references/roadbook-qa.md](references/roadbook-qa.md) before delivery.
- Use [references/privacy-rules.md](references/privacy-rules.md) whenever material will be shared or published.
