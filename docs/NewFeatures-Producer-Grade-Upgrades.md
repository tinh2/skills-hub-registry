# New Feature Ideas — Producer-Grade Upgrades

> Auto-generated from Remotion ecosystem research on 2026-03-26.
> Focus: Upgrading 4 existing video skills (wedding-video, tutorial-video, ad-video, social-clip) to producer-grade by integrating the Remotion ecosystem packages and AI services we are not using yet.

---

## Source Files Analyzed

| File | Key Insight |
|------|-------------|
| `build/wedding-video/SKILL.md` | v1.0 ships with Ken Burns, beat sync, multi-song audio, color grading via CSS filters, and DIY particle system. No WebGL effects, no real film grain, no LUT grading, no audio ducking. Transitions limited to fade/crossfade/whoosh. |
| `build/tutorial-video/SKILL.md` | v0.1 ships with Code Hike + Shiki Magic Move, Asciinema replay, auto-zoom, voiceover. No animated text beyond code transitions, no SVG path animation for diagrams, no 3D renders, no Google Fonts loading, hardcoded font families. |
| `build/ad-video/SKILL.md` | v1.0 ships with brand kit, KineticText, ProductShot, CTA system, batch rendering. No motion blur on product shots, no GLSL transitions, no particle effects (confetti on seasonal promos), no Rive/Lottie for animated logos. |
| `build/social-clip/SKILL.md` | v1.0 ships with captions, auto-reframe, hook structure, engagement overlays. No audio ducking (music stays loud under voice), no loudness normalization per platform, no GIF embedding, no procedural noise for aesthetic grain. |
| `docs/NewFeatures-Cinematic-Video-Pipeline.md` | Original feature ideation. Built the 4 skills from this doc. Many features shipped as custom implementations (particles via `interpolate()` on divs, film grain via CSS noise overlay) that official Remotion packages do better. |

---

## Feature Ideas

### HIGH Priority

These features use existing published npm packages we should integrate immediately. Zero custom code needed beyond wiring up the dependency.

---

#### 1. WebGL Light Leak Transitions and Effects

- **Name:** Light Leak Integration
- **Source:** `@remotion/light-leaks` (official Remotion package)
- **Problem:** Wedding-video currently uses basic fade-to-black and crossfade transitions between acts. Light leaks are the industry-standard cinematic transition for emotional montages, and we built a placeholder suggestion in the SKILL.md ("light-leaks between upbeat acts") without an actual implementation. Ad-video and social-clip also lack any premium transition options.
- **Description:** Install `@remotion/light-leaks` and replace the custom act transition system with WebGL-powered light leak overlays. The package provides both transition mode (between scenes) and effect mode (overlay on a scene). Use transition mode between wedding acts and ad scenes. Use effect mode for dreamy overlays on wedding proposal acts and seasonal promo reveals. Configure intensity, color tint (warm gold for weddings, brand-color for ads), and duration.
- **User story:** As a wedding video creator, I want cinematic light leak transitions between acts so that my montage feels like a professional film rather than a slideshow with fades.
- **Effort:** S
- **Dependencies:** `@remotion/light-leaks`
- **Which skills benefit:** wedding-video (act transitions + proposal scene overlay), ad-video (scene transitions for premium feel), social-clip (transition library expansion)

---

#### 2. Motion Blur for Product Shots and Transitions

- **Name:** Camera Motion Blur
- **Source:** `@remotion/motion-blur` (official Remotion package)
- **Problem:** Ad-video's `ProductShot` component supports `tilt-3d`, `float`, and `slide-in` animations, but they look synthetic because there is no motion blur. Real camera footage has natural blur on moving objects. Tutorial-video's auto-zoom transitions also look digital without blur. Social-clip's `whip-pan` transition simulates motion blur with CSS but it is a poor approximation.
- **Description:** Install `@remotion/motion-blur` and wrap moving elements with `<Trail>` for object-level blur (product shots sliding in, KineticText slamming) and `<CameraMotionBlur>` for full-frame blur (whip-pan transitions, zoom-rush). Configure `lagInFrames` and `trailOpacity` per use case: subtle (1 frame, 0.6 opacity) for product reveals, aggressive (3 frames, 0.8 opacity) for whip-pan.
- **User story:** As an ad creator, I want my product shot animations to have natural motion blur so that the movement looks like real camera footage instead of a CSS transform.
- **Effort:** S
- **Dependencies:** `@remotion/motion-blur`
- **Which skills benefit:** ad-video (ProductShot animations, KineticText slam), social-clip (whip-pan transition, zoom-rush), tutorial-video (auto-zoom transitions), wedding-video (Ken Burns panning at fast pacing)

---

#### 3. Procedural Film Grain via Noise Generation

- **Name:** Real Film Grain
- **Source:** `@remotion/noise` (official Remotion package)
- **Problem:** Wedding-video's `<FilmGrain>` effect uses a CSS noise overlay with "deterministic seeded noise frames." This produces a static, repeating pattern that looks artificial at full resolution. Real film grain is procedurally generated per-frame with varying intensity. The current approach also has no frequency control (fine grain vs coarse grain).
- **Description:** Replace the CSS-based `<FilmGrain>` with `@remotion/noise` procedural generation. Use `noise2D()` or `noise3D()` (with frame as the Z axis) to generate per-pixel grain that evolves over time. Expose grain presets: `fine-35mm` (high frequency, low amplitude), `coarse-16mm` (low frequency, high amplitude), `super8` (heavy grain + slight color shift), `digital-noise` (uniform). Apply as a canvas overlay composited with `mix-blend-mode: overlay`.
- **User story:** As a wedding filmmaker, I want authentic film grain that changes every frame so that my nostalgic childhood act feels like real vintage footage instead of a Photoshop filter.
- **Effort:** M
- **Dependencies:** `@remotion/noise`
- **Which skills benefit:** wedding-video (all acts with `filmGrain: true`), social-clip (aesthetic grain for lo-fi content), ad-video (vintage/retro ad styles)

