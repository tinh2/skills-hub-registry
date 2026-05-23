---
name: str-dynamic-pricing
description: Dynamic pricing engine for short-term rentals (Airbnb, VRBO, Booking.com, Direct) — sets nightly rates based on a comp set (40+ filters: bedrooms, bathrooms, amenities, location radius, rating tier), seasonality patterns (weekly + monthly + annual cycles per market), local events (concerts, conferences, sports), lead-time demand curves (60+ day, 30-day, last-minute), booking pace (year-over-year same-day-of-week), gap-night and orphan-night pricing, minimum-stay enforcement, and your property's historical performance. Integrates with PriceLabs, Beyond Pricing, Wheelhouse APIs OR runs as a standalone Python engine pulling AirDNA / Rabbu / Mashvisor market data. Generates: rate calendar (next 365 days), price-change explanation per night, occupancy + ADR + RevPAR forecasts, and a weekly performance report vs comp set. TRIGGER on "Airbnb pricing", "VRBO pricing", "vacation rental pricing", "STR revenue management", "dynamic pricing", "PriceLabs", "Beyond Pricing", "Wheelhouse", "RevPAR", "ADR", "occupancy optimization", "smart pricing".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Short-Term Rental Dynamic Pricing Engine

You generate nightly rates for STR listings. Flat-rate pricing in 2026 leaves measurable revenue on the table (industry data: dynamic-priced listings outperform flat-priced comparables by 20-40% on RevPAR). The discipline is reading the market — not just the calendar.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Property data**: bedrooms, bathrooms, sleeps capacity, amenities (pool, hot tub, EV charger, pet-friendly, A/C), location (lat/lng), photos count, listing age, current rating + review count.
- [ ] **Market**: city/region. Drives the comp set + event calendar.
- [ ] **Existing channels**: which OTAs are connected? PMS / channel manager (Hostaway, Hospitable, Guesty, OwnerRez)?
- [ ] **Cost floor**: minimum acceptable per-night rate (covers cleaning + utilities + minimal margin). Below this, the system blocks bookings rather than discount.
- [ ] **Historical data**: 6-12 months of booking history if available. Without it, defaults are softer (more comp-set weight, less property-history weight).
- [ ] **Pricing tool**: integrate with PriceLabs/Beyond/Wheelhouse OR run standalone.

Recovery:

- New listing (< 6 months): weight comp set + market data 80%, property history 20%. Be more aggressive on initial discount to build review count.
- No PMS integration: generate a rate calendar CSV that the user imports manually.

============================================================
=== PHASE 1: COMP SET DEFINITION ===
============================================================

Build the comparable property set with these filters:

| Filter               | Default                                                 |
| -------------------- | ------------------------------------------------------- |
| Geographic radius    | 1.5 miles (urban), 5 miles (suburban), 15 miles (rural) |
| Bedrooms             | Exact match OR ±1 (penalize 1-off variants)             |
| Bathrooms            | Exact OR +1                                             |
| Property type        | Same (SFR / condo / cabin / townhouse)                  |
| Pool                 | Match required if subject has pool                      |
| Hot tub              | Match required if subject has hot tub                   |
| Pet-friendly         | Match required if subject is pet-friendly               |
| Beachfront/lakefront | Match required if subject is waterfront                 |
| Rating               | ≥ 4.5 stars (top quartile) for premium comping          |
| Review count         | ≥ 25 (filters new/unscored properties)                  |
| Listing age          | ≥ 12 months (mature properties only)                    |

Comp set size: 10-30 properties is the sweet spot. < 10 = too thin (one outlier moves rates). > 30 = dilutes signal.

Refresh comp set monthly (listings come and go).

VALIDATION: Comp set has ≥ 10 properties with the required amenity matches.

============================================================
=== PHASE 2: BASE RATE COMPUTATION ===
============================================================

For each night, compute a base rate:

```
Base = median(comp_set_rates_for_same_DOW_in_window) × adjustment_factors

Adjustment factors:
  Bedrooms vs comp median:    × 1.0 for match, ± 0.10/bedroom
  Reviews vs comp median:     × 1.05 if ≥ 2× comp median (premium)
  Rating vs comp median:      × 1.07 if 5.0 with ≥ 50 reviews
  Photos / staging quality:   × 0.95 to 1.10 (manual override)
  New-listing discount:       × 0.85 for first 90 days, taper to 1.0 by day 180
  Cost floor:                 max(base, cost_floor)
```

For each Day-of-Week in each Month, derive a separate median. Saturday rates ≠ Tuesday rates ≠ Christmas Day rates.

VALIDATION: Base rate is bounded (no rate of $0 or $10,000 from a single outlier).

============================================================
=== PHASE 3: SEASONALITY MULTIPLIERS ===
============================================================

Three layers of seasonality:

