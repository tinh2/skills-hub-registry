---
name: storage
description: "Add file uploads and object storage to my app — set up AWS S3, Google Cloud Storage, Cloudflare R2, or Supabase Storage with presigned URLs, direct browser uploads, multipart chunked uploads, file type validation, lifecycle policies, CORS configuration, and CDN integration"
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect everything from the codebase and proceed.

PURPOSE:
Set up production-ready object storage. Auto-detect the project's framework and the requested
storage provider. Install the SDK, create a storage service with full CRUD operations, configure
presigned URLs for secure direct uploads, set up lifecycle policies, CORS, CDN integration, and
handle multipart uploads for large files.

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
   - Detect if project has both frontend and backend (monorepo / separate dirs).

2. PROVIDER DETECTION — determine storage provider from $ARGUMENTS or existing config:
   - If $ARGUMENTS names a provider, use it.
   - If AWS credentials or aws-sdk is already installed → AWS S3.
   - If @google-cloud/storage or firebase-admin is installed → Google Cloud Storage.
   - If supabase-js is installed → Supabase Storage.
   - If no provider specified and none detected, default to AWS S3 (most universal, R2-compatible).
   - Supported providers: AWS S3, Google Cloud Storage (GCS), Cloudflare R2, Supabase Storage.

3. EXISTING STORAGE CHECK — search for existing storage wrappers:
   - Grep for "s3", "storage", "upload", "bucket", "putObject", "getSignedUrl" in src/.
   - If a storage service already exists, extend it rather than creating a duplicate.

4. BACKEND REQUIREMENT CHECK:
   - Presigned URLs and lifecycle policies REQUIRE server-side code.
   - If only a frontend exists, note that an API route or serverless function is needed.
   - For Next.js/SvelteKit, use API routes. For SPAs, flag that a backend is required.

============================================================ PHASE 1: SDK INSTALLATION ============================================================

Install the correct SDK for the detected provider and framework:

AWS S3:
  - JS/TS: `@aws-sdk/client-s3`, `@aws-sdk/s3-request-presigner`
  - Flutter: `aws_s3_api` or HTTP with presigned URLs (preferred)
  - Python: `boto3`
  - Go: `github.com/aws/aws-sdk-go-v2/service/s3`

GOOGLE CLOUD STORAGE:
  - JS/TS: `@google-cloud/storage`
  - Flutter: `firebase_storage` (via Firebase) or HTTP with signed URLs
  - Python: `google-cloud-storage`
  - Go: `cloud.google.com/go/storage`

CLOUDFLARE R2:
  - JS/TS: `@aws-sdk/client-s3` (R2 is S3-compatible — use S3 SDK with R2 endpoint)
  - Python: `boto3` with custom endpoint
  - Go: aws-sdk-go-v2 with custom endpoint

SUPABASE STORAGE:
  - JS/TS: `@supabase/supabase-js` (storage is built into the client)
  - Flutter: `supabase_flutter`
  - Python: `supabase`

After installing:
- Add credentials to .env or environment config.
- Required env vars: `STORAGE_BUCKET`, `STORAGE_REGION`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`.
- For R2: add `STORAGE_ENDPOINT` (e.g., `https://<account-id>.r2.cloudflarestorage.com`).
- For Supabase: use existing `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`.
- Add all env vars to .env.example with placeholder values.
- NEVER commit real credentials.

============================================================ PHASE 2: STORAGE SERVICE ============================================================

Create a storage service that abstracts the provider. This lets the team swap providers
(e.g., S3 to R2) without touching application code.

FILE LOCATION:
  - JS/TS: `src/lib/storage.ts` or `src/services/storage.ts`
  - Flutter: `lib/services/storage_service.dart`
  - Python: `app/services/storage.py`
  - Go: `internal/storage/storage.go`