---

#### 4. SVG Path Animation for Diagrams and Reveals

- **Name:** Animated SVG Paths
- **Source:** `@remotion/paths` (official Remotion package)
- **Problem:** Tutorial-video has no way to animate diagrams, architecture drawings, or flow charts. The only visual types are code, terminal, screenshot, and plain images. Handwritten signature reveals for wedding end cards require manual frame-by-frame animation. Ad-video's comparison charts are static tables.
- **Description:** Install `@remotion/paths` and build three components: (1) `<AnimatedDiagram>` for tutorial-video that takes an SVG and progressively draws paths with `evolvePath()` and `getLength()`, perfect for architecture diagrams and flow charts. (2) `<SignatureReveal>` for wedding-video end cards that traces a cursive signature path. (3) `<AnimatedChart>` for ad-video that draws line charts, bar charts, and comparison graphs with path animation. All use `interpolate()` to control draw progress over frames.
- **User story:** As a tutorial creator, I want to show architecture diagrams that draw themselves line by line so that viewers follow the flow instead of seeing a wall of boxes.
- **Effort:** M
- **Dependencies:** `@remotion/paths`
- **Which skills benefit:** tutorial-video (animated diagrams, flow charts), wedding-video (signature reveal on end card), ad-video (animated comparison charts, growth metrics)

---

#### 5. Dynamic Text Layout with measureText

- **Name:** Smart Text Fitting
- **Source:** `@remotion/layout-utils` (official Remotion package)
- **Problem:** All 4 skills hardcode font sizes for text overlays. Wedding-video specifies `fontSize: 36` in config. Ad-video's KineticText has fixed sizes per mode. Social-clip's caption text overflows on long words. Tutorial-video's chapter titles clip on long names. None of them adapt text size to fit available space.
- **Description:** Install `@remotion/layout-utils` and use `fitText()` to auto-size headlines that must fit a container (ad hooks, wedding title cards, social CTAs). Use `fillTextBox()` for multi-line text that must fill a region without overflow (wedding text overlays, ad problem/solution copy). Use `measureText()` for precise caption word placement in social-clip. Replace all hardcoded `fontSize` values with dynamic sizing that respects container bounds.
- **User story:** As an ad creator, I want my headline text to automatically resize to fit the available space so that I never have text clipping or awkward wrapping across platform formats.
- **Effort:** M
- **Dependencies:** `@remotion/layout-utils`
- **Which skills benefit:** all 4 skills (wedding-video title cards, tutorial-video chapter titles, ad-video KineticText, social-clip captions and CTAs)

---

#### 6. Google Fonts Loading

- **Name:** Google Fonts Integration
- **Source:** `@remotion/google-fonts` (official Remotion package)
- **Problem:** Wedding-video references `Playfair Display` in config but has no font loading mechanism. Tutorial-video hardcodes `Inter` and `JetBrains Mono` in theme config. Ad-video loads fonts via `loadFont()` but the implementation details are unclear. Social-clip defaults to `Inter`. None of them have a reliable, tree-shakeable font loading solution.
- **Description:** Install `@remotion/google-fonts` and replace all font loading with the official package. Each font is a separate import (`import { loadFont } from '@remotion/google-fonts/Inter'`), ensuring tree-shaking. Build a `<FontLoader>` wrapper component that reads font families from config (wedding-config, tutorial theme, brand.json) and loads them at composition mount. This eliminates FOUT (flash of unstyled text) and ensures fonts render correctly in Lambda/cloud rendering where system fonts are unavailable.
- **User story:** As a video creator, I want to use any Google Font by name in my config and have it load reliably so that my text renders correctly on every machine and in cloud rendering.
- **Effort:** S
- **Dependencies:** `@remotion/google-fonts`
- **Which skills benefit:** all 4 skills

---

#### 7. GLSL Shader Transitions

- **Name:** GPU Shader Transition Library
- **Source:** `remotion-dev/gl-transitions` (community package, wraps gl-transitions.com)
- **Problem:** Social-clip has 7 transition types (swipe, zoom-rush, glitch, flash, whip-pan, fade, cut). Ad-video and tutorial-video have fewer. Wedding-video has 5 act transition types. All are implemented as custom CSS/React animations. The gl-transitions library has 65+ GPU-accelerated shader transitions (directional warp, morph, cube rotation, pixelize, burn, ripple, swirl) that look dramatically better and run faster.
- **Description:** Install `remotion-dev/gl-transitions` and expose the full transition catalog to all 4 skills. Map transitions to use cases: `Burn` and `CrossZoom` for wedding high-energy acts, `DirectionalWarp` and `Morph` for ad scene changes, `Pixelize` and `GlitchMemories` for social-clip tech content, `SimpleZoom` and `Fade` for tutorial-video. Add a `glTransition` option to all transition configs alongside existing custom transitions. Users can specify any gl-transition by name.
- **User story:** As a social clip creator, I want access to dozens of GPU-accelerated transitions so that I can match the visual polish of professional editing software.
- **Effort:** M
- **Dependencies:** `remotion-dev/gl-transitions`, WebGL support in render environment
- **Which skills benefit:** all 4 skills

---

#### 8. Animated Text System (Remotion Bits)

