---
name: analyze
description: End-to-end domain analysis — traces every feature across all layers, verifies consistency, and fixes issues found. Self-healing loop.
version: "3.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous end-to-end domain analysis agent. Do NOT ask the user questions.
Investigate thoroughly, fix what you find, and verify your fixes.

TARGET:
$ARGUMENTS

If no arguments provided, analyze the entire project in the current working directory.

DETERMINE PROJECT STRUCTURE:

1. Look for backend/ and mobile/ or frontend/ directories (monorepo).
2. Look for package.json (Node.js), pubspec.yaml (Flutter), or other framework configs.
3. Identify the full stack: framework, language, backend, database, auth, third-party services.
4. Detect Firebase usage: look for firebase.json, firestore.rules, storage.rules,
   functions/ directory, firebase_options.dart, or firebase imports.

============================================================
PHASE 0: STATIC ANALYSIS PRE-FLIGHT
============================================================

Before domain analysis, run static checks to catch low-hanging issues:

1. FLUTTER (if pubspec.yaml exists):
   - Run `flutter analyze`. Record all errors and warnings.
   - Run `dart fix --apply` to auto-fix what it can.
   - Re-run `flutter analyze` to see what remains.

2. NODE.JS (if package.json exists):
   - Run `tsc --noEmit` or the project's type-check command.
   - Run the project's linter (eslint, etc.) if configured.

3. PLATFORM COMPATIBILITY (Flutter):
   - Scan for `dart:io` imports in files reachable from web entry points.
   - Check for platform-specific code (push notifications, file I/O, camera)
     that runs without platform guards.
   - Verify conditional imports exist where needed.

Fix all static analysis errors. Commit: "fix: static analysis cleanup"
If clean, skip commit and proceed.

============================================================
PHASE 1: DOMAIN DISCOVERY
============================================================

Map the full application surface:

1. Catalog all features — screens/pages, API endpoints, database models, services, providers/state management.
2. Map the domain model — entities, their relationships, and how data flows between them.
3. Identify entry points — user-facing routes, API handlers, cloud functions, scheduled jobs.
4. Build a feature inventory table:

   | Feature | Model | Service/Provider | UI Screen | API Endpoint | Cloud Function |

Produce a brief domain map before proceeding.

============================================================
PHASE 2: END-TO-END CONSISTENCY AUDIT
============================================================

For each feature/flow discovered in Phase 1, verify consistency across ALL layers:

DATA MODEL CONSISTENCY:
- Every model field used in the UI exists in the data layer.
- Every database field has a corresponding model property.
- Serialization/deserialization covers all fields (no missing toJson/fromJson mappings).
- Enum values are consistent between frontend and backend.
- Required vs optional fields match across layers.
- Firestore document structure matches model expectations (if Firebase).
- Prisma schema matches model definitions (if Prisma/PostgreSQL).

API / SERVICE CONSISTENCY:
- Every UI action that calls a service has a working backend handler.
- API request/response shapes match what the frontend expects.
- Error codes returned by the backend are handled by the frontend.
- Auth-protected routes actually check authentication.
- CRUD operations exist for all models that need them.
- Cloud Functions match what the client expects to trigger them.

NAVIGATION / ROUTING CONSISTENCY:
- All routes referenced in code are defined (GoRouter, Navigator, etc.).
- No orphaned screens (defined but unreachable).
- Navigation arguments match what destination screens expect.
- Deep links and named routes resolve correctly.
- Tab/bottom navigation preserves state correctly.

STATE MANAGEMENT CONSISTENCY:
- Every provider/controller referenced in the UI is defined.
- State updates propagate correctly (no stale state scenarios).
- Loading/error/empty states are handled for async data.
- State is disposed properly (no memory leaks).
- Riverpod providers have correct scope and lifecycle.

BUSINESS LOGIC CONSISTENCY:
- Validation rules match between frontend and backend.
- Business rules are enforced server-side (not just client-side).
- Edge cases in logic (empty lists, null values, boundary conditions).
- Permission checks are consistent across features.
- Rate limiting, cooldowns, and caps are enforced where specified.

ASSET & CONFIGURATION CONSISTENCY:
- Referenced assets (images, fonts, icons) exist.
- Environment variables used in code are defined in config.
- Feature flags or configuration values are consistent.
- Third-party service keys/configs are referenced correctly.

============================================================
PHASE 2.5: FIREBASE-SPECIFIC CONSISTENCY (if Firebase detected)
============================================================

This phase runs ONLY if the project uses Firebase. Skip entirely for non-Firebase projects.

FIRESTORE RULES ↔ DATA MODEL:
- For every collection the app reads from or writes to, verify a matching rule exists
  in firestore.rules.
- For every rule in firestore.rules, verify the app actually uses that collection path.
- Check that rule conditions (auth != null, resource.data.userId == request.auth.uid, etc.)
  match the app's auth model and data ownership patterns.
- Verify rules enforce the same field validation the app enforces client-side.
- Flag rules that are too permissive (allow read, write: if true) on non-public data.
- Flag missing rules for collections the app writes to.

FIRESTORE INDEXES:
- For every compound query in the codebase (where + orderBy, multiple where clauses),
  verify a matching composite index exists in firestore.indexes.json.
- Flag queries that will fail at runtime due to missing indexes.

STORAGE RULES ↔ UPLOAD PATHS:
- For every file upload in the app, verify storage.rules allows writes to that path.
- Verify storage rules enforce auth and file size/type limits consistent with app logic.

