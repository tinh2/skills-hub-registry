# Engineering Spec: `/wedding-video` Skill

> Version: 1.0.0 | Author: Tho Le | Date: 2026-03-26
> Status: Draft

---

## 1. Overview

### What it does

The `/wedding-video` skill generates cinematic wedding montage videos from personal photos and songs using Remotion (React). The user provides a structured config containing photos organized by life chapter, song files with transition timestamps, names, date, and text overlays. The skill produces a complete Remotion project with act-based narrative structure, Ken Burns photo animations, multi-song audio with beat-synced cuts, cinematic color grading, film effects, and social media format exports.

### Target user

Developers and technical creators preparing wedding or anniversary videos who want cinematic quality without hiring a videographer or learning Premiere/Final Cut. Comfortable with the terminal and JSON/TypeScript config files.

### Value prop

- **Config to film in minutes.** Describe your wedding story in a structured config, get a 4-6 minute cinematic montage rendered as MP4.
- **Act-based emotional storytelling.** Five-act narrative structure (Two Worlds, Meeting, Adventure, Proposal, Tomorrow) with automatic pacing, color grading, and effect selection per act. No competitor offers this (0/6).
- **Beat-synced editing.** High-energy acts automatically cut photos on musical beats via librosa analysis. The difference between slideshow and film.
- **Multi-format export.** One config renders to 16:9 landscape, 9:16 TikTok/Reels, and 1:1 square.
- **Full control.** Every frame is a React component. Override any default with custom Remotion code.

### Relationship to existing skills

| Skill | Relationship |
|-------|-------------|
| `video-toolkit` | Foundation. Wedding-video extends its project structure, rendering pipeline, and Modal GPU endpoints. Does NOT duplicate voiceover/image-gen/talking-head features. |
| `remotion` | Reference skill for Remotion patterns. Wedding-video follows all Remotion conventions from this skill (staticFile, interpolate, spring, OffthreadVideo, no CSS animations). |
| `ffmpeg-media` | Post-processing. Used for social media format conversion, audio normalization, and final compression after Remotion render. |

---

## 2. Architecture

### System diagram

```
User Config (wedding-config.ts)
        |
        v
+-------------------+     +--------------------+
| tools/            |     | src/               |
| beat_detect.py    |---->| components/        |
| photo_import.py   |     |   KenBurnsPhoto    |
| validate_config.py|     |   FilmGrain        |
+-------------------+     |   Vignette         |
                          |   Letterbox        |
                          |   Particles        |
                          |   SplitScreen      |
                          |   DepthBlur        |
                          |   TextOverlay      |
                          |   PhotoMosaic      |
                          |   ColorGrade       |
                          |   BeatSyncedMontage|
                          |                    |
                          | compositions/      |
                          |   WeddingMontage   |
                          |   WeddingAct       |
                          |   WeddingScene     |
                          |                    |
                          | config/            |
                          |   wedding-config.ts|
                          |   acts.ts          |
                          |   color-grades.ts  |
                          |   effects.ts       |
                          +--------------------+
                                    |
                                    v
                          npx remotion render
                                    |
                                    v
                          out/WeddingMontage.mp4
                                    |
                                    v
                          ffmpeg social exports
                          (9:16, 1:1, 16:9)
```

### Directory structure

```
~/.openclaw/workspace/claude-code-video-toolkit/
  templates/
    wedding-montage/           <-- NEW template
      package.json
      tsconfig.json
      remotion.config.ts
      src/
        index.ts               <-- RemotionRoot with compositions
        config/
          wedding-config.ts    <-- User edits this
          acts.ts              <-- Act definitions and defaults
          color-grades.ts      <-- Color grade presets
          effects.ts           <-- Effect presets per act
          types.ts             <-- TypeScript interfaces
        compositions/
          WeddingMontage.tsx   <-- Top-level composition
          WeddingAct.tsx       <-- Single act renderer
          WeddingScene.tsx     <-- Single scene (photo + effects)
        components/
          KenBurnsPhoto.tsx
          FilmGrain.tsx
          Vignette.tsx
          Letterbox.tsx
          Particles.tsx
          SplitScreen.tsx
          DepthBlur.tsx
          TextOverlay.tsx
          PhotoMosaic.tsx
          ColorGrade.tsx
          BeatSyncedMontage.tsx
          AudioTrack.tsx
        lib/
          timing.ts            <-- Frame/time calculations
          beat-sync.ts         <-- Beat JSON reader + frame mapper
      public/
        photos/                <-- User drops photos here
          childhood-a/
          childhood-b/
          relationship/
          trips/
          family/
          proposal/
        audio/
          song-1.mp3
          song-2.mp3
          sfx/
            whoosh.mp3
            impact.mp3
        beats/
          song-1-beats.json    <-- Generated by beat_detect.py
          song-2-beats.json
  tools/
    beat_detect.py             <-- NEW
    photo_import.py            <-- NEW
    validate_config.py         <-- NEW
```

### New components vs reusable library

