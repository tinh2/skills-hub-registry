---
name: mls-listing-craft
description: Generate MLS-compliant property listing copy in five length variants (tagline, MLS-short ≤250 char, MLS-long ≤4000 char, marketing description ~600-800 words, social caption) PLUS schema.org RealEstateListing JSON-LD for SEO/AEO syndication. Auto-runs HUD Fair Housing Act compliance check (catches discriminatory language patterns — "perfect for families", "walking distance", "exclusive", "safe neighborhood", "Christian community", etc.). TRIGGER on phrases like "MLS listing", "property listing description", "listing copy", "real estate description", "Zillow listing", "compelling listing", "write the listing", "MLS remarks", "marketing copy for [property]", "open house copy". Saves agents 30-60 minutes per listing — and prevents the fair-housing violations that cost agents licenses.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# MLS Listing Generator

You generate property listing copy that is MLS-format-correct, character-limit-compliant, fair-housing-safe, and syndication-ready (Zillow, Realtor.com, Redfin, Apple Maps, Google). Five length variants from one input pass plus JSON-LD for structured-data SEO.

Listing copywriting is the #1 most-adopted AI use case among real estate agents (multiple 2026 industry surveys). The most common failures are (a) violating character limits and getting auto-rejected by MLS systems and (b) accidentally using language that triggers a Fair Housing Act violation. Both are solved by construction.

============================================================
=== PRE-FLIGHT ===
============================================================

Gather and verify before writing:

- [ ] **Property facts.** Required: address, beds, baths, sq ft, lot size, year built, asset type, list price. Optional: HOA, taxes, parking, school district, included appliances, recent updates.
- [ ] **Unique features.** What makes THIS property different? (Renovated kitchen? View? Lot? Floor plan? Garage? Pool?) Without this the copy is generic and useless.
- [ ] **Target audience.** First-time buyer, investor, downsizer, luxury, family — drives tone.
- [ ] **MLS system.** Different MLSs have different character limits. Defaults: most MLSs use 250 char "public remarks short" and 4000 char "public remarks long". Confirm with user OR default to these and flag for verification.
- [ ] **Photos described.** If photos are attached, run a vision pass to extract additional feature descriptors (white quartz countertops, dark hardwood floors, etc.) so the copy doesn't read generic.

Recovery:

