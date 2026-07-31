# Accommodation booking audit

## Reconcile every night

Create one row for every overnight date:

| Night | Planned base | Booked property/area | Arrival method | Status |
|---|---|---|---|---|

Flag missing nights, duplicate bookings, date gaps, wrong towns, and bookings that force backtracking.

## Operational checks

- Correct check-in and check-out dates.
- Occupancy and bed configuration fit the group.
- Arrival before reception or self-check-in cutoff.
- Parking availability and vehicle restrictions.
- Breakfast or kitchen assumptions.
- Cancellation deadline and payment timing.
- Distance from the next morning's first activity.
- Exact navigation pin confirmed by the property or platform.

## Data minimisation

The group roadbook normally needs only:

- property display name;
- city or neighbourhood;
- map link;
- check-in window;
- parking/check-in note;
- a neutral internal label such as `Stay 04`.

Keep confirmation numbers, PINs, guest phone numbers, payment amounts, and full private-home addresses in a separate restricted document. Do not add them to a public site or repository.
