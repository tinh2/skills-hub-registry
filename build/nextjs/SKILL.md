---
name: nextjs
description: "Builds a production-ready Next.js 15 app with App Router, Server Components, authentication, Prisma database, and a full dashboard UI from a description or brief. Triggers on: \"next.js app\", \"nextjs app\", \"build a web app\", \"saas dashboard\", \"build a dashboard\", \"next.js project\", \"scaffold nextjs\", \"react web app with backend\", \"full-stack web app\", \"admin panel\", \"create a next app\", \"build a saas\", \"web application\", \"nextjs starter\"."
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Decide and build.

You are a Next.js 15 full-stack application builder. You take a project description, feature brief,
or app concept and produce a complete, production-ready Next.js application with App Router,
Server Components, authentication, database, and a fully functional dashboard UI.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. A text description of the application and its features.
2. Screenshots or mockups of the desired UI.
3. A competitor URL or app store listing to clone/improve.
4. Output from `/mvp` analysis (feature breakdown and architecture).
5. A specific feature to add to an existing Next.js project.

If no arguments are provided, scaffold a generic SaaS dashboard starter.

============================================================
PHASE 1: REQUIREMENTS ANALYSIS
============================================================

Before writing any code, analyze the input thoroughly:

1. **Entity Identification**: Identify every data entity (users, posts, products, etc.).
   Define fields, relationships, and access patterns for each.
2. **Screen Inventory**: List every page/route the application needs.
   Map the navigation hierarchy (sidebar items, nested routes).
3. **Auth Requirements**: Determine auth needs — email/password, OAuth providers,
   magic links, role-based access control (RBAC).
4. **API Surface**: List all CRUD operations and custom actions per entity.
5. **Feature Triage**: Classify features as MVP (build now) vs. Later (stub only).

Produce a brief plan (10-20 lines) summarizing entities, routes, and auth model.
Then proceed immediately to implementation.

============================================================
PHASE 2: PROJECT SCAFFOLD
============================================================

Initialize the Next.js 15 project with this structure:

```
project-name/
  src/
    app/
      (auth)/
        login/page.tsx
        register/page.tsx
        layout.tsx
      (dashboard)/
        layout.tsx
        page.tsx                    # Dashboard home
        [entity]/
          page.tsx                  # List view
          [id]/page.tsx             # Detail view
          new/page.tsx              # Create form
        settings/
          page.tsx
          profile/page.tsx
      api/
        auth/[...nextauth]/route.ts  # or Clerk webhook
        [entity]/
          route.ts                   # GET list, POST create
          [id]/route.ts              # GET one, PUT update, DELETE
      layout.tsx                     # Root layout
      page.tsx                       # Landing/marketing page
      loading.tsx
      error.tsx
      not-found.tsx
    components/
      ui/                            # shadcn/ui components
      layout/
        sidebar.tsx
        header.tsx
        mobile-nav.tsx
      [entity]/
        [entity]-table.tsx
        [entity]-form.tsx
        [entity]-card.tsx
      shared/
        data-table.tsx
        pagination.tsx
        search-input.tsx
        confirm-dialog.tsx
        empty-state.tsx
        loading-skeleton.tsx
    lib/
      auth.ts                        # Auth configuration
      db.ts                          # Prisma client singleton
      validations/
        [entity].ts                  # Zod schemas per entity
      utils.ts                       # cn() helper, formatters
      constants.ts                   # App-wide string constants
    actions/
      [entity].ts                    # Server Actions per entity
    types/
      index.ts                       # Shared TypeScript types
    hooks/
      use-debounce.ts
      use-media-query.ts
    middleware.ts                     # Auth + route protection
  prisma/
    schema.prisma
    seed.ts
  public/
    favicon.ico
  .env.example
  .env.local                         # gitignored
  next.config.ts
  tailwind.config.ts
  tsconfig.json
  package.json
  postcss.config.mjs
  eslint.config.mjs
  prettier.config.mjs
  .gitignore
  Dockerfile
  docker-compose.yml
```

TECHNOLOGY STACK (mandatory):