- If unique features are not provided, prompt with: "What are 2-3 things that make this property stand out to a buyer?" — refuse to generate until answered (generic listings hurt the agent's brand).
- If user has a brokerage style guide, request it. Otherwise default to clean editorial: active voice, present tense, no exclamation points.

============================================================
=== PHASE 1: FAIR HOUSING COMPLIANCE GATE ===
============================================================

Before writing any copy, load the banned-pattern list and apply it as a hard filter on ALL output.

**HUD-enforced banned categories** (Fair Housing Act, 42 U.S.C. § 3604):

- Race / color / national origin
- Religion
- Sex (including gender identity)
- Familial status (presence of children)
- Disability

**Patterns that trigger violations** (NAR + HUD guidance):

- "Perfect for families" → familial status implication; use "spacious floor plan"
- "Empty nesters" → familial status / age; use "low-maintenance living"
- "Safe neighborhood" → race-coded; describe specific amenities instead
- "Walking distance" → ableist; use "X blocks" or specific distance
- "Master bedroom" → use "primary bedroom" (NAR adopted 2020+)
- "Exclusive community" → coded language; use "private" only if literally gated
- "Christian community" / "near temple" → religious targeting
- "Quiet street" → fine, but pair with objective fact ("cul-de-sac")
- "Original owner" → fine
- "Mother-in-law suite" → use "guest suite" or "accessory dwelling unit"
- "His and hers closets" → use "dual closets"
- "Maid's quarters" → use "guest suite"
- "Handyman special" → fine
- "Single-family" → fine (refers to zoning, not occupancy)

The compliance gate runs on the FINAL output, not the intermediate drafts. If any banned pattern is detected:

1. Highlight the offending phrase.
2. Suggest the compliant replacement inline.
3. Do NOT publish until clean.

VALIDATION: A red-team test fixture (`tests/fair_housing_redteam.txt`) contains 20 sample listings with known violations. The gate must catch ≥ 19 of 20.

FALLBACK: If a phrase is ambiguous (could be discriminatory in some contexts, not others), flag with a yellow "review required" rather than auto-rewrite.

============================================================
=== PHASE 2: FEATURE EXTRACTION & STRUCTURING ===
============================================================

Take the input facts and organize into a structured features dictionary:

```yaml
hero_feature: "Renovated chef's kitchen with quartz waterfall island"
secondary_features:
  - "Vaulted ceilings throughout main level"
  - "Primary suite with walk-in closet and spa bath"
  - "Fenced backyard with covered patio"
neighborhood:
  - "1/2 mile to Whole Foods"
  - "Walk Score 84"
  - "Highly rated public schools (avoid naming specific schools in copy — fair housing risk)"
financial_highlights:
  - "$8,400/year property taxes"
  - "$320 HOA covers exterior + landscaping"
recent_updates:
  - "New roof 2024"
  - "HVAC replaced 2023"
```

The HERO feature gets prime placement in every length variant. Secondary features get rotated to avoid each variant reading identical.

VALIDATION: Hero feature appears in tagline, MLS-short, and MLS-long. Secondary features rotate. No feature appears more than twice in the same variant.

============================================================
=== PHASE 3: GENERATE FIVE LENGTH VARIANTS ===
============================================================

Generate each variant with strict character/word limits:

### Variant 1: Tagline (≤ 80 characters)

One sentence. Hero feature + neighborhood signal.
Example: "Renovated 4-bed with chef's kitchen in walkable Westside neighborhood."

### Variant 2: MLS Short Remarks (≤ 250 characters)

The "search results card" copy. Hook + 3 features + call to action.
Example: "Light-filled 4-bed/3-bath with chef's kitchen, vaulted ceilings, and fenced yard. New roof and HVAC. Two-car garage. Move-in ready. See it before it's gone."

### Variant 3: MLS Long Remarks (≤ 4000 characters)

Full property description. Structure:

1. Hook (1-2 sentences)
2. Exterior / curb appeal (1 paragraph)
3. Main living areas (1-2 paragraphs)
4. Kitchen (1 paragraph — usually the hero in residential)
5. Primary suite (1 paragraph)
6. Additional bedrooms / baths (1 paragraph)
7. Outdoor / lot (1 paragraph)
8. Mechanical / updates / inclusions (1 paragraph)
9. Closing nudge (1 sentence)

### Variant 4: Marketing Description (600-800 words)

For the agent's website, brochures, social posts (long form). Same structure as Variant 3 plus:

- Add neighborhood narrative (cafes, parks, retail — no schools by name)
- Add lifestyle framing ("morning coffee on the patio", "evening sunsets")
- Stay objective on neighborhood feel — describe places, not people

### Variant 5: Social Caption (≤ 200 characters)

Instagram/Facebook ready. Hook + 1 feature + 3 hashtags.
Example: "Renovated kitchen, dreamy primary suite, fully fenced yard. Open house Saturday 1-3. #JustListed #YourCityRealEstate #DreamHome"

VALIDATION: Each variant under its character limit. No banned phrases from Phase 1. Each variant has the hero feature.

FALLBACK: If 4000-char MLS Long Remarks runs short on details (sparse input), do NOT pad — output what's substantive and note "Add: \_\_\_" placeholders.

============================================================
=== PHASE 4: SCHEMA.ORG JSON-LD ===
============================================================

Generate `schema.json` with the `RealEstateListing` schema for SEO + AEO (Answer Engine Optimization — surfaces in Google AI Overviews, ChatGPT real estate queries, Perplexity).

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateListing",
  "name": "4-Bedroom Home with Chef's Kitchen",
  "url": "{listing_url}",
  "datePosted": "{ISO_date}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "...",
    "addressLocality": "...",
    "addressRegion": "...",
    "postalCode": "...",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 0, "longitude": 0 },
  "offers": {
    "@type": "Offer",
    "price": 0,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "numberOfBedrooms": 4,
  "numberOfBathroomsTotal": 3,
  "floorSize": { "@type": "QuantitativeValue", "value": 0, "unitCode": "FTK" },
  "yearBuilt": 0,
  "description": "{MLS_long_remarks}"
}
```

VALIDATION: JSON-LD passes Google's Rich Results Test (no required-field errors). Lat/long, if missing, are flagged as TODO (don't fabricate coordinates).

============================================================
=== PHASE 5: OUTPUT PACKAGE ===
============================================================

Final deliverable directory:

```
listing-{address-slug}/
├── README.md              # how to publish where
├── tagline.txt
├── mls_short.txt          # paste into MLS public remarks (short)
├── mls_long.txt           # paste into MLS public remarks (long)
├── marketing.md           # paste into agent website / brochure
├── social.txt             # Instagram / Facebook caption
├── schema.json            # add to listing page <script type="application/ld+json">
└── compliance_report.md   # what was checked, anything flagged
```

The README explains exactly where each file goes and why.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 5 variants generated + JSON-LD + compliance report?
- **Robust**: Compliance gate caught all violations? Character limits respected? Hero feature consistent?
- **Clean**: No exclamation point overuse, no clichés ("must see!", "won't last!", "priced to sell"), no all-caps emphasis?
- **Fair-housing-safe**: Re-scan final output with the banned-pattern list — zero hits required, not "low".

If any < 4:

- Most common gap: clichés sneaking into MLS-long. Replace with specific factual details.
- Second most common: subtle familial-status language. Re-scan.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/mls-listing-craft/LEARNINGS.md`:

## <YYYY-MM-DD> — <property type, asset type, region>

- **What worked:** <approach that produced clean copy>
- **What was awkward:** <retry / rewrite needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never bypass the fair housing gate. A discriminatory listing is a license risk for the agent, not a stylistic preference.
- Never exceed character limits. MLS systems reject auto-truncated submissions and timestamp it as a fail.
- Never invent property details. If the input doesn't include a fact, omit it — don't infer.
- Never name specific schools by name in copy (NAR guidance — implies a "good schools = wealthy area = race-coded" loop).
- Never use the word "master" for the bedroom/bathroom. Use "primary".
- Never end every variant with "Don't miss out!" or similar. Vary the close or omit.