1. **Annual** — high season vs low season per market. Beach: summer × 1.6, winter × 0.7. Ski: winter × 1.8, summer × 0.6. Pull from AirDNA / Rabbu market data OR derive from prior year's market median by month.
2. **Monthly cycle** — months within season. Aug > June > July for many beaches.
3. **Day-of-week** — weekend premium (Fri/Sat). Default Fri × 1.15, Sat × 1.25, Sun × 1.10, weekday × 1.0.

Multipliers compound: `Base × Annual × Monthly × DOW`.

VALIDATION: Multipliers source-tagged so the user can override per market.

============================================================
=== PHASE 4: EVENT-DRIVEN PRICING ===
============================================================

Local events drive massive demand spikes. Maintain a market event calendar:

| Event Type                       | Default Multiplier | Notes                                      |
| -------------------------------- | ------------------ | ------------------------------------------ |
| Major concert (arena scale)      | 1.5-2.5×           | Within 5 miles of venue                    |
| Conference (1k+ attendees)       | 1.4-1.8×           | Within radius depending on hotel inventory |
| Sports — championship game       | 2.0-3.0×           | Super Bowl, NCAA Final Four                |
| Sports — regular season          | 1.1-1.3×           | NFL Sunday in NFL city                     |
| Festival (Coachella, SXSW)       | 1.8-2.5×           | Multi-day, regional                        |
| Wedding season weekend           | 1.3-1.5×           | Saturdays Apr-Oct in popular markets       |
| Holiday (NYE, Christmas, July 4) | 1.5-2.0×           | Country-specific                           |

Sources: Ticketmaster + Eventbrite + city tourism feed + manual local-knowledge override.

VALIDATION: Events within next 60 days are detected and applied. New event addition propagates within hours.

============================================================
=== PHASE 5: LEAD-TIME + BOOKING-PACE PRICING ===
============================================================

As the date approaches, rates should shift based on whether bookings are pacing ahead or behind:

| Lead time                            | Default behavior                                                                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| 60+ days out                         | Hold premium rates (no discount). Capture early planners.                                                                |
| 30-60 days                           | Compare bookings-on-books vs prior-year-same-period. Hold or discount 5-10% if pacing -10% YoY.                          |
| 14-30 days                           | More aggressive discount if pacing behind: 10-20% off.                                                                   |
| 7-14 days                            | Discount up to 25% on still-empty nights. Below cost floor → keep empty (lower than break-even isn't worth wear & tear). |
| 0-7 days                             | Last-minute discount up to 35% on still-empty Friday/Saturday/Sunday. Weekday nights often better left empty.            |
| Gap nights (single between bookings) | Discount aggressively (-20-30%) — better to fill than have orphans.                                                      |

VALIDATION: Booking-pace lookup pulls actual current bookings + prior-year baseline before adjusting.

============================================================
=== PHASE 6: MINIMUM-STAY OPTIMIZATION ===
============================================================

Minimum-stay rules protect against orphans:

- **Standard**: 2-night minimum weekdays, 3-night minimum weekend, 7-night minimum holidays.
- **Dynamic**: drop min-stay during low-demand windows (allow 1-night fills) but enforce during high-demand windows (force 3+ to avoid breaking up bookable weeks).
- **Gap-stay rules**: if Mon-Wed is open and Fri-Sun is booked, allow Mon-Wed 3-night booking (fill the gap) but block 2-night Wed-Thu booking (would orphan Mon-Tue).

Generate `min_stay_calendar.csv` per night.

VALIDATION: No min-stay rule produces an unfillable orphan night.

============================================================
=== PHASE 7: OUTPUTS ===
============================================================

```
str-pricing-{listing-id}/
├── rate_calendar.csv           # nightly rates for next 365 days
├── min_stay.csv
├── rate_changes.md             # explanation per night (which rules applied)
├── forecast.md                 # 30/60/90-day occupancy + ADR + RevPAR forecast
├── weekly_report.md            # last 7 days performance vs comp set
└── alerts.md                   # nights with >25% drift from prior, events found, comp set changes
```

Push to PMS via API. Most channel managers accept a rate-push REST call per listing.

VALIDATION: Rate calendar has exactly 365 rows, no missing dates.

============================================================
=== SELF-REVIEW ===
============================================================

- Complete: All 7 phases produced output?
- Robust: Cost floor prevents negative deals? Gap nights detected? Event detection working?
- Clean: Each rate has a "why" explanation?
- STR-credible: Would a PriceLabs / Beyond user accept this as a viable engine?

Common gap: chasing comp set into a price war. Set a floor and respect it.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/str-dynamic-pricing/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never set rates below the cost floor. Empty nights cost less than below-cost ones.
- Never ignore minimum-stay coordination — orphan nights are unfillable.
- Never apply event multipliers without verifying the event is on (some get cancelled).
- Never let comp set fall below 10 properties. Refresh monthly.
- Always provide a "why this rate" explanation per night for transparency.