- **Name:** Character/Word/Line Staggered Text Animation
- **Source:** Remotion Bits (`remotion-bits` — remotion-bits.dev) `AnimatedText` component
- **Problem:** Ad-video has `KineticText` with 6 modes (slide-up, pop-word, typewriter, wave, split-reveal, counter). Wedding-video has basic fade text overlays. Social-clip has hook text with zoom-in/shake/flash. Tutorial-video has no text animation beyond code transitions. None of them support character-level stagger, word-level stagger with custom easing per character, or line-by-line reveals with configurable spring physics.
- **Description:** Install Remotion Bits (`npx remotion-bits fetch AnimatedText`) and use `<AnimatedText>` alongside existing KineticText. AnimatedText provides granular control: animate by character, word, or line with independent easing, stagger delay, and spring config per unit. Use for: wedding text overlays (word-by-word romantic reveals), ad headlines (character-stagger slam effect), social hook text (per-character spring bounce), tutorial chapter titles (line-by-line slide). Does not replace KineticText but complements it for cases needing finer control.
- **User story:** As a wedding video creator, I want my text overlays to reveal word-by-word with elegant timing so that each phrase lands with emotional weight.
- **Effort:** S
- **Dependencies:** `remotion-bits` CLI + `AnimatedText` component
- **Which skills benefit:** all 4 skills

---

#### 9. Particle System Upgrade (Remotion Bits)

- **Name:** Physics-Based Particle System
- **Source:** Remotion Bits (`remotion-bits`) `ParticleSystem` component + `remotion-confetti`
- **Problem:** Wedding-video has a custom particle system with 6 types (confetti, golden-rain, sparkles, snow, bokeh, dust) "all rendered via `interpolate()` on divs." This is CPU-bound, limited to simple linear motion, and cannot simulate physics (gravity, wind, turbulence, collision). Ad-video has no particle effects at all despite seasonal promos needing confetti/celebration effects.
- **Description:** Replace the div-based particle system with Remotion Bits `ParticleSystem` (configurable emitter position, velocity, gravity, wind, lifetime, spawn rate, particle size/color/opacity curves) and `remotion-confetti` (canvas-based with real physics). Map to existing wedding presets: `confetti` uses `remotion-confetti` for realistic paper physics, `golden-rain` and `snow` use `ParticleSystem` with gravity, `sparkles` and `bokeh` use `ParticleSystem` with zero gravity + fade. Add new presets: `fireworks` (burst emitter), `bubbles` (float up with wobble), `embers` (glow particles with wind). Add to ad-video for seasonal-promo celebrations and social-clip for engagement moments.
- **User story:** As a wedding video creator, I want my golden-rain particles to drift realistically with wind and gravity so that the finale act feels magical rather than mechanical.
- **Effort:** M
- **Dependencies:** `remotion-bits` `ParticleSystem`, `remotion-confetti`
- **Which skills benefit:** wedding-video (all particle effects), ad-video (seasonal promos, celebration moments), social-clip (engagement moments, hook effects)

---

#### 10. Lottie and Rive Animation Embedding

- **Name:** Vector Animation Support
- **Source:** `@remotion/lottie` + `@remotion/rive` (official Remotion packages)
- **Problem:** Ad-video's brand kit stores logos as static SVG files. Many brands have animated logos (Lottie format) that should play in video intros. Tutorial-video has no way to embed animated icons or illustrations. Wedding-video could use animated decorative elements (animated hearts, rings, floral frames). Social-clip engagement overlays (like/subscribe animations) are static.
- **Description:** Install both `@remotion/lottie` and `@remotion/rive`. Build an `<AnimatedAsset>` wrapper that auto-detects format (.json = Lottie, .riv = Rive) and renders with timeline sync via `useCurrentFrame()`. Use cases: (1) Ad-video animated brand logos in hook and end card, (2) Tutorial-video animated icons for step transitions and concept illustrations, (3) Wedding-video decorative frames and animated overlays (hearts, rings, sparkle borders), (4) Social-clip animated engagement icons (thumbs up, subscribe bell, share arrow). Source animations from LottieFiles.com (free tier) and Rive community.
- **User story:** As an ad creator, I want to use my brand's animated Lottie logo in the video intro so that the ad matches our website and app experience.
- **Effort:** M
- **Dependencies:** `@remotion/lottie`, `@remotion/rive`
- **Which skills benefit:** ad-video (animated logos, brand elements), tutorial-video (animated icons, concept illustrations), wedding-video (decorative animations), social-clip (engagement icons)

---

#### 11. GIF Sync with Timeline

- **Name:** GIF Embedding
- **Source:** `@remotion/gif` (official Remotion package)
- **Problem:** Social-clip and tutorial-video cannot embed GIF content. Reaction GIFs are a staple of social content. Tutorial-video could use GIFs to show UI interactions or quick demos. Currently, users must convert GIFs to MP4 manually before using them.
- **Description:** Install `@remotion/gif` and add GIF as a supported media type across skills. The package syncs GIF frame timing with Remotion's timeline, so GIFs play at correct speed and can be seeked. Add `type: 'gif'` to social-clip scene types and tutorial-video asset types. Support looping configuration and playback speed control.
- **User story:** As a social clip creator, I want to embed reaction GIFs directly in my clips so that I can add personality without converting file formats.
- **Effort:** S
- **Dependencies:** `@remotion/gif`
- **Which skills benefit:** social-clip (reaction GIFs, meme content), tutorial-video (UI interaction demos)

---

#### 12. Geometric Shape Components

