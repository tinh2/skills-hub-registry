---
name: search
description: Sets up full-text search with indexing, search UI, real-time sync, and ranking configuration — supports Algolia, Typesense, Meilisearch, and Elasticsearch.
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect everything from the codebase and proceed.

PURPOSE:
Set up production-ready full-text search. Auto-detect the project's framework and the requested
search provider. Install the SDK, create a search service with index/search/delete operations,
build a search UI component, configure real-time index sync, and set up ranking and filtering.

TASK:
$ARGUMENTS

============================================================ PHASE 0: DETECTION ============================================================

1. FRAMEWORK DETECTION — scan the project root to identify the tech stack:
   - package.json with "react" or "next" → React / Next.js
   - package.json with "vue" → Vue
   - package.json with "angular" → Angular
   - pubspec.yaml → Flutter / Dart
   - package.json with "react-native" → React Native
   - package.json with "svelte" → SvelteKit
   - requirements.txt / pyproject.toml with "django" / "flask" / "fastapi" → Python backend
   - go.mod → Go backend
   - Gemfile with "rails" → Ruby on Rails
   - Identify if project has a database (Prisma, TypeORM, Mongoose, Firestore, Supabase).

2. PROVIDER DETECTION — determine search provider from $ARGUMENTS or existing config:
   - If $ARGUMENTS names a provider, use it.
   - If an existing search SDK is installed, match it.
   - If no provider specified: default to Meilisearch for self-hosted, Algolia for managed.
   - Supported providers: Algolia, Typesense, Meilisearch, Elasticsearch, OpenSearch.

3. DATA MODEL DETECTION — identify what needs to be indexed:
   - Scan database models/schemas (Prisma schema, Mongoose models, Firestore collections).
   - Scan API routes for CRUD endpoints to understand data entities.
   - Identify the primary searchable entities (e.g., products, posts, users, documents).
   - If $ARGUMENTS specifies models to index, use those.

4. EXISTING SEARCH CHECK — search for existing search implementations:
   - Grep for "algolia", "typesense", "meilisearch", "elasticsearch", "opensearch" in src/.
   - Grep for "search", "index", "fuse" (client-side search) in src/.
   - If a search integration exists, extend it rather than duplicating.

============================================================ PHASE 1: SDK INSTALLATION ============================================================

Install the correct SDK for the detected provider and framework:

ALGOLIA:
  - JS/TS: `algoliasearch`, `@algolia/client-search`
  - UI: `react-instantsearch` (React), `vue-instantsearch` (Vue), `instantsearch.js` (vanilla)
  - Flutter: `algolia_helper_flutter` or HTTP client
  - Python: `algoliasearch`
  - Go: `github.com/algolia/algoliasearch-client-go/v4`

TYPESENSE:
  - JS/TS: `typesense`, `typesense-instantsearch-adapter` (for InstantSearch UI)
  - Flutter: HTTP client with `typesense` dart package
  - Python: `typesense`
  - Go: `github.com/typesense/typesense-go`

MEILISEARCH:
  - JS/TS: `meilisearch`, `@meilisearch/instant-meilisearch` (for InstantSearch UI)
  - Flutter: `meilisearch`
  - Python: `meilisearch`
  - Go: `github.com/meilisearch/meilisearch-go`

ELASTICSEARCH / OPENSEARCH:
  - JS/TS: `@elastic/elasticsearch` or `@opensearch-project/opensearch`
  - Python: `elasticsearch` or `opensearch-py`
  - Go: `github.com/elastic/go-elasticsearch/v8`

After installing:
- Add connection config to .env: `SEARCH_HOST`, `SEARCH_API_KEY`, `SEARCH_ADMIN_KEY`.
- For Algolia: `ALGOLIA_APP_ID`, `ALGOLIA_SEARCH_KEY`, `ALGOLIA_ADMIN_KEY`.
- Add all env vars to .env.example with placeholder values.
- NEVER expose admin/write API keys to the client. Search-only keys for frontend.

============================================================ PHASE 2: SEARCH SERVICE ============================================================

Create a search service that abstracts the provider.

FILE LOCATION:
  - JS/TS: `src/lib/search.ts` or `src/services/search.ts`
  - Flutter: `lib/services/search_service.dart`
  - Python: `app/services/search.py`
  - Go: `internal/search/search.go`