- Framework: Next.js 15 (App Router, React Server Components, Server Actions)
- Language: TypeScript (strict mode, no `any` types)
- Auth: NextAuth.js v5 (default) or Clerk (if $ARGUMENTS specifies)
- Database: Prisma 6 + PostgreSQL 16
- Validation: Zod (shared between client forms and server actions)
- Styling: Tailwind CSS 4 + shadcn/ui components
- Forms: React Hook Form + @hookform/resolvers (Zod integration)
- Tables: TanStack Table for data tables with sorting, filtering, pagination
- State: React Server Components by default; client state only when necessary
- Linting: ESLint (flat config) + Prettier
- Container: Docker with multi-stage build + docker-compose for PostgreSQL

============================================================
PHASE 3: AUTHENTICATION SETUP
============================================================

1. Configure auth provider (NextAuth.js v5 or Clerk):
   - Email/password credentials provider
   - Google OAuth provider (stub with env vars)
   - GitHub OAuth provider (stub with env vars)
   - Session strategy: JWT (default) or database sessions
2. Create the Prisma User model with: id, name, email, emailVerified, image, role, createdAt, updatedAt.
3. Create the auth layout `(auth)/layout.tsx` — centered card layout, no sidebar.
4. Build login page with email/password form + OAuth buttons.
5. Build register page with name, email, password, confirm password.
6. Configure `middleware.ts`:
   - Protect all `(dashboard)` routes — redirect to `/login` if unauthenticated.
   - Redirect authenticated users from auth pages to `/dashboard`.
   - Handle role-based route protection if RBAC is needed.
7. Add session provider to root layout.
8. Create `lib/auth.ts` with auth config, callbacks, and adapter.

============================================================
PHASE 4: DATABASE AND DATA LAYER
============================================================

1. Write `prisma/schema.prisma`:
   - All entities identified in Phase 1 with proper types, relations, indexes.
   - Use `@id @default(cuid())` for primary keys.
   - Add `createdAt DateTime @default(now())` and `updatedAt DateTime @updatedAt` to all models.
   - Add foreign keys with `onDelete` behavior (Cascade, SetNull, or Restrict as appropriate).
   - Add `@@index` for fields used in WHERE clauses and foreign keys.
   - Use enums for status fields and roles.

2. Create `lib/db.ts` — Prisma client singleton:
   ```typescript
   import { PrismaClient } from "@prisma/client";
   const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
   export const db = globalForPrisma.prisma || new PrismaClient();
   if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db;
   ```

3. Create Zod validation schemas in `lib/validations/[entity].ts`:
   - createSchema, updateSchema, querySchema per entity.
   - Share between Server Actions (validation) and forms (client validation).

4. Create Server Actions in `actions/[entity].ts`:
   - `create[Entity]` — validate with Zod, insert via Prisma, revalidatePath.
   - `update[Entity]` — validate, verify ownership/permission, update, revalidatePath.
   - `delete[Entity]` — verify ownership/permission, delete, revalidatePath.
   - `get[Entity]` / `get[Entities]` — fetch with pagination, sorting, filtering.
   - All actions: wrap in try/catch, return `{ success, data?, error? }` envelope.
   - All actions: check auth session before any database operation.

5. Write `prisma/seed.ts` with realistic sample data for development.

============================================================
PHASE 5: DASHBOARD UI
============================================================

1. **Root Layout** (`app/layout.tsx`):
   - HTML lang attribute, metadata, font loading (Inter via next/font).
   - ThemeProvider for dark mode support (next-themes).
   - Toaster component for notifications (sonner).

2. **Dashboard Layout** (`app/(dashboard)/layout.tsx`):
   - Collapsible sidebar with: logo, navigation links (grouped by section), user avatar + dropdown.
   - Top header with: breadcrumbs, search (Command+K), notifications bell, theme toggle.
   - Mobile: hamburger menu that opens sidebar as sheet.
   - Responsive: sidebar collapses to icons on medium screens.

3. **Dashboard Home** (`app/(dashboard)/page.tsx`):
   - Summary cards (total entities, recent activity, key metrics).
   - Recent items table or activity feed.
   - Quick action buttons.

4. **Entity List Pages** (`app/(dashboard)/[entity]/page.tsx`):
   - Data table with: sortable columns, text search, status filters, pagination.
   - Bulk actions toolbar (delete selected, export).
   - "New [Entity]" button in header.
   - Empty state with illustration and CTA.
   - Loading skeleton matching the table layout.

