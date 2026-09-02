---
name: wedding-video
description: "Create cinematic wedding montage videos from photos and songs using Remotion."
version: "1.0.1"
category: build
platforms:
  - CLAUDE_CODE
permissions:
  - filesystem
  - shell
  - network
---

# Wedding Video

Create cinematic wedding montage videos from personal photos and songs. Describe your love story in a structured config and render a professional montage with act-based narrative, Ken Burns animations, beat-synced editing, and cinematic effects.

## Prerequisites

- video-toolkit installed (`~/.openclaw/workspace/claude-code-video-toolkit`)
- Node.js 18+
- Python 3.10+ with pip
- FFmpeg + FFprobe installed

## Setup

### Step 1: Install Python Dependencies

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
pip3 install --break-system-packages librosa numpy soundfile Pillow imagehash piexif
```

### Step 2: Create Project

```bash
cd $TOOLKIT
cp -r templates/wedding-montage projects/MY_WEDDING
cd projects/MY_WEDDING
npm install
```

## Creating a Wedding Video

### Step 1: Organize Photos

Drop photos into `public/photos/` organized by category:

```
public/photos/
  childhood-a/       # Person A childhood/family
  childhood-b/       # Person B childhood/family
  relationship/      # Couple photos (dating, milestones)
  trips/             # Adventures, travel
  family/            # Family and friends
  proposal/          # Proposal/engagement photos
```

Or use the auto-import tool:

```bash
cd $TOOLKIT
python3 tools/photo_import.py \
  --input ~/Photos/wedding/ \
  --output projects/MY_WEDDING/public/photos/ \
  --config projects/MY_WEDDING/src/config/photos.json
```

The import tool handles EXIF date sorting, blur detection, duplicate removal via perceptual hashing, and organized directory output.

### Step 2: Add Songs

```bash
cp ~/Music/slow-song.mp3 projects/MY_WEDDING/public/audio/song-1.mp3
cp ~/Music/upbeat-song.mp3 projects/MY_WEDDING/public/audio/song-2.mp3
```

### Step 3: Detect Beats

```bash
cd $TOOLKIT
python3 tools/beat_detect.py \
  --input projects/MY_WEDDING/public/audio/song-1.mp3 \
  --output projects/MY_WEDDING/public/beats/song-1-beats.json

python3 tools/beat_detect.py \
  --input projects/MY_WEDDING/public/audio/song-2.mp3 \
  --output projects/MY_WEDDING/public/beats/song-2-beats.json
```

Beat detection uses librosa to extract beats, downbeats, BPM, and energy segments. The output JSON drives automatic photo placement on musical beats during high-energy acts.

### Step 4: Edit Config

Edit `src/config/wedding-config.ts`:

```typescript
import { WeddingConfig } from './types';