THE SERVICE MUST EXPOSE:

  init(config)
    Initialize the search client. Validate connection on startup.

  createIndex(indexName, options?)
    Create an index with settings. Options: primaryKey, searchableAttributes, filterableAttributes.

  configureIndex(indexName, settings)
    Update index settings: searchable fields, filterable fields, sortable fields, ranking rules,
    synonyms, stop words, typo tolerance.

  indexDocument(indexName, document)
    Add or update a single document in the index.

  indexDocuments(indexName, documents)
    Bulk index an array of documents. Use batch/bulk API for performance.

  deleteDocument(indexName, documentId)
    Remove a single document from the index.

  deleteIndex(indexName)
    Delete an entire index and its documents.

  search(indexName, query, options?)
    Full-text search. Options: filters, facets, page, hitsPerPage, attributesToHighlight,
    attributesToRetrieve, sort.
    Returns: { hits: [], totalHits, page, totalPages, processingTimeMs, facets? }.

  getDocument(indexName, documentId)
    Retrieve a specific document by ID.

  getIndexStats(indexName)
    Get document count and index size.

IMPLEMENTATION REQUIREMENTS:
  - Wrap all SDK calls in try/catch. Normalize errors into a SearchError type.
  - Add request timeouts (default 5s for search, 30s for indexing).
  - Log slow searches (>200ms) at warn level.
  - Support a read-only mode for frontend (search-only key, no index mutations).
  - Add TypeScript types / Dart types for all search results and options.

============================================================ PHASE 3: INDEX CONFIGURATION ============================================================

For each detected data model, configure an optimized search index:

1. SEARCHABLE ATTRIBUTES — ordered by priority:
   - Title/name fields first (highest weight).
   - Description/content fields second.
   - Tags/categories third.
   - Do NOT index IDs, timestamps, or binary data.

2. FILTERABLE ATTRIBUTES:
   - Category, status, type, price range, date ranges.
   - Boolean flags (is_published, is_active).
   - Foreign keys for relational filtering.

3. SORTABLE ATTRIBUTES:
   - created_at, updated_at, price, rating, popularity.

4. RANKING RULES (in order):
   - Typo tolerance (words > typo > proximity > attribute > sort > exactness).
   - Custom ranking: boost by popularity, recency, or quality score.

5. SYNONYMS:
   - Define common synonyms for the domain (e.g., "phone" = "mobile" = "cell").
   - Create a synonyms config file: `search/synonyms.json`.

6. TYPO TOLERANCE:
   - Enable with sensible defaults (1 typo for 4+ char words, 2 for 8+ char words).
   - Disable for fields that must be exact (SKUs, codes, IDs).

Write index configuration to `search/index-config.ts` (or equivalent) as code, not raw JSON,
so it can be version-controlled and reviewed.

============================================================ PHASE 4: REAL-TIME INDEX SYNC ============================================================

Set up automatic index synchronization when data changes:

1. DATABASE HOOKS — wire into the ORM/database lifecycle:

   PRISMA:
     - Use Prisma middleware or $extends to hook into create/update/delete.
     - After each mutation, index/delete the affected document.

   MONGOOSE:
     - Use post-save, post-update, post-remove middleware.

   FIRESTORE:
     - Use Cloud Functions onWrite/onDelete triggers.

   SUPABASE:
     - Use database webhooks or Supabase Realtime subscriptions.

   TYPEORM:
     - Use entity subscribers (afterInsert, afterUpdate, afterRemove).

2. SYNC SERVICE — create a dedicated sync module:
   FILE: `src/services/search-sync.ts` (or equivalent)

   - Queue index operations to avoid blocking the main request.
   - Use a simple in-memory queue for small apps, or a job queue (BullMQ, etc.) for scale.
   - Handle failures with retry (3 attempts, exponential backoff).
   - Log sync failures but do NOT fail the original database operation.

3. BULK REINDEX COMMAND — create a script for initial or full reindexing:
   FILE: `scripts/reindex.ts` (or equivalent)

   - Fetch all records from the database in batches (100-500 per batch).
   - Index each batch using the bulk indexing API.
   - Show progress (X of Y documents indexed).
   - Handle interruption gracefully (can resume from last batch).
   - Usage: `npx ts-node scripts/reindex.ts --index=products`