- **Name:** Animated Shape Primitives
- **Source:** `@remotion/shapes` (official Remotion package)
- **Problem:** Ad-video uses CSS for all geometric elements (buttons, price tags, badges). Tutorial-video has no shape primitives for diagrams. Social-clip engagement overlays use div-based shapes. None of them have clean SVG-based shapes with animation support.
- **Description:** Install `@remotion/shapes` and use Triangle, Star, Circle, Pie for: (1) Ad-video rating stars in testimonials, pie charts for market share claims, triangles as directional indicators. (2) Tutorial-video diagram nodes, progress indicators, step markers. (3) Social-clip engagement overlays (star ratings, circular progress for countdowns). (4) Wedding-video decorative elements. All shapes support `makeShape()` for path extraction, enabling animation with `@remotion/paths`.
- **User story:** As an ad creator, I want animated star ratings in my testimonial ads so that social proof feels dynamic rather than static.
- **Effort:** S
- **Dependencies:** `@remotion/shapes`, enhanced by `@remotion/paths` for animation
- **Which skills benefit:** ad-video (ratings, charts, indicators), tutorial-video (diagrams), social-clip (overlays), wedding-video (decorative)

---

#### 13. Declarative Animation Chaining

- **Name:** Fluent Animation API
- **Source:** `remotion-animated` (remotion-animated.dev)
- **Problem:** All 4 skills write animation logic as raw `interpolate()` and `spring()` calls, which is verbose and hard to read. A simple "fade in, slide up, then scale" requires 15+ lines of interpolation code. This makes the generated Remotion compositions harder to maintain and debug.
- **Description:** Install `remotion-animated` and use the declarative `<Animated>` component with chainable animations: `<Animated animations={[Move({ y: 50 }), Scale({ initial: 0.8 }), Fade({ to: 1 })]}}>`. Use as the default animation wrapper in all skills. This reduces animation code by 60-70% while maintaining the same visual output. Does not replace `spring()` for physics-based motion but covers the 80% case of entrance/exit animations.
- **User story:** As a skill maintainer, I want a concise animation API so that generated Remotion code is readable and easy to customize.
- **Effort:** S
- **Dependencies:** `remotion-animated`
- **Which skills benefit:** all 4 skills (reduces code complexity across all generated compositions)

---

#### 14. Audio Waveform Visualization

- **Name:** Audio Spectrum Visualizer
- **Source:** `remotion-audio-visualizers` (community package)
- **Problem:** Social-clip has no visual representation of audio. Tutorial-video plays voiceover with no visual indicator that audio is present. Wedding-video's beat-synced montage could benefit from a visual beat indicator. Podcast clips and music content need waveform displays.
- **User story:** As a social clip creator, I want an audio waveform visualization behind my voiceover so that viewers can see the audio energy and the clip feels more dynamic.
- **Description:** Install `remotion-audio-visualizers` and add spectrum visualization components. Use cases: (1) Social-clip waveform behind talking-head content, circular visualizer for music clips. (2) Tutorial-video subtle waveform indicator when voiceover is active. (3) Wedding-video beat visualization during montage acts. Support bar, circular, and line waveform styles with color and size configuration.
- **Effort:** S
- **Dependencies:** `remotion-audio-visualizers`
- **Which skills benefit:** social-clip (waveform overlays), tutorial-video (voiceover indicator), wedding-video (beat visualization)

---

### MEDIUM Priority

These features require building on top of existing packages and services. More integration work but high-impact improvements.

---

#### 15. Audio Ducking (Auto Music Volume Control)

- **Name:** Intelligent Audio Ducking
- **Source:** Producer intelligence pattern + FFmpeg sidechain compression
- **Problem:** All 4 skills layer voiceover and background music at fixed volumes. Social-clip sets `backgroundMusicVolume: 0.12`. Ad-video uses `volume={0.12}`. Tutorial-video uses `volume={0.08}`. But when the speaker pauses, the music should rise, and when they speak, it should duck. Fixed volume means music is either too quiet during pauses or too loud during speech.
- **Description:** Build a `tools/analyze_audio_levels.py` script that takes a voiceover file and outputs a volume envelope JSON: timestamp-to-volume array marking speech segments (duck to 0.08) and silence segments (rise to 0.25). Use `whisper.cpp` (already a dependency for captions) to detect speech segments. The `<AudioTrack>` component reads this envelope and applies `interpolate()` on the background music volume, ducking 6-12dB during speech and restoring during silence. Configurable duck depth, attack time (how fast music drops), and release time (how fast it rises back). Apply across all skills that mix voiceover + music.
- **User story:** As a tutorial creator, I want the background music to automatically lower when I am speaking and rise during pauses so that the audio mix sounds professionally produced.
- **Effort:** M
- **Dependencies:** `whisper.cpp` (already installed for social-clip captions), FFmpeg
- **Which skills benefit:** all 4 skills (any skill mixing voiceover + background music)

---

#### 16. Loudness Normalization Per Platform

- **Name:** Platform-Specific Loudness Targeting
- **Source:** Producer intelligence pattern + FFmpeg loudnorm filter
- **Problem:** Social-clip documents codec and bitrate per platform but ignores loudness standards. TikTok targets -14 LUFS, YouTube targets -14 LUFS, Instagram targets -14 LUFS, podcasts target -16 LUFS, broadcast targets -24 LUFS. Our renders have whatever loudness the source audio had. Videos that are too quiet get skipped; videos that are too loud get compressed and sound distorted.
- **Description:** Add a post-render loudness normalization step using FFmpeg's `loudnorm` filter. Build `tools/normalize_audio.py` that analyzes the rendered video's loudness (integrated LUFS, true peak, LRA) and applies two-pass loudness normalization to the target. Add platform-specific targets to the platform preset tables in social-clip and ad-video. Run automatically as part of the batch render pipeline. Command: `ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1:LRA=11 -c:v copy output.mp4`.
- **User story:** As an ad creator, I want my TikTok ads to hit -14 LUFS automatically so that they sound consistent with native TikTok content and do not get volume-compressed by the platform.
- **Effort:** S
- **Dependencies:** FFmpeg (already required)
- **Which skills benefit:** ad-video (all platform renders), social-clip (all platform renders), tutorial-video (YouTube render), wedding-video (final output)

