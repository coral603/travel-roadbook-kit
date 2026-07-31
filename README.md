# Travel Roadbook Kit

A privacy-first Codex Skill and small set of deterministic tools for turning flights, group preferences, route ideas, and bookings into a verified travel roadbook.

It is designed for the difficult middle of trip planning: comparing route structures, checking whether a plan works on real maps and real dates, reconciling booked accommodation, and publishing a mobile-friendly offline guide.

## What it includes

- `travel-roadbook` Skill with an end-to-end planning workflow
- route comparison and verification checklists
- booking-location audit and privacy rules
- JSON trip template and anonymous Norway example
- responsive single-file roadbook generator
- concise English visa-itinerary generator
- trip-data validator and repository privacy scanner

## What it does not do

It does not guarantee live availability, prices, road openings, weather, or visa approval. Those facts must be checked against current primary sources. It also deliberately avoids embedding third-party photographs or private confirmation documents.

## Install the Skill

Copy `skills/travel-roadbook` into your Codex skills folder, or install it from this repository with the Codex skill installer.

Then ask:

> Use $travel-roadbook to compare two feasible routes for my trip and tell me what information is still missing.

## Generate the anonymous demo

```bash
cd skills/travel-roadbook
python3 scripts/validate_trip.py ../../examples/norway-demo-anonymized/trip.json
python3 scripts/build_roadbook.py ../../examples/norway-demo-anonymized/trip.json \
  --output ../../examples/norway-demo-anonymized/roadbook.html
python3 scripts/build_visa_itinerary.py ../../examples/norway-demo-anonymized/trip.json \
  --output ../../examples/norway-demo-anonymized/visa-itinerary.html
```

Open the generated HTML files locally. Use the browser's print dialog when a PDF is needed.

## Privacy model

The public example uses synthetic travellers, properties, and booking labels. Do not place original confirmations, passport data, PINs, phone numbers, private-home addresses, local computer paths, or deployment credentials in this repository.

Before committing:

```bash
python3 skills/travel-roadbook/scripts/privacy_scan.py .
git diff --cached
```

The scanner catches common patterns, but it cannot understand every secret. Human review remains required.

## Data format

Start from `skills/travel-roadbook/assets/trip-template.json`. The required core is:

- trip title and date range
- one record for every calendar day
- overnight base and transport mode for each day
- map links using public place names
- optional flights, stays, and verification sources

The validator checks dates, daily coverage, stay alignment, URLs, and common privacy leaks.

## License

MIT. Public map and operator links remain subject to their providers' terms. No third-party photographs are included.
