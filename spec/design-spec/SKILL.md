---
name: design-spec
description: "Lock down design decisions before implementation — app name, terminology, design tokens, screen inventory, data models, and microcopy. Outputs a design-spec.md that other skills reference."
version: 1.0.0
category: spec
instructions: |
  You are in FULLY AUTONOMOUS MODE. Zero questions. Just produce the spec.

  TASK:
  $ARGUMENTS

  RULES:
  - Do NOT ask the user anything. Decide and move.
  - If you're unsure between two options, pick the one that is simpler and more conventional.
  - Read the entire codebase before producing any output.
  - If a design-spec.md already exists, read it and update it rather than replacing from scratch.
  - Output is a single file: `design-spec.md` in the project root.

  === WHY THIS SKILL EXISTS ===

  Every project without a locked design spec experienced cascading rework:
  - PawPass: 3 UI redesign waves hitting 20+ screen files, "Credits" to "Paw Points"
    rename caused 149 test failures, branding change on Day 7 after features were built.
  - Recipe AI: No locked design spec led to reactive UI changes across the entire app.
  - Confidence Coach: Design token consolidation required 6 separate commits to
    standardize colors and spacing that should have been defined from Day 1.

  This skill locks ALL design decisions into a single source of truth BEFORE any
  implementation begins. Other skills (/iterate, /ship, /bootstrap) reference this
  file to avoid drift.

  === PROCESS ===

  1. SCAN THE PROJECT

     Read all existing files to understand:
     - What the app does (README, pubspec.yaml, package.json, etc.)
     - Existing design decisions (theme files, constants, styles)
     - Existing screens and navigation structure
     - Existing data models and collection/table names
     - Existing user-facing strings and microcopy
     - The tech stack (Flutter, React, Node.js, etc.)

     If the project is empty or just scaffolded, infer from the task description.

  2. PRODUCE THE DESIGN SPEC

     Generate `design-spec.md` with ALL of the following sections.
     Every section is MANDATORY. Do not skip sections even if they seem
     premature — decisions made now prevent rework later.

  === DESIGN SPEC TEMPLATE ===

  The output file must follow this exact structure:

  ```markdown
  # Design Spec — {App Name}

  > Version: 1.0 | Created: {date} | Status: LOCKED
  >
  > This file is the single source of truth for all design decisions.
  > Do NOT change values here without updating all code that references them.
  > All skills (/iterate, /ship, /qa) must conform to this spec.

  ## 1. Identity

  ### App Name
  - **Display name:** {name as shown to users}
  - **Package/bundle ID:** {com.example.appname}
  - **Internal project name:** {snake_case or kebab-case used in code}

  ### Terminology Lock

  These terms are FINAL. Do not use synonyms, abbreviations, or alternatives
  in code, UI, tests, or documentation.

  | Concept | User-Facing Term | Internal Field Name | Notes |
  |---------|-----------------|--------------------:|-------|
  | {e.g., virtual currency} | {e.g., Paw Points} | {e.g., pawPoints} | {context} |
  | ... | ... | ... | ... |

  ## 2. Design Tokens

  ### Color Palette

  | Token Name | Hex | Usage |
  |-----------|-----|-------|
  | primary | #{hex} | Main action buttons, app bar, links |
  | primaryVariant | #{hex} | Pressed/hover state of primary |
  | secondary | #{hex} | Secondary actions, accents |
  | secondaryVariant | #{hex} | Pressed/hover state of secondary |
  | surface | #{hex} | Card backgrounds, input fields |
  | background | #{hex} | Page/scaffold background |
  | error | #{hex} | Error states, destructive actions |
  | onPrimary | #{hex} | Text/icons on primary color |
  | onSecondary | #{hex} | Text/icons on secondary color |
  | onSurface | #{hex} | Text/icons on surface color |
  | onBackground | #{hex} | Text/icons on background color |
  | onError | #{hex} | Text/icons on error color |
  | success | #{hex} | Success states, confirmations |
  | warning | #{hex} | Warning states, caution indicators |
  | neutral100 | #{hex} | Lightest neutral (borders, dividers) |
  | neutral500 | #{hex} | Mid neutral (secondary text, icons) |
  | neutral900 | #{hex} | Darkest neutral (primary text) |

  All colors MUST be referenced via theme tokens in code. Zero hardcoded hex values.

  ### Typography Scale

  | Style Name | Font Family | Size (sp/px) | Weight | Line Height | Usage |
  |-----------|-------------|-------------|--------|------------|-------|
  | displayLarge | {font} | {size} | {weight} | {height} | Hero text, onboarding |
  | headlineMedium | {font} | {size} | {weight} | {height} | Screen titles |
  | titleLarge | {font} | {size} | {weight} | {height} | Section headers |
  | titleMedium | {font} | {size} | {weight} | {height} | Card titles |
  | bodyLarge | {font} | {size} | {weight} | {height} | Primary body text |
  | bodyMedium | {font} | {size} | {weight} | {height} | Secondary body text |
  | labelLarge | {font} | {size} | {weight} | {height} | Button text |
  | labelSmall | {font} | {size} | {weight} | {height} | Captions, hints |

  All text styles MUST be referenced via TextTheme/typography tokens. Zero inline font sizes.

  ### Spacing Grid

  Base unit: {N}dp/px

  | Token | Value | Usage |
  |-------|-------|-------|
  | xs | {N}dp | Tight padding (icon gaps, inline spacing) |
  | sm | {N}dp | Small padding (list item internal) |
  | md | {N}dp | Standard padding (card content, form fields) |
  | lg | {N}dp | Section spacing (between cards, groups) |
  | xl | {N}dp | Major section breaks, screen margins |
  | xxl | {N}dp | Hero spacing, onboarding gaps |

  ### Border Radii

  | Token | Value | Usage |
  |-------|-------|-------|
  | none | 0 | Sharp corners (dividers, full-width elements) |
  | sm | {N}dp | Subtle rounding (chips, tags) |
  | md | {N}dp | Standard rounding (cards, buttons) |
  | lg | {N}dp | Prominent rounding (modals, sheets) |
  | full | 9999dp | Pill shape (avatar, badges) |

  ### Elevation / Shadows

  | Token | Value | Usage |
  |-------|-------|-------|
  | none | 0 | Flat elements |
  | low | {N} | Cards, subtle depth |
  | medium | {N} | Floating action buttons, dropdowns |
  | high | {N} | Modals, overlays |

  ## 3. Screen Inventory

  ### Navigation Structure

  {Describe the navigation pattern: bottom tabs, drawer, stack-only, etc.}

  ### Screen List

  | Screen | Route/Path | Purpose | Key Components |
  |--------|-----------|---------|----------------|
  | {name} | {/path} | {what it does} | {main widgets/sections} |
  | ... | ... | ... | ... |

  ### Navigation Flow

  ```
  {ASCII diagram or description of screen-to-screen navigation}
  ```

  ## 4. Data Models

  ### Collection/Table Names

  | Entity | Collection/Table Name | Primary Key | Notes |
  |--------|----------------------|-------------|-------|
  | {entity} | {name} | {field} | {notes} |
  | ... | ... | ... | ... |

  ### Field Naming Convention

  - Case: {camelCase / snake_case}
  - Timestamps: {createdAt/created_at} format, stored as {DateTime/ISO8601/epoch}
  - IDs: {uuid / auto-increment / firestore-generated}
  - Booleans: prefix with {is/has/can} (e.g., isActive, hasPermission)
  - Enums: stored as {string / int}, values: {UPPER_CASE / lowercase}

  ### Core Models

  For each model, list ALL fields with types:

  #### {ModelName}
  | Field | Type | Required | Default | Notes |
  |-------|------|----------|---------|-------|
  | {field} | {type} | {Y/N} | {default} | {notes} |
  | ... | ... | ... | ... | ... |

  ## 5. Copy & Microcopy

  ### Key UI Strings

  | Context | String | Notes |
  |---------|--------|-------|
  | Empty state — {screen} | "{text}" | Shown when no data exists |
  | Error — generic | "{text}" | Fallback error message |
  | Error — network | "{text}" | No internet connection |
  | Error — auth | "{text}" | Session expired / unauthorized |
  | Success — {action} | "{text}" | Confirmation after action |
  | CTA — primary | "{text}" | Main call-to-action button |
  | Loading | "{text}" | Loading indicator text |
  | Onboarding — step 1 | "{text}" | First onboarding screen |
  | ... | ... | ... |

  ### String Storage Convention

  All user-facing strings MUST be stored in:
  - {location: e.g., lib/constants/strings.dart, src/i18n/en.json, etc.}

  Zero hardcoded strings in UI code.

  ## 6. Iconography & Assets

  | Icon/Asset | Source | Usage |
  |-----------|--------|-------|
  | App icon | {path or description} | Launcher icon |
  | {feature icon} | {MaterialIcons.name / custom asset path} | {where used} |
  | ... | ... | ... |

  ## 7. Platform-Specific Decisions

  | Decision | Value | Rationale |
  |----------|-------|-----------|
  | Min SDK/OS version | {value} | {why} |
  | Target platforms | {list} | {why} |
  | Orientation lock | {portrait/landscape/both} | {why} |
  | Dark mode support | {yes/no/later} | {why} |
  | Offline support | {yes/no/later} | {why} |
  | Auth method | {email/social/anonymous} | {why} |

  ## 8. Change Log

  | Date | Section | Change | Reason |
  |------|---------|--------|--------|
  | {date} | — | Initial spec created | — |
  ```

  === POST-GENERATION ===

  After generating design-spec.md:

  1. VERIFY CONSISTENCY: Cross-check that:
     - Every screen in the inventory uses only colors from the palette
     - Every data model field name follows the naming convention
     - Every user-facing term matches the terminology lock table
     - All routes in the screen inventory are unique

  2. VERIFY AGAINST EXISTING CODE (if code exists):
     - Flag any hardcoded colors, strings, or spacing values in existing code
       that contradict the spec. List them as "Migration Items" at the bottom.
     - Flag any existing field names that don't match the spec's naming convention.
     - Flag any screens that exist in code but are missing from the inventory.

  3. COMMIT the design-spec.md:
     - Commit message: "spec: lock design decisions in design-spec.md"

  === OUTPUT ===

  After generating the file:

    ## Design Spec Locked
    - App: {app name}
    - Screens: {count}
    - Models: {count}
    - Design tokens: {count of unique tokens defined}
    - Terminology entries: {count}
    - Migration items: {count of existing code violations, or "none — greenfield"}
    - File: design-spec.md

  NEXT STEPS:

  Recommended pipeline after `/design-spec`:
  - "Run `/iterate` to start building with the locked spec."
  - "Run `/arch-review` to validate architecture against the spec."
  - "Run `/bootstrap` to scaffold the project from the spec."
---
