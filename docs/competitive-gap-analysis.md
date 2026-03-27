# Competitive Gap Analysis — Remotion + AI Video Creation Skill

> Generated 2026-03-26 | Domain: Programmatic video creation via Claude Code + Remotion — wedding montages, social media clips, tutorial videos, and advertising/marketing content

---

## Our Product

- **What it does:** The `video-toolkit` skill in skills-hub-registry enables autonomous video creation from a text brief using Remotion (React) for composition, with AI-generated voiceovers (Qwen3-TTS), images (FLUX.2), background music (MusicGen), and talking head animation (SadTalker). Cloud GPU rendering via Modal or RunPod.
- **Target user:** Developers and technical creators who want to generate professional videos programmatically from Claude Code — product demos, sprint reviews, explainer videos.
- **Core value prop:** Full pipeline from text brief to rendered MP4, entirely from the terminal. No GUI video editor needed. ~$1-3 per 60s video.
- **Features implemented:** 14

### Current Feature Set (video-toolkit)

- [x] Remotion (React) video composition
- [x] Per-scene voiceover generation (Qwen3-TTS, 9 speakers, 8 tones)
- [x] Voice cloning from reference audio
- [x] AI image generation (FLUX.2) with presets
- [x] Background music generation (MusicGen, 8 presets)
- [x] Talking head animation (SadTalker)
- [x] Cloud GPU rendering (Modal endpoints)
- [x] Per-scene audio timing sync via ffprobe
- [x] TransitionSeries with fade transitions
- [x] Narrator picture-in-picture overlay
- [x] Scene-based config system (TypeScript)
- [x] Project templates (product-demo, sprint-review)
- [x] Image upscaling (RealESRGAN)
- [x] Cloudflare R2 file transfer

### What's NOT in video-toolkit

- No wedding/montage templates
- No photo slideshow/Ken Burns support
- No multi-song audio with hard-cut transitions
- No beat-synced editing
- No social media format presets (TikTok/Reels/Shorts)
- No stock footage/photo integration
- No cinematic color grading per act
- No film grain/letterboxing/vignette effects
- No split-screen compositions
- No particle/confetti effects
- No photo mosaic/grid layouts
- No user photo import pipeline (Google Photos, folders)

---

## Competitive Landscape

| Competitor | Positioning | Pricing | Market Position | Key Differentiator |
|---|---|---|---|---|
| **Remotion Superpowers** (open-source plugin) | Full production studio via Claude Code MCP servers | Free (OSS) | Niche — developer tool | 13 slash commands, Suno music, ElevenLabs, Pexels, 100+ AI models via Replicate |
| **Animoto** | Drag-and-drop video maker with wedding templates | Free–$59/mo | Challenger — consumer/SMB | 100+ wedding templates, 3,000 licensed songs, social posting |
| **InVideo AI** | Prompt-based video generation | Free–$60/mo | Leader — AI video | 16M+ stock assets, VEO 3.1 integration, voice cloning |
| **CapCut** | Free video editor with AI features | Free–$20/mo | Leader — consumer | AI Clipper (long-to-shorts), auto-captions, 12M+ assets |
| **FlexClip** | AI-assisted online video editor | Free–$20/mo | Challenger — SMB | AI Recreate, wedding templates, Hailuo/Kling/Veo integration |
| **Runway ML** | Generative AI video platform | Free–$28/mo | Leader — generative | Gen-4.5 text/image-to-video, best temporal consistency |
| **Vidio.ai** | AI wedding-specific video maker | Freemium | Niche — wedding | Smart photo ordering, music-aware pacing, auto duplicate/blur detection |
| **Mootion** | AI video generator | Freemium | Niche — speed | 3-min video in under 2 min, 65% faster than competitors |
| **Shotstack** | Programmatic video API (JSON) | Pay-per-render | Niche — developer | Cloud rendering API, event-triggered renders, template system |
| **Pictory** | Text/script to video | $19–$119/mo | Challenger — content | Blog-to-video, 3M+ clips, 15K music tracks |

---

## Feature Matrix

