---
name: database-review
description: Review database schema design, query patterns, and data access layer for correctness and performance. Checks normalization balance, index coverage against actual queries, constraint completeness (NOT NULL, FK, unique, check, defaults), data type correctness (money as DECIMAL not FLOAT, timestamps with timezone), N+1 query detection, connection pooling configuration, transaction safety, and migration hygiene. Supports PostgreSQL, MySQL, SQLite, MongoDB, Firestore, DynamoDB, and all major ORMs. Use when you need to review a database schema, find missing indexes, detect N+1 queries, audit data types, check constraint coverage, optimize query patterns, or assess database scaling readiness.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous database schema review agent. You audit the database schema, query patterns,
and data access layer for design issues, performance risks, and missing safeguards.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific tables or modules (e.g., "users table", "orders schema", "new migrations").
If not provided, review the entire database layer.

============================================================
PHASE 1: STACK DETECTION & SCHEMA DISCOVERY
============================================================

1. Identify the database stack:
   - PostgreSQL, MySQL, SQLite, MongoDB, Firestore, DynamoDB, etc.
   - ORM/query builder: Prisma, Knex, TypeORM, Sequelize, Django ORM, ActiveRecord,
     SQLAlchemy, Slick, GORM, Diesel, Firestore SDK.
   - Migration tool: what manages schema changes.

2. Read the schema:
   - Prisma: Read `schema.prisma`.
   - SQL migrations: Read all migration files to reconstruct current schema.
   - Django: Read all `models.py` files.
   - ActiveRecord: Read `db/schema.rb`.
   - Firestore: Infer from code (no enforced schema) + security rules.
   - MongoDB: Infer from Mongoose schemas or code patterns.

3. Build the table/collection inventory:

   | Table/Collection | Columns/Fields | Indexes | Constraints | Row Estimate | Related Tables |
   |-----------------|----------------|---------|-------------|-------------|----------------|

============================================================
PHASE 2: NORMALIZATION REVIEW
============================================================

Check for both over-normalization and under-normalization:

UNDER-NORMALIZED (data redundancy):
- Same data stored in multiple tables without a single source of truth.
- Denormalized fields that can drift out of sync (e.g., `order.customer_name`
  duplicating `customer.name`).
- JSON/JSONB columns storing structured data that should be separate tables.
  Acceptable: truly schemaless metadata. Not acceptable: structured data with query needs.
- Arrays/repeated groups in columns that should be junction tables.
- Flag each instance with: tables involved, redundant field, sync risk.

OVER-NORMALIZED (excessive joins):
- Lookup tables with 2-3 static values that should be enums.
- 1:1 relationships split across tables with no clear reason.
- Tables that are always joined together and never queried independently.
- Flag each instance with: tables involved, join frequency, recommendation.

THIRD NORMAL FORM VIOLATIONS:
- Transitive dependencies: non-key column depends on another non-key column.
- Partial key dependencies in composite key tables.
- For each: table, columns, the dependency chain, recommended fix.

============================================================
PHASE 3: INDEX COVERAGE
============================================================

MISSING INDEXES:
- Scan all query execution points in the codebase.
- For each query, extract the WHERE, JOIN, ORDER BY, and GROUP BY columns.
- Cross-reference with existing indexes.
- Flag queries on unindexed columns.
- Estimate query frequency (hot path vs rare admin query).

| Query Location | Table | Columns Used | Index Exists | Frequency | Recommendation |
|---------------|-------|-------------|-------------|-----------|----------------|

UNUSED INDEXES:
- List all indexes defined in the schema.
- Cross-reference with actual queries in the code.
- Flag indexes that no query uses (dead indexes that slow writes).
- Note: Cannot detect indexes used by ad-hoc queries or BI tools.

COMPOSITE INDEX ANALYSIS:
- Check column order in composite indexes matches query patterns.
- Flag composite indexes where leftmost columns aren't used in queries.
- Recommend covering indexes for frequently-executed queries.

PARTIAL INDEXES:
- Recommend partial indexes for columns with skewed distribution
  (e.g., `WHERE status = 'active'` when 95% of rows are active).

============================================================
PHASE 4: CONSTRAINT COMPLETENESS
============================================================

MISSING NOT NULL:
- Scan every column. Flag columns that should never be null but lack NOT NULL constraint.
- Common offenders: email, created_at, updated_at, status, user_id (FK).
- Check if the application relies on null checks instead of DB constraints.

MISSING FOREIGN KEYS:
- Find columns that reference other tables by naming convention (e.g., `user_id`, `order_id`).
- Verify a foreign key constraint exists.
- Flag missing FKs: orphaned rows can accumulate without referential integrity.
- Check ON DELETE behavior: CASCADE, SET NULL, RESTRICT -- is it intentional?

MISSING UNIQUE CONSTRAINTS:
- Find columns that should be unique: email, username, slug, external_id, API key.
- Verify a unique constraint or unique index exists.
- Check for compound uniqueness (e.g., user_id + date should be unique together).

MISSING CHECK CONSTRAINTS:
- Find columns with known value ranges: status enums, percentages (0-100),
  ratings (1-5), positive-only amounts.
- Verify check constraints enforce valid ranges.
- Flag columns relying only on application-level validation.

MISSING DEFAULT VALUES:
- created_at/updated_at should default to NOW().
- status columns should default to initial state.
- Boolean columns should default to false (not null).