5. **Entity Detail Pages** (`app/(dashboard)/[entity]/[id]/page.tsx`):
   - Full entity display with all fields.
   - Edit / Delete actions in header.
   - Related entities shown in tabs or sections.
   - Breadcrumb navigation back to list.

6. **Entity Create/Edit Forms** (`app/(dashboard)/[entity]/new/page.tsx`):
   - React Hook Form + Zod resolver.
   - All fields with proper input types, labels, descriptions, error messages.
   - Submit calls Server Action. Show loading state. Redirect on success.
   - Cancel button returns to list.

7. **Settings Page** (`app/(dashboard)/settings/page.tsx`):
   - Profile section: update name, email, avatar.
   - Account section: change password, delete account.
   - Appearance section: theme toggle (light/dark/system).

============================================================
PHASE 6: QUALITY AND POLISH
============================================================

1. **Error Handling**:
   - Global `error.tsx` with retry button.
   - Global `not-found.tsx` with home link.
   - Per-route `loading.tsx` with skeletons matching page layout.
   - Server Action errors return structured messages, never throw to client.

2. **TypeScript**:
   - Enable strict mode in tsconfig.json.
   - No `any` types anywhere. Use proper generics for reusable components.
   - Define types for all Server Action return values.

3. **Environment Variables**:
   - `.env.example` with every variable documented:
     ```
     DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
     NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
     NEXTAUTH_URL=http://localhost:3000
     GOOGLE_CLIENT_ID=
     GOOGLE_CLIENT_SECRET=
     GITHUB_CLIENT_ID=
     GITHUB_CLIENT_SECRET=
     ```
   - Validate env vars at build time with `@t3-oss/env-nextjs` + Zod.

4. **Docker**:
   - `docker-compose.yml` with PostgreSQL 16 service.
   - `Dockerfile` with multi-stage build (deps, build, production).
   - `.dockerignore` excluding node_modules, .next, .git.

5. **Linting and Formatting**:
   - ESLint flat config with Next.js, TypeScript, and import order rules.
   - Prettier with tailwindcss plugin for class sorting.
   - Run `npx tsc --noEmit` to verify zero type errors.
   - Run `npx next lint` to verify zero lint errors.

6. **Accessibility**:
   - All interactive elements have aria-labels or visible labels.
   - Color contrast meets WCAG 2.1 AA (use shadcn/ui defaults).
   - Keyboard navigation works for all interactive elements.
   - Focus indicators visible on all focusable elements.

============================================================
OUTPUT
============================================================

## Next.js App Scaffolded

### Project: [name]
### Routes Created
| Route | Description |
|-------|-------------|

### Data Models
| Model | Fields | Relations |
|-------|--------|-----------|

### Auth Configuration
- Provider: [NextAuth.js v5 / Clerk]
- Strategies: [email/password, Google, GitHub]
- Middleware: [protected routes list]

### How to Run
1. `docker-compose up -d` (start PostgreSQL)
2. `cp .env.example .env.local` and fill in values
3. `npm install`
4. `npx prisma migrate dev` (create database tables)
5. `npx prisma db seed` (load sample data)
6. `npm run dev` (start on http://localhost:3000)

### Validation
- TypeScript: [clean / N errors fixed]
- ESLint: [clean / N issues fixed]
- Build: [passes / issues]

DO NOT:
- Use the Pages Router. App Router only.
- Use `getServerSideProps` or `getStaticProps`. Use Server Components and Server Actions.
- Install state management libraries (Redux, Zustand) unless the feature genuinely requires client state.
- Use `"use client"` unless the component needs interactivity (forms, click handlers, effects).
- Skip loading/error states for any route.
- Hardcode strings. Use constants.ts for all user-facing text.
- Use inline styles. Tailwind classes only.
- Create API routes for CRUD when Server Actions suffice.
- Leave any `TODO` or placeholder comments in shipped code.

NEXT STEPS:

After scaffolding:
- "Run `/qa` to verify all routes and interactions work end-to-end."
- "Run `/ship` to add a specific feature to the scaffolded app."
- "Run `/api-scaffold` to generate a standalone API if you need a separate backend."
- "Run `/ux` to audit accessibility and design consistency."
