---
name: image_storage_optimization
description: Reduce storage costs by automatically resizing and compressing all uploaded user images while preserving acceptable visual quality.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are enforcing a MANDATORY image storage optimization policy.

PRODUCT RULE: Full-resolution original images must NEVER be stored.

Whenever a user uploads or sends any photo, the system must:

1. REJECT files larger than 20MB before any processing.
2. Do NOT store the original file under any circumstances.
3. Strip ALL EXIF and metadata from the image.
4. Resize the image so that the maximum width or height is 1280px (maintain aspect ratio).
5. Convert to WebP format at 80% quality (fallback to JPEG at 75% quality if WebP is not supported).
6. Optimize for mobile viewing.
7. Store ONLY the optimized image version.

All image resizing and compression MUST happen server-side before storage.

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

=== IMPLEMENTATION PATTERN ===

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

=== EXPECTED SAVINGS ===

Modern phone photos: 3MB-12MB each, 4000px+ dimensions
After optimization: 150KB-400KB typical (~90% smaller)

Example at scale:
- 50k images at original avg 5MB = 250GB storage
- 50k images at optimized avg 300KB = 15GB storage

=== RULES ===

- NEVER store original unprocessed images.
- ALWAYS process server-side before writing to storage.
- ALWAYS strip metadata before storage (privacy + size).
- ALWAYS maintain aspect ratio when resizing.
- REJECT uploads over 20MB immediately with a clear error message.
- Use WebP as the primary format; fall back to JPEG only when WebP is unsupported.
- For profile and listing images, generate both thumbnail (300px) and display (1280px) sizes at upload time.
- Never resize images on the fly at request time — pre-generate all needed sizes.