| Feature | Us (video-toolkit) | Remotion Superpowers | Animoto | InVideo AI | CapCut | FlexClip | Vidio.ai | Pressure | Effort |
|---|---|---|---|---|---|---|---|---|---|
| **Remotion/React composition** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | — | — |
| **CLI/terminal workflow** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | — | — |
| **AI voiceover generation** | ✅ | ✅ (ElevenLabs) | ❌ | ✅ | ✅ | ✅ | ❌ | — | — |
| **Voice cloning** | ✅ | ✅ (ElevenLabs) | ❌ | ✅ | ❌ | ❌ | ❌ | — | — |
| **AI image generation** | ✅ | ✅ (FLUX/Imagen) | ❌ | ❌ | ❌ | ✅ | ❌ | — | — |
| **AI music generation** | ✅ (MusicGen) | ✅ (Suno) | ❌ | ❌ | ❌ | ❌ | ❌ | — | — |
| **Cloud GPU rendering** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | — | — |
| **Wedding templates** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CRITICAL | M |
| **Photo slideshow / Ken Burns** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CRITICAL | M |
| **Multi-song audio w/ transitions** | ❌ | ❌ | partial | partial | ✅ | partial | ✅ | HIGH | M |
| **Beat-synced editing** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | HIGH | L |
| **Split-screen compositions** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | MEDIUM | S |
| **Cinematic color grading** | ❌ | ❌ | partial | partial | ✅ | partial | ❌ | HIGH | M |
| **Film grain / vignette effects** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | MEDIUM | S |
| **Letterboxing (cinematic bars)** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | MEDIUM | S |
| **Particle / confetti effects** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | MEDIUM | M |
| **Photo mosaic / grid layout** | ❌ | ❌ | ❌ | partial | ❌ | ❌ | ❌ | LOW | S |
| **Stock footage integration** | ❌ | ✅ (Pexels) | ✅ (Getty) | ✅ (iStock/Shutterstock) | ✅ | ✅ | ❌ | HIGH | M |
| **Social media format presets** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | CRITICAL | S |
| **TikTok-style captions** | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | HIGH | M |
| **Auto-captions (Whisper)** | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | HIGH | M |
| **Text-to-video (generative)** | ❌ | ✅ (Veo/Wan/Kling) | ❌ | ✅ | ✅ | ✅ | ❌ | MEDIUM | L |
| **AI video clips (gen. B-roll)** | ❌ | ✅ (Replicate) | ❌ | ✅ (VEO 3.1) | ❌ | ✅ (Kling) | ❌ | MEDIUM | L |
| **Licensed music library** | ❌ | ❌ | ✅ (3K tracks) | ✅ (16M assets) | ✅ | ✅ (4M assets) | ❌ | HIGH | M |
| **User photo import pipeline** | ❌ | ❌ | ✅ (Facebook/IG) | ❌ | ❌ | ❌ | ✅ | HIGH | M |
| **Smart photo ordering** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | MEDIUM | L |
| **Duplicate/blur detection** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | MEDIUM | M |
| **Direct social media posting** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | LOW | L |
| **Act-based narrative structure** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | — | M |
| **Remotion Lambda rendering** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | MEDIUM | L |

---

## Critical Gaps (Build Now)

These are table-stakes features that nearly every competitor offers and our skill completely lacks.

### 1. Wedding / Event Montage Template System
- **Who has it:** Animoto, InVideo, CapCut, FlexClip, Vidio.ai (5/6)
- **Why it matters:** The user's wedding video spec demonstrates a clear need for act-based, emotionally-driven narrative templates. This is the #1 missing capability. Without it, every wedding video requires writing the full Remotion composition from scratch.
- **Effort:** M
- **Implementation hint:** Create a `wedding-montage` template under `templates/` with act-based Sequences, configurable photo arrays per act, text overlays with timing, and pre-wired music segments.

### 2. Photo Slideshow with Ken Burns Effect
- **Who has it:** Animoto, InVideo, CapCut, FlexClip, Vidio.ai (5/6)
- **Why it matters:** Core mechanic of every wedding/memorial video. Still photos need motion to feel cinematic. The user's spec explicitly calls for "slow Ken Burns zoom" in Act 1.
- **Effort:** M
- **Implementation hint:** Remotion `interpolate()` + CSS `transform: scale() translate()` on `<Img>` components. Parameterize start/end zoom levels and pan directions.

