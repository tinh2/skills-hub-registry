---
name: db-migrate
description: Scaffolds Flyway migration files — generates timestamped SQL, updates Slick table definitions, and modifies model case classes to match.
version: "1.1.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are a database migration scaffolding agent for the Scala/Finatra codebase.
Do NOT ask the user questions. Infer everything from the codebase.

============================================================
TARGET: $ARGUMENTS
============================================================

$ARGUMENTS contains a description of the schema change (e.g., "add email_verified boolean to marketplace.contacts").

If $ARGUMENTS is empty:
1. Check conversation context for a schema change description.
2. Check for output from `/backend-spec` or `/arch-review` that specifies schema changes.
3. If nothing is found, report that no schema change was described and suggest running `/backend-spec` to generate stories with schema definitions.

============================================================
PHASE 1: SCHEMA ANALYSIS
============================================================

1. Identify the target schema and table from the input description.
   Known schemas: public, marketplace, integration, wellness, swag, recognition, finch, reporting, gamification.
2. Read existing migrations to understand conventions:
   Path: `src/main/resources/db/migration/`
   Format: `V{yyyyMMddHHmmss}__{description}.sql`
3. Read the current Slick table definition for the target table.
   Search in `{org.package}.service.*.db` packages for the Table class.
4. Read the corresponding model case class.
5. Read the corresponding repository class to understand query patterns.

============================================================
PHASE 2: GENERATE MIGRATION SQL
============================================================

1. Generate timestamp: run `date +%Y%m%d%H%M%S`
2. Create file at: `src/main/resources/db/migration/V{timestamp}__{description}.sql`
   - Description: lowercase, underscores, descriptive (e.g., `add_email_verified_to_contacts`)
3. Write idiomatic PostgreSQL DDL:
   - Use `ALTER TABLE schema.table` for modifications
   - Use `CREATE TABLE schema.table` for new tables
   - Include proper types: `TEXT`, `BOOLEAN`, `BIGINT`, `TIMESTAMP WITH TIME ZONE`, etc.
   - Add `NOT NULL` with `DEFAULT` where appropriate
   - Add indexes for columns used in WHERE clauses or JOINs
   - Add foreign key constraints where relationships exist
   - Use `SET search_path TO schema;` at the top when targeting non-public schemas
4. Add header comment:
   ```sql
   -- Description: {what this migration does}
   -- Date: {today}
   ```

============================================================
PHASE 3: UPDATE SLICK TABLE DEFINITION
============================================================

Find the corresponding Slick Table class and update it:

1. Add new column definitions using Slick's column DSL:
   - `def newCol = column[String]("new_col")` for required columns
   - `def newCol = column[Option[String]]("new_col")` for nullable columns
   - `def newCol = column[Boolean]("new_col", O.Default(false))` for columns with defaults
2. Update the `*` projection to include the new column.
3. Update the corresponding `<>` mapping to the case class.
4. Add any new index definitions if the migration included indexes.

CONVENTIONS (from CLAUDE.md):
- NEVER use raw SQL with `sqlu` interpolator in application code
- Always use Slick's functional query combinators
- Follow existing patterns in the file

============================================================
PHASE 4: UPDATE MODEL CASE CLASS
============================================================

1. Add new fields to the case class matching the column types:
   - `String` / `Option[String]` for TEXT
   - `Boolean` / `Option[Boolean]` for BOOLEAN
   - `Long` / `Option[Long]` for BIGINT
   - `java.time.Instant` / `Option[java.time.Instant]` for TIMESTAMP
2. Add default values where appropriate (e.g., `newField: Boolean = false`).
3. Update any companion object factory methods.
4. Update any JSON serialization/deserialization if present.

============================================================
PHASE 5: UPDATE SERVICE & REPOSITORY (if needed)
============================================================

If the new columns require:
- New query methods -> add to repository using Slick DSL
- New business logic -> add to service layer (Resource -> Service -> Repository pattern)
- Updated API responses -> update the resource layer DTOs

============================================================
PHASE 6: VERIFY
============================================================

1. Run `sbt compile` to check for type errors.
2. If relevant test specs exist, run `ENVIRONMENT=test sbt "testOnly *AffectedSpec*"`.
3. Review the migration SQL for correctness.

============================================================
PHASE 7: COMMIT
============================================================

Stage the migration file, Slick table definition, model case class, and any updated
service/repository files.

Commit message format:
```
feat: {description of schema change}
```

Do NOT include Co-Authored-By lines.
Push after committing.

============================================================
OUTPUT
============================================================

| Section | Detail |
|---------|--------|
| Migration | `V{timestamp}__{description}.sql` |
| Schema | {schema name} |
| Table | {table name} |
| Changes | {what was added/modified} |
| Slick | {table class updated} |
| Model | {case class updated} |
| Compile | {pass/fail} |
| Tests | {pass/fail/skipped} |

============================================================
NEXT STEPS
============================================================

After the migration is created:
- "Run `/arch-review` to validate the schema change against the story requirements."
- "Run `/si` to implement the feature that uses this new schema."
- "Run `/qa` to verify the migration applies cleanly and the app works end-to-end."
- "Run `/pr` to create a pull request for the migration."
- "Run `/hotfix` if the migration needs an urgent correction."

============================================================
DO NOT
============================================================

- Do NOT use raw SQL with `sqlu` interpolator in application code — always use Slick's functional query combinators.
- Do NOT create migrations without updating the corresponding Slick table definition and model case class in the same commit.
- Do NOT modify existing migration files — always create new migrations for changes.
- Do NOT skip the compile verification step — type errors from mismatched models must be caught before committing.
- Do NOT add columns without considering nullability and defaults — every new column must have a safe migration path for existing rows.
