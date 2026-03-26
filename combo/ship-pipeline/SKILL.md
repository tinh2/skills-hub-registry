---
name: ship-pipeline
description: "Full-stack app pipeline — build, test, review, and deploy across one or ALL repos. Scans CLAUDE.md, MEMORY.md, TODOs, open PRs, and issues for shippable work. Supports 'ship all' for multi-repo. Use when: 'build and ship', 'ship it', 'ship all', 'deploy everything', 'full pipeline', 'what needs shipping', 'end to end'."
version: "3.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

# Ship Pipeline

Full-stack app development pipeline — frontend (Flutter/Next.js), backend (Node/Fastify/Cloud Functions),
database (Firestore/PostgreSQL/Supabase), infrastructure (CI/CD, deploy, monitoring).
Ralph Wiggum builds it fast, the safety net catches everything before production.

Do NOT ask the user questions unless truly blocked. Run the entire pipeline autonomously.

## INPUT

$ARGUMENTS — what to build or ship. Can be:
- A feature description ("add a settings page with dark mode toggle")
- A full-stack feature ("add Stripe payments with webhook handler and checkout screen")
- A backend-only feature ("add email verification endpoint")
- A spec or story (from /spec output)
- A screenshot or design reference
- **"ship"** or **"deploy"** — ship uncommitted changes in the current repo
- **"ship all"** — scan ALL repos in the current directory (or ~/personal/) for anything shippable and ship everything

If no arguments provided, check for uncommitted changes and ship those.

============================================================
PHASE 0: CONTEXT & DISCOVERY
============================================================

### 0.1 Multi-Repo Detection

If the user said "ship all" or "all", or if the current directory contains multiple git repos:

1. Scan for all git repos: `find . -maxdepth 2 -name ".git" -type d`
2. For each repo, gather:
   - Uncommitted changes (`git status --short`)
   - Unpushed commits (`git log origin/main..HEAD --oneline`)
   - Dirty worktrees
   - Failing CI (`gh api repos/{owner}/{repo}/actions/runs?per_page=1`)
3. Present the ship manifest:

```
SHIP MANIFEST
====================================
pet-sitter:       3 uncommitted files, 0 unpushed
recipe-ai:        clean, 2 unpushed commits
confidence-coach:  clean, clean
skills-hub:       1 uncommitted, 0 unpushed, CI failing
deal-worthy:      clean, clean
====================================
Repos to ship: 3 (pet-sitter, recipe-ai, skills-hub)
Repos clean: 2 (confidence-coach, deal-worthy)
```

4. For each repo with something to ship, run Phases 0.2 through 4 sequentially.
   Use subagents for repos that are independent (no shared state).

### 0.2 Project Discovery (per repo, 30 seconds max)

1. Read CLAUDE.md for project conventions, stack, and architecture.
2. Read MEMORY.md for debt items, open issues, or pending work from last /recall.
3. Scan for shippable items:
   - `git status` — uncommitted changes
   - `git log origin/main..HEAD` — unpushed commits
   - `grep -r "TODO\|FIXME\|WIP\|HACK" --include="*.ts" --include="*.dart" --include="*.tsx" -l` — unfinished work in code
   - `docs/` — any specs or stories that reference unimplemented features
   - `gh pr list --state open` — open PRs that might need merging
   - `gh issue list --state open --limit 5` — open issues assigned to you
4. Identify the tech stack:
   - Flutter (Dart) — check pubspec.yaml
   - Web backend (Node/Express/Fastify) — check package.json
   - Database (Firebase/Supabase/PostgreSQL) — check configs
   - State management (Riverpod/Bloc/Provider) — check imports
5. Summarize in 3 bullets: what exists, what's shippable, what's the priority.

DO NOT spend more than 30 seconds per repo on this phase.

============================================================
PHASE 1: ARCH REVIEW (if new feature)
============================================================

Skip this phase if the user said "deploy" or "ship" (feature already exists).

Run a quick architectural review of the proposed changes:

1. COMPONENT REUSE CHECK: Search for existing screens/widgets that do similar things.
   If 50%+ overlap exists, extend the existing component — do NOT create a new one.

2. SERVICE ARCHITECTURE CHECK: If adding new data operations, verify they go in the
   right domain service (not a god-object service file).

3. FIRESTORE/DB RULES CHECK (if Firebase): Design security rules upfront for any
   new collections. Write rules in the SAME commit as the feature.

4. FILE SIZE CHECK: No new file should exceed 300 lines on creation. Plan the
   decomposition before writing.

Output: One paragraph summary of the plan. Then move immediately to Phase 2.

============================================================
PHASE 2: RALPH MODE — BUILD IT (60% of time budget)
============================================================

Build the feature with maximum velocity. This is Ralph Wiggum energy.

RULES:
- Ship working code, not perfect code. Polish comes later.
- One feature at a time. No scope creep.
- Use existing patterns from the codebase — don't invent new ones.
- Every screen gets: loading state, error state, empty state. No exceptions.
- Every interactive element gets: 48dp touch target, Semantics wrapper. No exceptions.
- Use design tokens from the theme (AppSpacing, AppColors, etc.), not hardcoded values.
- Write tests ALONGSIDE features, not after. Every screen gets a widget test.