export const weddingConfig: WeddingConfig = {
  meta: {
    personA: 'Gina',
    personB: 'Tho',
    weddingDate: '2026-10-17',
    titleCard: {
      headline: 'Gina & Tho',
      subheadline: 'October 17, 2026',
      durationSeconds: 6,
    },
    endCard: {
      headline: 'Forever starts now',
      durationSeconds: 8,
    },
  },
  acts: [
    {
      id: 'two-worlds',
      title: 'Two Worlds',
      subtitle: 'Before they met',
      emotion: 'nostalgic',
      pacing: 'slow',
      colorGrade: 'warm-nostalgic',
      durationSeconds: 60,
      scenes: [
        {
          id: 'childhood-gina',
          type: 'photo',
          photos: [
            { src: 'photos/childhood-a/photo1.jpg' },
            { src: 'photos/childhood-a/photo2.jpg' },
          ],
          kenBurns: { motion: 'zoom-in' },
        },
        {
          id: 'childhood-tho',
          type: 'split-screen',
          photos: [
            { src: 'photos/childhood-a/teen.jpg' },
            { src: 'photos/childhood-b/teen.jpg' },
          ],
        },
      ],
      effects: { filmGrain: true, vignette: true },
      textOverlays: [
        {
          text: 'Two worlds apart...',
          position: 'bottom',
          style: { fontSize: 36, fontFamily: 'Playfair Display' },
          startSeconds: 5,
          durationSeconds: 4,
          animation: 'fade',
        },
      ],
    },
    {
      id: 'meeting',
      title: 'The Meeting',
      emotion: 'joyful',
      pacing: 'moderate',
      colorGrade: 'natural',
      durationSeconds: 45,
      scenes: [/* photo scenes */],
      transition: { type: 'fade-to-black', durationSeconds: 1.5 },
    },
    {
      id: 'adventure',
      title: 'The Adventure',
      emotion: 'energetic',
      pacing: 'fast',
      colorGrade: 'vibrant-adventure',
      durationSeconds: 75,
      scenes: [/* beat-synced photo montage */],
      effects: { particles: { type: 'confetti', density: 0.3 } },
    },
    {
      id: 'proposal',
      title: 'The Proposal',
      emotion: 'romantic',
      pacing: 'slow-dramatic',
      colorGrade: 'soft-cinematic',
      durationSeconds: 50,
      scenes: [/* proposal/engagement photos */],
      effects: { letterbox: true, depthBlur: true },
    },
    {
      id: 'tomorrow',
      title: 'Tomorrow',
      emotion: 'grateful',
      pacing: 'uplifting',
      colorGrade: 'golden-sunset',
      durationSeconds: 50,
      scenes: [
        { id: 'mosaic', type: 'mosaic', photos: [/* all favorites */] },
      ],
      effects: { particles: { type: 'golden-rain', density: 0.5 } },
    },
  ],
  audio: {
    tracks: [
      {
        id: 'slow-song',
        src: 'audio/song-1.mp3',
        startSeconds: 0,
        endSeconds: 132,
        fadeIn: 2,
        beatSyncEnabled: false,
        beatsFile: 'beats/song-1-beats.json',
      },
      {
        id: 'upbeat-song',
        src: 'audio/song-2.mp3',
        startSeconds: 132,
        fadeOut: 4,
        beatSyncEnabled: true,
        beatsFile: 'beats/song-2-beats.json',
        transition: { type: 'whoosh', sfxFile: 'audio/sfx/whoosh.mp3' },
      },
    ],
  },
  output: {
    formats: [
      { id: 'landscape', width: 1920, height: 1080, name: '16:9 Landscape' },
    ],
    fps: 30,
    quality: 'high',
  },
};
```

### Step 5: Validate

```bash
cd $TOOLKIT
python3 tools/validate_config.py \
  --config projects/MY_WEDDING/src/config/wedding-config.ts
```

Checks file existence for all referenced photos and audio, timing consistency (act durations vs total audio), and config completeness.

### Step 6: Preview

```bash
cd $TOOLKIT/projects/MY_WEDDING
npm start
```

Opens Remotion Studio. Preview individual acts or the full montage in the browser. Use this to check pacing, transitions, and color grading before committing to a full render.

### Step 7: Render

```bash
cd $TOOLKIT/projects/MY_WEDDING
npx remotion render WeddingMontage out/wedding.mp4
```

Output: `out/wedding.mp4`

### Step 8: Social Media Export

```bash
# TikTok/Reels (9:16)
ffmpeg -i out/wedding.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:a copy out/wedding-tiktok.mp4

# Instagram Square (1:1)
ffmpeg -i out/wedding.mp4 \
  -vf "crop=ih:ih:(iw-ih)/2:0,scale=1080:1080" \
  -c:a copy out/wedding-square.mp4

