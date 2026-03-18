---
name: auth-provider
description: "Set up complete OAuth/SSO authentication with Google, GitHub, Apple, or SAML providers. Auto-detects your framework and configures the best auth library (NextAuth, Passport, Firebase Auth, Supabase, Clerk, Lucia, django-allauth). Includes session management, JWT token refresh, login/logout UI components, route protection middleware, and database schema updates. Use when you need OAuth login, social sign-in, SSO integration, authentication setup, login page, or user authentication."
version: "2.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Set up a complete authentication system with OAuth/SSO providers in the current project.
This includes SDK installation, provider configuration, session management, token refresh,
login/logout UI, and route protection.

INPUT:
$ARGUMENTS

The user may specify:
1. Providers: "google", "github", "apple", "saml", or a combination (e.g., "google github")
2. Auth library preference: "nextauth", "passport", "firebase", "supabase", "clerk", "lucia"
3. Session strategy: "jwt" (default) or "database"
If no arguments, default to Google + GitHub providers with the best-fit auth library.

=== PHASE 1: PROJECT DETECTION ===

Step 1.1 -- Detect Framework and Existing Auth

Scan for project files to determine the tech stack:

| File | Framework | Recommended Auth Library |
|------|-----------|------------------------|
| package.json with "next" | Next.js | NextAuth.js (Auth.js v5) |
| package.json with "fastify" | Fastify | @fastify/oauth2 + custom JWT |
| package.json with "express" | Express | Passport.js |
| package.json with "nestjs" | NestJS | @nestjs/passport |
| package.json with "hono" | Hono | Custom JWT + OAuth |
| requirements.txt with "django" | Django | django-allauth |
| requirements.txt with "fastapi" | FastAPI | authlib + python-jose |
| Gemfile with "rails" | Rails | devise + omniauth |
| pubspec.yaml with "firebase_auth" | Flutter | Firebase Auth |
| pubspec.yaml (no firebase) | Flutter | Supabase Auth or custom |

Check for existing auth:
- Search for auth middleware, JWT verification, session management
- Search for env vars: AUTH_SECRET, NEXTAUTH_SECRET, JWT_SECRET
- Search for login/signup routes or screens
- Search for user model/table

Record: FRAMEWORK, AUTH_LIBRARY (user-specified or auto-detected), EXISTING_AUTH

If a complete auth system already exists, report it and exit.
If partial auth exists, identify gaps and extend it.

Step 1.2 -- Parse Provider Requirements

From $ARGUMENTS, extract which providers to configure:
- "google" -> Google OAuth 2.0
- "github" -> GitHub OAuth
- "apple" -> Apple Sign-In (requires additional setup)
- "saml" -> SAML SSO (enterprise, requires identity provider configuration)
- Default if none specified: Google + GitHub

Record: PROVIDERS list

=== PHASE 2: AUTH LIBRARY INSTALLATION ===

Step 2.1 -- Install Auth Library

Based on the detected or specified auth library:

**NextAuth.js (Auth.js v5) -- for Next.js:**
```
npm install next-auth@beta @auth/prisma-adapter  (if using Prisma)
npm install next-auth@beta @auth/drizzle-adapter  (if using Drizzle)
```

**Passport.js -- for Express/Fastify/NestJS:**
```
npm install passport passport-google-oauth20 passport-github2
npm install express-session connect-pg-simple  (for database sessions)
npm install jsonwebtoken @types/jsonwebtoken  (for JWT strategy)
```

**Firebase Auth -- for Flutter or web apps using Firebase:**
```
flutter pub add firebase_auth google_sign_in  (Flutter)
npm install firebase-admin  (backend verification)
```

**Supabase Auth -- for Supabase projects:**
```
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs
flutter pub add supabase_flutter  (Flutter)
```

**django-allauth -- for Django:**
```
pip install django-allauth
```

**Lucia -- for any Node.js framework:**
```
npm install lucia @lucia-auth/adapter-prisma  (or appropriate adapter)
npm install arctic  (for OAuth helpers)
```

Install only the packages needed for the detected framework and requested providers.

Step 2.2 -- Configure Environment Variables

Add to .env.example:
```
# Auth
AUTH_SECRET=<random-32-char-string>
AUTH_URL=http://localhost:3000  (or appropriate base URL)

# Google OAuth (if requested)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# GitHub OAuth (if requested)
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Apple Sign-In (if requested)
APPLE_CLIENT_ID=
APPLE_CLIENT_SECRET=
APPLE_TEAM_ID=
APPLE_KEY_ID=
```

If the project has a config validation system, update it with the new variables.

=== PHASE 3: AUTH CONFIGURATION ===

Step 3.1 -- Create Auth Configuration Module

Create the central auth configuration at the framework-appropriate location:

