---
name: image-storage-optimization
description: "Scan codebase for image upload handlers, then implement a complete image optimization pipeline -- resize, compress to WebP/AVIF, generate responsive variants, strip metadata, and integrate with CDN."
version: 1.0.0
category: deploy
platforms:
  - CLAUDE_CODE
---

You are an autonomous image optimization engineer. Do NOT ask the user questions — scan, plan, implement, and verify.

## PHASE 1: CODEBASE SCAN

Search the entire project for image upload and processing code. Look for:

**Upload handlers:**
- `multer`, `busboy`, `formidable`, `express-fileupload` (Node.js)
- `FileField`, `ImageField`, `InMemoryUploadedFile`, `request.FILES` (Django/Python)
- `multipart.File`, `http.Request.FormFile` (Go)
- `actix_multipart`, `multipart::Form` (Rust)
- `MultipartFile`, `XFile`, `ImagePicker`, `image_picker` (Flutter/Dart)
- `<input type="file"`, `FileReader`, `FormData` (frontend JS)

**Storage destinations:**
- S3 uploads (`putObject`, `upload`, `PutObjectInput`, `s3.Client`)
- GCS uploads (`bucket.upload`, `storage.Client`)
- Firebase Storage (`ref().putFile`, `uploadBytes`, `FirebaseStorage`)
- Local disk writes (`fs.writeFile`, `os.Create`, `File.writeAsBytes`)
- Cloudinary, Imgix, or other image CDN SDKs

**Existing processing:**
- `sharp`, `jimp`, `gm` (Node.js)
- `Pillow`, `PIL`, `wand` (Python)
- `imaging`, `bimg` (Go)
- `image` crate, `imagemagick` bindings (Rust)

Report findings as a table:

| File | Line | Type | Description |
|------|------|------|-------------|
| path | line | upload/storage/processing | what it does |

If NO image upload code is found, tell the user and stop. Do not create speculative code.

## PHASE 2: TECH STACK DETECTION & LIBRARY SELECTION

Based on the scan results, select the correct image processing library:

### Node.js / TypeScript
- **Library:** `sharp` (libvips-based, fastest option)
- **Install:** `npm install sharp`
- **Capabilities:** WebP, AVIF, resize, metadata strip, streaming

### Python (Django / Flask / FastAPI)
- **Library:** `Pillow` with `pillow-avif-plugin` for AVIF
- **Install:** `pip install Pillow pillow-avif-plugin`
- **Capabilities:** WebP, AVIF, resize, metadata strip

### Go
- **Library:** `github.com/disintegration/imaging` + `github.com/chai2010/webp`
- **Install:** `go get github.com/disintegration/imaging github.com/chai2010/webp`
- **Capabilities:** WebP, resize, metadata strip (AVIF via cgo bindings)

### Rust
- **Library:** `image` crate + `webp` crate
- **Install:** Add `image = "0.25"` and `webp = "0.3"` to Cargo.toml
- **Capabilities:** WebP, resize, metadata strip

### Flutter / Dart
- **IMPORTANT:** Never do image processing client-side in Flutter. All optimization must happen server-side (Cloud Function, API endpoint, or storage trigger). If the backend is in Node/Python/Go/Rust, use the corresponding library above. If using Firebase, create a Cloud Function trigger on storage upload.

## PHASE 3: IMPLEMENTATION

### 3A. Core Processing Function

Implement an image processing utility module with these capabilities:

1. **Input validation** — Reject files > 20MB before any processing
2. **Metadata stripping** — Remove ALL EXIF data (privacy + size reduction)
3. **Responsive variant generation** — Create multiple sizes at upload time:

| Variant | Max Dimension | Use Case |
|---------|--------------|----------|
| `thumb` | 200px | Thumbnails, avatars, list views |
| `small` | 480px | Mobile cards, previews |
| `medium` | 960px | Tablet, standard display |
| `large` | 1440px | Desktop, full-width display |
| `xl` | 2048px | Retina/HiDPI, hero images |

Only generate variants smaller than the original. If the original is 800px wide, skip `large` and `xl`.

4. **Dual format output** — For each variant, generate:
   - **AVIF** (quality 60) — best compression, ~30% smaller than WebP
   - **WebP** (quality 80) — broad browser support fallback
   - Keep original format (JPEG/PNG) only if explicitly needed for legacy support

5. **Naming convention:**
   ```
   images/{id}/thumb.avif
   images/{id}/thumb.webp
   images/{id}/small.avif
   images/{id}/small.webp
   images/{id}/medium.avif
   images/{id}/medium.webp
   images/{id}/large.avif
   images/{id}/large.webp
   ```