FOR FLUTTER FRONTEND:
- New screens follow the existing screen pattern (ConsumerWidget/ConsumerStatefulWidget)
- State management follows existing provider pattern (Riverpod/Bloc/whatever's used)
- Navigation follows existing router pattern (GoRouter/auto_route/Navigator)
- Models include fromJson/toJson/fromFirestore as needed
- Services are domain-split (BookingService, UserService — not one giant service)
- Screens must handle: loading state, error state, empty state, offline state

FOR BACKEND (Node/Fastify/Express/Cloud Functions):
- New endpoints follow existing route pattern and naming conventions
- Input validation with Zod/Joi/class-validator on every endpoint
- Error handling: typed errors with codes, never leak internal details to client
- Auth middleware on every protected endpoint
- Rate limiting on public endpoints
- Database queries use parameterized queries (no string interpolation)
- Cloud Functions: idempotency keys on mutations, proper error codes (HttpsError)
- Tests: at least 2 tests per endpoint (happy path + error case)

FOR DATABASE (Firestore/PostgreSQL/Supabase):
- Schema changes tracked via migrations (Prisma migrate, node-pg-migrate, etc.)
- Firestore: security rules written in the SAME commit as the feature
- Every new collection/table has indexes for expected query patterns
- No raw DDL edits without a migration tool
- Seed data for development/testing if new tables added

FOR WEB FRONTEND (Next.js/React):
- New pages follow existing route pattern (App Router conventions)
- API calls go through a typed client (not raw fetch scattered everywhere)
- Server Components by default, Client Components only when needed
- SEO: proper meta tags, OpenGraph, title for every page
- Input validation on every form field
- Error boundaries around async components

FOR CI/CD & INFRASTRUCTURE:
- Workflow files validated before push (runner labels, secret refs, artifact paths)
- Docker builds tested locally before pushing (if Dockerized)
- Environment variables documented in .env.example
- No secrets in source code — use GitHub Secrets or env vars

COMMIT AFTER EACH LOGICAL UNIT:
- Screen + provider + service + test = one commit
- Use conventional commits: `feat: add settings screen with dark mode toggle`
- Never commit secrets, .env files, or PII

============================================================
PHASE 3: SAFETY NET — VERIFY EVERYTHING (30% of time budget)
============================================================

Ralph built it. Now make sure it doesn't blow up in production.

Run these checks IN ORDER. Fix issues as you find them — don't just report them.

### 3.1 Tests
```
flutter test          # or: npm test, pnpm test
flutter analyze       # or: tsc --noEmit
dart format --set-exit-if-changed .
```
If tests fail: fix the test or the code. Re-run until green.
If analyzer has issues: fix them. Zero issues required.
If formatting fails: run `dart format .` and commit.

### 3.2 Security Review (quick pass)
Check for:
- [ ] No API keys or secrets in source code
- [ ] No PII logged or exposed in error messages
- [ ] Input validation on all user-facing forms
- [ ] Firestore rules cover all new collections (if Firebase)
- [ ] No SQL injection vectors (if SQL)
- [ ] Auth checks on all new endpoints/screens that need them

### 3.3 Accessibility Check
- [ ] Every image/icon has semanticLabel or alt text
- [ ] Touch targets are 48dp minimum
- [ ] Contrast ratios meet WCAG AA (4.5:1 text, 3:1 large text)
- [ ] Screen reader can navigate all interactive elements

### 3.4 Performance Check
- [ ] No unnecessary rebuilds (const constructors where possible)
- [ ] Lists use ListView.builder (not Column with children for long lists)
- [ ] Images are appropriately sized (not loading 4K images for thumbnails)
- [ ] No blocking operations on the main thread

### 3.5 Design Consistency
- [ ] Colors use theme tokens (no hardcoded hex values)
- [ ] Spacing uses AppSpacing tokens (no magic numbers)
- [ ] Typography uses theme text styles
- [ ] New screens match existing design language

Fix EVERY issue found. Commit fixes separately: `fix: resolve analyzer warnings`

============================================================
PHASE 4: PREFLIGHT & SHIP (10% of time budget)
============================================================

### 4.1 Preflight
- `git status` — no uncommitted changes
- `git diff origin/main` — review the full diff one more time
- All tests pass
- Build succeeds: `flutter build web` or `flutter build apk --debug`
- No TODO or FIXME left in new code

### 4.2 Push
- Push to main (if solo project per CLAUDE.md) or create PR (if team project)
- If pre-push hook exists, let it run — fix any failures

### 4.3 Deploy (if deploy workflows exist)
- Check for deploy workflows: `ls .github/workflows/deploy*`
- If found, trigger: `gh workflow run deploy.yml`
- Monitor until deploy succeeds or fails
- If deploy fails on a fixable issue (build number, signing, path): fix and retry once

### 4.4 If deploying to App Stores:
- iOS: `gh workflow run deploy-ios.yml` (or `fastlane ios upload`)
- Android: `gh workflow run deploy-android.yml -f track=internal`
- Wait for both to complete
- Report upload status

============================================================
OUTPUT
============================================================

After the pipeline completes, print:

```
## Ship Pipeline Complete

**Feature:** {what was built}
**Commits:** {N} commits
**Tests:** {pass count} passing, {fail count} failing
**Analyzer:** {issue count} issues (should be 0)

### What shipped
- {bullet summary of each commit}

### Safety checks
- Tests: PASS
- Security: PASS (or: {issues found and fixed})
- A11y: PASS (or: {issues found and fixed})
- Performance: PASS
- Design consistency: PASS

### Deploy
- CI: {status}
- TestFlight: {status or N/A}
- Play Store: {status or N/A}

### Time
- Build: {X} min
- Safety net: {X} min
- Deploy: {X} min
```

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md`

Entry format:
### /ship-pipeline -- {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Feature: {{what was built}}
- Commits: {{N}}
- Tests: {{pass/fail count}}
- Security issues: {{N found, N fixed}}
- A11y issues: {{N found, N fixed}}
- Deploy: {{success/failure/skipped}}
- Self-healed: {{yes -- what | no}}
- Bottleneck: {{which phase took longest}}
- Suggestion: {{improvement idea or "none"}}

Only log if the memory directory exists. Skip silently if not found.