### 3. Social Media Format Presets (9:16, 1:1, 4:5)
- **Who has it:** Animoto, InVideo, CapCut, FlexClip, Remotion Superpowers (5/6)
- **Why it matters:** User explicitly wants TikTok, Instagram, YouTube clips. Vertical video (9:16) is now the dominant format. Without presets, users must manually reconfigure compositions.
- **Effort:** S
- **Implementation hint:** Composition variants with different width/height/fps. Add `--format tiktok|reel|short|square` flag to render pipeline.

---

## Strategic Gaps (Plan & Schedule)

High-pressure features requiring significant effort.

### 4. Beat-Synced Editing Pipeline
- **Who has it:** CapCut, Vidio.ai (2/6 — but it's what makes montages feel professional)
- **Why it matters:** The user's spec requires "beat-synced montage" in Act 3 with "cuts every 1-2 seconds" on high-energy beats. This is the difference between slideshow and film.
- **Effort:** L
- **Implementation hint:** Use Python `librosa` for beat detection, export beat timestamps as JSON, Remotion reads JSON to place `<Sequence>` boundaries and transition triggers on beat frames. Remotion's `visualizeAudio()` can supplement with reactive effects.

### 5. Multi-Song Audio with Hard-Cut Transitions
- **Who has it:** CapCut, Vidio.ai, partial in Animoto/InVideo/FlexClip (5/6)
- **Why it matters:** User's spec uses two songs with an exact hard-cut at 2:12 plus a "cinematic audio whoosh." Current video-toolkit only supports single background music track.
- **Effort:** M
- **Implementation hint:** Multiple `<Audio>` components with `startFrom` and `endAt` props in Remotion. Add audio effects layer for whoosh/transition SFX. Config schema needs `audio.tracks[]` array.

### 6. Cinematic Color Grading Per Act
- **Who has it:** CapCut (full), partial in InVideo/FlexClip/Animoto (4/6)
- **Why it matters:** User spec requires different color palettes per act: "warm nostalgic" to "vibrant" to "soft cinematic" to "golden tone." This emotional progression is core to documentary filmmaking.
- **Effort:** M
- **Implementation hint:** CSS `filter` properties (brightness, contrast, saturate, sepia, hue-rotate) applied per-act `<Sequence>`. Create preset color grade objects. Remotion's `interpolateColors()` for transitions between grades.

### 7. Stock Footage / Photo Integration (Pexels API)
- **Who has it:** Remotion Superpowers, Animoto (Getty), InVideo (iStock/Shutterstock), CapCut, FlexClip (5/6)
- **Why it matters:** Not everyone has enough personal photos. Stock footage fills gaps (e.g., "Denver skyline" in the user's spec). Pexels API is free.
- **Effort:** M
- **Implementation hint:** `python3 tools/pexels_search.py --query "denver skyline" --type video --output projects/PROJECT/public/stock/`. Pexels API: 200 req/hr, free, no attribution required.

### 8. User Photo Import & Organization Pipeline
- **Who has it:** Animoto (Facebook/IG import), Vidio.ai (smart ordering) (2/6)
- **Why it matters:** Wedding videos need 50-200+ photos organized by timeline. Manual import is painful. Google Photos Picker API still allows user-selected album import.
- **Effort:** M
- **Implementation hint:** Script to import from local folder, sort by EXIF date, auto-categorize by basic heuristics or CLIP embeddings. Output organized arrays matching the config schema's photo placeholders.

---

## Differentiator Opportunities

Features that could set us apart.

### 9. Act-Based Narrative Structure Engine
- **Who has it:** Nobody (0/6)
- **Why it matters:** No competitor offers a structured narrative engine with acts, emotional arcs, and music-synced pacing. They all offer templates or freeform timelines. An act-based system that maps emotional beats to music timestamps would be unique.
- **Effort:** M

### 10. Prompt-to-Wedding-Video (Full Autonomy)
- **Who has it:** Nobody at this level
- **Why it matters:** "Make me a 6-minute wedding video for Gina and Tho with these photos and these two songs" to rendered MP4. No other tool does this from a single prompt in the terminal.
- **Effort:** XL

### 11. TikTok-Style Captions with Whisper
- **Who has it:** Remotion Superpowers, InVideo, CapCut (3/6)
- **Why it matters:** Word-by-word animated captions are now standard for social content. Remotion has `createTikTokStyleCaptions()` built in.
- **Effort:** M

### 12. AI B-Roll Generation (Veo/Kling/Wan)
- **Who has it:** Remotion Superpowers (Replicate), InVideo (VEO 3.1), FlexClip (Kling) (3/6)
- **Why it matters:** Generate short video clips to fill gaps between photos. "Dancing clip (if available)" from the spec could be generated if not available.
- **Effort:** L

---

## Our Competitive Edges

Features where we're ahead. Protect and promote these.

| Edge | Why It Matters |
|---|---|
| **Full terminal/CLI workflow** | No GUI needed. Fits developer workflow. No competitor except Remotion Superpowers offers this. |
| **Open-source AI models** | Qwen3-TTS, FLUX.2, MusicGen, SadTalker — no API key costs for core generation. Competitors lock you into subscriptions. |
| **Cloud GPU with pay-per-second** | ~$1-3 per 60s video vs $19-60/mo subscriptions. Massive cost advantage for occasional use. |
| **Claude Code integration** | Natural language to video code. The user describes what they want; Claude writes the Remotion composition. No other tool has this depth of AI-assisted composition. |
| **Fully customizable (React)** | Every frame is a React component. Unlimited creative control vs template-locked competitors. |
| **Voice cloning** | Clone any voice from a 30-second sample. Only InVideo AI matches this (and charges $60/mo). |
| **Self-hosted / no vendor lock-in** | Runs on your own infra. No account needed. No content ownership issues. |

---

## Industry Trends

| Trend | Adoption Stage | Competitors With It | Our Status | Recommendation |
|---|---|---|---|---|
| **Generative AI video (text/image to video)** | Mainstream | Runway, InVideo, CapCut, FlexClip, Superpowers | Missing | Add via Replicate (Kling, Wan, Veo) — L effort |
| **Beat-synced auto-editing** | Growing | CapCut, Vidio.ai | Missing | Build with librosa + Remotion — L effort |
| **TikTok-style word-by-word captions** | Standard | CapCut, InVideo, Superpowers | Missing | Remotion has native support — M effort |
| **Character consistency across scenes** | Emerging | Runway (Gen-4.5), InVideo (VEO 3.1) | Missing | Wait for API maturity — defer |
| **Personalized video at scale** | Growing | Synthesia, Shotstack | Partial (config-driven) | Strengthen with batch render pipeline — M effort |
| **Synchronized audio-visual generation** | Emerging | Kling 2.6 | Missing | Monitor — not actionable yet |
| **Multi-format adaptive content** | Growing | Canva, CapCut, InVideo | Missing | Social media presets — S effort |
| **Sub-second generation / real-time preview** | Early | Runway (Aleph editor) | Have (Remotion Studio) | Already ahead — Remotion Studio is real-time |
| **Sora shutdown = market fragmentation** | Current | All shifting | N/A | Opportunity to integrate multiple gen providers |

---

## Recommended Roadmap

### Sprint 1 — Quick Wins (1-2 days each)

1. **Social media format presets** — CRITICAL pressure, S effort. Add `--format tiktok|reel|short|square` to render.
2. **Split-screen composition component** — MEDIUM pressure, S effort. CSS flexbox in Remotion.
3. **Film grain / vignette / letterbox effects** — MEDIUM pressure, S effort. CSS filters + pseudo-elements.
4. **Photo mosaic / grid layout** — LOW pressure, S effort. CSS grid composition.

### Sprint 2 — Wedding Montage Core (1 week)

5. **Photo slideshow with Ken Burns** — CRITICAL pressure, M effort. Core mechanic for all photo-based videos.
6. **Wedding montage template** — CRITICAL pressure, M effort. Act-based structure with configurable photo arrays, text overlays, music segments.
7. **Multi-song audio pipeline** — HIGH pressure, M effort. Multiple `<Audio>` tracks with crossfade/hard-cut.
8. **Cinematic color grading presets** — HIGH pressure, M effort. Per-act color palettes via CSS filters.
9. **Particle / confetti effects** — MEDIUM pressure, M effort. Canvas-based or CSS animation particles.

### Next Quarter — Strategic Features

10. **Beat-synced editing pipeline** — HIGH pressure, L effort. librosa to JSON to Remotion beat-aligned cuts.
11. **Stock footage integration (Pexels)** — HIGH pressure, M effort. Free API, huge value.
12. **User photo import & sort pipeline** — HIGH pressure, M effort. EXIF sorting, basic categorization.
13. **TikTok-style captions (Whisper)** — HIGH pressure, M effort. Remotion native support.
14. **Remotion Lambda rendering** — MEDIUM pressure, L effort. 80s video in 15s, $0.01-0.10/render.

### Future — Differentiators

15. **Act-based narrative structure engine** — Unique differentiator, M effort.
16. **AI B-roll generation** — MEDIUM pressure, L effort. Via Replicate/Kling/Veo APIs.
17. **Prompt-to-wedding-video (full autonomy)** — Ultimate differentiator, XL effort.

---

## Summary

| Metric | Count |
|---|---|
| **Total features across competitors** | 29 |
| **We have** | 7 (24%) |
| **Partial** | 1 (3%) |
| **Missing** | 18 (62%) |
| **Our edges** | 7 |
| **Critical gaps to close** | 3 |
| **Strategic gaps to plan** | 5 |

- **Biggest threat:** **CapCut** — free, has nearly every feature (beat sync, AI clipper, auto-captions, color grading, effects), and is owned by ByteDance with massive resources. However, it's a GUI tool, not programmable.
- **Biggest opportunity:** **Full video creation suite from the terminal.** No competitor offers structured emotional storytelling + tutorial generation + ad creation from the CLI. Building wedding montage, tutorial, social clip, and ad skills creates a category of one: "describe what you need, get a film."

---

## Extended Analysis: Tutorial Video Competitors

| Competitor | Positioning | Pricing | Key Differentiator |
|---|---|---|---|
| **Screen Studio** | Premium macOS screen recorder | $9-29/mo | Auto-zoom on clicks, smooth cursor, cinematic feel |
| **Descript** | AI-powered text-based video editor | Free-$65/user/mo | Edit video by editing transcript; Overdub voice clone |
| **Code Hike** | Animated code walkthroughs (OSS) | Free | Markdown to animated code; Remotion integration |
| **Motion Canvas** | Procedural animation engine (OSS) | Free | 3Blue1Brown-style vector animations |
| **Guidde** | AI video documentation from workflow capture | ~$50/creator/mo | One-click Chrome capture to video guide |
| **Synthesia** | AI avatar training videos | $18-custom/mo | 240+ avatars, 160+ languages, Doc2Video |
| **Colossyan** | AI training video platform | $19-70/mo | MCQ/branching, SCORM export, avatar from photo |
| **Loom AI** | Screen recording with AI features | Business plan | Auto titles/summaries/chapters, filler word removal |
| **Tella** | All-in-one screen recorder | $12-39/mo | 30+ layouts, separate camera/screen tracks |
| **Creatomate** | Video API (JSON-based) | Credit-based | Pure API; no UI needed; CI/CD integration |

### Tutorial Features We're Missing

| Feature | Screen Studio | Descript | Code Hike | Guidde | Synthesia | Pressure | Effort |
|---|---|---|---|---|---|---|---|
| **Animated code transitions** | ❌ | ❌ | ✅ | ❌ | ❌ | HIGH | M |
| **Terminal replay in video** | ❌ | ❌ | ❌ | ❌ | ❌ | HIGH | M |
| **Auto-zoom on regions** | ✅ | ❌ | ❌ | ❌ | ❌ | HIGH | M |
| **Screen recording** | ✅ | ✅ | ❌ | ✅ | ❌ | MEDIUM | L |
| **Text-based editing** | ❌ | ✅ | ❌ | ❌ | ❌ | LOW | XL |
| **AI avatar presenter** | ❌ | ❌ | ❌ | ❌ | ✅ | MEDIUM | L |
| **Step-by-step annotations** | ❌ | ❌ | ✅ | ✅ | ❌ | HIGH | M |
| **Progress bar / chapters** | ❌ | ❌ | ❌ | ❌ | ❌ | MEDIUM | S |
| **Smooth cursor animation** | ✅ | ❌ | ❌ | ❌ | ❌ | MEDIUM | M |
| **Filler word removal** | ❌ | ✅ | ❌ | ❌ | ❌ | LOW | L |

---

## Extended Analysis: Advertising/Marketing Video Competitors

| Competitor | Positioning | Pricing | Key Differentiator |
|---|---|---|---|
| **Shotstack** | Programmatic video API | Pay-per-render | JSON-based, event-triggered, batch rendering |
| **Creatomate** | Video rendering API | Credit-based | Template + API, multi-format output |
| **InVideo AI** | Prompt-based video generation | Free-$60/mo | 16M+ stock assets, prompt-to-ad workflow |
| **Canva Video** | Design suite with video | Free-$20/mo | Brand kits, massive template library |
| **Lumen5** | Text/blog to marketing video | $29-199/mo | Blog-to-video, NLP scene selection |
| **Revid.ai** | AI short-form ad generator | Free-$39/mo | Prompt to TikTok/Instagram ad |

### Advertising Features We're Missing

| Feature | Shotstack | Creatomate | InVideo | Canva | Lumen5 | Pressure | Effort |
|---|---|---|---|---|---|---|---|
| **Brand kit (logos, colors, fonts)** | ✅ | ✅ | ✅ | ✅ | ✅ | HIGH | M |
| **Ad template library** | ✅ | ✅ | ✅ | ✅ | ✅ | HIGH | M |
| **Batch personalization** | ✅ | ✅ | ❌ | ❌ | ❌ | HIGH | L |
| **A/B variant generation** | ❌ | ✅ | ❌ | ❌ | ❌ | MEDIUM | M |
| **Blog/URL to video** | ❌ | ❌ | ❌ | ❌ | ✅ | MEDIUM | L |
| **Product shot integration** | ❌ | ✅ | ✅ | ✅ | ❌ | HIGH | M |
| **CTA overlay system** | ✅ | ✅ | ✅ | ✅ | ✅ | HIGH | S |
| **Platform-specific ad specs** | ✅ | ✅ | ✅ | ✅ | ❌ | CRITICAL | S |
| **Dynamic text/price injection** | ✅ | ✅ | ❌ | ❌ | ❌ | HIGH | M |
| **Render-at-scale (100s/1000s)** | ✅ | ✅ | ❌ | ❌ | ❌ | MEDIUM | L |

---

## Sources

- [Remotion Documentation](https://www.remotion.dev/docs/)
- [Remotion Lambda](https://www.remotion.dev/lambda)
- [Remotion AI Integration](https://www.remotion.dev/docs/ai/)
- [Remotion Superpowers](https://github.com/DojoCodingLabs/remotion-superpowers)
- [Remotion Skills](https://www.remotion.dev/docs/ai/skills)
- [Animoto](https://animoto.com)
- [InVideo AI](https://invideo.io)
- [CapCut](https://www.capcut.com)
- [FlexClip](https://www.flexclip.com)
- [Runway ML](https://runwayml.com)
- [Vidio.ai](https://www.vidio.ai)
- [Mootion](https://www.mootion.com)
- [Pictory](https://pictory.ai)
- [Shotstack](https://shotstack.io)
- [ElevenLabs](https://elevenlabs.io)
- [Pexels API](https://www.pexels.com/api/)
- [librosa](https://librosa.org)
- [Google Photos Picker API](https://developers.google.com/photos/picker)