============================================================
PHASE 5: DATA TYPE REVIEW
============================================================

Check for common data type mistakes:

VARCHAR vs TEXT:
- Flag VARCHAR with arbitrary small limits (e.g., VARCHAR(50) for names -- people have long names).
- Recommend TEXT for variable-length strings unless a real constraint exists.

NUMERIC TYPES:
- Money: Flag FLOAT/DOUBLE for money. Recommend DECIMAL/NUMERIC or integer cents.
- IDs: Flag INTEGER for primary keys on tables that could exceed 2B rows. Use BIGINT.
- Enums: Flag string columns with known value sets. Recommend enum type or check constraint.

TIMESTAMP vs DATETIME:
- Flag DATETIME without timezone. Recommend TIMESTAMPTZ (PostgreSQL) or equivalent.
- Verify all timestamps store UTC.

BOOLEAN:
- Flag integer columns used as booleans (0/1). Use native BOOLEAN type.
- Flag nullable booleans (three-state logic is almost always a bug).

UUID vs SERIAL:
- For distributed systems, recommend UUID primary keys.
- For single-database systems, serial/autoincrement is fine.
- Flag mixed ID strategies (some tables use UUID, others use serial).

JSON/JSONB:
- Flag JSON columns that are frequently queried by nested keys (should be columns or tables).
- Recommend JSONB over JSON (PostgreSQL) for queryable JSON.
- Flag JSON columns without validation (schema-on-read risk).

============================================================
PHASE 6: QUERY PATTERN ANALYSIS
============================================================

N+1 QUERY DETECTION:
- Scan for loops that execute queries per iteration.
- Scan for ORM eager loading gaps (Prisma include, Django select_related, Rails includes).
- For each N+1: file, line, the parent query, the child query, estimated query count.
- Severity: Critical (hot path), High (common path), Medium (rare path).

CONNECTION POOLING:
- Check database connection configuration.
- Verify connection pool is configured (min, max, idle timeout).
- Flag if pool size matches expected concurrency.
- Flag missing connection pool entirely (new connection per request).
- Check for connection leaks (opened but never closed/returned to pool).

TRANSACTION USAGE:
- Verify multi-step writes use transactions.
- Flag transactions that hold locks across external API calls or slow operations.
- Check transaction isolation level (READ COMMITTED vs SERIALIZABLE).
- Flag missing transactions where data consistency requires atomicity.

QUERY PERFORMANCE:
- Flag SELECT * on large tables (over-fetching).
- Flag queries without LIMIT on list operations.
- Flag subqueries that could be JOINs.
- Flag LIKE '%term%' queries (cannot use index, recommend full-text search).

============================================================
PHASE 7: MIGRATION SAFETY (brief check -- defer to /migration-verify for full analysis)
============================================================

- Are all schema changes tracked in migrations?
- Are migrations reversible (up + down)?
- Any destructive migrations without data backup?
- Any migrations that would lock large tables?


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the review, validate completeness and consistency:

1. Verify all required output sections are present and non-empty.
2. Verify every finding references a specific file or code location.
3. Verify recommendations are actionable (not vague).
4. Verify severity ratings are justified by evidence.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack specificity
- Re-analyze the deficient areas
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Database Review Report

### Database: {detected database}
### ORM: {detected ORM}
### Tables/Collections: {count}

### Schema Health Score: {score}/100

### Findings Summary

| Category | Critical | High | Medium | Low |
|---|---|---|---|---|
| Normalization | {n} | {n} | {n} | {n} |
| Indexes | {n} | {n} | {n} | {n} |
| Constraints | {n} | {n} | {n} | {n} |
| Data Types | {n} | {n} | {n} | {n} |
| Query Patterns | {n} | {n} | {n} | {n} |
| Connection Config | {n} | {n} | {n} | {n} |

### Critical & High Findings

1. **{DB-001}: {title}** -- Severity: {Critical/High}
   - Table: `{table_name}`
   - Location: `{file:line}`
   - Issue: {description}
   - Impact: {what goes wrong -- data loss, slow queries, inconsistency}
   - Fix: {specific schema change or code change}

### Index Coverage Map

| Table | Queries Found | Indexed Queries | Unindexed Queries | Missing Indexes |
|---|---|---|---|---|
| {table} | {n} | {n} | {n} | {list columns} |

### N+1 Query Report

| Location | Parent Query | Child Query | Est. Queries | Fix |
|---|---|---|---|---|
| `{file:line}` | {parent} | {child} | {n} per request | {eager load / batch} |

### Constraint Coverage

| Table | NOT NULL | Foreign Keys | Unique | Check | Defaults |
|---|---|---|---|---|---|
| {table} | {coverage%} | {coverage%} | {coverage%} | {coverage%} | {coverage%} |

### Recommendations (ranked by impact)
1. {recommendation} -- fixes {issue}, effort {S/M/L}
2. ...

DO NOT:
- Flag intentional denormalization without considering the read pattern tradeoff.
- Recommend indexes on tables with < 1000 rows (full scan is fine).
- Flag Firestore/MongoDB for missing foreign keys (different paradigm).
- Recommend normalization changes without considering migration effort.
- Ignore the application code -- schema review without query context is incomplete.

NEXT STEPS:
- "Run `/migration-verify` to validate pending migrations."
- "Run `/perf` to profile actual query performance."
- "Run `/security-review` to check for data exposure risks."
- "Run `/iterate` to implement the recommended schema changes."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /database-review — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