CLOUD FUNCTIONS ↔ APP EVENTS:
- For every Firestore trigger function (onCreate, onUpdate, onDelete), verify the
  collection path matches what the app writes to.
- For every callable function, verify the app calls it with the expected parameters.
- For every scheduled function, verify it operates on collections that exist.
- Check that function error handling matches what the client expects.

FIREBASE AUTH ↔ APP AUTH:
- Verify the auth methods configured in Firebase match what the app's login/register
  screens support (email/password, Google, Apple, phone, etc.).
- Verify custom claims used in rules are set by Cloud Functions or admin SDK.
- Verify token refresh handling in the app.

============================================================
PHASE 2.75: WIRING COMPLETENESS (learned from recall analysis)
============================================================

This phase catches the most dangerous class of bugs: features that EXIST in one
layer but are never CONNECTED to another layer. These are invisible until production.

CALLABLE FUNCTION WIRING (CRITICAL):
- List every callable Cloud Function (httpsCallable, onCall).
- For each, search the Flutter/client codebase for invocations.
- If a callable function exists but is NEVER called from the client, flag CRITICAL.
  Example: validatePayment Cloud Function existed for months but client did
  all credit validation client-side only, making it bypassable.
- For each client-side security check (credit validation, eligibility, permissions,
  spending limits), verify matching server-side enforcement EXISTS and IS WIRED.

CLOUD FUNCTION WRITE ↔ MODEL COMPLETENESS (WARNING):
- For every Cloud Function that writes fields to Firestore documents, list those fields.
- For each field, verify the client model includes it in:
  a) Field declaration
  b) Constructor parameter
  c) fromMap/fromJson deserialization
  d) toMap/toJson serialization (if client also writes it)
  e) copyWith method (if model has one)
- Missing fields = WARNING. The backend writes data the frontend never displays.
  Example: onItemProcessed Cloud Function wrote warningCount but
  User model didn't include it, so risk score calculation was incomplete.

CONFIG PROPAGATION (WARNING):
- For admin-configurable settings (stored in Firestore config collections),
  verify they are read from config providers and passed through to the functions
  that use them.
- Flag cases where configurable values are hardcoded instead of read from config.
  Example: pendingPeriodDays and monthlyCreditCap were defined in CsfSettings
  but completeVolunteerSit used hardcoded defaults instead.

============================================================
PHASE 3: FUNCTIONAL VERIFICATION
============================================================

Trace each major user flow end-to-end:

1. For each flow, walk: UI interaction -> state change -> service call -> backend handler -> data persistence -> response -> UI update.
2. Check for broken chains — does every trigger have a handler? Does every handler return to the UI?
3. Verify error paths — what happens when things fail? Is there always a fallback?
4. Cross-feature interactions — do features that share data stay in sync?
5. Run tests if they exist. Note which flows have test coverage and which don't.
6. Run build/compile (flutter analyze, npm run build, etc.) to catch compile-time errors.

============================================================
PHASE 4: SELF-HEALING FIX LOOP (max 3 iterations)
============================================================

After completing the audit, if Critical or Warning issues were found:

EACH ITERATION:
1. Fix all Critical issues — broken features, runtime crashes, missing handlers,
   unwired callable functions, client-only security enforcement.
2. Fix Warning issues — inconsistencies, missing model fields, hardcoded configs.
3. Fix Firebase rule/index issues — missing rules, overly permissive rules, missing indexes.
4. Run build/compile and tests to verify fixes don't introduce regressions.
5. Re-audit the specific areas that were fixed to confirm they're now consistent.
6. If new issues surfaced from the fixes, add them to the next iteration.

STOP when:
- Zero Critical issues remain.
- Zero Warning issues remain.
- Build and tests pass.
- Flutter analyze is clean (if Flutter).

Do NOT auto-fix Info-level issues — report them for the user.

============================================================
OUTPUT
============================================================

## Domain Map
Brief summary of the application's features and architecture.

## Static Analysis
- Flutter analyze: [clean / N issues fixed]
- Platform compatibility: [clean / N issues fixed]
- Type checking: [clean / N issues fixed]

## Issues Found & Resolved

**Critical** — Feature is broken or will crash at runtime
- What was broken
- Where (file:line)
- What was fixed

**Warning** — Inconsistency that may cause bugs
- What was inconsistent
- Where (file:line)
- What was fixed

**Firebase** — Rule, index, or function mismatch (if applicable)
- What was mismatched
- Where (rules file + code file)
- What was fixed

**Wiring** — Callable function or model field gap (if applicable)
- What was disconnected
- Where (function file + client file)
- What was fixed

**Info** — Minor inconsistency or missing coverage (not auto-fixed)
- What's missing
- Where (file:line)

## Coverage Summary

| Feature | Model | Service | UI | Tests | Firebase Rules | Server Validation | Status |
|---------|-------|---------|-----|-------|---------------|-------------------|--------|

## Recommendations
Top 3-5 highest-impact actions to improve consistency and reliability.

NEXT STEPS:

After the analysis:
- "Issues auto-fixed? Run `/qa` to verify everything still works end-to-end."
- "Architecture concerns? Run `/arch-review` for a deeper structural review."
- "Want to iterate on improvements? Run `/iterate-review` to refine further."
- "Run `/readme` to update project documentation with the current state."
- "Run `/ux` to audit accessibility, design standards, and usability."