# YouTube (16:9, already native -- just add faststart)
ffmpeg -i out/wedding.mp4 -c copy -movflags +faststart out/wedding-youtube.mp4
```

## Asset Manifest

Each asset (photo or video) gets a manifest entry in the config. This tells the skill what the asset contains, how important it is, and where it should appear. Instead of manually placing every photo into acts and scenes, annotate your assets and let the skill auto-place them based on tags, emotion, people, and weight.

```typescript
interface AssetEntry {
  path: string;                    // relative path to file
  type: 'photo' | 'video';
  description: string;             // what's in this asset — Claude uses this for placement
  tags: string[];                  // searchable tags: ['childhood', 'gina', 'kansas-city']
  people: string[];                // who's in it: ['gina', 'tho', 'bear']
  weight: 1 | 2 | 3 | 4 | 5;     // importance: 1=filler, 3=good, 5=hero moment
  emotion: string;                 // emotional tone: 'nostalgic', 'joyful', 'intimate', 'triumphant'
  act?: string;                    // force into specific act: 'two-worlds', 'adventure', etc.
  duration?: number;               // suggested screen time in seconds (higher weight = longer)
  kenBurns?: 'zoom-in' | 'zoom-out' | 'pan-left' | 'pan-right' | 'drift';
  notes?: string;                  // special instructions: "this is THE proposal moment"
}

