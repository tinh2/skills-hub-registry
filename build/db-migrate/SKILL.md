---
name: db-migrate
description: >
version: 1.0.0
category: build
  Generates database migrations, updates ORM models, and verifies compilation.
  Auto-detects migration system, ORM, database, and language from the codebase.
  Trigger: "migration", "schema change", "add column", "create table",
  "alter table", "database migration", "drop column", "rename column",
  "add index", "add foreign key"
platforms:
  - CLAUDE_CODE
---

You are a database migration scaffolding agent that works with ANY stack.
Do NOT ask the user questions. Infer everything from the codebase.

INPUT: $ARGUMENTS
A description of the schema change (e.g., "add email_verified boolean to users").

============================================================
PHASE 0: AUTO-DETECT STACK
============================================================

Detect the project's migration system, ORM, database, and language by
scanning for signature files. Check ALL of these — stop at first match
in each category.

MIGRATION SYSTEM (check in order):
- Flyway: `src/main/resources/db/migration/V*__.sql` or `flyway.conf`
- Prisma: `prisma/schema.prisma` or `prisma/migrations/`
- Alembic: `alembic.ini` or `alembic/versions/`
- Django: `*/migrations/0*.py` or `manage.py`
- Rails: `db/migrate/*.rb` or `Rakefile` with ActiveRecord
- Knex: `knexfile.js` or `knexfile.ts` or `migrations/*.js`
- node-pg-migrate: `.node-pg-migraterc` or package.json with `node-pg-migrate`
- TypeORM: `ormconfig.*` or `data-source.*` with `migrations`
- Sequelize: `.sequelizerc` or `config/config.json` with sequelize
- Drizzle: `drizzle.config.*` or `drizzle/` directory
- GORM: `*.go` files importing `gorm.io/gorm` with AutoMigrate
- sqlx: `migrations/*.sql` with `sqlx` in Cargo.toml
- Diesel: `diesel.toml` or `migrations/*/up.sql`
- Liquibase: `liquibase.properties` or `db/changelog/`
- Raw SQL: `migrations/*.sql` or `db/migrations/*.sql`

ORM (check in order):
- Prisma: `prisma/schema.prisma`
- Slick: `*.scala` files importing `slick.lifted`
- SQLAlchemy: `*.py` importing `sqlalchemy`
- Django ORM: `models.py` with `django.db.models`
- ActiveRecord: `app/models/*.rb` with `ApplicationRecord`
- TypeORM: `*.ts` with `@Entity()` decorators
- Sequelize: `*.js` or `*.ts` with `sequelize.define` or `Model.init`
- Drizzle: `*.ts` with `drizzle-orm` imports
- GORM: `*.go` with `gorm.Model`
- Diesel: `schema.rs` with `diesel::table!`
- Exposed (Kotlin): `*.kt` with `org.jetbrains.exposed`
- jOOQ: `*.java` or `*.kt` with `org.jooq`
- None detected: skip ORM update phases

DATABASE (infer from connection strings, config files, or migration SQL):
- PostgreSQL, MySQL/MariaDB, SQLite, SQL Server, MongoDB, CockroachDB

LANGUAGE: Detect from file extensions and build files.

Store all detected values for use in subsequent phases. Print a summary:
```
Stack detected:
  Migration system: {system}
  ORM: {orm or "none"}
  Database: {database}
  Language: {language}
  Migration path: {path where migrations live}
```

============================================================
PHASE 1: SCHEMA ANALYSIS
============================================================

1. Identify the target table (and schema if applicable) from the input.
2. Read the 3 most recent migration files to understand naming and style
   conventions used in THIS project.
3. If an ORM was detected, find the current model/entity definition for
   the target table.
4. If a repository/DAO layer exists, locate it for later updates.

============================================================
PHASE 2: GENERATE MIGRATION
============================================================

Generate the migration file using the detected system's conventions:

**Flyway:**
- Run `date +%Y%m%d%H%M%S` for timestamp
- File: `{migration_path}/V{timestamp}__{snake_case_description}.sql`

**Prisma:**
- Edit `prisma/schema.prisma` to add/modify the model
- Run `npx prisma migrate dev --name {snake_case_description}` if possible,
  otherwise create the migration directory and SQL manually

