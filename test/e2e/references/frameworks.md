# Framework Detection & Commands Reference

## Framework Detection Table

Check for these files in order to identify the project stack:

| File/Pattern | Stack |
|---|---|
| pubspec.yaml with flutter SDK | Flutter |
| next.config.* or .next/ | Next.js |
| nuxt.config.* or .nuxt/ | Nuxt/Vue |
| angular.json | Angular |
| svelte.config.* | SvelteKit |
| remix.config.* | Remix |
| astro.config.* | Astro |
| vite.config.* + src/App.vue | Vue + Vite |
| vite.config.* + src/App.tsx or src/App.jsx | React + Vite |
| package.json with "react-scripts" | Create React App |
| package.json with "expo" | React Native (Expo) |
| manage.py + settings.py | Django |
| app.py or wsgi.py + requirements.txt with flask | Flask |
| main.py + requirements.txt with fastapi | FastAPI |
| go.mod | Go |
| Cargo.toml | Rust |
| Gemfile with rails | Ruby on Rails |
| deno.json or deno.jsonc | Deno |
| bunfig.toml or bun.lockb | Bun |
| package.json with fastify | Fastify (Node.js) |
| package.json with express | Express (Node.js) |
| package.json with nest | NestJS |

## Backend Detection Matrix

| Category | Options to Detect |
|---|---|
| Framework | Fastify, Express, NestJS, Django, FastAPI, Flask, Go net/http, Gin, Echo, Rails, Deno Oak/Hono, Bun Elysia/Hono |
| ORM/Database | Prisma, TypeORM, Sequelize, Django ORM, SQLAlchemy, GORM, Drizzle |
| Database | PostgreSQL, MySQL, SQLite, MongoDB, Firestore |
| Auth | JWT, session-based, OAuth, Firebase Auth, Supabase Auth, Clerk, Auth0 |
| Validation | Zod, Joi, class-validator, Pydantic, marshmallow |

## Frontend Detection Matrix

| Category | Options to Detect |
|---|---|
| Framework | Flutter, React, Next.js, Vue, Nuxt, Angular, Svelte, React Native |
| State management | Riverpod, Bloc, Redux, Zustand, Pinia, Vuex, NgRx, Jotai, MobX |
| Routing | GoRouter, react-router, Next.js app router, vue-router, Angular router |
| HTTP client | Dio, Axios, fetch, ky, got |
| UI library | Material 3, Tailwind, shadcn/ui, Chakra UI, Vuetify, PrimeVue, Angular Material |

## API Endpoint Discovery

| Framework | Discovery Method |
|---|---|
| Fastify | Read src/modules/*/routes.ts or route registration files |
| Express | Search for app.get/post/put/patch/delete and router.* calls |
| NestJS | Read *.controller.ts files for @Get/@Post/@Put/@Delete decorators |
| Django | Read urls.py files for path() and urlpatterns |
| FastAPI | Read *.py files for @app.get/@router.post decorators |
| Flask | Read *.py files for @app.route and @blueprint.route |
| Go | Search for http.HandleFunc, mux.Handle, r.GET/POST (gin/echo) |
| Rails | Read config/routes.rb |
| Deno (Oak) | Search for router.get/post/put/delete calls |
| Deno (Hono) | Search for app.get/post/put/delete calls |
| Bun (Elysia) | Search for app.get/post/put/delete or .group() calls |
| Bun (Hono) | Search for app.get/post/put/delete calls |

## Frontend Route Discovery

| Framework | Discovery Method |
|---|---|
| Flutter | Read routes.dart / GoRouter config, find all Screen/Page widgets |
| Next.js (app router) | Scan app/**/page.tsx and app/**/route.ts |
| Next.js (pages router) | Scan pages/**/*.tsx |
| React + react-router | Read route config, find all Route components |
| Vue/Nuxt | Scan pages/**/*.vue or read router config |
| Angular | Read *-routing.module.ts files |
| SvelteKit | Scan src/routes/**/+page.svelte |

## Infrastructure Setup

### Docker

- If docker-compose.yml or compose.yaml exists: `docker compose up -d`
- Wait for all services to be healthy (check with `docker compose ps`).
- If no Docker file but PostgreSQL/MySQL/Redis needed: check if the service is already running locally.

### Database Migrations