THE SERVICE MUST EXPOSE:

  init(config)
    Initialize the storage client with credentials and bucket name.

  upload(key, file, options?)
    Upload a file to storage. Options: contentType, metadata, acl, onProgress callback.
    Returns: { key, url, size, contentType }.

  download(key)
    Download a file by key. Returns a stream or buffer depending on framework.

  delete(key)
    Delete a single object by key. Idempotent — no error if key does not exist.

  deleteMany(keys)
    Batch delete multiple objects. Use the provider's bulk delete API.

  list(prefix?, options?)
    List objects with optional prefix filter. Options: maxKeys, cursor/continuationToken.
    Returns: { objects: [{ key, size, lastModified }], cursor?, hasMore }.

  getUrl(key)
    Get the public URL for an object (if bucket is public or CDN is configured).

  getSignedUrl(key, options?)
    Generate a presigned URL for private access. Options: expiresIn (seconds, default 3600),
    method ("GET" or "PUT"), contentType (for PUT).

  getUploadUrl(key, contentType, options?)
    Generate a presigned PUT URL for direct browser uploads.
    Returns: { uploadUrl, fields?, key }.

  copy(sourceKey, destinationKey)
    Server-side copy without downloading.

  getMetadata(key)
    Get object metadata (size, contentType, lastModified, custom metadata).

IMPLEMENTATION REQUIREMENTS:
  - Wrap all SDK calls in try/catch. Normalize errors into a consistent StorageError type.
  - Add retry logic with exponential backoff for transient failures (network, 503).
  - Support a configurable max file size (default 50MB, configurable via env).
  - Log upload/download operations at debug level — never log credentials.
  - Add TypeScript types / Dart types for all return values and options.

============================================================ PHASE 3: FILE VALIDATION ============================================================

Create a validation layer that runs before every upload:

FILE: `src/lib/storage-validation.ts` (or framework equivalent)

