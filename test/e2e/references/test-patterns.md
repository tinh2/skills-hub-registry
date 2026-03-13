# Test Generation Patterns Reference

## User Flow Catalog (Phase 0.3)

Identify every end-to-end user flow from these categories:

### Authentication Flows
- Sign up (email/password, social/OAuth, phone, magic link)
- Sign in
- Forgot password / reset
- Sign out
- Session expiry / token refresh
- Account deletion / deactivation
- Multi-factor authentication (if present)

### Core CRUD Flows (for each data entity)
- Create: navigate to form, fill fields, submit, verify created
- Read (list): navigate to list, verify items render, test pagination/filtering/sorting
- Read (detail): navigate to detail, verify all fields displayed
- Update: open item, edit fields, save, verify updated
- Delete: delete item, confirm, verify removed

### Navigation Flows
- Tab/sidebar switching
- Deep navigation (3+ levels, then back)
- Breadcrumb navigation
- Deep link / direct URL access
- Back button behavior

### Form Flows (for each form)
- Valid submission
- Each validation rule triggered individually
- All fields empty submission
- Maximum length inputs
- Special characters

### Edge Case Flows
- Empty states (no data)
- Error states (API failure, network error)
- Loading states
- Unauthorized access to protected routes
- Concurrent modifications (if applicable)
- Large data sets (pagination boundaries)

### Real-Time Flows (if present)
- WebSocket connections
- Server-Sent Events
- Push notifications
- Live updates across tabs/sessions

---

## Phase 2: Backend Test Generation Patterns

### Step 2.1 — Test Helpers / Setup

**FOR NODE.JS (Vitest/Jest + Supertest):**

Create tests/e2e/helpers/setup.ts:
- Build the Fastify/Express app instance for supertest (do not start a server, use app.inject() for Fastify or supertest(app) for Express).
- Set up test database connection (use test-specific DATABASE_URL if available).
- Provide helper: createAuthenticatedAgent(role?) that registers a test user, logs in, and returns an agent/token for authenticated requests.
- Provide helper: cleanupTestData() for teardown.
- Use unique identifiers (timestamps, UUIDs) in test data to avoid collisions.

**FOR PYTHON (pytest + httpx):**

Create tests/e2e/conftest.py:
- Set up TestClient (httpx.AsyncClient for FastAPI, Django test client for Django).
- Provide fixture: authenticated_client that creates a user and returns a client with auth headers.
- Provide fixture: test_db that handles database setup/teardown.

**FOR GO:**

Create tests/e2e/helpers_test.go:
- Set up httptest.Server with the application handler.
- Provide helper: authenticatedRequest(method, path, body) with auth token.
- Provide helper: setupTestDB() and teardownTestDB().

**FOR DENO:**

Create tests/e2e/helpers.ts:
- Set up the application handler for Deno.test.
- Use Deno's built-in fetch or std/http for making test requests.
- Provide helper: createAuthHeaders() for authenticated requests.
- Use Deno.env.get() for test-specific configuration.

**FOR BUN:**

Create tests/e2e/helpers.ts:
- Set up the application instance (Elysia/Hono/custom).
- Use bun:test's describe/it/expect for assertions.
- Provide helper: createAuthenticatedClient() for auth requests.
- Use Bun's built-in fetch for HTTP testing or supertest if installed.

### Step 2.2 — Endpoint Test Patterns

For EVERY endpoint in the endpoint table from Phase 0, generate tests covering:

**HAPPY PATH:**
- Send a valid request with realistic test data.
- Verify correct HTTP status code (200, 201, 204, etc.).
- Verify response body structure matches the expected schema.
- Verify response data contains expected values.
- For list endpoints: verify pagination works (cursor/offset, limit, total).
- For list endpoints: verify filtering and sorting if supported.

**VALIDATION / ERROR CASES:**
- Missing required fields -- verify 400 with descriptive error.
- Invalid field types (string where number expected) -- verify 400.
- Invalid field values (negative price, future date for birthdate) -- verify 400.
- Empty request body when body is required -- verify 400.
- Extra/unknown fields -- verify they are ignored or rejected per convention.

**AUTHENTICATION / AUTHORIZATION:**
- Request without auth token on protected endpoint -- verify 401.
- Request with expired/invalid token -- verify 401.
- Request with wrong role (user accessing admin endpoint) -- verify 403.
- Request to own resource vs. other user's resource -- verify ownership rules.

**RESOURCE LIFECYCLE:**
- Create -> Read (verify created) -> Update -> Read (verify updated) -> Delete -> Read (verify 404).
- Test idempotency where applicable (PUT, DELETE).
- Test duplicate creation (unique constraints) -- verify 409 or appropriate error.

**EDGE CASES:**
- Request non-existent resource by ID -- verify 404.
- Request with malformed ID format -- verify 400 or 404.
- Boundary values (empty strings, very long strings, zero, negative numbers, max int).
- Concurrent requests to same resource (if relevant).

**FILE ORGANIZATION:**
- One test file per feature/module: tests/e2e/[feature].test.ts (or .py, _test.go).
- Group related tests with describe/context blocks.
- Use descriptive test names that map to flow numbers from Phase 0.

### Step 2.3 — Auth Flow Tests

Generate a dedicated auth test file covering the complete auth lifecycle:

- Register with valid data -- verify 201 + user created.
- Register with duplicate email -- verify 409.
- Register with weak password -- verify 400.
- Login with valid credentials -- verify 200 + token returned.
- Login with wrong password -- verify 401.
- Login with non-existent email -- verify 401.
- Access protected endpoint with valid token -- verify 200.
- Access protected endpoint with no token -- verify 401.
- Access protected endpoint with malformed token -- verify 401.
- Token refresh (if applicable) -- verify new valid token returned.
- Logout (if applicable) -- verify token invalidated.
- Password reset flow (if applicable) -- request reset, verify email sent logic, reset with token.