All components under `src/components/` are designed as standalone, reusable Remotion components with their own props interfaces. They can be extracted into a shared `@skills-hub/remotion-effects` package later for use by `/social-clip`, `/tutorial-video`, and `/ad-video` skills.

---

## 3. Data Model

### WeddingConfig (top-level)

```typescript
// src/config/types.ts

export interface WeddingConfig {
  meta: WeddingMeta;
  acts: WeddingAct[];
  audio: AudioConfig;
  output: OutputConfig;
}

export interface WeddingMeta {
  personA: string;                    // "Gina"
  personB: string;                    // "Tho"
  weddingDate: string;               // "2026-10-17"
  tagline?: string;                   // "Two worlds, one story"
  titleCard?: {
    headline: string;                 // "Gina & Tho"
    subheadline?: string;            // "October 17, 2026"
    durationSeconds: number;          // 6
  };
  endCard?: {
    headline: string;                 // "Forever starts now"
    subheadline?: string;
    durationSeconds: number;
  };
}

export interface WeddingAct {
  id: string;                         // "two-worlds" | "meeting" | "adventure" | "proposal" | "tomorrow"
  title: string;                      // "Two Worlds"
  subtitle?: string;                  // "Before they met"
  emotion: ActEmotion;
  pacing: ActPacing;
  colorGrade: ColorGradePreset;
  durationSeconds: number;            // Total act duration
  scenes: WeddingScene[];
  effects?: ActEffects;
  transition?: ActTransition;         // Transition INTO this act
  textOverlays?: TextOverlay[];
}

export type ActEmotion =
  | 'nostalgic'
  | 'joyful'
  | 'intimate'
  | 'energetic'
  | 'triumphant'
  | 'grateful'
  | 'romantic'
  | 'bittersweet';

export type ActPacing =
  | 'slow'            // 4-6s per photo
  | 'moderate'        // 3-4s per photo
  | 'building'        // starts slow, accelerates
  | 'fast'            // 1-2s per photo (beat-synced)
  | 'slow-dramatic'   // 5-8s per photo with long dissolves
  | 'uplifting';      // moderate with energy build

export interface WeddingScene {
  id: string;
  type: 'photo' | 'split-screen' | 'mosaic' | 'video-clip' | 'text-only' | 'blank';
  photos?: PhotoEntry[];
  videoClip?: string;                 // path to video file
  kenBurns?: KenBurnsConfig;
  durationSeconds?: number;           // Override auto-calculated duration
  textOverlay?: TextOverlay;
  transition?: SceneTransition;
}

export interface PhotoEntry {
  src: string;                        // "photos/childhood-a/baby-gina.jpg"
  alt?: string;                       // Accessibility description
  kenBurns?: KenBurnsConfig;          // Per-photo override
  cropFocus?: { x: number; y: number }; // 0-1 normalized focal point
}

export interface KenBurnsConfig {
  motion: KenBurnsMotion;
  startScale?: number;                // default 1.0
  endScale?: number;                  // default 1.15
  startPosition?: { x: number; y: number }; // 0-1 normalized
  endPosition?: { x: number; y: number };
  easing?: 'linear' | 'ease-in-out' | 'ease-out'; // default ease-in-out
}

export type KenBurnsMotion =
  | 'zoom-in'        // Slowly zoom into center
  | 'zoom-out'       // Slowly zoom out from center
  | 'pan-left'       // Slow pan left with slight zoom
  | 'pan-right'      // Slow pan right with slight zoom
  | 'pan-up'         // Slow pan up
  | 'pan-down'       // Slow pan down
  | 'drift'          // Gentle diagonal drift
  | 'random';        // Random selection per photo

export interface TextOverlay {
  text: string;
  position: 'top' | 'center' | 'bottom' | 'lower-third';
  style: TextStyle;
  startSeconds: number;               // Relative to act start
  durationSeconds: number;
  animation?: 'fade' | 'slide-up' | 'typewriter' | 'scale-in';
}

export interface TextStyle {
  fontSize?: number;                  // default 48
  fontFamily?: string;                // default 'Inter'
  fontWeight?: number;                // default 400
  color?: string;                     // default '#FFFFFF'
  backgroundColor?: string;           // optional background
  textShadow?: boolean;              // default true for readability
  letterSpacing?: number;
  textTransform?: 'none' | 'uppercase' | 'lowercase';
}
```

### AudioConfig

```typescript
export interface AudioConfig {
  tracks: AudioTrack[];
  masterVolume?: number;              // default 1.0
}

export interface AudioTrack {
  id: string;
  src: string;                        // "audio/song-1.mp3"
  startSeconds: number;               // When this track starts in the video timeline
  endSeconds?: number;                // When to cut (auto = end of file)
  volume?: number;                    // default 1.0
  fadeIn?: number;                    // Fade-in duration in seconds
  fadeOut?: number;                   // Fade-out duration in seconds
  transition?: AudioTransition;
  beatSyncEnabled?: boolean;          // Enable beat detection for this track
  beatsFile?: string;                 // "beats/song-1-beats.json" (auto-generated)
}

export interface AudioTransition {
  type: 'hard-cut' | 'crossfade' | 'whoosh' | 'impact' | 'reverse-cymbal';
  durationSeconds?: number;           // For crossfade, default 1.0
  sfxFile?: string;                   // Optional SFX file for whoosh/impact
}
```