1. FILE TYPE VALIDATION:
   - Define allowed MIME types per upload context (e.g., avatars: image/*, documents: pdf/docx).
   - Validate by both file extension AND magic bytes (first few bytes of file content).
   - Reject files where extension does not match magic bytes (renamed malware prevention).

2. FILE SIZE VALIDATION:
   - Enforce per-context size limits (e.g., avatars: 5MB, documents: 50MB, videos: 500MB).
   - Return clear error messages: "File too large. Maximum size for avatars is 5MB."
   - Check size BEFORE uploading, not after.

3. FILENAME SANITIZATION:
   - Strip special characters, spaces, and path traversal sequences.
   - Generate storage keys with structure: `{context}/{userId}/{timestamp}-{sanitized-name}`.
   - Prevent key collisions by including a short random suffix or UUID.

4. IMAGE PROCESSING (if applicable):
   - Validate image dimensions if the context requires it.
   - Note where server-side image resizing should happen (do not implement, just mark the hook).

============================================================ PHASE 4: PRESIGNED URLS & DIRECT UPLOAD ============================================================

Implement secure direct-to-storage uploads from the browser/client:

1. SERVER-SIDE ENDPOINT — create an API route:
   - POST `/api/storage/upload-url`
   - Accepts: { filename, contentType, context, fileSize }
   - Validates: file type, size, user authentication.
   - Returns: { uploadUrl, key, fields? (for POST-based uploads) }

2. CLIENT-SIDE UPLOAD HELPER:
   - Request the presigned URL from the server endpoint.
   - Upload directly to storage using fetch/XMLHttpRequest/dio with PUT.
   - Track upload progress via onProgress callback.
   - Handle failures with retry (up to 3 attempts).
   - After upload completes, notify the server to confirm and store the record.

3. MULTIPART UPLOAD (files > 10MB):
   - Server: Create multipart upload, return upload ID and part presigned URLs.
   - Client: Split file into 5MB chunks, upload each part in parallel (max 4 concurrent).
   - Server: Complete multipart upload after all parts are uploaded.
   - Handle abort: if upload is cancelled, call abort multipart to clean up.

============================================================ PHASE 5: CORS CONFIGURATION ============================================================

Generate CORS configuration for the storage bucket:

AWS S3 / R2:
```json
{
  "CORSRules": [{
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
    "AllowedOrigins": ["${APP_URL}"],
    "ExposeHeaders": ["ETag", "Content-Length", "x-amz-request-id"],
    "MaxAgeSeconds": 3600
  }]
}
```

GCS:
```json
[{
  "origin": ["${APP_URL}"],
  "method": ["GET", "PUT", "POST", "DELETE", "HEAD"],
  "responseHeader": ["Content-Type", "Content-Length"],
  "maxAgeSeconds": 3600
}]
```

- Write CORS config to a file: `storage/cors.json`.
- Include setup instructions as comments (aws s3api put-bucket-cors / gsutil cors set).
- For development, allow localhost origins. For production, restrict to the app domain.

============================================================ PHASE 6: LIFECYCLE POLICIES ============================================================

Create lifecycle rules to manage storage costs:

1. TEMP FILES — auto-delete after 24 hours:
   - Prefix: `tmp/` or `uploads/pending/`
   - Action: Delete after 1 day.

2. OLD VERSIONS — archive or delete after 90 days:
   - Enable versioning on the bucket.
   - Move non-current versions to cheaper storage tier after 30 days.
   - Delete non-current versions after 90 days.

3. INCOMPLETE MULTIPART — auto-abort after 7 days:
   - Abort incomplete multipart uploads older than 7 days.
   - Prevents orphaned parts from consuming storage.

4. LOG ARCHIVAL (if applicable):
   - Move access logs to Glacier/Archive tier after 30 days.

Write lifecycle config to `storage/lifecycle.json` with provider-specific format.
Include CLI commands to apply the policies as comments in the file.

============================================================ PHASE 7: CDN INTEGRATION ============================================================

Set up CDN for serving stored files:

1. CDN URL HELPER:
   - Add a `getCdnUrl(key)` method to the storage service.
   - Transform storage URLs to CDN URLs: `https://cdn.example.com/{key}`.
   - Configure the CDN domain via `STORAGE_CDN_URL` env var.

2. CACHE HEADERS:
   - Set `Cache-Control: public, max-age=31536000, immutable` for content-addressed files.
   - Set `Cache-Control: public, max-age=3600` for user-uploaded content.
   - Set `Cache-Control: no-cache` for frequently changing content.

3. CONFIGURATION FILE:
   - Write CDN setup notes to `storage/cdn-setup.md` covering:
     - CloudFront distribution setup (for S3/R2).
     - Cloud CDN setup (for GCS).
     - Supabase built-in CDN (for Supabase Storage).
   - Include cache invalidation commands.

============================================================ PHASE 8: VALIDATION ============================================================

1. Run the project's build/compile step — fix any errors.
2. Run existing tests — fix any failures caused by storage integration.
3. Verify the storage service can be imported and instantiated without errors.
4. Write at least 3 unit tests for the storage service:
   - Test file validation (type, size, name sanitization).
   - Test signed URL generation (mock the SDK).
   - Test upload/download flow (mock the SDK).
5. Commit all changes with descriptive messages:
   - "feat: add storage service with [Provider] SDK"
   - "feat: add file validation and sanitization"
   - "feat: add presigned URL generation and direct upload"
   - "feat: add lifecycle policies and CDN configuration"

============================================================ DO NOT ============================================================

- Do NOT commit real credentials, access keys, or secret keys.
- Do NOT make bucket publicly writable. All writes must go through presigned URLs or server-side.
- Do NOT allow path traversal in storage keys (../../etc/passwd).
- Do NOT trust client-provided content types without server-side validation.
- Do NOT skip multipart abort cleanup — orphaned parts are invisible storage costs.
- Do NOT hardcode bucket names — use environment variables.
- Do NOT create a second storage wrapper if one already exists — extend it.
- Do NOT set CORS AllowedOrigins to "*" in production.
- Do NOT store sensitive data (PII, credentials) in object storage without encryption.
- Do NOT generate presigned URLs with expiresIn longer than 7 days (S3 max for IAM users).

============================================================ OUTPUT ============================================================

## Storage Setup

- **Framework**: [detected framework and version]
- **Provider**: [storage provider configured]
- **SDK**: [package name and version installed]
- **Service**: [path to storage service file]
- **Validation**: [path to validation file, rules configured]
- **Methods**: [list of implemented methods]
- **Presigned URLs**: [endpoint path, expiry defaults]
- **Multipart**: [threshold, chunk size, max concurrent]
- **CORS**: [path to config, origins allowed]
- **Lifecycle**: [policies configured, path to config]
- **CDN**: [configured yes/no, CDN URL env var]
- **Tests**: [count, path to test file]
- **Build status**: [passing/failing]
- **Caveats**: [any known issues or manual steps remaining]

NEXT STEPS:

After storage is set up:
- "Run `/ship` to build features that use file uploads."
- "Run `/analytics-tracking` to track upload events and storage usage metrics."
- "Run `/search` to index stored documents for full-text search."
- "Run `/perf` to benchmark upload speeds and optimize chunk sizes."
- "Run `/check-vanta` to verify storage security meets compliance requirements."