---

#### 17. LUT-Based Color Grading

- **Name:** Real Color Grading with .cube LUT Files
- **Source:** Producer intelligence pattern + FFmpeg LUT3D filter
- **Problem:** Wedding-video's color grading system uses CSS filters (`brightness`, `contrast`, `saturate`, `sepia`, `hue-rotate`) wrapped in a `<ColorGrade>` component. CSS filters are limited: they cannot reproduce the nonlinear color transformations of real film stocks (Kodak Portra 400, Fuji Pro 400H) or professional color grades (teal-and-orange, bleach bypass). Professional colorists use 3D LUT (.cube) files, and there are hundreds available for free.
- **Description:** Add LUT-based color grading as an alternative to CSS filters. Ship a curated set of .cube LUT files: `portra-400` (warm skin tones), `pro-400h` (soft greens, muted highlights), `ektar-100` (vivid saturated), `teal-orange` (Hollywood blockbuster), `bleach-bypass` (desaturated, high contrast), `moonlight` (cool blue shadows). Apply via FFmpeg post-render: `ffmpeg -i input.mp4 -vf lut3d=portra-400.cube output.mp4`. Also build a real-time preview path using WebGL LUT shader for Remotion Studio preview. Map to wedding emotion tags: `nostalgic` -> `portra-400`, `vibrant-adventure` -> `ektar-100`, `soft-cinematic` -> `pro-400h`, `golden-sunset` -> custom warm LUT.
- **User story:** As a wedding filmmaker, I want to grade my video with a Kodak Portra 400 LUT so that it has the authentic warm film look instead of CSS filter approximations.
- **Effort:** M
- **Dependencies:** FFmpeg (already required), .cube LUT files (free from multiple sources)
- **Which skills benefit:** wedding-video (replaces CSS color grading), social-clip (aesthetic grading), ad-video (brand-specific color treatments)

---

#### 18. fal.ai Unified Video Generation API

- **Name:** Multi-Model AI Video Generation via fal.ai
- **Source:** fal.ai (single API for Veo 3.1, Sora 2, Kling 3, Wan 2.2, Hailuo)
- **Problem:** The cinematic pipeline doc mentions Replicate API for AI B-roll generation. But fal.ai offers a single API key that routes to ALL major video generation models (Veo 3.1, Sora 2, Kling 3, Wan 2.2, Hailuo) at $0.05-0.50/sec. Instead of managing multiple API keys and SDKs, one integration covers everything. Wedding-video needs B-roll clips for scenes the user has no photos of. Ad-video needs product demo simulations. Social-clip needs hook visuals.
- **Description:** Build `tools/generate_video_clip.py` that calls fal.ai's video generation endpoint. Support model selection (`--model veo3`, `--model kling3`, `--model wan2`) or auto-select based on use case (Veo 3.1 for photorealism, Kling 3 for motion quality, Wan 2.2 for budget). Input: text prompt, duration (2-8 sec), aspect ratio. Output: MP4 to project's public directory. Integrate as a new scene type `type: 'ai-generated'` across all skills. Add to config schemas: `{ type: 'ai-generated', prompt: 'couple walking on beach at sunset', model: 'veo3', duration: 4 }`.
- **User story:** As a wedding video creator, I want to generate a short cinematic clip of a sunset beach walk to fill a scene where I do not have footage, using whichever AI model produces the best result.
- **Effort:** M
- **Dependencies:** fal.ai API key, $0.05-0.50/sec per generation
- **Which skills benefit:** wedding-video (B-roll for missing scenes), ad-video (product simulations, lifestyle footage), social-clip (hook visuals, B-roll), tutorial-video (concept visualizations)

---

#### 19. AI Music with Vocals via Suno