### OutputConfig

```typescript
export interface OutputConfig {
  formats: OutputFormat[];
  fps?: number;                       // default 30
  quality?: 'draft' | 'standard' | 'high'; // Maps to CRF values
}

export interface OutputFormat {
  id: string;                         // "landscape" | "tiktok" | "square"
  width: number;
  height: number;
  name: string;
  cropStrategy?: 'center' | 'face-detect' | 'custom'; // How to reframe for aspect ratio
}

// Preset formats
export const FORMAT_PRESETS = {
  landscape: { id: 'landscape', width: 1920, height: 1080, name: '16:9 Landscape' },
  tiktok:    { id: 'tiktok',    width: 1080, height: 1920, name: '9:16 TikTok/Reels' },
  square:    { id: 'square',    width: 1080, height: 1080, name: '1:1 Square' },
} as const;
```

### ActEffects

```typescript
export interface ActEffects {
  filmGrain?: FilmGrainConfig | boolean;    // true = default settings
  vignette?: VignetteConfig | boolean;
  letterbox?: LetterboxConfig | boolean;
  particles?: ParticlesConfig;
  depthBlur?: DepthBlurConfig | boolean;
}

export interface FilmGrainConfig {
  intensity: number;                  // 0-1, default 0.3
  fps?: number;                       // Grain animation speed, default 24
}

export interface VignetteConfig {
  intensity: number;                  // 0-1, default 0.5
  radius: number;                     // 0-1, default 0.7
  color?: string;                     // default '#000000'
}

export interface LetterboxConfig {
  ratio: number;                      // Aspect ratio, default 2.35 (cinematic)
  color?: string;                     // Bar color, default '#000000'
  animated?: boolean;                 // Animate bars in/out, default false
}

export interface ParticlesConfig {
  type: 'confetti' | 'golden-rain' | 'sparkles' | 'snow' | 'bokeh' | 'dust';
  density: number;                    // 0-1
  speed?: number;                     // 0-2, default 1.0
  colors?: string[];                  // Particle colors
  startSeconds?: number;              // When particles begin (relative to act)
  durationSeconds?: number;           // How long particles last
}

export interface DepthBlurConfig {
  intensity: number;                  // 0-20px, default 4
  mask?: 'center-clear' | 'bottom-clear' | 'custom';
}
```

### ColorGradePreset

```typescript
export type ColorGradePreset =
  | 'warm-nostalgic'
  | 'vibrant-adventure'
  | 'soft-cinematic'
  | 'golden-sunset'
  | 'cool-dramatic'
  | 'vintage-film'
  | 'noir'
  | 'pastel-dream'
  | 'natural'
  | ColorGradeCustom;

export interface ColorGradeCustom {
  brightness?: number;               // default 1.0
  contrast?: number;                 // default 1.0
  saturate?: number;                 // default 1.0
  sepia?: number;                    // default 0
  hueRotate?: number;               // degrees, default 0
  temperature?: number;              // -100 (cool) to 100 (warm)
  overlayColor?: string;            // Semi-transparent overlay
  overlayOpacity?: number;          // 0-1
}

// Preset definitions
export const COLOR_GRADES: Record<string, ColorGradeCustom> = {
  'warm-nostalgic': {
    brightness: 1.05, contrast: 0.95, saturate: 0.85, sepia: 0.15,
    temperature: 30, overlayColor: '#FF8C00', overlayOpacity: 0.05,
  },
  'vibrant-adventure': {
    brightness: 1.1, contrast: 1.1, saturate: 1.3, sepia: 0,
    temperature: 10,
  },
  'soft-cinematic': {
    brightness: 0.95, contrast: 1.05, saturate: 0.9, sepia: 0.05,
    temperature: 15, overlayColor: '#FFF0E0', overlayOpacity: 0.03,
  },
  'golden-sunset': {
    brightness: 1.08, contrast: 1.0, saturate: 1.1, sepia: 0.1,
    temperature: 40, overlayColor: '#FFD700', overlayOpacity: 0.06,
  },
  'cool-dramatic': {
    brightness: 0.9, contrast: 1.2, saturate: 0.8, sepia: 0,
    temperature: -20, overlayColor: '#1a1a2e', overlayOpacity: 0.08,
  },
  'vintage-film': {
    brightness: 0.95, contrast: 0.9, saturate: 0.7, sepia: 0.25,
    temperature: 20, overlayColor: '#8B7355', overlayOpacity: 0.07,
  },
  'noir': {
    brightness: 0.85, contrast: 1.3, saturate: 0, sepia: 0,
    overlayColor: '#000000', overlayOpacity: 0.1,
  },
  'pastel-dream': {
    brightness: 1.15, contrast: 0.85, saturate: 0.6, sepia: 0.05,
    temperature: 5, overlayColor: '#FFE4E1', overlayOpacity: 0.08,
  },
  'natural': {
    brightness: 1.0, contrast: 1.0, saturate: 1.0, sepia: 0,
  },
};
```

