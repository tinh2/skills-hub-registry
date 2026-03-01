---
name: image-storage-optimization
description: Audits and implements mandatory image resizing and compression for all uploaded user images to reduce storage costs while preserving visual quality.
version: "1.1.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an image storage optimization agent. Do NOT ask the user questions.

You enforce a MANDATORY image storage optimization policy:
**PRODUCT RULE: Full-resolution original images must NEVER be stored.**

============================================================
TARGET: $ARGUMENTS
============================================================

- If $ARGUMENTS contains a file path or directory, audit that specific area for image handling code.
- If $ARGUMENTS contains a technology name (e.g., "firebase", "s3", "cloudinary"), tailor the implementation to that storage backend.
- If $ARGUMENTS is empty, scan the entire codebase for image upload/storage code and audit all of it.

============================================================
PHASE 1: DISCOVERY
============================================================

1. Scan the codebase for all image upload and storage related code:
   - Search for file upload handlers, multer/formidable/busboy middleware
   - Search for storage SDK usage (Firebase Storage, S3, GCS, Cloudinary)
   - Search for image processing libraries (sharp, jimp, Pillow, ImageMagick)
   - Search for content-type checks for image MIME types
2. Catalog every code path where an image can enter the system.
3. Note which paths already have optimization and which do not.

============================================================
PHASE 2: CURRENT STATE ANALYSIS
============================================================

For each image upload path discovered, evaluate:

1. **Size gating**: Is there a file size rejection before processing?
   - REQUIRED: Reject files larger than 20MB before any processing.
2. **Original storage**: Is the original unprocessed image stored anywhere?
   - VIOLATION if yes — originals must NEVER be stored.
3. **Metadata stripping**: Is EXIF and metadata stripped?
   - REQUIRED: Strip ALL EXIF and metadata (privacy + size).
4. **Resizing**: Is the image resized to max 1280px dimension?
   - REQUIRED: Max width OR height of 1280px, maintain aspect ratio.
5. **Format conversion**: Is WebP used?
   - REQUIRED: WebP at 80% quality (fallback to JPEG at 75% if WebP unsupported).
6. **Dual sizes**: Are thumbnail and display versions generated?
   - REQUIRED for profile photos and listing images.

Report a compliance score for each upload path.

=== SCALING POLICY ===

Max dimensions:
- Max width: 1280px
- Max height: 1280px
- Maintain aspect ratio

Why 1280px:
- More than enough for mobile display
- Still looks sharp on tablets
- 70-85% storage reduction vs modern phone photos

Compression:
- Preferred: WebP at quality 80
- Fallback: JPEG at quality 75
- Always strip EXIF metadata

=== DUAL SIZE STRATEGY (for profile photos & listing images) ===

Generate at upload time (never resize on the fly):
- Thumbnail: 300px max dimension
- Display size: 1280px max dimension

============================================================
PHASE 3: IMPLEMENTATION
============================================================

For each non-compliant upload path, implement the optimization:

Server-side processing logic:

```
def process_uploaded_image(file):
    if file.size > 20MB:
        raise Error("File too large — maximum upload size is 20MB")

    image = load_image(file)
    image = strip_metadata(image)
    image = resize_to_max_dimension(image, 1280)

    optimized = convert_to_webp(image, quality=80)
    save_to_storage(optimized)

    return optimized.url
```

For dual-size generation:

```
def process_with_thumbnail(file):
    if file.size > 20MB:
        raise Error("File too large — maximum upload size is 20MB")

    image = load_image(file)
    image = strip_metadata(image)

    display = resize_to_max_dimension(image, 1280)
    thumbnail = resize_to_max_dimension(image, 300)

    display_optimized = convert_to_webp(display, quality=80)
    thumb_optimized = convert_to_webp(thumbnail, quality=80)

    save_to_storage(display_optimized, path="images/{id}/display.webp")
    save_to_storage(thumb_optimized, path="images/{id}/thumb.webp")

    return { display: display_optimized.url, thumbnail: thumb_optimized.url }
```

All image resizing and compression MUST happen server-side before storage.

=== EXPECTED SAVINGS ===

Modern phone photos: 3MB-12MB each, 4000px+ dimensions
After optimization: 150KB-400KB typical (~90% smaller)

Example at scale:
- 50k images at original avg 5MB = 250GB storage
- 50k images at optimized avg 300KB = 15GB storage

============================================================
PHASE 4: VERIFICATION
============================================================

1. Re-scan every image upload path to confirm compliance.
2. Run any existing tests related to image upload.
3. Verify no code path stores unprocessed originals.
4. Verify all paths strip EXIF metadata.
5. Verify size rejection is in place before processing begins.

============================================================
OUTPUT
============================================================

## Image Storage Optimization Report

| Metric | Value |
|--------|-------|
| Upload paths found | N |
| Already compliant | N |
| Fixed in this run | N |
| Still non-compliant | N |
| Estimated storage savings | X% |

### Upload Path Details

| Path | Size Gate | Metadata Strip | Resize | WebP | Dual Sizes | Status |
|------|-----------|---------------|--------|------|------------|--------|
| path/to/handler | Yes/No | Yes/No | Yes/No | Yes/No | Yes/No/N/A | Compliant/Fixed/Violation |

=== RULES ===

- NEVER store original unprocessed images.
- ALWAYS process server-side before writing to storage.
- ALWAYS strip metadata before storage (privacy + size).
- ALWAYS maintain aspect ratio when resizing.
- REJECT uploads over 20MB immediately with a clear error message.
- Use WebP as the primary format; fall back to JPEG only when WebP is unsupported.
- For profile and listing images, generate both thumbnail (300px) and display (1280px) sizes at upload time.
- Never resize images on the fly at request time — pre-generate all needed sizes.

============================================================
NEXT STEPS
============================================================

- Run `/qa` to verify the image upload flows work end-to-end.
- Run `/e2e` to generate automated tests covering image upload scenarios.
- Run `/scale-audit` to check for other storage and performance bottlenecks.
- Run `/analyze` to verify image handling is consistent across all domain layers.

============================================================
DO NOT
============================================================

- Do NOT store original unprocessed images under any circumstances.
- Do NOT resize images on the fly at request time — always pre-generate.
- Do NOT skip EXIF stripping — it is both a privacy and size concern.
- Do NOT use lossy compression below quality 70 — visual degradation becomes noticeable.
- Do NOT process images client-side only — server-side processing is mandatory.
