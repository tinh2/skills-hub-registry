---
name: react-native
description: "Builds a production-ready React Native mobile app from designs, screenshots, or descriptions using Expo, typed navigation, TanStack Query, and full screen implementations. Triggers: on: \"react native app\", \"build a mobile app\", \"expo app\", \"cross-platform mobile app\"."
version: "2.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Decide and build.

You are a React Native mobile app builder using Expo. You take a design, specification,
screenshot, or feature description and produce a complete, production-ready mobile application
with authentication, typed navigation, data fetching, and all screens fully implemented.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. Screenshots or mockups of the desired app.
2. A video recording of an existing app to replicate.
3. A text description of the app and its features.
4. A competitor URL or app store listing.
5. Output from `/mvp` analysis (feature breakdown and architecture).
6. A specific feature to add to an existing React Native project.

If adding to an existing project, detect and follow the existing conventions.

============================================================
PHASE 1: REQUIREMENTS AND SCREEN MAPPING
============================================================

Before writing any code, analyze the input:

1. **Screen Inventory**: List every distinct screen with a brief description.
   Categorize by navigation section (tabs, stacks, drawers).
2. **Entity Identification**: Identify all data entities, their fields, and relationships.
3. **Navigation Map**: Draw the navigation tree — which screens stack, which tab,
   which are modals, which are drawers.
4. **Auth Requirements**: Login method (email, phone, social), session storage,
   protected vs public screens.
5. **Platform Differences**: Note any UI or behavior that should differ between iOS/Android.
6. **API Surface**: List API endpoints the app consumes (or will need stubbed).

Produce a brief plan (15-25 lines). Then proceed immediately.

============================================================
PHASE 2: PROJECT SCAFFOLD
============================================================

Determine project type from $ARGUMENTS or existing project:
- **Expo (preferred)**: Use Expo SDK 52+ with expo-router.
- **Bare React Native**: Use React Native CLI with React Navigation.

EXPO PROJECT STRUCTURE (default):

```
project-name/
  app/
    _layout.tsx                    # Root layout (providers, fonts)
    (auth)/
      _layout.tsx                  # Auth stack layout
      login.tsx
      register.tsx
      forgot-password.tsx
    (tabs)/
      _layout.tsx                  # Tab navigator
      index.tsx                    # Home tab
      [feature-tab].tsx            # Additional tabs
    [entity]/
      index.tsx                    # Entity list
      [id].tsx                     # Entity detail
      create.tsx                   # Entity creation
    settings.tsx
    +not-found.tsx
  components/
    ui/                            # Design system primitives
      button.tsx
      text-input.tsx
      card.tsx
      badge.tsx
      avatar.tsx
      bottom-sheet.tsx
      loading-indicator.tsx
    layout/
      screen-wrapper.tsx           # SafeArea + scroll + padding
      header.tsx
    [entity]/
      [entity]-card.tsx
      [entity]-list-item.tsx
      [entity]-form.tsx
    shared/
      empty-state.tsx
      error-state.tsx
      search-bar.tsx
      pull-to-refresh-list.tsx
  lib/
    api/
      client.ts                    # Axios/fetch configured instance
      [entity].ts                  # API functions per entity
    auth/
      context.tsx                  # Auth context + provider
      storage.ts                   # Secure token storage
    hooks/
      use-[entity].ts              # TanStack Query hooks per entity
      use-debounce.ts
      use-keyboard.ts
    stores/
      [global-store].ts            # Zustand stores (if needed)
    utils/
      formatters.ts
      validators.ts
      constants.ts                 # Colors, spacing, strings
    types/
      index.ts                     # Shared types
      api.ts                       # API response types
  assets/
    fonts/
    images/
    icons/
  app.json                         # Expo config
  eas.json                         # EAS Build config
  babel.config.js
  metro.config.js
  tsconfig.json
  package.json
  .env.example
  .gitignore
```

TECHNOLOGY STACK:

- Framework: Expo SDK 52+ (or bare RN 0.76+ if specified)
- Language: TypeScript (strict mode)
- Navigation: expo-router (Expo) or React Navigation 7 (bare RN)
- Data Fetching: TanStack Query v5 (React Query) for server state
- Local State: Zustand (only for truly global client state — auth, theme, cart)
- Styling: NativeWind v4 (Tailwind for RN — default) or StyleSheet (if specified)
- Forms: React Hook Form + Zod validation
- Storage: expo-secure-store (tokens), @react-native-async-storage (preferences)
- HTTP: Axios with interceptors (auth header, refresh token, error normalization)
- Testing: Jest + React Native Testing Library
- Build: EAS Build (Expo) or Fastlane (bare RN)

============================================================
PHASE 3: CORE INFRASTRUCTURE
============================================================

1. **Auth Flow**:
   - Create `AuthContext` with: user, token, isLoading, login, logout, register.
   - Store tokens in expo-secure-store (not AsyncStorage).
   - Axios interceptor attaches Bearer token to all requests.
   - Axios interceptor handles 401 — attempts token refresh, then logout on failure.
   - Root layout checks auth state and redirects accordingly.
   - Protected routes redirect to login if unauthenticated.

2. **API Client** (`lib/api/client.ts`):
   - Base URL from environment variable.
   - Request interceptor: attach auth token, set Content-Type.
   - Response interceptor: normalize errors to `{ code, message }`.
   - Timeout: 30 seconds default.
   - Retry: 1 retry on network errors, no retry on 4xx.