| ORM | Migration Command |
|-----|-------------------|
| Prisma | `npx prisma migrate deploy` |
| TypeORM | `npx typeorm migration:run` |
| Sequelize | `npx sequelize-cli db:migrate` |
| Django | `python manage.py migrate` |
| SQLAlchemy/Alembic | `alembic upgrade head` |
| GORM | (auto-migrates, verify connection) |
| Drizzle | `npx drizzle-kit push` |
| Rails | `rails db:migrate` |

Run seed data if available (prisma db seed, python manage.py loaddata, rails db:seed, etc.).

### Firebase (if detected)

Start emulators: `firebase emulators:start --only auth,firestore,storage,functions &`
Wait for emulators to be ready (check http://localhost:4000).

## Backend Start Commands

| Framework | Start Command |
|---|---|
| Fastify/Express/NestJS | `npm run dev` or `npx tsx src/server.ts` |
| Django | `python manage.py runserver 0.0.0.0:8000` |
| FastAPI | `uvicorn main:app --reload --port 8000` |
| Flask | `flask run --port 8000` |
| Go | `go run ./cmd/server` or `go run main.go` |
| Rails | `rails server -p 3000` |
| Deno | `deno task dev` or `deno run --allow-net --allow-read main.ts` |
| Bun | `bun run dev` or `bun run src/server.ts` |

## Frontend Start Commands

| Framework | Start Command |
|---|---|
| Next.js | `npm run dev` |
| Vite (React/Vue/Svelte) | `npm run dev` |
| Angular | `ng serve` |
| Create React App | `npm start` |
| Nuxt | `npm run dev` |

## Test Framework Installation

### Backend Test Frameworks

| Stack | Test Framework | Install Check | Install Command |
|---|---|---|---|
| Node.js (Vitest) | vitest + supertest | Check package.json devDependencies | `npm install -D vitest supertest @types/supertest` |
| Node.js (Jest) | jest + supertest | Check package.json devDependencies | `npm install -D jest supertest ts-jest @types/jest` |
| Python | pytest + httpx | Check requirements.txt or pyproject.toml | `pip install pytest httpx pytest-asyncio` |
| Go | testing (stdlib) | Always available | No install needed |
| Rails | rspec + rack-test | Check Gemfile | `bundle add rspec-rails rack-test --group test` |
| Deno | Deno.test (built-in) | Always available | No install needed |
| Bun | bun:test (built-in) | Always available | No install needed; for HTTP testing: `bun add -D supertest` |

### Frontend E2E Frameworks

| Stack | Test Framework | Install Check | Install Command |
|---|---|---|---|
| React/Next.js/Vue/Angular/Svelte (web) | Playwright | Check package.json or playwright.config.* | `npm init playwright@latest` |
| Flutter | integration_test | Check pubspec.yaml dev_dependencies | Add integration_test sdk + flutter_test sdk to pubspec.yaml |
| React Native | Detox or Maestro | Check package.json | `npx detox init` or install maestro |

## Test Run Commands

### Backend

| Framework | Run Command |
|---|---|
| Vitest | `npx vitest run tests/e2e/ --reporter=verbose` |
| Jest | `npx jest tests/e2e/ --verbose --forceExit` |
| pytest | `pytest tests/e2e/ -v --tb=short` |
| Go | `go test ./tests/e2e/... -v -count=1` |
| RSpec | `bundle exec rspec spec/e2e/ --format documentation` |
| Deno | `deno test tests/e2e/ --allow-net --allow-read` |
| Bun | `bun test tests/e2e/` |

### Frontend

| Framework | Run Command |
|---|---|
| Playwright | `npx playwright test --reporter=list` |
| Cypress | `npx cypress run --spec "cypress/e2e/**/*"` |
| Flutter integration_test | `flutter test integration_test/ --device-id <device_id> --timeout 600` |

## Coverage Commands

| Stack | Coverage Command | Output |
|---|---|---|
| Node.js (Vitest) | `npx vitest run --coverage` | coverage/ directory |
| Node.js (Jest) | `npx jest --coverage` | coverage/ directory |
| Python | `pytest --cov=. --cov-report=term-missing` | terminal + .coverage |
| Go | `go test -coverprofile=coverage.out ./...` | coverage.out |
| Flutter | `flutter test --coverage` | coverage/lcov.info |
| Deno | `deno test --coverage=coverage/` then `deno coverage coverage/` | coverage/ directory |
| Bun | `bun test --coverage` | terminal output |
