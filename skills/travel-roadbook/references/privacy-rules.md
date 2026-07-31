# Privacy and publication rules

## Never publish

- passport, visa, identity-card, or birth-date data;
- booking confirmation numbers, PINs, ticket numbers, or loyalty accounts;
- phone numbers, personal email addresses, or payment details;
- full address of a private home or short-term rental;
- local filesystem paths or cloud-folder identifiers;
- session cookies, API keys, deployment tokens, or repository credentials;
- unredacted confirmation PDFs, screenshots, or spreadsheets.

## Usually safe after review

- public airport, station, hotel, and attraction names;
- city or neighbourhood of an overnight stay;
- public operator and map links;
- generic group description such as “four adults”;
- dates and route when the travellers accept that the itinerary itself is public.

Travel dates plus exact lodging can reveal an absence pattern. For a fully public example, shift dates and use fictional properties.

## Cleanroom publication

1. Create a new repository outside the private project.
2. Re-type reusable logic; do not copy the private folder wholesale.
3. Use synthetic travellers, bookings, and accommodation.
4. Avoid screenshots and third-party photos unless redistribution rights are clear.
5. Run automated scanning.
6. Inspect staged files and generated artifacts.
7. Commit only after the first six steps pass.

If a secret enters Git history, rotate/revoke it and rewrite or recreate the repository. A later deletion commit does not make it private again.