interface AssetManifest {
  assets: AssetEntry[];
  defaults: {
    weight: number;                // default weight for unweighted assets
    durationByWeight: {            // screen time mapping
      1: number; // 2s — filler
      2: number; // 3s — supporting
      3: number; // 4s — standard
      4: number; // 5s — featured
      5: number; // 7s — hero moment
    };
  };
}
```

### How Weights Work

| Weight | Role | Screen Time | Position | Effects |
|--------|------|-------------|----------|---------|
| 5 — Hero | The defining moment | 6-8s | Beat drop, act climax, or finale | Slow zoom, full frame, extra glow |
| 4 — Featured | Key memory | 4-6s | Act transitions, emotional peaks | Ken Burns with gentle effects |
| 3 — Standard | Good photo | 3-4s | Regular sequence | Standard Ken Burns |
| 2 — Supporting | Context/filler | 2-3s | Montage sequences, fast cuts | Quick cuts in beat-synced sections |
| 1 — Background | Nice but not essential | 1-2s | Only if needed to fill time | Flash in montage or mosaic grid |

### Smart Placement Rules

The skill uses tags, emotion, people, and description to auto-place assets:
- Assets tagged `childhood` + person → Act 1 (Two Worlds), placed on the correct side of split-screen
- Assets tagged `relationship` + `early` → Act 2 (Denver/Meeting)
- Assets tagged `trip` or `adventure` → Act 3 (Adventure), beat-synced montage
- Assets tagged `proposal` or emotion `intimate` → Act 4 (The Question)
- Assets tagged `family` or `group` → Act 5 (Tomorrow)
- `weight: 5` assets get placed at the emotional peak of their assigned act
- `weight: 1-2` assets fill the beat-synced montage in Act 3

### Example Manifest

```typescript
const assets: AssetManifest = {
  assets: [
    {
      path: 'photos/gina-childhood-01.jpg',
      type: 'photo',
      description: 'Gina as a toddler in Kansas City backyard',
      tags: ['childhood', 'kansas-city'],
      people: ['gina'],
      weight: 3,
      emotion: 'nostalgic',
      act: 'two-worlds',
    },
    {
      path: 'photos/proposal-moment.jpg',
      type: 'photo',
      description: 'The exact moment Tho proposed — Gina crying happy tears',
      tags: ['proposal'],
      people: ['gina', 'tho'],
      weight: 5,
      emotion: 'intimate',
      act: 'the-question',
      kenBurns: 'zoom-in',
      notes: 'THE hero shot. Hold this for 7+ seconds at the act climax.',
    },
    {
      path: 'photos/bear-hiking.jpg',
      type: 'photo',
      description: 'Bear on the hiking trail with mountains behind',
      tags: ['adventure', 'bear', 'outdoors'],
      people: ['bear'],
      weight: 2,
      emotion: 'joyful',
    },
    {
      path: 'videos/first-dance-clip.mp4',
      type: 'video',
      description: '8 second clip of first dance practice in living room',
      tags: ['relationship', 'dancing'],
      people: ['gina', 'tho'],
      weight: 4,
      emotion: 'intimate',
      duration: 5,
    },
  ],
  defaults: {
    weight: 3,
    durationByWeight: { 1: 2, 2: 3, 3: 4, 4: 5, 5: 7 },
  },
};
```

### Quick Asset Annotation

For users who don't want to write full manifest entries, support a shorthand CSV:

```
path,weight,tags,act,notes
photos/gina-kid-01.jpg,3,childhood;gina,two-worlds,
photos/proposal.jpg,5,proposal,the-question,THE moment
photos/denver-cafe.jpg,4,relationship;early,denver,where they met
videos/bear-park.mp4,2,adventure;bear,,
```

Generate a starter manifest from existing photos using EXIF data and basic image analysis:

```bash
cd $TOOLKIT
python3 tools/generate_manifest.py --dir photos/ --output manifest.csv
```

## Five-Act Structure

The default wedding narrative follows five emotional acts:

| Act | Emotion | Pacing | Color Grade | Typical Duration |
|-----|---------|--------|-------------|-----------------|
| Two Worlds | Nostalgic | Slow (4-6s/photo) | Warm Nostalgic | 45-75s |
| The Meeting | Joyful | Moderate (3-4s/photo) | Natural | 30-50s |
| The Adventure | Energetic | Fast, beat-synced (1-2s/photo) | Vibrant Adventure | 60-90s |
| The Proposal | Romantic | Slow-dramatic (5-8s/photo) | Soft Cinematic | 40-60s |
| Tomorrow | Grateful | Uplifting, building | Golden Sunset | 40-60s |

Customize any act or add/remove acts. The structure is a starting point -- not a constraint.

## Color Grade Presets

| Preset | Look | Best For |
|--------|------|----------|
| `warm-nostalgic` | Warm, slightly desaturated, touch of sepia | Childhood, memories |
| `vibrant-adventure` | High contrast, saturated | Travel, energy |
| `soft-cinematic` | Soft, low contrast, warm | Romance, proposals |
| `golden-sunset` | Golden overlay, warm tones | Finale, celebration |
| `cool-dramatic` | Cool, high contrast | Drama, tension |
| `vintage-film` | Heavy sepia, desaturated | Retro looks |
| `noir` | High contrast, fully desaturated | B&W drama |
| `pastel-dream` | Bright, low contrast, soft pastels | Dreamy, ethereal |
| `natural` | No grading | When photos speak for themselves |

Color grades are applied via CSS filters on the `<ColorGrade>` wrapper component. They support interpolated transitions between acts so grade changes feel cinematic rather than abrupt.

## Ken Burns Motions

| Motion | Effect |
|--------|--------|
| `zoom-in` | Slowly zoom into center |
| `zoom-out` | Slowly zoom out from center |
| `pan-left` | Pan left with slight zoom |
| `pan-right` | Pan right with slight zoom |
| `pan-up` | Slow pan up with slight zoom |
| `pan-down` | Slow pan down with slight zoom |
| `drift` | Gentle diagonal movement |
| `random` | Varies per photo (deterministic seed for render consistency) |

All Ken Burns animations use Remotion's `interpolate()` with `Easing.bezier()` curves. Never CSS transitions or `@keyframes`. The `<KenBurnsPhoto>` component accepts `motion`, `scale`, and custom `startPosition`/`endPosition` overrides.

## Beat-Synced Editing

The `<BeatSyncedMontage>` component reads beat JSON from librosa and auto-places photos on beat boundaries:

1. **Beat detection** extracts beat timestamps, downbeats, BPM, and energy per segment.
2. **Energy-aware pacing** -- high-energy segments get faster cuts (every beat), low-energy segments hold photos for 2-4 beats.
3. **Downbeat emphasis** -- scene transitions align with downbeats (bar boundaries) for stronger visual rhythm.
4. **Minimum hold time** -- set `minPhotoFrames` to prevent cuts from being too fast (floor on beat-driven duration).
5. **Photo ordering** preserves config order by default. Set `shuffle: true` for randomized placement.

Enable beat sync only for high-energy acts (Adventure). Slow acts with beat sync feel jarring.

## Multi-Song Audio

The `<AudioTrack>` component handles multiple songs with precise timing:

- **Start/end offsets** -- trim songs to specific sections via `startSeconds`/`endSeconds`.
- **Fade in/out** -- smooth volume interpolation at song boundaries.
- **Crossfade** -- overlap two songs with volume ramps for seamless transitions.
- **Hard cut with SFX** -- whoosh, impact, or reverse-cymbal between songs.
- **Volume curves** -- per-track volume envelopes via Remotion's `interpolate()`.
- **Master volume** -- global `masterVolume` control on the `audio` config (default 1.0).

Song transitions should align with act boundaries. Map each act to the appropriate song segment in the config.

## Effects

All effects are composable and applied per-act via the `effects` config property:

- **Film Grain** -- Use `@remotion/noise` `noise2D()`/`noise3D()` for procedural grain with configurable intensity (0.0-1.0). Deterministic seeded noise for render consistency.
- **Vignette** -- Darkened edges with configurable spread and intensity. Draws focus to center.
- **Letterbox** -- Cinematic 2.35:1 black bars. Applied as absolute-positioned overlays.
- **Particles** -- Six types: `confetti`, `golden-rain`, `sparkles`, `snow`, `bokeh`, `dust`. Use Remotion Bits ParticleSystem (`npx remotion-bits find ParticleSystem`) for confetti and golden-rain. Each has `density` (0.0-1.0) and `speed` controls.
- **Depth Blur** -- Simulated depth of field via backdrop-filter blur with mask options.
- **Split Screen** -- 2, 3, or 4 photos side by side with configurable gap and animation.

Stack multiple effects: `{ filmGrain: true, vignette: true, letterbox: true }`.

## Component Architecture

```
WeddingMontage (top-level composition)
  TitleCard
  WeddingAct (per act)
    ColorGrade (wraps entire act)
    WeddingScene (per scene)
      KenBurnsPhoto | SplitScreen | PhotoMosaic | BeatSyncedMontage | VideoClip | TextOnly
      TextOverlay (optional, per scene)
    FilmGrain | Vignette | Letterbox | Particles | DepthBlur (effects layer)
  ActTransition (between acts: fade-to-black, crossfade, title-card, whoosh-cut, @remotion/light-leaks, GL Transitions)
  AudioTrack (multi-song with beat data)
  EndCard