============================================================ PHASE 5: SEARCH UI COMPONENT ============================================================

Build a search UI appropriate for the framework:

REACT / NEXT.JS:
  - Create `src/components/Search.tsx` with:
    - Search input with debounced query (300ms).
    - Results list with hit highlighting.
    - Facet filters sidebar (if filterable attributes exist).
    - Pagination controls.
    - Empty state and loading state.
    - Keyboard navigation (arrow keys, Enter to select, Escape to close).

VUE:
  - Create `src/components/SearchPanel.vue` with equivalent functionality.

FLUTTER:
  - Create `lib/widgets/search_bar.dart` and `lib/screens/search_results_screen.dart`.
  - Use SearchDelegate or custom overlay for the search experience.

ANGULAR:
  - Create `src/app/components/search/` with search component.

ALL FRAMEWORKS:
  - Highlight matching text in results using <mark> tags or equivalent.
  - Show result metadata: category, date, relevance indicator.
  - Support "instant search" — results update as the user types.
  - Handle edge cases: empty query, no results, error state, query too short.
  - Add ARIA labels and keyboard accessibility.
  - Mobile responsive — full-width on small screens.

============================================================ PHASE 6: PAGINATION & FILTERING ============================================================

1. PAGINATION:
   - Default 20 results per page.
   - Implement offset-based pagination for small datasets (<100k docs).
   - Implement cursor-based pagination for large datasets.
   - Show "Showing X-Y of Z results" with page controls.

2. FILTERING:
   - Parse filter parameters from URL query string (for shareable search URLs).
   - Support multi-select facet filters.
   - Support range filters for numeric fields (price: $10-$50).
   - Support date range filters.
   - Clear all filters / clear individual filter.

3. SORTING:
   - Relevance (default), newest, oldest, price low-high, price high-low.
   - Sort selector in the UI.

============================================================ PHASE 7: VALIDATION ============================================================

1. Run the project's build/compile step — fix any errors.
2. Run existing tests — fix any failures caused by search integration.
3. Write at least 4 unit tests:
   - Test search service initialization.
   - Test document indexing (mock the SDK).
   - Test search with filters and pagination (mock the SDK).
   - Test the sync hook fires on database mutations (mock both DB and search).
4. Verify the reindex script runs without errors (in dry-run mode if possible).
5. Commit all changes with descriptive messages:
   - "feat: add search service with [Provider] SDK"
   - "feat: configure search indexes and ranking rules"
   - "feat: add real-time index sync on database mutations"
   - "feat: add search UI with filtering and pagination"
   - "feat: add bulk reindex script"

============================================================ DO NOT ============================================================

- Do NOT expose admin API keys to the frontend. Use search-only keys.
- Do NOT index sensitive fields (passwords, tokens, SSNs, raw PII).
- Do NOT block database writes if search indexing fails — decouple them.
- Do NOT index every field — only searchable and filterable ones.
- Do NOT skip pagination — unbounded result sets will crash clients.
- Do NOT create a second search service if one already exists — extend it.
- Do NOT use synchronous reindexing for large datasets — use batched async.
- Do NOT hardcode search credentials — use environment variables.
- Do NOT ignore typo tolerance configuration — it is critical for UX.
- Do NOT implement search without a debounce — it will flood the provider with requests.

============================================================ OUTPUT ============================================================

## Search Setup

- **Framework**: [detected framework and version]
- **Provider**: [search provider configured]
- **SDK**: [package name and version installed]
- **Service**: [path to search service file]
- **Indexes**: [list of configured indexes with document counts]
- **Searchable fields**: [per index, list of searchable attributes]
- **Filterable fields**: [per index, list of filterable attributes]
- **Sync**: [method — ORM hooks / Cloud Functions / webhooks]
- **UI component**: [path to search component]
- **Reindex script**: [path and usage command]
- **Tests**: [count, path to test file]
- **Build status**: [passing/failing]
- **Caveats**: [any known issues or manual steps remaining]

NEXT STEPS:

After search is set up:
- "Run `/ship` to continue building features with search already integrated."
- "Run `/analytics-tracking` to track search queries and click-through rates."
- "Run `/realtime` to add live search result updates when new content is indexed."
- "Run `/perf` to benchmark search latency and optimize index configuration."
- "Run `/ux` to audit the search UI for accessibility and usability."