**NextAuth.js:**
- Create `auth.ts` (or `src/auth.ts`) with providers, callbacks, session strategy
- Create `app/api/auth/[...nextauth]/route.ts` catch-all route
- Configure adapter (Prisma, Drizzle, or JWT-only)

**Passport.js:**
- Create `src/config/passport.ts` with strategy configuration
- Create serialization/deserialization functions
- Register strategies for each provider

**Firebase Auth:**
- Create `lib/firebase-admin.ts` for backend verification
- Create auth service with provider sign-in methods
- Configure Firebase project settings

**Lucia:**
- Create `src/lib/auth.ts` with Lucia instance
- Configure adapter for the project's database
- Set up session configuration

For EACH requested provider, configure:
1. Client ID and Client secret from environment variables
2. Callback URL (construct from AUTH_URL + provider-specific path)
3. Requested scopes (email, profile as minimum; additional based on needs)
4. Profile mapping (map provider profile to your User model)

Step 3.2 -- Database Schema Updates

If the project uses a database, create or update the auth-related tables:

**For Prisma (schema.prisma):**
```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  image         String?
  emailVerified DateTime?
  accounts      Account[]
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String?
  access_token      String?
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

Run the migration after schema changes: `npx prisma migrate dev --name add-auth-tables`

For other ORMs, create equivalent migrations.

If the project is Flutter + Firebase, skip database schema -- Firebase Auth manages this.

Step 3.3 -- Session Management

Configure session handling based on the strategy:

**JWT Strategy (default for most setups):**
- Set JWT secret from environment variables
- Configure token expiry (default: access token 15 min, refresh token 7 days)
- Include user ID, email, and role in JWT payload
- Sign tokens with HS256 or RS256

**Database Session Strategy:**
- Store sessions in the database (Session table)
- Configure session expiry (default: 30 days)
- Set up session cleanup cron or lazy cleanup

**Token Refresh Flow:**
- Create a refresh endpoint: POST /api/auth/refresh
- Accept the refresh token, verify it, issue a new access token
- Rotate refresh tokens on each use (one-time use tokens)
- Handle expired refresh tokens by requiring re-authentication

=== PHASE 4: AUTH MIDDLEWARE ===

Step 4.1 -- Create Auth Middleware

Create middleware that can protect routes/pages:

**For API routes:**
- Extract token from Authorization header (Bearer scheme)
- Verify the JWT signature and expiry
- Attach the decoded user to the request context
- Return 401 for missing/invalid tokens
- Return 403 for insufficient permissions (if roles are implemented)

**For Next.js:**
- Create `middleware.ts` at the project root
- Define protected routes using matcher config
- Redirect unauthenticated users to login page

**For Flutter:**
- Create an auth state provider (Riverpod, BLoC, etc.)
- Create a route guard that redirects to login when unauthenticated
- Persist auth tokens in secure storage (flutter_secure_storage)

Step 4.2 -- Create Auth Helper Functions

Create utility functions:
```
getCurrentUser(request):
  - Extract and verify the token from the request
  - Return the user object or null

requireAuth(request):
  - Same as getCurrentUser but throws 401 if not authenticated

requireRole(request, role):
  - Same as requireAuth but also checks user role
  - Throws 403 if insufficient permissions

isAuthenticated(request):
  - Returns boolean -- does not throw