### Beat detection output

```typescript
// Generated by tools/beat_detect.py -> public/beats/song-1-beats.json
export interface BeatData {
  filename: string;
  durationSeconds: number;
  bpm: number;
  beats: number[];                    // Timestamps in seconds [0.43, 0.86, 1.29, ...]
  downbeats: number[];                // Strong beats (every 4th typically)
  energy: EnergySegment[];           // For energy-aware cut pacing
}

export interface EnergySegment {
  startSeconds: number;
  endSeconds: number;
  level: 'low' | 'medium' | 'high';  // Mapped from RMS energy
}
```

### Scene transitions

```typescript
export type SceneTransition =
  | { type: 'cut' }
  | { type: 'fade'; durationFrames?: number }
  | { type: 'dissolve'; durationFrames?: number }
  | { type: 'wipe'; direction?: 'left' | 'right' | 'up' | 'down' }
  | { type: 'zoom-rush'; durationFrames?: number }
  | { type: 'light-leak'; durationFrames?: number }
  | { type: 'slide'; direction?: 'left' | 'right' };

export type ActTransition =
  | { type: 'fade-to-black'; durationSeconds?: number }
  | { type: 'crossfade'; durationSeconds?: number }
  | { type: 'title-card'; durationSeconds?: number }  // Shows act title
  | { type: 'whoosh-cut' };
```

---

## 4. Components

### KenBurnsPhoto

The core photo animation component. Applies slow pan + zoom to still images using `interpolate()` and CSS `transform`.

```typescript
interface KenBurnsPhotoProps {
  src: string;                        // staticFile path
  motion: KenBurnsMotion;
  startScale?: number;
  endScale?: number;
  startPosition?: { x: number; y: number };
  endPosition?: { x: number; y: number };
  easing?: 'linear' | 'ease-in-out' | 'ease-out';
  durationInFrames: number;
  style?: React.CSSProperties;        // Container style overrides
}
```

Implementation approach:
- Uses `useCurrentFrame()` and `interpolate()` to animate `transform: scale() translate()`
- Photo rendered via `<Img>` at 120-130% of container to allow pan room
- `object-fit: cover` ensures no gaps
- Each motion preset maps to start/end scale + position pairs
- `'random'` selects from presets using deterministic seed (photo index)

### FilmGrain

Animated noise overlay simulating film grain.

```typescript
interface FilmGrainProps {
  intensity?: number;                 // 0-1, default 0.3
  fps?: number;                       // Grain refresh rate, default 24
}
```

Implementation: CSS `background-image` with `url("data:image/svg+xml,...")` containing fractal noise, re-seeded every `Math.floor(frame / (videoFps / grainFps))` frames. Rendered as absolute-positioned overlay with `pointer-events: none` and `mix-blend-mode: overlay`.

### Vignette

Radial gradient overlay that darkens edges.

```typescript
interface VignetteProps {
  intensity?: number;                 // 0-1
  radius?: number;                    // 0-1
  color?: string;
}
```

Implementation: `radial-gradient(ellipse at center, transparent ${radius*100}%, ${color} 100%)` with `opacity: intensity`.

### Letterbox

Cinematic aspect ratio bars.

```typescript
interface LetterboxProps {
  ratio?: number;                     // default 2.35
  color?: string;
  animated?: boolean;
  animationDurationFrames?: number;
}
```

Implementation: Two `<div>` elements positioned at top and bottom. Bar height calculated as `(containerHeight - containerWidth / ratio) / 2`. If `animated`, bars slide in using `interpolate()`.

### Particles

Configurable particle system for confetti, sparkles, golden rain, etc.

```typescript
interface ParticlesProps {
  type: 'confetti' | 'golden-rain' | 'sparkles' | 'snow' | 'bokeh' | 'dust';
  density: number;                    // 0-1 maps to particle count (10-200)
  speed?: number;
  colors?: string[];
  opacity?: number;
}
```

Implementation: Array of particle `<div>` elements with deterministic initial positions (seeded random). Each particle animated via `interpolate()` for y-position, rotation, and opacity. No `<canvas>` for Remotion rendering compatibility. Particle count = `Math.floor(density * 200)`.

### SplitScreen

CSS grid-based split composition.

```typescript
interface SplitScreenProps {
  layout: '2-vertical' | '2-horizontal' | '3-column' | '4-grid';
  children: React.ReactNode[];
  gap?: number;                       // pixels, default 4
  borderRadius?: number;
}
```

### DepthBlur

Simulated depth-of-field using CSS backdrop-filter.

```typescript
interface DepthBlurProps {
  intensity?: number;                 // blur radius in px
  mask: 'center-clear' | 'bottom-clear' | 'custom';
  customMask?: string;               // CSS mask-image value
}
```