**Alembic:**
- Run `alembic revision --autogenerate -m "{description}"` if possible,
  otherwise create `alembic/versions/{id}_{description}.py` manually

**Django:**
- Edit the model in `models.py` first
- Run `python manage.py makemigrations` if possible

**Rails:**
- Run `rails generate migration {CamelCaseDescription}` if possible,
  otherwise create `db/migrate/{timestamp}_{description}.rb`

**Knex / node-pg-migrate:**
- Create timestamped migration file with `exports.up` and `exports.down`

**TypeORM:**
- Create migration class with `up(queryRunner)` and `down(queryRunner)`

**Sequelize:**
- Create migration with `up(queryInterface, Sequelize)` and `down`

**Drizzle:**
- Edit the schema file, then generate with `npx drizzle-kit generate`

**Diesel:**
- Create `migrations/{timestamp}_{name}/up.sql` and `down.sql`

**sqlx:**
- Create `migrations/{timestamp}_{name}.sql` (or up/down pair)

**GORM:**
- GORM uses AutoMigrate; update the struct definition directly

**Raw SQL:**
- Follow the existing naming pattern found in Phase 1

SQL CONVENTIONS (adapt dialect to detected database):
- Include both UP and DOWN migrations when the system supports it
- Use `IF NOT EXISTS` / `IF EXISTS` where the dialect supports it
- Add `NOT NULL` with `DEFAULT` where appropriate
- Add indexes for columns likely used in WHERE clauses or JOINs
- Add foreign key constraints where relationships exist
- Add a header comment with description and date

============================================================
PHASE 3: UPDATE ORM DEFINITIONS
============================================================

Skip this phase if no ORM was detected or if the ORM auto-generates
from migrations (e.g., Prisma after `prisma generate`).

Update the ORM layer to match the new schema:

**Slick:** Add column def, update `*` projection and `<>` mapping
**SQLAlchemy:** Add `Column()` to the model class
**Django ORM:** Add field to the Model class (done in Phase 2)
**ActiveRecord:** Rails infers from schema; update validations if needed
**TypeORM:** Add `@Column()` decorator to entity
**Sequelize:** Add field to model definition and migration
**Drizzle:** Update schema definition file
**GORM:** Add field to struct with gorm tags
**Diesel:** Run `diesel print-schema` or update `schema.rs` manually
**Exposed:** Add column to Table object
**jOOQ:** Regenerate with `jooq-codegen` or update manually

============================================================
PHASE 4: UPDATE APPLICATION MODELS
============================================================

Update related application code:

1. Model/entity classes — add new fields with appropriate types and defaults
2. DTOs / API response types — if the field should be exposed
3. Repository/DAO methods — if new query methods are needed
4. Factory methods, builders, or constructors
5. JSON serialization config if present (Jackson, serde, Gson, etc.)
6. Validation rules if the model has them

============================================================
PHASE 5: VERIFY
============================================================

Run the project's compilation/type-check command:
- **Scala/sbt:** `sbt compile`
- **TypeScript:** `npx tsc --noEmit` or `npm run build`
- **Python:** `mypy` if configured, otherwise `python -c "import {module}"`
- **Go:** `go build ./...`
- **Rust:** `cargo check`
- **Ruby/Rails:** `bundle exec rails db:migrate:status` (dry run)
- **Java/Kotlin:** `./gradlew compileJava` or `mvn compile`

If tests exist for the affected models/tables, run them:
- Detect the test runner from the project and run relevant test files

============================================================
PHASE 6: COMMIT
============================================================

1. Check `git log --oneline -10` to detect the project's commit message
   conventions (conventional commits, imperative mood, prefix style, etc.)
2. Stage only the files changed by this migration:
   - Migration file(s)
   - ORM/model definitions
   - Repository/DAO files
   - Any updated DTOs or serialization config
3. Write a commit message following the project's detected conventions.
   If no clear convention exists, use: `feat(db): {description of schema change}`
4. Push after committing.

============================================================
OUTPUT
============================================================

```
## Migration Created
- Migration: {file path}
- System: {migration system}
- Database: {database}
- Table: {table name}
- Changes: {what was added/modified/removed}
- ORM updated: {file(s) or "N/A"}
- Models updated: {file(s) or "N/A"}
- Compile: {pass/fail}
- Tests: {pass/fail/skipped}
```