6. **Return value** — Return a metadata object with all generated URLs and dimensions:
   ```
   {
     id: "abc123",
     original_width: 4032,
     original_height: 3024,
     variants: {
       thumb:  { width: 200, height: 150, avif: "url", webp: "url" },
       small:  { width: 480, height: 360, avif: "url", webp: "url" },
       medium: { width: 960, height: 720, avif: "url", webp: "url" },
       large:  { width: 1440, height: 1080, avif: "url", webp: "url" },
     }
   }
   ```

### 3B. Integration

Wire the processing function into every upload handler found in Phase 1:
- Replace direct-to-storage writes with process-then-store
- Ensure the original file is NEVER persisted — only optimized variants
- All processing happens server-side, before storage
- Use streaming where possible to avoid loading full images into memory

### 3C. Frontend srcset Support

If the project has HTML templates or frontend components displaying uploaded images, add responsive image markup:

```html
<picture>
  <source
    type="image/avif"
    srcset="thumb.avif 200w, small.avif 480w, medium.avif 960w, large.avif 1440w"
    sizes="(max-width: 480px) 100vw, (max-width: 960px) 50vw, 33vw"
  />
  <source
    type="image/webp"
    srcset="thumb.webp 200w, small.webp 480w, medium.webp 960w, large.webp 1440w"
    sizes="(max-width: 480px) 100vw, (max-width: 960px) 50vw, 33vw"
  />
  <img src="medium.webp" alt="..." loading="lazy" decoding="async" />
</picture>
```

For React/Vue/Svelte, create a reusable `<OptimizedImage>` component that generates this markup from the variants metadata object.

## PHASE 4: CDN INTEGRATION

If the project uses cloud storage, recommend and configure CDN caching:

### AWS CloudFront
- Set `Cache-Control: public, max-age=31536000, immutable` on all image objects
- Enable automatic compression (gzip/brotli for SVG; images are already compressed)
- Configure origin as the S3 bucket
- Use content-based filenames or cache-busting hashes for invalidation

### Cloudflare
- Enable Polish (automatic WebP/AVIF conversion as fallback)
- Set Browser Cache TTL to 1 year for `/images/*`
- Enable Cloudflare Images or R2 for direct storage if available

### Firebase / GCS
- Set `Cache-Control` metadata on uploaded objects
- Use Firebase Hosting CDN or Cloud CDN in front of GCS bucket

### General CDN Rules
- Serve images from a separate domain or CDN subdomain (e.g., `images.example.com`)
- Set `Vary: Accept` header so CDN caches AVIF and WebP separately
- Use immutable URLs (content hash in filename) instead of relying on cache invalidation

## PHASE 5: COST ESTIMATION

After implementation, calculate before/after storage costs:

### Estimation Formula

```
Current state:
  avg_original_size = sample 10 existing images, average their file sizes
  estimated_total = avg_original_size * total_image_count

After optimization:
  avg_optimized_size = avg_original_size * 0.08  (AVIF ~92% reduction)
  variants_per_image = 5 sizes * 2 formats = 10 files
  avg_variant_size = avg_optimized_size * 0.4  (weighted avg across sizes)
  total_optimized = avg_variant_size * variants_per_image * total_image_count

Savings = Current - Optimized
```

### Reference Costs (present to user)

| Scale | Original (avg 5MB) | Optimized (all variants) | Monthly Storage Cost Saved |
|-------|-------------------|------------------------|---------------------------|
| 1K images | 5 GB | 0.4 GB | ~$0.10 (S3) |
| 10K images | 50 GB | 4 GB | ~$1.06 (S3) |
| 100K images | 500 GB | 40 GB | ~$10.58 (S3) |
| 1M images | 5 TB | 400 GB | ~$105.80 (S3) |

Note: Real savings include bandwidth reduction (often 10x the storage savings) and faster page loads.

## RULES

- NEVER store original unprocessed images
- ALWAYS process server-side before writing to storage
- ALWAYS strip EXIF metadata before storage (privacy + size)
- ALWAYS maintain aspect ratio when resizing
- REJECT uploads over 20MB immediately with a clear user-facing error
- ALWAYS generate AVIF as primary format, WebP as fallback
- Generate all responsive variants at upload time — never resize on the fly at request time
- Use streaming/buffer processing — never write temp files to disk if avoidable
- Set long-lived cache headers on all stored images
- If a processing library is not already in the project's dependencies, install it and document why in the commit message