3. **TanStack Query Setup**:
   - QueryClient in root layout with sensible defaults:
     `staleTime: 5 * 60 * 1000`, `retry: 2`, `refetchOnWindowFocus: true`.
   - Per-entity hooks: `useEntities()`, `useEntity(id)`, `useCreateEntity()`,
     `useUpdateEntity()`, `useDeleteEntity()`.
   - Optimistic updates for mutations.
   - Invalidate related queries on mutation success.

4. **Theme System**:
   - Design tokens in `lib/utils/constants.ts`: colors, spacing scale, radii, typography.
   - Light and dark mode support via `useColorScheme()`.
   - All components consume tokens — zero hardcoded colors or sizes.
   - NativeWind: configure tailwind.config.js with custom theme tokens.

5. **Environment Variables**:
   - Use expo-constants for env vars in Expo.
   - `.env.example` documenting all variables:
     ```
     EXPO_PUBLIC_API_URL=http://localhost:3000/api/v1
     EXPO_PUBLIC_APP_NAME=MyApp
     ```

============================================================
PHASE 4: SCREEN IMPLEMENTATION
============================================================

Build every screen identified in Phase 1. For each screen:

1. **Layout**: Use `ScreenWrapper` component that handles SafeAreaView, scroll behavior,
   keyboard avoidance, and consistent padding.
2. **Data**: Fetch via TanStack Query hooks. Handle loading, error, and empty states.
3. **Loading State**: Skeleton placeholders matching the final layout shape.
4. **Error State**: Retry button with error message. Never show raw error objects.
5. **Empty State**: Illustration + descriptive text + CTA button.
6. **Pull to Refresh**: On all list screens via `RefreshControl`.
7. **Infinite Scroll**: Use `onEndReached` with cursor-based pagination for long lists.
8. **Animations**: Subtle entry animations via `react-native-reanimated` where appropriate.

SCREEN QUALITY CHECKLIST (apply to every screen):

a) **Touch Targets**: All tappable areas >= 44x44pt (iOS) / 48x48dp (Android).
b) **Accessibility**: All images have `accessibilityLabel`. Interactive elements have
   `accessibilityRole` and `accessibilityHint`. Screen reader navigation order is logical.
c) **Keyboard**: Forms scroll to focused input. "Next" keyboard action moves to next field.
   "Done" submits or dismisses. `KeyboardAvoidingView` on all form screens.
d) **Platform Adaptive**: Use `Platform.select()` for iOS/Android differences.
   Alert dialogs use native platform style.
e) **Haptics**: Use `expo-haptics` for important interactions (submit, delete, toggle).
f) **Safe Areas**: Content never overlaps status bar, home indicator, or notch.

============================================================
PHASE 5: TESTING
============================================================

1. **Component Tests**: At least 1 test per screen component:
   - Renders correctly with data.
   - Shows loading state.
   - Shows error state with retry.
   - Shows empty state.

2. **Hook Tests**: Test custom hooks:
   - API hooks return correct data shape.
   - Auth hooks handle login/logout flows.

3. **Utility Tests**: Test formatters, validators, and helpers.

4. **Run Tests**: Execute `npx jest --passWithNoTests` and fix all failures.

============================================================
PHASE 6: BUILD VERIFICATION
============================================================

1. Run `npx tsc --noEmit` — fix all type errors.
2. Run `npx expo lint` or ESLint — fix all warnings and errors.
3. Verify `npx expo start` launches without errors (if Expo).
4. Verify all screens render without crashes.
5. Verify auth flow: register -> login -> protected screen -> logout -> redirect.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## React Native App Built

### Project: [name]
### Framework: [Expo / Bare RN]

### Screen Inventory
| Screen | Route | Description |
|--------|-------|-------------|

### Navigation Structure
- Tab 1: [screens]
- Tab 2: [screens]
- Auth Stack: [screens]
- Modals: [screens]

### Data Models
| Entity | Fields | API Endpoints |
|--------|--------|---------------|

### How to Run
1. `npm install`
2. `cp .env.example .env.local` and configure
3. `npx expo start` (Expo) or `npx react-native start` (bare)
4. Press `i` for iOS simulator or `a` for Android emulator

### Validation
- TypeScript: [clean / N errors fixed]
- Tests: [X passing / Y total]
- Lint: [clean / N issues fixed]

DO NOT:
- Use class components. Functional components with hooks only.
- Use Redux unless $ARGUMENTS explicitly requests it. Zustand + TanStack Query covers all cases.
- Store auth tokens in AsyncStorage. Use expo-secure-store.
- Hardcode colors, spacing, or font sizes. Use design tokens.
- Skip loading, error, or empty states on any screen.
- Use inline styles for anything beyond one-off layout tweaks.
- Ignore keyboard handling on form screens.
- Leave `console.log` statements in production code.
- Use `any` type anywhere. Define proper types for all data.
- Create screens without accessibility labels on interactive elements.

NEXT STEPS:

After building:
- "Run `/qa` to test all screens and flows end-to-end."
- "Run `/ux` to audit accessibility and design consistency."
- "Run `/api-scaffold` to generate the backend API this app consumes."
- "Run `/ship` to add a new feature to the app."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /react-native — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
