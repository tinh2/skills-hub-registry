# New Feature Ideas — Cinematic Video Pipeline

> Auto-generated from 4 markdown files in docs/ + web research on 2026-03-26.
> Focus: Wedding montages, social media clips, tutorial videos, and advertising/marketing content via Claude Code + Remotion.

---

## Source Files Analyzed

| File | Key Insight |
|------|-------------|
| `docs/competitive-gap-analysis.md` | 18 missing features vs competitors; no wedding templates, no beat sync, no social format presets, no Ken Burns, no color grading. Act-based narrative is a unique differentiator opportunity. |
| `docs/NewFeatures-Registry-Expansion.md` | Registry growth strategy — video/media is an underserved category with only 2 skills (video-toolkit, ffmpeg-media) out of 417. |
| `docs/NewFeatures-education-monetization-growth.md` | Non-technical audience demand — wedding video creation is a perfect "wow" demo for teaching Claude Code to non-developers. |
| `build/video-toolkit/SKILL.md` | Existing pipeline covers voiceover, image gen, music gen, talking head, but zero support for photo-based montages, multi-song audio, or cinematic effects. |

---

## Feature Ideas

### HIGH Priority

#### 1. Wedding Montage Skill (`/wedding-video`)
- **Source:** `competitive-gap-analysis.md` — Critical gap: 5/6 competitors have wedding templates; we have zero. User's detailed spec proves the workflow exists.
- **Problem:** Creating a wedding video currently requires writing 500+ lines of custom Remotion code from scratch. No template, no photo pipeline, no act structure.
- **Description:** A new standalone skill that takes a wedding brief (names, date, photos by category, songs with timestamps, text overlays with timing) and generates a complete Remotion project with act-based narrative structure, Ken Burns photo animations, multi-song audio, cinematic effects, and color grading. Renders to MP4 via existing video-toolkit infrastructure.
- **User story:** As a developer preparing for my wedding, I want to describe my wedding video in a structured config and have Claude Code generate a cinematic montage so that I don't need to hire a videographer or learn video editing software.
- **Effort:** L
- **Dependencies:** Ken Burns component (#2), multi-song audio (#4), color grading (#5), cinematic effects (#6)

#### 2. Ken Burns Photo Animation Component
- **Source:** `competitive-gap-analysis.md` — Critical gap: 5/6 competitors have this. Core mechanic for all photo-based videos.
- **Problem:** Still photos in video look lifeless without motion. The current video-toolkit has no photo slideshow capability.
- **Description:** A reusable Remotion component that applies configurable Ken Burns effect (slow pan + zoom) to still images. Supports multiple motion presets: zoom-in, zoom-out, pan-left, pan-right, drift, and random. Parameterized start/end scale and position. Uses `interpolate()` and CSS transforms.
- **User story:** As a video creator, I want to add cinematic motion to still photos so that my montages feel like films instead of slideshows.
- **Effort:** M
- **Dependencies:** None

#### 3. Social Media Video Skill (`/social-clip`)
- **Source:** `competitive-gap-analysis.md` — Critical gap: 5/6 competitors have format presets. User explicitly wants TikTok/Insta/YouTube content.
- **Problem:** Creating vertical (9:16) or square (1:1) video requires manually changing Remotion composition dimensions, repositioning all elements, and re-thinking layout. No quick way to repurpose landscape content for social.
- **Description:** A skill that either creates social-first short-form video from a prompt/brief, or takes an existing Remotion project and auto-adapts it to social formats. Includes format presets (TikTok 9:16 1080x1920 60fps, Reel 9:16 1080x1920 30fps, YouTube Short 9:16, Square 1:1 1080x1080, Story 9:16), auto-reframing of key content, and TikTok-style animated captions via Remotion's `createTikTokStyleCaptions()`.
- **User story:** As a content creator, I want to turn my wedding montage into TikTok and Instagram clips so that I can share highlights on social media without re-editing.
- **Effort:** M
- **Dependencies:** None (standalone, but enhanced by #1)

#### 4. Multi-Song Audio Engine
- **Source:** `competitive-gap-analysis.md` — HIGH gap: user spec requires two songs with hard-cut at 2:12. Current toolkit supports only one background track.
- **Problem:** Emotional videos need multiple songs to match act pacing. A slow ballad for the emotional open, an upbeat track for the adventure montage. Current `audio.backgroundMusicFile` is a single field.
- **Description:** Extends the video-toolkit config schema to support `audio.tracks[]` — an array of audio segments with start/end times, volume levels, fade-in/out durations, and transition types (hard-cut, crossfade, whoosh). Renders as multiple `<Audio>` components with `startFrom`, `endAt`, and `volume` interpolation. Includes a library of audio transition SFX (whoosh, impact, reverse cymbal, vinyl scratch).
- **User story:** As a video creator, I want to use multiple songs with precise transition timing so that each act of my video has its own emotional soundtrack.
- **Effort:** M
- **Dependencies:** None

#### 5. Cinematic Color Grading System
- **Source:** `competitive-gap-analysis.md` — HIGH gap: user spec requires 4 different color palettes across 5 acts. CapCut has full support; 3 others have partial.
- **Problem:** Color grading is essential for emotional storytelling. "Warm nostalgic" for childhood photos, "vibrant" for adventures, "soft cinematic" for proposals, "golden" for the finale. No way to do this in current toolkit without manual CSS per scene.
- **Description:** A color grading preset system with named grades (warm-nostalgic, vibrant-adventure, soft-cinematic, golden-sunset, cool-dramatic, vintage-film, noir, pastel-dream). Each grade maps to CSS filter values (brightness, contrast, saturate, sepia, hue-rotate) plus optional overlay colors. Applied per-act via config. Supports smooth interpolated transitions between grades using `interpolateColors()`.
- **User story:** As a filmmaker, I want to apply different color moods to each act of my video so that the visual tone matches the emotional arc.
- **Effort:** M
- **Dependencies:** None

#### 6. Cinematic Effects Library
- **Source:** `competitive-gap-analysis.md` — MEDIUM gaps across film grain, vignette, letterboxing, particles, split-screen. All present in CapCut; needed for the wedding spec.
- **Problem:** The wedding spec calls for film grain, vignette, letterboxing, confetti/particles, split-screen, depth-of-field blur, parallax, and zoom-rush transitions. None of these exist in the current toolkit.
- **Description:** A library of reusable Remotion effect components: `<FilmGrain>` (CSS noise overlay), `<Vignette>` (radial gradient overlay), `<Letterbox>` (cinematic 2.35:1 bars), `<Particles>` (configurable particle system — confetti, golden rain, sparkles, snow), `<SplitScreen>` (CSS grid, configurable split ratio), `<DepthBlur>` (CSS backdrop-filter), `<ParallaxLayer>` (scroll-driven offset), `<ZoomRush>` (spring-based zoom transition). All composable, all driven by `spring()` and `interpolate()`.
- **User story:** As a video creator, I want a library of cinematic effects I can layer onto any scene so that my videos look professionally produced.
- **Effort:** M
- **Dependencies:** None

#### 7. Beat-Synced Editing Pipeline
- **Source:** `competitive-gap-analysis.md` — HIGH gap: only CapCut and Vidio.ai have this, but it's what separates "film" from "slideshow."
- **Problem:** The wedding spec's Act 3 requires "beat-synced montage" with "cuts every 1-2 seconds" on high-energy beats. Manually identifying beats and aligning cuts is tedious and error-prone.
- **Description:** A Python tool (`tools/beat_detect.py`) using `librosa` that analyzes an audio file and exports beat timestamps as JSON (`{ beats: [0.43, 0.86, 1.29, ...], bpm: 140, downbeats: [...] }`). A companion Remotion component (`<BeatSyncedMontage>`) reads this JSON and auto-places photo/video clips on beat boundaries with configurable transitions (cut, zoom-rush, wipe). Supports "energy mapping" — louder sections get faster cuts, quieter sections get slower dissolves.
- **User story:** As a montage editor, I want my photo cuts to land on musical beats automatically so that the video feels rhythmically alive.
- **Effort:** L
- **Dependencies:** librosa (Python), `@remotion/media-utils`

---

### MEDIUM Priority

#### 8. Stock Footage Integration (Pexels API)
- **Source:** `competitive-gap-analysis.md` — HIGH gap: 5/6 competitors have stock media. Pexels is free (200 req/hr, no attribution required).
- **Problem:** Wedding spec references "Denver skyline" and "cafe meeting" — users may not have footage of every scene. Stock fills gaps.
- **Description:** A tool (`tools/pexels_search.py`) that searches Pexels for photos and videos by keyword, downloads to the project's public directory, and returns metadata (dimensions, duration, attribution). Integrates with config schema: `{ source: "pexels", query: "denver skyline sunset", type: "video" }`.
- **User story:** As a video creator, I want to search for and download stock footage from within Claude Code so that I can fill gaps in my personal photo collection.
- **Effort:** M
- **Dependencies:** Pexels API key (free)

#### 9. Photo Import & Smart Sorting Pipeline
- **Source:** `competitive-gap-analysis.md` — HIGH gap: Vidio.ai has smart ordering; Animoto imports from social. Wedding videos need 50-200+ photos organized chronologically.
- **Problem:** Users dump 200 wedding photos into a folder. Manually sorting into `childhoodPhotosGina[]`, `relationshipPhotos[]`, `familyPhotos[]` etc. is painful.
- **Description:** A tool (`tools/photo_import.py`) that reads a folder of photos, extracts EXIF dates, sorts chronologically, detects faces (OpenCV or dlib), estimates group size (solo/couple/group/crowd), filters blurry shots (Laplacian variance), removes near-duplicates (perceptual hash), and outputs organized JSON arrays matching the wedding config schema. Optional: CLIP-based semantic categorization ("outdoors", "formal", "candid").
- **User story:** As a wedding video creator, I want to point at my photo folder and have it automatically organized by date and category so that I can populate my video config instantly.
- **Effort:** L
- **Dependencies:** OpenCV, EXIF reader, perceptual hash library

#### 10. TikTok-Style Animated Captions
- **Source:** `competitive-gap-analysis.md` — HIGH gap: 3/6 competitors have this. Remotion has native `createTikTokStyleCaptions()`.
- **Problem:** Social media videos without captions lose 80% of viewers who watch with sound off. Manual caption placement is tedious.
- **Description:** Integrates Whisper.cpp transcription (already in Remotion's TikTok template) with `createTikTokStyleCaptions()` to generate word-by-word animated captions. Configurable styles (pop, highlight, karaoke, subtitle). Automatically transcribes voiceover audio files and places styled captions on the composition.
- **User story:** As a social media creator, I want auto-generated animated captions on my videos so that viewers can follow along without sound.
- **Effort:** M
- **Dependencies:** Whisper.cpp, `@remotion/captions`

#### 11. Act-Based Narrative Structure Engine
- **Source:** `competitive-gap-analysis.md` — Unique differentiator: 0/6 competitors have this.
- **Problem:** Every emotional video follows a narrative arc (setup, rising action, climax, resolution), but no tool codifies this. Users reinvent the structure each time.
- **Description:** A config-driven narrative engine where users define acts with emotional tags (nostalgic, joyful, intimate, triumphant, grateful), pacing profiles (slow, building, fast, slow-dramatic, uplifting), and content types. The engine auto-calculates scene durations to fit total runtime, selects appropriate transitions between acts, and applies matching color grades and effects. Supports narrative templates: `wedding` (Two Worlds > Meeting > Adventure > Proposal > Tomorrow), `memorial` (Life > Legacy > Community > Farewell), `birthday` (Childhood > Growth > Today > Future), `travel` (Departure > Discovery > Adventure > Return).
- **User story:** As a storyteller, I want to define my video's emotional arc and have the pacing, transitions, and effects automatically match so that the video feels like a story, not a sequence of clips.
- **Effort:** M
- **Dependencies:** Color grading (#5), cinematic effects (#6)

#### 12. Remotion Lambda Integration
- **Source:** `competitive-gap-analysis.md` — MEDIUM gap. Lambda renders 80-second video in 15 seconds at $0.01-0.10/render.
- **Problem:** Local Remotion rendering is slow for long videos (6-minute wedding video could take 10-20 minutes). Modal GPU rendering is overkill for composition rendering (no GPU needed for CSS/React).
- **Description:** Add Remotion Lambda deployment and rendering as an alternative to local `npx remotion render`. Configure Lambda function via `tools/deploy_lambda.py`, trigger renders via `tools/render_lambda.py --composition WeddingMontage --output s3://bucket/output.mp4`. Massively parallel — splits video into chunks across Lambda functions.
- **User story:** As a video creator, I want to render my 6-minute video in under a minute so that I can iterate quickly on the composition.
- **Effort:** L
- **Dependencies:** AWS account, Remotion Lambda license ($10/1000 renders on Company plan)

---

### LOW Priority

#### 13. AI B-Roll Video Generation
- **Source:** `competitive-gap-analysis.md` — MEDIUM gap: Remotion Superpowers, InVideo, FlexClip have this via Veo/Kling/Wan.
- **Problem:** Some scenes need short video clips that don't exist in the user's collection (e.g., "dancing clip (if available)" from the spec).
- **Description:** Integration with Replicate API to generate 2-5 second video clips from text prompts using Kling, Wan, or Veo models. Outputs MP4 to project's public directory. Configurable in the scene config: `{ type: "generated-clip", prompt: "couple dancing in warm lighting", duration: 4 }`.
- **User story:** As a video creator, I want to generate short AI video clips for scenes where I don't have real footage so that there are no gaps in my story.
- **Effort:** L
- **Dependencies:** Replicate API key, per-generation cost ($0.05-0.50/clip)

#### 14. Music Discovery & Licensing Integration
- **Source:** `competitive-gap-analysis.md` — HIGH gap: competitors have 3K-16M licensed tracks. We have zero library.
- **Problem:** Users need to bring their own music files. No discovery, no licensing, no mood-based search.
- **Description:** Integration with free/low-cost music APIs (Pixabay Music API — free, no attribution; Epidemic Sound API; Artlist API) for mood-based music search. Tool searches by mood/genre/tempo, previews, and downloads. Also integrates with existing MusicGen for custom AI-generated tracks when licensed music isn't needed.
- **User story:** As a video creator, I want to search for royalty-free music by mood so that I can find the perfect track without leaving my terminal.
- **Effort:** M
- **Dependencies:** Music API key(s)

#### 15. Direct Social Media Publishing
- **Source:** `competitive-gap-analysis.md` — LOW gap (4/6 competitors have it, but developers are comfortable with manual upload).
- **Problem:** After rendering, users manually upload to each platform. Minor friction for power users.
- **Description:** Post-render publishing tool that uploads to TikTok (Creator API), Instagram (Graph API), YouTube (Data API v3) with optimized metadata (title, description, hashtags, thumbnail). Requires OAuth per platform.
- **User story:** As a content creator, I want to publish my rendered video directly to social platforms from the terminal so that I don't break my workflow.
- **Effort:** L
- **Dependencies:** Platform API credentials, OAuth setup

---

### HIGH Priority (Tutorial)

#### 16. Tutorial Video Skill (`/tutorial-video`)
- **Source:** `competitive-gap-analysis.md` (tutorial section) — Screen Studio ($29/mo), Descript ($65/mo), Guidde ($50/mo) all solve this. We have zero tutorial support.
- **Problem:** Creating polished tutorial videos requires multiple tools: screen recorder, code highlighter, voiceover, editor, zoom effects. Developers cobble together OBS + Premiere + ElevenLabs. No single CLI tool does it all.
- **Description:** A skill that generates tutorial videos from a structured script. Input: markdown with `!!steps` sections containing code blocks, terminal commands, and narration text. Pipeline: (1) Code Hike parses markdown into animated code transitions, (2) Asciinema replays terminal sessions, (3) Qwen3-TTS or ElevenLabs generates voiceover per step, (4) Remotion composes everything with zoom effects, progress bar, chapter markers, and webcam/avatar PiP. Output: polished tutorial MP4.
- **User story:** As a developer educator, I want to write my tutorial as markdown and have Claude Code produce a Fireship-quality video so that I can teach without learning video editing.
- **Effort:** XL
- **Dependencies:** Code animation (#17), terminal replay (#18), voiceover (existing), zoom effects (#19)

#### 17. Animated Code Transition Component (Code Hike + Shiki)
- **Source:** Tutorial research — Code Hike (free, OSS) has native Remotion integration. Shiki Magic Move adds smooth token animations. No competitor combines both in a CLI workflow.
- **Problem:** Showing code changes in video is either a static screenshot (boring) or requires manual animation in After Effects (expensive). Code transitions should animate like Keynote's Magic Move but for syntax-highlighted code.
- **Description:** A Remotion component library that renders animated code blocks. Uses Code Hike's `parseRoot()` to extract step-by-step code states from annotated markdown, then Shiki Magic Move to animate token-level transitions (Move, Enter, Leave) between states. Supports: multi-language syntax highlighting (150+ languages via Shiki), line annotations (highlight, mark, fold), step-through with frame timing, and theme customization.
- **User story:** As a tutorial creator, I want my code examples to smoothly animate between states so that viewers can follow exactly what changed and why.
- **Effort:** M
- **Dependencies:** `@code-hike/mdx`, `shiki-magic-move`, Remotion

#### 18. Terminal Replay Component (Asciinema + Remotion)
- **Source:** Tutorial research — `asciinema-mp4` project (OSS) already bridges Asciinema to Remotion. No tutorial platform integrates terminal replay into programmatic video.
- **Problem:** Terminal demos are essential for CLI tool tutorials. Screen recording captures the whole screen; asciinema captures just the terminal but outputs to a web player, not video.
- **Description:** A Remotion component that embeds asciinema-player, seeks to exact frame timestamps, and renders terminal sessions as part of the video composition. Supports: custom themes (Dracula, Monokai, etc.), configurable terminal size, typing speed adjustment, pause/highlight at key moments, and overlay annotations (arrows, callouts).
- **User story:** As a CLI tool author, I want to include terminal demos in my tutorial videos with precise timing control so that viewers see exactly what to type and what to expect.
- **Effort:** M
- **Dependencies:** `asciinema`, `asciinema-player`, Remotion

#### 19. Auto-Zoom & Smooth Cursor Effects
- **Source:** Tutorial research — Screen Studio's auto-zoom ($29/mo) is the #1 reason people buy it. We can replicate this programmatically in Remotion.
- **Problem:** Tutorial videos need zoom-to-region effects to guide viewer attention. Without them, viewers squint at full-screen recordings trying to find what changed.
- **Description:** A Remotion component and tooling for zoom effects: (1) `<AutoZoom>` — takes a list of `{ frame, x, y, width, height }` focus regions and smoothly zooms between them using `spring()`. (2) `tools/detect_clicks.py` — analyzes screen recording or Playwright trace to auto-detect click positions and generate zoom keyframes. (3) `<SmoothCursor>` — replays cursor movement with Bezier curve smoothing (like Screen Studio). (4) `<FocusHighlight>` — dims everything except the focus region with animated spotlight.
- **User story:** As a tutorial creator, I want automatic zoom effects that follow my actions so that viewers always see exactly what I'm doing.
- **Effort:** M
- **Dependencies:** Remotion `spring()`, `interpolate()`

### HIGH Priority (Advertising)

#### 20. Ad Video Skill (`/ad-video`)
- **Source:** `competitive-gap-analysis.md` (advertising section) — Shotstack, Creatomate, InVideo all offer programmatic ad creation. 5/6 competitors have brand kits and ad templates.
- **Problem:** Creating video ads for multiple platforms requires manually reformatting the same content for TikTok (9:16, 15-60s), Instagram (1:1 or 4:5, 15-30s), YouTube (16:9, 6-15s pre-roll), Facebook (16:9 or 1:1, 15s). Each platform has different specs, safe zones, and best practices.
- **Description:** A skill that generates platform-optimized video ads from a product brief. Input: product name, tagline, key features, product shots/screenshots, brand colors/fonts/logo, CTA, target platforms. Pipeline: (1) Claude generates ad script with hook/problem/solution/CTA structure, (2) Remotion composes with brand kit, animated text, product shots, (3) Auto-generates variants for each platform format, (4) Renders all variants in parallel. Supports ad types: product launch, feature highlight, testimonial, comparison, seasonal promo.
- **User story:** As a startup founder, I want to describe my product and get video ads for every platform so that I can run paid campaigns without hiring a video agency.
- **Effort:** L
- **Dependencies:** Brand kit (#21), social format presets (#3), CTA system (#22)

#### 21. Brand Kit System
- **Source:** `competitive-gap-analysis.md` (advertising section) — 5/5 ad competitors have brand kits. Essential for consistent ad output.
- **Problem:** Every ad and marketing video needs consistent branding (logo, colors, fonts, tone). Currently, users manually specify these per project.
- **Description:** A shared brand configuration file (`brand.json` or `brand.ts`) that stores: logo (with light/dark variants), primary/secondary/accent colors, font families (heading, body, accent), favicon, tagline, website URL, social handles, brand voice guidelines. All video skills read from this file. Includes logo placement rules (safe zones, minimum sizes) and color contrast validation.
- **User story:** As a brand owner, I want to define my brand once and have every video skill automatically use correct colors, fonts, and logos so that all content looks on-brand.
- **Effort:** M
- **Dependencies:** None

#### 22. CTA Overlay & End Card System
- **Source:** `competitive-gap-analysis.md` (advertising section) — 5/5 ad competitors have CTA overlays.
- **Problem:** Every marketing video needs a call-to-action (visit site, download app, subscribe, buy now). Currently no reusable CTA component exists.
- **Description:** A library of animated CTA components: `<CTAButton>` (animated button with text + URL), `<EndCard>` (logo + tagline + CTA + social links), `<LowerThird>` (name/title bar), `<PriceTag>` (animated price display with strike-through for discounts), `<QRCode>` (animated QR code reveal). All brand-kit-aware, all animated with `spring()`.
- **User story:** As a marketer, I want professional CTA overlays and end cards that match my brand so that every video drives action.
- **Effort:** M
- **Dependencies:** Brand kit (#21)

### MEDIUM Priority (Advertising)

#### 23. Batch Personalization & A/B Variants
- **Source:** `competitive-gap-analysis.md` (advertising section) — Shotstack and Creatomate both support batch rendering with dynamic data injection.
- **Problem:** Running ads at scale requires dozens of variants: different headlines, different CTAs, different audiences, different languages. Manually creating each is wasteful.
- **Description:** A batch rendering system that takes a video template + CSV/JSON data file and renders personalized variants. Each row produces a unique video with injected text, images, and audio. Supports: dynamic text injection (names, prices, locations), image swaps (product shots per variant), A/B headline testing (generate 3-5 headline variants), language variants (swap voiceover + text). Renders in parallel via Remotion Lambda or local multi-process.
- **User story:** As a performance marketer, I want to generate 50 ad variants from one template and a spreadsheet so that I can A/B test at scale.
- **Effort:** L
- **Dependencies:** Brand kit (#21), Remotion Lambda (#12)

#### 24. Programmatic Screen Recording (Playwright)
- **Source:** Tutorial research — Playwright supports headless screen capture via DevTools Protocol. Perfect for generating product demo footage without manual recording.
- **Problem:** Product demo videos and tutorials often need browser recordings showing the product in action. Manual screen recording is inconsistent and hard to reproduce.
- **Description:** A tool (`tools/screen_record.py`) that uses Playwright to execute a scripted browser session (navigate, click, type, scroll) while capturing frames. Output: MP4 or frame sequence importable into Remotion. Supports: custom viewport sizes, device emulation (mobile, tablet), network throttling for realistic loading, and click/type highlighting overlays.
- **User story:** As a product marketer, I want to script a product demo and generate a perfect screen recording every time so that my demo videos are reproducible and consistent.
- **Effort:** M
- **Dependencies:** Playwright

---

## Theme Summary

| Priority | Count | Total Effort |
|----------|-------|-------------|
| HIGH     | 11    | 2S + 7M + 2L + 1XL = ~8 weeks |
| MEDIUM   | 7     | 4M + 3L = ~4 weeks |
| LOW      | 6     | 2M + 4L = ~4 weeks |

---

## Recommended Build Order

### Phase 1: Foundation Components (shared across all skills)
1. **Ken Burns Photo Animation** (#2) — Foundation for all photo-based video. Zero deps.
2. **Multi-Song Audio Engine** (#4) — Required for any multi-act video.
3. **Cinematic Effects Library** (#6) — Film grain, vignette, letterbox, particles, split-screen.
4. **Color Grading System** (#5) — Per-act emotional palettes.
5. **Social Media Format Presets** (#3) — Quick win: S effort, CRITICAL pressure.
6. **Brand Kit System** (#21) — Feeds into ads, tutorials, and all branded content.
7. **CTA Overlay & End Card System** (#22) — Used by ads, tutorials, social clips.

### Phase 2: Wedding Skill
8. **Beat-Synced Editing** (#7) — The "wow" feature for montages.
9. **Wedding Montage Skill** (#1) — Full `/wedding-video` skill.
10. **Act-Based Narrative Engine** (#11) — Generalizes wedding into reusable narrative system.

### Phase 3: Tutorial Skill
11. **Animated Code Transitions** (#17) — Code Hike + Shiki Magic Move.
12. **Terminal Replay Component** (#18) — Asciinema in Remotion.
13. **Auto-Zoom & Smooth Cursor** (#19) — Screen Studio-quality zoom effects.
14. **Tutorial Video Skill** (#16) — Full `/tutorial-video` skill.

### Phase 4: Ad Skill
15. **Ad Video Skill** (#20) — Full `/ad-video` skill.
16. **Programmatic Screen Recording** (#24) — Playwright-based demos.
17. **Batch Personalization** (#23) — Scale to 50+ variants.

### Phase 5: Polish & Scale
18. **Photo Import Pipeline** (#9), **Stock Footage** (#8), **TikTok Captions** (#10)
19. **Lambda Rendering** (#12) — Speed at scale.
20. **AI B-Roll** (#13), **Music Discovery** (#14), **Social Publishing** (#15) — Nice-to-haves.

---

## Next Steps

- Run `/spec wedding-video` to generate an engineering spec for the wedding montage skill.
- Run `/spec tutorial-video` to generate an engineering spec for the tutorial video skill.
- Run `/spec ad-video` to generate an engineering spec for the advertising video skill.
- Run `/spec social-clip` to generate an engineering spec for the social media clip skill.
- Run `/iterate` to start building the Ken Burns component (the foundation).
- Run `/arch-review` to assess whether the current video-toolkit architecture can support multi-song audio, beat sync, code animation, and batch rendering.