Implementation: Overlay div with `backdrop-filter: blur(${intensity}px)` and CSS `mask-image` gradient to create depth effect.

### TextOverlay

Animated text with configurable position, style, and entrance animation.

```typescript
interface TextOverlayProps {
  text: string;
  position: 'top' | 'center' | 'bottom' | 'lower-third';
  style: TextStyle;
  animation?: 'fade' | 'slide-up' | 'typewriter' | 'scale-in';
  animationDurationFrames?: number;   // default 20
}
```

Implementation: Each animation type uses `interpolate()` or `spring()`. Typewriter uses `text.slice(0, charCount)` where charCount interpolates over frames.

### PhotoMosaic

Grid layout for displaying multiple photos simultaneously.

```typescript
interface PhotoMosaicProps {
  photos: string[];                   // Array of staticFile paths
  layout: 'grid-4' | 'grid-6' | 'grid-9' | 'collage' | 'growing';
  animateIn?: boolean;                // Staggered entrance
  staggerDelayFrames?: number;        // Delay between each photo appearing
}
```

Implementation: CSS grid with `spring()` scale-in animations staggered per cell. `'growing'` layout starts with 1 photo and adds more over time. `'collage'` uses slightly rotated, overlapping positioning.

### ColorGrade

Wrapper component applying color grading via CSS filters.

```typescript
interface ColorGradeProps {
  preset: ColorGradePreset;
  children: React.ReactNode;
  transitionFromPrevious?: boolean;   // Smooth transition from previous grade
  transitionDurationFrames?: number;
}
```

Implementation: Wraps children in a `<div>` with `filter: brightness() contrast() saturate() sepia() hue-rotate()`. If `transitionFromPrevious`, uses `interpolateColors()` and interpolated filter values over the first N frames.

### BeatSyncedMontage

Auto-places photos on beat boundaries from beat detection JSON.

```typescript
interface BeatSyncedMontageProps {
  photos: string[];
  beatsFile: string;                  // Path to beat detection JSON
  startBeatIndex?: number;            // Which beat to start from
  endBeatIndex?: number;
  minPhotoFrames?: number;            // Minimum frames per photo (floor)
  transition?: 'cut' | 'zoom-rush' | 'wipe';
  kenBurns?: KenBurnsConfig;          // Applied to each photo
}
```

Implementation: Reads beat JSON via `staticFile()` + fetch in component. Maps each photo to a beat boundary. High-energy segments get 1-beat photos, low-energy gets 2-4 beat photos. Uses `<Sequence>` per photo with `from` calculated from beat timestamps.

### AudioTrack

Multi-song audio component with transitions.

```typescript
interface AudioTrackProps {
  tracks: AudioTrack[];
  masterVolume?: number;
}
```

Implementation: Renders multiple `<Audio>` components inside `<Sequence>` wrappers. Each track gets `startFrom` (trim from audio file start) and wrapping `<Sequence from={startFrame}>`. Volume interpolation handles fade-in/fade-out. Crossfade: overlapping sequences with inverse volume curves. Hard-cut: adjacent sequences with no overlap.

---

## 5. Tools

### tools/beat_detect.py

Beat detection using librosa.

```bash
cd $TOOLKIT
python3 tools/beat_detect.py \
  --input projects/PROJECT/public/audio/song-1.mp3 \
  --output projects/PROJECT/public/beats/song-1-beats.json
```

Output schema:
```json
{
  "filename": "song-1.mp3",
  "durationSeconds": 213.5,
  "bpm": 128,
  "beats": [0.43, 0.86, 1.29, 1.72, ...],
  "downbeats": [0.43, 2.15, 3.87, ...],
  "energy": [
    { "startSeconds": 0, "endSeconds": 30, "level": "low" },
    { "startSeconds": 30, "endSeconds": 90, "level": "high" },
    { "startSeconds": 90, "endSeconds": 120, "level": "medium" }
  ]
}
```

Dependencies: `librosa`, `numpy`, `soundfile`.

Implementation:
1. Load audio with `librosa.load()`
2. Extract tempo and beats with `librosa.beat.beat_track()`
3. Extract downbeats with `librosa.beat.plp()` or `madmom`
4. Calculate RMS energy per segment with `librosa.feature.rms()`
5. Classify energy segments into low/medium/high by percentile thresholds
6. Output JSON

### tools/photo_import.py

Organizes a folder of photos into the config schema structure.

```bash
cd $TOOLKIT
python3 tools/photo_import.py \
  --input ~/Photos/wedding/ \
  --output projects/PROJECT/public/photos/ \
  --config projects/PROJECT/src/config/photos.json
```

Features:
- Reads EXIF dates, sorts chronologically
- Detects and removes blurry photos (Laplacian variance threshold)
- Removes near-duplicates (perceptual hash, hamming distance < 5)
- Copies photos to organized subdirectories
- Outputs JSON arrays matching `PhotoEntry[]` schema

Dependencies: `Pillow`, `imagehash`, `piexif`.

### tools/validate_config.py

Validates the wedding config before rendering.