- **Name:** AI Music Generation with Lyrics
- **Source:** Suno (via KIE API — $0.03-0.04/song on Premier plan)
- **Problem:** The current pipeline uses MusicGen for instrumental background tracks. But wedding-video needs songs with actual vocals for emotional montages (imagine a custom love song with the couple's names). Ad-video could use jingles with brand-specific lyrics. Social-clip hook music with vocals is more engaging than instrumentals.
- **Description:** Build `tools/suno_music.py` that generates songs with vocals from text prompts via Suno's API. Input: genre, mood, lyrics (optional — Suno can generate lyrics from a description), duration. Output: MP3 with vocals. Use alongside MusicGen: MusicGen for instrumental background, Suno for hero tracks with vocals. Add to wedding config: `{ type: 'suno', prompt: 'romantic acoustic love song about Gina and Tho', genre: 'folk', duration: 180 }`. Add to ad config: `{ type: 'suno', prompt: 'upbeat tech jingle: ship faster break nothing', genre: 'electronic', duration: 30 }`.
- **User story:** As a wedding video creator, I want to generate a custom love song with vocals that mentions our names so that the soundtrack is truly personal.
- **Effort:** M
- **Dependencies:** Suno API key via KIE, $0.03-0.04/song
- **Which skills benefit:** wedding-video (custom love songs), ad-video (brand jingles), social-clip (hook music with vocals)

---

#### 20. AI Video Review Loop via TwelveLabs

- **Name:** Automated Quality Review
- **Source:** TwelveLabs (video understanding API, free tier available)
- **Problem:** After rendering, there is no automated quality check. Users must manually watch the entire video to catch issues: misaligned text, awkward transitions, pacing problems, scenes that do not match the brief. The Remotion Superpowers architecture uses a 3-agent system where a "post-producer" agent watches the render and provides feedback.
- **Description:** Build `tools/review_video.py` that uploads a rendered video to TwelveLabs, then queries it with structured prompts: "Does the hook grab attention in the first 3 seconds?", "Are there any scenes where text is cut off or unreadable?", "Does the pacing feel rushed or slow in any segment?", "Does the color grading change match the emotional arc?", "Is the audio mix clear — can you hear the voiceover over the music?". Output a structured review JSON with pass/fail per criterion and suggestions. Integrate as an optional post-render step across all skills.
- **User story:** As a video creator, I want an AI to watch my rendered video and flag quality issues before I publish so that I catch problems without watching the full video myself.
- **Effort:** L
- **Dependencies:** TwelveLabs API key (free tier: 600 API calls/month, 10 hours of video indexing)
- **Which skills benefit:** all 4 skills (post-render quality gate)

---

#### 21. Three.js 3D Rendering in Video

- **Name:** 3D Scene Integration
- **Source:** `@remotion/three` (official Remotion package)
- **Problem:** Ad-video's `ProductShot` supports `tilt-3d` animation but it is a CSS perspective transform, not true 3D. Tutorial-video cannot render 3D diagrams or architectural visualizations. Wedding-video cannot create 3D text or flying-through-photos effects. No skill can render actual 3D scenes.
- **Description:** Install `@remotion/three` and build 3D components: (1) `<Product3D>` for ad-video that renders a product in a real 3D scene with lighting, rotation, and camera movement. (2) `<Text3D>` for wedding title cards with depth, metallic materials, and dramatic lighting. (3) `<PhotoGallery3D>` for wedding-video that arranges photos in 3D space and flies the camera through them. (4) `<Diagram3D>` for tutorial-video 3D architecture visualizations. Use `useThree()` hook for camera control synced to Remotion frames.
- **User story:** As an ad creator, I want to render my product in a real 3D scene with dramatic lighting so that it looks like a premium commercial.
- **Effort:** L
- **Dependencies:** `@remotion/three`, `three`, `@react-three/fiber`
- **Which skills benefit:** ad-video (3D product renders), wedding-video (3D title cards, photo gallery), tutorial-video (3D architecture diagrams)

---

#### 22. Local Speech-to-Text via whisper.cpp

- **Name:** Zero-Cost Local Transcription
- **Source:** whisper.cpp (already partially used in social-clip for captions)
- **Problem:** Social-clip already uses Whisper for caption generation, but the setup is fragmented: `pip3 install openai-whisper` OR `npx remotion install-whisper-cpp`. The other 3 skills do not use transcription at all despite needing it. Tutorial-video could auto-generate chapter markers from voiceover. Wedding-video could detect speech in video clips for audio ducking. Ad-video could verify voiceover content matches the script.
- **Description:** Standardize on `whisper.cpp` via `npx remotion install-whisper-cpp` across all 4 skills (it runs locally on Apple Silicon with sub-second latency, zero cost, zero telemetry). Build a shared `tools/transcribe_local.py` wrapper that outputs both caption JSON (for `@remotion/captions`) and speech-segment JSON (for audio ducking). Integrate into: (1) Social-clip caption pipeline (already done, just standardize). (2) Tutorial-video auto-chapter detection from voiceover content. (3) Wedding-video speech detection in video clips. (4) Ad-video script-vs-voiceover verification.
- **User story:** As a tutorial creator, I want my voiceover automatically transcribed locally so that chapters are generated and captions are created without sending audio to any cloud service.
- **Effort:** M
- **Dependencies:** `whisper.cpp` via Remotion installer
- **Which skills benefit:** all 4 skills (captions, ducking, chapters, verification)

---

#### 23. Edit Pacing Engine

- **Name:** Genre-Aware Cut Rhythm
- **Source:** Producer intelligence — pacing theory from film editing (Walter Murch "In the Blink of an Eye")
- **Problem:** Wedding-video has pacing presets (slow = 4-6s/photo, fast = 1-2s/photo) but they are static values. Real film editing uses variable pacing that responds to emotional arc: tension builds with shortening cuts, resolution uses lengthening cuts. Ad-video has fixed duration allocations per scene. Social-clip has no pacing intelligence. Tutorial-video relies on narration duration only.
- **Description:** Build a `PacingEngine` class that encodes pacing theory: (1) Cut length curves that accelerate toward climax and decelerate toward resolution. (2) Genre profiles: `wedding` (slow build, fast montage, slow resolution), `ad` (fast hook, medium problem, fast solution, slow CTA), `tutorial` (steady with emphasis holds), `social` (fast throughout with micro-holds on key moments). (3) Energy mapping from audio analysis (high BPM = shorter cuts). (4) Minimum/maximum cut duration guardrails per platform (TikTok minimum 0.5s, wedding minimum 2s). The engine takes a sequence of scenes and redistributes their durations based on the pacing profile and position in the narrative arc.
- **User story:** As a wedding video creator, I want the pacing to automatically accelerate toward the adventure montage climax and slow down for the proposal so that the video breathes like a real film.
- **Effort:** M
- **Dependencies:** None (pure logic, informed by audio analysis from librosa)
- **Which skills benefit:** all 4 skills (wedding-video act pacing, ad-video scene timing, social-clip beat pacing, tutorial-video step timing)

---

#### 24. Platform-Specific Encoding Profiles

- **Name:** Codec/Bitrate/Container Optimization
- **Source:** Producer intelligence + platform documentation
- **Problem:** Social-clip documents codec and bitrate per platform in a table but does not enforce them in the render pipeline. Ad-video renders all platforms with the same settings. The batch render scripts do not apply platform-specific FFmpeg flags. Missing: CRF tuning (TikTok needs lower CRF than YouTube for quality at smaller file size), faststart for web streaming, color space tagging (bt709), HDR support for YouTube.
- **Description:** Build a `tools/encode_for_platform.py` that takes a rendered video and optimizes it for a specific platform. Profiles: TikTok (H.264 High, CRF 18, -pix_fmt yuv420p, -colorspace bt709, 8Mbps cap, faststart), YouTube (H.264 High, CRF 17, 10Mbps, faststart, chapter markers in metadata), Instagram (H.264 Main, CRF 20, 6Mbps, 3500kbps audio), LinkedIn (H.264 Main, CRF 21, 5Mbps). Integrate as the final step in all batch render pipelines. Also add: thumbnail extraction at the hook frame, subtitle file generation (.srt) for platform-native captions.
- **User story:** As an ad creator, I want each platform render to use the optimal encoding settings so that my videos look their best and load quickly on every platform.
- **Effort:** M
- **Dependencies:** FFmpeg (already required)
- **Which skills benefit:** ad-video (all platform renders), social-clip (all platform renders), tutorial-video (YouTube optimization), wedding-video (export optimization)

---

### LOW Priority

Nice-to-have producer intelligence features that add professional polish.

---

#### 25. Quality Scoring System

- **Name:** Automated Video Quality Assessment
- **Source:** Producer intelligence pattern
- **Problem:** There is no objective way to measure whether a generated video is "good" before publishing. Users rely on subjective preview watching. Professional post-production uses scoring rubrics for technical quality (resolution, bitrate, audio levels) and creative quality (pacing, composition, color consistency).
- **Description:** Build `tools/score_video.py` that analyzes a rendered video and produces a quality score (0-100) across dimensions: (1) Technical — resolution matches target, bitrate within range, no dropped frames, audio levels within LUFS target. (2) Pacing — average cut length, cut length variance, hook speed (time to first scene change). (3) Audio — voice-to-music ratio, silence percentage, clipping detection. (4) Visual — black frame detection, static frame detection (frozen video), consistent color temperature. Output a report card with per-dimension scores and flagged issues. Run automatically after render as an optional step.
- **User story:** As a video creator, I want an automated quality score after rendering so that I know whether the video meets professional standards before I publish.
- **Effort:** L
- **Dependencies:** FFmpeg (for analysis), numpy (for statistics)
- **Which skills benefit:** all 4 skills

---

#### 26. Narrative Framework Templates

- **Name:** Story Structure Library
- **Source:** Producer intelligence — narrative theory (Joseph Campbell, Dan Harmon)
- **Problem:** Wedding-video has a single narrative template (Two Worlds > Meeting > Adventure > Proposal > Tomorrow). The Cinematic Pipeline doc mentions memorial, birthday, and travel templates but they are not implemented. Tutorial-video has no narrative structure beyond linear steps. Ad-video uses Hook > Problem > Solution > CTA which is one framework of many.
- **Description:** Build a `NarrativeFramework` library with templates beyond the 5-act wedding structure: (1) Hero's Journey (12 stages, mapped to video acts). (2) Dan Harmon Story Circle (8 beats). (3) Pixar Story Spine ("Once upon a time... Every day... One day... Because of that..."). (4) Before/After/Bridge (for ads and testimonials). (5) Problem/Agitate/Solve (for ad-video). (6) Inverted Pyramid (for tutorial-video — conclusion first, then details). Each framework maps to: act count, emotion per act, pacing profile, suggested color grades, and transition styles. Users select a framework in config and the narrative engine applies it.
- **User story:** As a memorial video creator, I want to select the "Hero's Journey" narrative framework so that the video follows a proven emotional arc without me designing the structure from scratch.
- **Effort:** M
- **Dependencies:** Narrative engine (feature #11 from Cinematic Pipeline doc)
- **Which skills benefit:** wedding-video (memorial, birthday, travel templates), ad-video (PAS, BAB frameworks), tutorial-video (inverted pyramid)

---

#### 27. Clippkit Scene Templates

- **Name:** Pre-Built Scene Templates
- **Source:** Clippkit (clippkit.com) — scene templates, text animations, audio waveforms, card flip
- **Problem:** Every video starts from a blank composition. Users must design each scene's layout, animation, and timing from scratch. Clippkit offers pre-built scene templates (text reveal scenes, product showcase scenes, testimonial cards) that can be dropped into a composition and customized.
- **Description:** Integrate Clippkit's template library as an additional scene source. Pull templates for: glitch text (social-clip hooks), typing text (tutorial-video code reveals), popping text (ad-video feature highlights), card flip (ad-video before/after comparisons), audio waveform scenes (social-clip music content). Each template is a self-contained Remotion component that accepts customization props (colors, text, timing). Users reference templates by name in config: `{ type: 'template', template: 'glitch-text-reveal', text: 'Stop Scrolling' }`.
- **User story:** As a social clip creator, I want to use a pre-built glitch text template for my hook so that I get a polished result without designing the animation from scratch.
- **Effort:** M
- **Dependencies:** Clippkit package or manual recreation of templates
- **Which skills benefit:** social-clip (hook templates), ad-video (product showcase, testimonial cards), tutorial-video (intro/outro templates)

---

#### 28. 3-Agent Architecture (Director / Media Scout / Post-Producer)

- **Name:** Multi-Agent Production Pipeline
- **Source:** Remotion Superpowers architecture pattern
- **Problem:** Currently, video creation is a linear pipeline: write config, gather assets, generate composition, render. There is no intelligence in asset selection, no automated feedback loop, and no orchestration across the production stages. The user must manually decide which photos to use, which transitions fit, and whether the result is good.
- **Description:** Implement a 3-agent architecture: (1) **Director Agent** reads the brief/config, selects the narrative framework, assigns scenes to acts, chooses transitions and effects, and writes the full Remotion composition spec. (2) **Media Scout Agent** takes the director's asset requirements and finds/generates media: searches Pexels for stock, calls fal.ai for AI clips, selects from the user's photo library using manifest weights, and generates voiceover/music. (3) **Post-Producer Agent** renders the video, runs it through TwelveLabs review, scores quality, and iterates (adjusting pacing, swapping weak scenes, re-grading) until the quality score passes threshold. Each agent is a Claude Code skill invocation with structured output, composable into a single `/produce` command.
- **User story:** As a video creator, I want to run `/produce wedding` and have three AI agents collaboratively direct, source assets, and quality-check my video so that I get a polished result with minimal manual intervention.
- **Effort:** XL
- **Dependencies:** Features #18 (fal.ai), #20 (TwelveLabs review), #25 (quality scoring), all HIGH-priority package integrations
- **Which skills benefit:** all 4 skills (meta-architecture that orchestrates any skill)

---

## Theme Summary

| Priority | Count | Total Effort | Key Theme |
|----------|-------|-------------|-----------|
| HIGH | 14 | 6S + 6M + 2L | Integrate existing npm packages we already pay for in the Remotion ecosystem. Zero invention, pure wiring. |
| MEDIUM | 10 | 2S + 7M + 1L | Producer intelligence features that require building logic on top of existing tools and services. |
| LOW | 4 | 1M + 2L + 1XL | Advanced automation, narrative theory, and multi-agent orchestration. |

**Estimated total:** 14 HIGH features deliverable in ~3 weeks. 10 MEDIUM features in ~4 weeks. 4 LOW features in ~4 weeks.

---

## Recommended Build Order

### Phase 1: Drop-In Package Integrations (1 week)

These require only `npm install` + component wiring. No new tools or services.

1. **Google Fonts** (#6) — S effort, fixes font loading across all 4 skills immediately.
2. **Declarative Animation Chaining** (#13) — S effort, simplifies all generated composition code.
3. **GIF Sync** (#11) — S effort, unlocks GIF content in social-clip.
4. **Geometric Shapes** (#12) — S effort, adds diagram/chart primitives.
5. **Audio Waveform Visualizer** (#14) — S effort, adds audio visualization to social-clip.
6. **Light Leak Transitions** (#1) — S effort, dramatically improves wedding act transitions.
7. **Motion Blur** (#2) — S effort, improves all moving element quality.
8. **Animated Text (Remotion Bits)** (#8) — S effort, complements existing KineticText.

### Phase 2: Package Integrations Requiring Component Work (1.5 weeks)

These require building components on top of the packages.

9. **Procedural Film Grain** (#3) — M effort, replaces CSS grain in wedding-video.
10. **SVG Path Animation** (#4) — M effort, unlocks animated diagrams in tutorial-video.
11. **Smart Text Fitting** (#5) — M effort, fixes text overflow across all skills.
12. **GLSL Shader Transitions** (#7) — M effort, massive transition library expansion.
13. **Particle System Upgrade** (#9) — M effort, replaces div particles in wedding-video.
14. **Lottie/Rive Animation** (#10) — M effort, enables animated logos and icons.

### Phase 3: Producer Intelligence (2 weeks)

These require building tools and integrating external services.

15. **Loudness Normalization** (#16) — S effort, quick FFmpeg integration.
16. **Audio Ducking** (#15) — M effort, uses existing whisper.cpp.
17. **LUT Color Grading** (#17) — M effort, replaces CSS filters in wedding-video.
18. **Local Whisper Standardization** (#22) — M effort, unifies transcription across all skills.
19. **Platform Encoding Profiles** (#24) — M effort, optimizes output per platform.
20. **Edit Pacing Engine** (#23) — M effort, adds intelligent cut rhythm.

### Phase 4: AI Service Integrations (2 weeks)

These require new API keys and service integrations.

21. **fal.ai Video Generation** (#18) — M effort, new API integration.
22. **Suno AI Music** (#19) — M effort, new API integration.
23. **TwelveLabs Review Loop** (#20) — L effort, new API integration + review pipeline.

### Phase 5: Advanced Features (3+ weeks)

24. **Three.js 3D Rendering** (#21) — L effort, significant new capability.
25. **Quality Scoring** (#25) — L effort, analysis pipeline.
26. **Narrative Frameworks** (#26) — M effort, content library.
27. **Clippkit Templates** (#27) — M effort, template integration.
28. **3-Agent Architecture** (#28) — XL effort, orchestration system.

---

## Next Steps

1. **Run `npm install` for Phase 1 packages** in the video-toolkit workspace:
   ```bash
   cd ~/.openclaw/workspace/claude-code-video-toolkit
   npm install @remotion/light-leaks @remotion/motion-blur @remotion/noise \
     @remotion/paths @remotion/shapes @remotion/layout-utils @remotion/google-fonts \
     @remotion/lottie @remotion/rive @remotion/gif @remotion/three \
     remotion-animated remotion-audio-visualizers
   npx remotion-bits fetch AnimatedText ParticleSystem StaggeredMotion
   ```

2. **Run `/spec producer-grade-phase1`** to generate an engineering spec for Phase 1 (drop-in packages).

3. **Run `/spec audio-ducking`** to generate an engineering spec for the audio ducking system.

4. **Run `/spec lut-grading`** to generate an engineering spec for LUT-based color grading.

5. **Sign up for API keys** needed for Phase 4:
   - fal.ai: https://fal.ai (single key for all video models)
   - Suno via KIE: for music with vocals
   - TwelveLabs: https://twelvelabs.io (free tier for review loop)

6. **Curate LUT files** for the color grading system — source free .cube files for the 6 presets (Portra 400, Pro 400H, Ektar 100, Teal-Orange, Bleach Bypass, Moonlight).