```

All components use Remotion primitives: `useCurrentFrame()`, `useVideoConfig()`, `interpolate()`, `spring()`, `staticFile()`, `<Sequence>`, `<Audio>`, `<Img>`. Never CSS animations, `setTimeout`, or `requestAnimationFrame`.

## Remotion Ecosystem Packages

Install the official Remotion skills for best results: `npx skills i remotion-dev/skills/skills/remotion`. This provides 35 production rules covering animations, audio, transitions, text, 3D, and more.

### Core Packages

| Package | What it does |
|---------|-------------|
| `@remotion/transitions` | fade, slide, wipe, flip, clockWipe, iris |
| `@remotion/captions` | TikTok-style word-by-word captions |
| `@remotion/media-utils` | `visualizeAudio()`, `getAudioData()`, `getAudioDurationInSeconds()` |
| `@remotion/layout-utils` | `measureText()`, `fitText()`, `fillTextBox()` |
| `@remotion/light-leaks` | WebGL light leak overlays — use for act transitions instead of fade-to-black |
| `@remotion/motion-blur` | `<Trail>` and `<CameraMotionBlur>` — use for slow-mo proposal moments |
| `@remotion/noise` | Procedural noise — use `noise2D()`/`noise3D()` for film grain instead of CSS overlay |
| `@remotion/google-fonts` | Google Fonts loading |
| `@remotion/shapes` | Geometric shape components |
| `@remotion/paths` | SVG path animation |
| `remotion-animated` | Declarative `<Animated>` with `Move()`, `Scale()`, `Fade()` |

### Community Packages

| Package | What it does |
|---------|-------------|
| **Remotion Bits** (`npx remotion-bits find/fetch`) | ParticleSystem (confetti, golden rain, starfields), AnimatedText (char/word/line stagger), StaggeredMotion — use ParticleSystem instead of custom CSS particles |
| **GL Transitions** (`remotion-gl-transitions`) | Hundreds of GLSL shader transitions from gl-transitions.com — use for cinematic dissolves between acts |
| **remotion-confetti** | Canvas-based confetti with physics |

### AI Services

| Service | What it does | Cost |
|---------|-------------|------|
| **fal.ai** | Single API for video gen (Veo 3.1, Kling 3, Wan 2.2). One key, all models | $0.05-0.50/sec |
| **whisper.cpp** | LOCAL speech-to-text, zero cost. Use for caption generation | Free |
| **Suno** (via KIE) | AI music with vocals — custom wedding songs with lyrics | $0.03/song |

### Producer Intelligence

**Audio ducking:** Auto-lower music volume when voiceover speaks. Use Remotion's `interpolate()` on volume based on voiceover audio presence. Essential for wedding videos with narration over music.

**Loudness normalization:** Target LUFS per platform: YouTube -14, TikTok -14, Instagram -14, Podcast -16. Post-process:
```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 output.mp4
```

**Film grain via `@remotion/noise`:** Use `noise2D()` or `noise3D()` for procedural film grain instead of CSS overlay. Renders consistently across frames with deterministic seeds.

**Light leaks via `@remotion/light-leaks`:** WebGL overlays for transitions between acts/scenes. Use instead of fade-to-black between upbeat acts.

## Remotion Rules

These rules apply to ALL Remotion code in this project:

1. **Always use `staticFile()`** for assets in `public/`. Never relative paths.
2. **Always use `<Img>`** from `remotion`, never `<img>`.
3. **Always use `<OffthreadVideo>`** for video clips, never `<video>`.
4. **Never use CSS animations or transitions.** Use `interpolate()` and `spring()` only.
5. **Never use `useEffect` for animation.** Derive everything from `useCurrentFrame()`.
6. **Never use `Math.random()`.** Use deterministic seeded random for render consistency.
7. **Import transitions from specific paths**, not barrel exports: `import { fade } from '@remotion/transitions/fade'`.

## Scene Types

| Type | Description |
|------|-------------|
| `photo` | Single photo with Ken Burns animation |
| `split-screen` | 2, 3, or 4 photos side by side |
| `mosaic` | Grid of photos with staggered entrance |
| `video-clip` | Short video clip (use `<OffthreadVideo>`) |
| `text-only` | Full-screen text card (no photo) |
| `blank` | Empty scene for spacing or manual composition |

## Cost Estimate

| Item | Cost | Notes |
|------|------|-------|
| Local Remotion render | $0 | 10-20 min for a 5-min video on M1 Mac |
| Beat detection (local) | $0 | librosa runs locally, ~5s per song |
| Photo import (local) | $0 | All local processing |
| **Total (local pipeline)** | **$0** | All processing is local |

## Tips

1. **Photo count:** 40-80 photos for a 4-6 minute video. More photos means faster pacing.
2. **Song length:** Total song duration should roughly match total video duration.
3. **Beat sync:** Enable only for high-energy acts. Slow acts with beat sync feel jarring.
4. **Preview often.** Use `npm start` to check pacing in Remotion Studio before full render.
5. **Photo quality:** 1920x1080 minimum. Larger is fine -- Remotion scales down.
6. **Text overlays:** Less is more. 3-5 text moments across the whole video.
7. **Act transitions:** Use fade-to-black between emotional shifts, `@remotion/light-leaks` between upbeat acts, GL Transitions for cinematic dissolves.
8. **Render time:** Expect 10-20 minutes for a 5-minute video on an M1 Mac.