```bash
cd $TOOLKIT
python3 tools/validate_config.py \
  --config projects/PROJECT/src/config/wedding-config.ts
```

Checks:
- All photo files exist in `public/`
- All audio files exist and are valid (ffprobe duration check)
- Act durations sum to total video duration
- Audio tracks cover the full timeline without gaps
- Beat files exist for tracks with `beatSyncEnabled: true`
- Text overlay timing falls within act boundaries
- No orphaned files in `public/photos/`

---

## 6. Pipeline

### Step-by-step flow: config to rendered MP4

**Step 0: Create project from template**

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
cp -r templates/wedding-montage projects/my-wedding
cd projects/my-wedding
npm install
```

**Step 1: Organize photos**

```bash
cd $TOOLKIT
python3 tools/photo_import.py \
  --input ~/Photos/wedding-photos/ \
  --output projects/my-wedding/public/photos/ \
  --config projects/my-wedding/src/config/photos.json
```

Or manually copy photos into `public/photos/{category}/`.

**Step 2: Add songs**

Copy song files to `public/audio/`:
```bash
cp ~/Music/our-song.mp3 projects/my-wedding/public/audio/song-1.mp3
cp ~/Music/upbeat-song.mp3 projects/my-wedding/public/audio/song-2.mp3
```

**Step 3: Run beat detection**

```bash
cd $TOOLKIT
python3 tools/beat_detect.py \
  --input projects/my-wedding/public/audio/song-1.mp3 \
  --output projects/my-wedding/public/beats/song-1-beats.json

python3 tools/beat_detect.py \
  --input projects/my-wedding/public/audio/song-2.mp3 \
  --output projects/my-wedding/public/beats/song-2-beats.json
```

**Step 4: Edit config**

Edit `projects/my-wedding/src/config/wedding-config.ts` with act structure, photo assignments, audio tracks, text overlays, and effect selections. The template includes a complete example config with sensible defaults.

**Step 5: Validate**

```bash
cd $TOOLKIT
python3 tools/validate_config.py \
  --config projects/my-wedding/src/config/wedding-config.ts
```

**Step 6: Preview**

```bash
cd $TOOLKIT/projects/my-wedding
npm start
# Opens Remotion Studio at http://localhost:3000
# Preview individual acts or full montage
```

**Step 7: Render**

```bash
cd $TOOLKIT/projects/my-wedding

# Full quality landscape
npx remotion render WeddingMontage out/wedding-landscape.mp4

# Draft quality for review (faster)
npx remotion render WeddingMontage out/wedding-draft.mp4 --quality=draft
```

**Step 8: Export social formats**

```bash
cd $TOOLKIT

# TikTok/Reels (9:16)
ffmpeg -i projects/my-wedding/out/wedding-landscape.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:a copy projects/my-wedding/out/wedding-tiktok.mp4

# Square (1:1)
ffmpeg -i projects/my-wedding/out/wedding-landscape.mp4 \
  -vf "crop=ih:ih:(iw-ih)/2:0,scale=1080:1080" \
  -c:a copy projects/my-wedding/out/wedding-square.mp4
```

Or, if the config specifies multiple formats, Remotion renders each as a separate composition automatically.

---

## 7. SKILL.md Draft

```markdown
---
name: wedding-video
description: Create cinematic wedding montage videos from photos and songs using Remotion. Features act-based narrative structure (5 acts), Ken Burns photo animations, multi-song audio with beat-synced cuts, cinematic color grading, film effects (grain, vignette, letterbox, particles), split-screen, photo mosaic, and social media format export (16:9, 9:16, 1:1). Config-driven -- describe your story, get a film.
version: 1.0.0
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
      scenes: [/* ... */],
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
      scenes: [/* ... */],
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

### Step 6: Preview

```bash
cd $TOOLKIT/projects/MY_WEDDING
npm start
```

Opens Remotion Studio. Preview individual acts or the full montage in the browser.

### Step 7: Render

```bash
cd $TOOLKIT/projects/MY_WEDDING
npx remotion render WeddingMontage out/wedding.mp4
```

### Step 8: Social Media Export (Optional)

```bash
# TikTok/Reels (9:16)
ffmpeg -i out/wedding.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:a copy out/wedding-tiktok.mp4

# Square (1:1)
ffmpeg -i out/wedding.mp4 \
  -vf "crop=ih:ih:(iw-ih)/2:0,scale=1080:1080" \
  -c:a copy out/wedding-square.mp4
```

## Five-Act Structure

The default wedding narrative follows five acts:

| Act | Emotion | Pacing | Color Grade | Typical Duration |
|-----|---------|--------|-------------|-----------------|
| Two Worlds | Nostalgic | Slow (4-6s/photo) | Warm Nostalgic | 45-75s |
| The Meeting | Joyful | Moderate (3-4s/photo) | Natural | 30-50s |
| The Adventure | Energetic | Fast, beat-synced (1-2s/photo) | Vibrant Adventure | 60-90s |
| The Proposal | Romantic | Slow-dramatic (5-8s/photo) | Soft Cinematic | 40-60s |
| Tomorrow | Grateful | Uplifting, building | Golden Sunset | 40-60s |