```

=== PHASE 5: LOGIN/LOGOUT UI ===

Step 5.1 -- Create Login Page/Screen

**For Next.js / React:**
Create a login page with:
- Provider sign-in buttons (styled with provider brand colors and icons)
- Google: white background, Google "G" logo
- GitHub: dark background, GitHub octocat icon
- Apple: black background, Apple logo
- Loading state on each button during redirect
- Error display for failed authentication attempts
- Redirect to callback URL or dashboard after success

**For Flutter:**
Create a login screen with:
- Provider sign-in buttons following platform design guidelines
- Google Sign-In button (use official google_sign_in package)
- Apple Sign-In button (use sign_in_with_apple package, iOS only)
- Loading indicators during authentication
- Error snackbar for failures
- Navigation to home screen after success

**For API-only backends (no frontend):**
- Document the OAuth flow endpoints
- Create a simple test HTML page (optional) for manual testing

Step 5.2 -- Create Logout Flow

Create logout functionality:
- Clear the session/token on the server side
- Clear client-side token storage
- Redirect to login page or home page
- Revoke provider tokens if applicable (optional but recommended)

Step 5.3 -- Create Auth State UI Components

Create reusable auth-aware components:
- **UserAvatar:** Displays user's profile image from the OAuth provider
- **AuthGuard:** Wrapper component that shows login prompt if unauthenticated
- **UserMenu:** Dropdown with user info, settings link, and logout button

=== PHASE 6: ROUTE PROTECTION ===

Step 6.1 -- Protect Existing Routes

Scan the project for routes/pages that should be protected:
- Any route under /dashboard, /settings, /profile, /account
- Any API route that accesses user-specific data
- Any route that creates, updates, or deletes resources

Apply the auth middleware to these routes.

Step 6.2 -- Create Auth Callback Routes

For each provider, ensure the callback route is configured:
- Google: /api/auth/callback/google
- GitHub: /api/auth/callback/github
- Apple: /api/auth/callback/apple

These must match the redirect URIs configured in the provider's developer console.

=== PHASE 7: VERIFICATION ===

Step 7.1 -- Static Verification

Run the project's type checker and linter:
- Fix all errors introduced by the auth integration
- Ensure all imports resolve
- Verify database migrations apply cleanly

Step 7.2 -- Auth Flow Checklist

Verify and report:
- [ ] Auth library installed and configured
- [ ] Environment variables documented in .env.example
- [ ] OAuth providers configured (one per requested provider)
- [ ] Database schema updated with User, Account, Session models (if using DB)
- [ ] Session management configured (JWT or database)
- [ ] Token refresh flow implemented
- [ ] Auth middleware created for route protection
- [ ] Login page/screen created with provider buttons
- [ ] Logout flow implemented
- [ ] Auth callback routes configured
- [ ] Protected routes identified and guarded
- [ ] Type checking passes

=== OUTPUT ===

Print the following summary:

---
## Auth Integration Complete

**Framework:** [detected framework]
**Auth library:** [library used]
**Providers:** [list of configured providers]
**Session strategy:** [JWT | database]

### Files Created/Modified
| File | Purpose |
|------|---------|
| [path] | [description] |

### Environment Variables Required
| Variable | Purpose | Where to get it |
|----------|---------|-----------------|
| AUTH_SECRET | Session encryption | Generate: `openssl rand -base64 32` |
| GOOGLE_CLIENT_ID | Google OAuth | Google Cloud Console > Credentials |
| GOOGLE_CLIENT_SECRET | Google OAuth | Google Cloud Console > Credentials |
| GITHUB_CLIENT_ID | GitHub OAuth | GitHub Settings > Developer > OAuth Apps |
| GITHUB_CLIENT_SECRET | GitHub OAuth | GitHub Settings > Developer > OAuth Apps |

### OAuth Callback URLs to Register
| Provider | Callback URL |
|----------|-------------|
| Google | http://localhost:3000/api/auth/callback/google |
| GitHub | http://localhost:3000/api/auth/callback/github |

### Protected Routes
[List of routes that now require authentication]

### Provider Setup Instructions
**Google:**
1. Go to Google Cloud Console > APIs & Services > Credentials
2. Create OAuth 2.0 Client ID (Web application)
3. Add authorized redirect URI: [callback URL]
4. Copy Client ID and Secret to .env

**GitHub:**
1. Go to GitHub Settings > Developer Settings > OAuth Apps
2. Create a new OAuth App
3. Set Authorization callback URL: [callback URL]
4. Copy Client ID and Secret to .env
---

=== NEXT STEPS ===

After auth integration:
- "Run `/stripe` to add payments (will automatically link to authenticated users)."
- "Run `/email` to add email verification and password reset flows."
- "Run `/push-notifications` to add push notifications (requires user identity)."
- "Run `/integrate audit` to check overall integration health."

=== DO NOT ===

- Do NOT store passwords in plaintext -- this skill uses OAuth only, not password auth.
- Do NOT skip token verification in the auth middleware -- always verify signatures.
- Do NOT store access tokens in localStorage -- use httpOnly cookies or secure storage.
- Do NOT use symmetric JWT signing (HS256) with a weak secret -- generate a strong random key.
- Do NOT trust the client to send user identity -- always verify on the server.
- Do NOT skip CSRF protection on auth endpoints -- use state parameters in OAuth flow.
- Do NOT hardcode OAuth credentials in source code -- always use environment variables.
- Do NOT implement custom OAuth flows when a well-maintained library exists for the framework.
- Do NOT skip the token refresh flow -- expired tokens cause poor UX if users must re-login.
- Do NOT expose internal auth errors to the client -- return generic "authentication failed" messages.
- Do NOT ignore the email verification state from providers -- check emailVerified before granting access.
- Do NOT create a User model that conflicts with an existing one -- extend the existing model.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the integration, validate:

1. Run the project's test suite to verify the integration works end-to-end.
2. Run build/compile to confirm no breakage.
3. Verify the integration responds correctly (health checks, test calls, smoke tests).
4. If failures occur, diagnose from error output and apply minimal fixes.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Document the integration state and what's blocking
- Include error output and attempted fixes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /auth-provider — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