---

## Phase 3: Frontend Test Generation Patterns

### Step 3.1 — Test Helpers / Setup

**FOR WEB (Playwright):**

Create e2e/helpers/setup.ts:
- Extend base test with authenticatedPage fixture that logs in and returns an authenticated page context.
- Create e2e/helpers/test-data.ts with functions to generate unique test data (users, entities) using timestamps/UUIDs.
- Functions to seed test data via API before UI tests.
- Functions to clean up test data after tests.

**FOR FLUTTER (integration_test):**

Create helpers in integration_test/helpers/:
- app_launcher.dart -- starts the app with test configuration
- interaction_helpers.dart -- tapByKey, enterText, scrollUntilVisible, verifySnackbar
- auth_helpers.dart -- login/signup helper flows

**FOR WEB (Cypress -- if already in use):**

Create cypress/support/commands.ts:
- cy.login(email, password) custom command.
- cy.seedData(fixture) custom command.
- cy.cleanupData() custom command.

### Step 3.2 — Page/Screen Test Patterns

For EVERY page/screen in the screen table from Phase 0, generate tests covering:

**PAGE RENDERING:**
- Navigate to the page -- verify it loads without errors.
- Verify all expected UI elements are present (headings, buttons, forms, lists).
- Verify data loads and displays correctly.
- Verify page title / meta tags (web) or app bar title (mobile).

**NAVIGATION:**
- Navigate to page from every entry point (menu, link, direct URL, deep link).
- Navigate away from page using every exit point.
- Browser back button / mobile back gesture returns to correct previous screen.
- Verify query parameters / route params are consumed correctly.

**FORMS (for every form on the page):**
- Fill all fields with valid data, submit -- verify success feedback and data persisted.
- Submit with all fields empty -- verify validation messages appear.
- Test each validation rule individually (too short, invalid format, required, etc.).
- Test field interactions (password confirmation match, conditional fields).
- Verify submit button disabled state during submission (no double submit).
- Verify form preserves data on validation failure (fields not cleared).

**LISTS / DATA DISPLAY:**
- Verify items render when data exists.
- Verify empty state when no data.
- Verify loading state while data fetches.
- Verify error state when API fails (if testable).
- Test pagination: load more / infinite scroll / page navigation.
- Test filtering: apply filter, verify results change.
- Test sorting: change sort order, verify order changes.
- Test search: enter search term, verify results filter.

**INTERACTIVE ELEMENTS:**
- Test every button -- click and verify expected action.
- Test every link -- click and verify navigation.
- Test dropdowns/selects -- open, select option, verify selection.
- Test modals/dialogs -- open, interact, close (both confirm and cancel).
- Test tooltips/popovers -- hover/tap, verify shown, dismiss.
- Test accordions/expandable sections -- expand, collapse, verify content.

**STATES:**
- Loading state: verify skeleton/spinner appears before data loads.
- Error state: verify error message and retry option.
- Empty state: verify helpful message and CTA.
- Authenticated vs. unauthenticated view differences.

**RESPONSIVE (web only):**
- Test at mobile viewport (375px width).
- Test at tablet viewport (768px width).
- Test at desktop viewport (1280px width).
- Verify navigation changes (hamburger menu on mobile).
- Verify layout reflows correctly.

**FILE ORGANIZATION:**
- Playwright: e2e/[feature].spec.ts
- Cypress: cypress/e2e/[feature].cy.ts
- Flutter: integration_test/[feature]_test.dart

### Step 3.3 — User Flow Tests (Multi-Page Journeys)

Generate tests for complete user journeys that span multiple pages:

- Signup flow: landing -> signup form -> email verification (if applicable) -> onboarding -> dashboard
- Login flow: landing -> login form -> dashboard -> verify user data displayed
- CRUD journey: list page -> create form -> submit -> back to list (verify new item) -> click item -> detail page -> edit -> save -> back to detail (verify changes) -> delete -> back to list (verify removed)
- Settings flow: navigate to settings -> change profile info -> save -> verify persisted -> change password -> verify
- Error recovery: trigger error -> verify error state -> retry -> verify recovery

Each flow test should be a single test that exercises the full journey without interruption.

---

## Phase 4: Integration Test Patterns

### Step 4.1 — Vertical Slice Tests

For each major feature, generate a test that:

1. **STARTS in the UI** -- perform a user action (click button, submit form).
2. **VERIFIES the API call was made** -- intercept network request (Playwright: page.route(), Cypress: cy.intercept(), Flutter: custom HTTP interceptor).
3. **VERIFIES the database changed** -- query the API to confirm the data was persisted (GET the resource after creating/updating it).
4. **VERIFIES the UI updated** -- check the screen reflects the new state without manual refresh.

### Step 4.2 — Cross-Feature Integration Tests

Test interactions between features:

- User creates entity A -> entity A appears in related entity B's view.
- User changes profile -> profile data updates across all screens that display it.
- User performs action that triggers side effect (email, notification, webhook).
- Admin action affects regular user's view.
- Deleting a parent entity cascades correctly to child entities in UI.

### Step 4.3 — Real-Time Integration Tests (if applicable)

If the app uses WebSocket, SSE, or real-time updates:

- Open two browser contexts (simulating two users).
- User A performs an action.
- Verify User B's view updates without refresh.
- Test reconnection after connection drop.
- Test message ordering and delivery guarantees.