Customize any act or add/remove acts as needed.

## Color Grade Presets

| Preset | Look | Best For |
|--------|------|----------|
| `warm-nostalgic` | Warm, slightly desaturated, touch of sepia | Childhood, memories |
| `vibrant-adventure` | High contrast, saturated | Travel, energy |
| `soft-cinematic` | Soft, low contrast, warm | Romance, proposals |
| `golden-sunset` | Golden overlay, warm tones | Finale, celebration |
| `cool-dramatic` | Cool, high contrast | Drama, tension |
| `vintage-film` | Heavy sepia, desaturated | Retro looks |
| `natural` | No grading | When photos speak for themselves |

## Ken Burns Motions

| Motion | Effect |
|--------|--------|
| `zoom-in` | Slowly zoom into center |
| `zoom-out` | Slowly zoom out |
| `pan-left` | Pan left with slight zoom |
| `pan-right` | Pan right with slight zoom |
| `drift` | Gentle diagonal movement |
| `random` | Varies per photo (deterministic) |

## Effects

All effects are composable and applied per-act:

- **Film Grain** — Animated noise overlay (vintage feel)
- **Vignette** — Darkened edges (focus on center)
- **Letterbox** — Cinematic 2.35:1 bars (film look)
- **Particles** — Confetti, golden rain, sparkles, snow, bokeh, dust
- **Depth Blur** — Simulated depth of field
- **Split Screen** — 2, 3, or 4 photos side by side

## Tips

1. **Photo count:** 40-80 photos for a 4-6 minute video. More = faster pacing needed.
2. **Song length:** Total song duration should roughly match total video duration.
3. **Beat sync:** Enable only for high-energy acts. Slow acts with beat sync feel jarring.
4. **Preview often.** Use `npm start` to check pacing before full render.
5. **Photo quality:** 1920x1080 minimum. Larger is fine; Remotion scales down.
6. **Text overlays:** Less is more. 3-5 text moments across the whole video.
```

---

## 8. Dependencies

### npm packages (in template package.json)

| Package | Version | Purpose |
|---------|---------|---------|
| `remotion` | `^4.x` | Core video framework |
| `@remotion/cli` | `^4.x` | CLI rendering |
| `@remotion/transitions` | `^4.x` | Scene transitions (fade, slide, wipe) |
| `@remotion/media` | `^4.x` | Audio/Video components |
| `@remotion/light-leaks` | `^4.x` | Light leak transition overlays |
| `@remotion/google-fonts` | `^4.x` | Font loading (Inter, Playfair Display) |
| `react` | `^18.x` | React core |
| `react-dom` | `^18.x` | React DOM |
| `typescript` | `^5.x` | TypeScript |
| `zod` | `^3.x` | Config validation schemas |

### Python packages (tools/)

| Package | Version | Purpose |
|---------|---------|---------|
| `librosa` | `>=0.10` | Beat detection, tempo estimation, energy analysis |
| `numpy` | `>=1.24` | Array operations for librosa |
| `soundfile` | `>=0.12` | Audio file I/O for librosa |
| `Pillow` | `>=10.0` | Image processing for photo import |
| `imagehash` | `>=4.3` | Perceptual hashing for duplicate detection |
| `piexif` | `>=1.1` | EXIF date extraction |

### System dependencies

| Tool | Purpose |
|------|---------|
| FFmpeg | Social format export, audio normalization |
| FFprobe | Audio duration measurement, config validation |
| Node.js 18+ | Remotion rendering |
| Python 3.10+ | Beat detection, photo import tools |

### Optional future dependencies

| Package | Purpose | When needed |
|---------|---------|-------------|
| `@remotion/lambda` | Cloud rendering (15s vs 10-20min local) | Phase 2 |
| `opencv-python` | Face detection for smart cropping | Photo import v2 |
| `clip-interrogator` | AI photo categorization | Photo import v2 |

---

## 9. Cost Estimate

### Per-video rendering cost

| Item | Cost | Notes |
|------|------|-------|
| Local Remotion render | $0 | 10-20 min for 5-min video on M1 Mac |
| Remotion Lambda render (future) | $0.01-0.10 | 15-30s render time |
| Beat detection (local) | $0 | librosa runs locally, ~5s per song |
| Photo import (local) | $0 | All local processing |
| Total (local pipeline) | **$0** | All processing is local |
| Total (Lambda pipeline) | **$0.01-0.10** | Only Lambda has a cost |

### Comparison to alternatives

| Alternative | Cost per video | Notes |
|-------------|---------------|-------|
| Videographer | $2,000-5,000 | Professional wedding video |
| Animoto Pro | $15/mo subscription | Template-locked |
| InVideo AI | $25/mo subscription | Less control |
| CapCut Pro | $10/mo subscription | GUI-only |
| This skill | $0 (local) | Full control, reusable |

---

## 10. Implementation Stories

Ordered by dependency chain. Each story is independently shippable.

### Phase 1: Foundation Components

| # | Story | Description | Effort | Dependencies |
|---|-------|-------------|--------|-------------|
| 1 | **KenBurnsPhoto component** | Implement the `<KenBurnsPhoto>` component with all 6 motion presets, configurable scale/position, and easing via `interpolate()`. Include unit test with `npx remotion still` snapshot. | M | None |
| 2 | **ColorGrade component + presets** | Implement `<ColorGrade>` wrapper with CSS filter-based grading. Define all 8 preset objects. Support interpolated transitions between grades. | S | None |
| 3 | **FilmGrain + Vignette + Letterbox** | Implement three simple overlay effect components. Each takes intensity/config props. All use absolute positioning and pointer-events: none. | S | None |
| 4 | **TextOverlay component** | Implement `<TextOverlay>` with 4 position modes, 4 animation types, configurable style. Test with multiple simultaneous overlays. | S | None |
| 5 | **Particles component** | Implement `<Particles>` with 6 particle types. Deterministic seeded positions for render consistency. All via `interpolate()` on divs (no canvas). | M | None |
| 6 | **SplitScreen + PhotoMosaic** | Implement grid-based split-screen layouts and photo mosaic with staggered animations. | S | None |

### Phase 2: Audio Engine

| # | Story | Description | Effort | Dependencies |
|---|-------|-------------|--------|-------------|
| 7 | **Multi-song AudioTrack component** | Implement `<AudioTrack>` rendering multiple `<Audio>` components with precise start/end timing, volume interpolation for fade-in/out, and hard-cut/crossfade transitions. | M | None |
| 8 | **Beat detection tool** | Implement `tools/beat_detect.py` with librosa. Extract beats, downbeats, BPM, and energy segments. Output JSON. Include tests with a sample audio file. | M | None |
| 9 | **BeatSyncedMontage component** | Implement `<BeatSyncedMontage>` that reads beat JSON and auto-places photos on beat boundaries. Support energy-aware pacing (faster cuts in high-energy segments). | L | #1, #8 |

### Phase 3: Composition Assembly

| # | Story | Description | Effort | Dependencies |
|---|-------|-------------|--------|-------------|
| 10 | **TypeScript config schema + types** | Define all TypeScript interfaces in `types.ts`. Create Zod validation schemas. Include default config with example data. | M | None |
| 11 | **WeddingScene component** | Implement single scene renderer that selects component based on scene type (photo, split-screen, mosaic, video-clip, text-only). Applies Ken Burns, text overlays, and scene transitions. | M | #1, #4, #6 |
| 12 | **WeddingAct component** | Implement act renderer that sequences scenes, applies color grade, effects, and act transitions. Handles pacing calculations (auto-duration per scene from act duration / scene count). | L | #2, #3, #5, #7, #11 |
| 13 | **WeddingMontage top-level composition** | Implement `<WeddingMontage>` that reads full config, renders title card, all acts with transitions, and end card. Registers Remotion composition with calculated total duration. | M | #12 |

### Phase 4: Tools and Template

| # | Story | Description | Effort | Dependencies |
|---|-------|-------------|--------|-------------|
| 14 | **Photo import tool** | Implement `tools/photo_import.py` with EXIF sorting, blur detection, duplicate removal, and organized output. | M | None |
| 15 | **Config validation tool** | Implement `tools/validate_config.py` checking file existence, timing consistency, and completeness. | S | #10 |
| 16 | **Wedding template scaffold** | Create `templates/wedding-montage/` with package.json, tsconfig, remotion.config, example config, and placeholder photos/audio. Ready to `cp` and customize. | M | #13 |
| 17 | **Social media format export** | Add FFmpeg post-processing commands for 9:16 and 1:1 export. Optional: register additional Remotion compositions per format with adapted layouts. | S | #13 |

### Phase 5: Polish

| # | Story | Description | Effort | Dependencies |
|---|-------|-------------|--------|-------------|
| 18 | **Audio SFX library** | Bundle whoosh, impact, reverse-cymbal SFX files in `public/audio/sfx/`. Wire into AudioTrack transitions. | S | #7 |
| 19 | **DepthBlur component** | Implement backdrop-filter based depth blur with mask options. | S | None |
| 20 | **End-to-end test** | Create a minimal but complete wedding config with 10 photos and 1 song. Render and verify output. Measure render time. Document in README. | M | #16 |

### Effort summary

| Size | Count | Estimated days each | Total |
|------|-------|-------------------|-------|
| S | 7 | 0.5 day | 3.5 days |
| M | 10 | 1-2 days | 15 days |
| L | 3 | 2-3 days | 7.5 days |
| **Total** | **20 stories** | | **~26 days (5-6 weeks)** |

### Recommended build order

**Week 1-2:** Stories 1-6 (foundation components, all parallelizable)
**Week 3:** Stories 7-9 (audio engine + beat sync)
**Week 4:** Stories 10-13 (composition assembly, sequential)
**Week 5:** Stories 14-17 (tools and template)
**Week 6:** Stories 18-20 (polish and testing)
