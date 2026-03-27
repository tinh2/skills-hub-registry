# Engineering Spec: `/social-clip` Skill

> Version: 1.0.0 | Author: Tho Le | Date: 2026-03-26
> Priority: HIGH | Effort: M-L | Dependencies: video-toolkit (existing)

---

## 1. Overview

### What it does

The `/social-clip` skill creates short-form social media videos optimized for TikTok, Instagram Reels, YouTube Shorts, Instagram Stories, and other platforms. It operates in two modes:

1. **Create mode** -- generate a social clip from scratch given a text brief, images, video clips, and/or audio files.
2. **Repurpose mode** -- take an existing long-form video (MP4 or Remotion project) and extract/reformat it into short-form clips for social platforms.

### Target user

Developers and content creators who want to produce platform-optimized short-form video from the terminal without a GUI editor or monthly subscription.

### Value proposition

- **No subscription** -- runs locally or on your own GPU infra. CapCut is free but cloud-locked; OpusClip is $19+/mo; InVideo is $60/mo.
- **Fully programmable** -- every clip is a React composition you can customize, version control, and template.
- **Batch export** -- render one piece of content across all platforms in a single command.
- **CLI-native** -- fits into developer and creator automation workflows (CI/CD, cron, scripting).
- **TikTok-style captions** -- word-by-word animated captions via Whisper transcription, matching what CapCut and InVideo charge for.

### Key competitors

| Competitor | Strength | Our edge |
|---|---|---|
| **CapCut** | Free, AI Clipper for long-to-shorts, auto-captions, 12M+ assets | No CLI, cloud-locked, not programmable |
| **OpusClip** | AI identifies best moments from long-form, auto-reformats | $19+/mo, no customization, no batch |
| **Revid.ai** | Prompt-to-short-form, beginner-friendly | $39/mo, limited control |
| **InVideo AI** | Prompt-based with 16M+ stock assets | $60/mo, GUI-only |
| **Remotion Superpowers** | OSS Claude Code plugin with `/create-short` command | No caption styles, no auto-reframe, no batch |

---

## 2. Architecture

### How it fits with existing skills

```
skills-hub-registry/build/
  video-toolkit/     <-- existing: voiceover, image gen, music gen, talking head, Modal GPU
  remotion/          <-- existing: Remotion composition patterns, transitions, audio
  ffmpeg-media/      <-- existing: format conversion, trimming, social media export recipes
  social-clip/       <-- NEW: this skill
```

The `social-clip` skill builds on all three existing skills:

- **video-toolkit** -- reuses Qwen3-TTS for voiceover, FLUX.2 for image generation, MusicGen for background music, Modal for cloud GPU rendering.
- **remotion** -- all compositions are Remotion React components. Uses `interpolate()`, `spring()`, `<Sequence>`, `<TransitionSeries>`, `<Audio>`, `<OffthreadVideo>`, `staticFile()`.
- **ffmpeg-media** -- post-render processing: format conversion, audio normalization, thumbnail extraction.

### New components needed

```
social-clip/
  SKILL.md                          # Skill instructions
  templates/
    social-clip/                    # Remotion project template
      package.json
      tsconfig.json
      src/
        Root.tsx                    # Remotion entry -- registers all platform compositions
        index.ts                    # Entry point
        config/
          clip-config.ts            # TypeScript config schema
          platform-presets.ts       # Platform format definitions
        components/
          SocialClip.tsx            # Main composition orchestrator
          HookOpener.tsx            # First 3s hook component
          CaptionOverlay.tsx        # TikTok-style animated captions
          TextOverlay.tsx           # Animated titles, subtitles, callouts
          EngagementOverlay.tsx     # CTA, polls, countdowns
          AutoReframe.tsx           # 16:9 to 9:16 intelligent crop
          ThumbnailFrame.tsx        # Cover frame generator
        components/content-types/
          TalkingHead.tsx           # Single speaker with captions
          Montage.tsx               # Multi-clip rapid cut montage
          BeforeAfter.tsx           # Side-by-side or sequential comparison
          Listicle.tsx              # Numbered list with animations
          QuoteCard.tsx             # Styled quote with attribution
          ProductShowcase.tsx       # Product shots with text overlays
          TutorialSnippet.tsx       # Quick how-to with step indicators
        lib/
          transitions/
            swipe.ts                # Directional swipe transition
            zoom-rush.ts            # Rapid zoom in/out
            glitch.ts               # Digital glitch effect
            flash.ts                # White flash transition
            whip-pan.ts             # Simulated whip pan blur
          captions/
            caption-styles.ts       # Pop, highlight, karaoke, subtitle, bounce
            caption-renderer.tsx    # Word-by-word caption component
          hooks/
            use-captions.ts         # Hook for loading Whisper transcript
            use-beat-sync.ts        # Hook for beat-aligned timing
      public/
        audio/                      # User-provided audio, generated music
        images/                     # User-provided images, generated assets
        video/                      # User-provided video clips
        captions/                   # Whisper transcription JSON output
  tools/
    transcribe.py                   # Whisper.cpp transcription wrapper
    auto_reframe.py                 # Intelligent crop detection for 16:9 -> 9:16
    extract_clips.py                # Long-form to short-form clip extraction
    batch_render.sh                 # Multi-platform batch render script
```

---

## 3. Data Model

### Platform presets

```typescript
// src/config/platform-presets.ts

export type PlatformId =
  | 'tiktok'
  | 'instagram-reel'
  | 'youtube-short'
  | 'instagram-story'
  | 'square'
  | 'landscape';

export interface PlatformPreset {
  id: PlatformId;
  name: string;
  width: number;
  height: number;
  fps: number;
  minDurationSeconds: number;
  maxDurationSeconds: number;
  aspectRatio: string;
  safeZone: {
    top: number;    // px from top to avoid platform UI overlap
    bottom: number; // px from bottom to avoid platform UI overlap
    left: number;
    right: number;
  };
  codec: 'h264' | 'h265';
  audioBitrate: string;
  videoBitrate: string;
}

export const PLATFORM_PRESETS: Record<PlatformId, PlatformPreset> = {
  tiktok: {
    id: 'tiktok',
    name: 'TikTok',
    width: 1080,
    height: 1920,
    fps: 60,
    minDurationSeconds: 15,
    maxDurationSeconds: 60,
    aspectRatio: '9:16',
    safeZone: { top: 150, bottom: 270, left: 40, right: 40 },
    codec: 'h264',
    audioBitrate: '128k',
    videoBitrate: '8M',
  },
  'instagram-reel': {
    id: 'instagram-reel',
    name: 'Instagram Reel',
    width: 1080,
    height: 1920,
    fps: 30,
    minDurationSeconds: 15,
    maxDurationSeconds: 90,
    aspectRatio: '9:16',
    safeZone: { top: 120, bottom: 300, left: 40, right: 40 },
    codec: 'h264',
    audioBitrate: '128k',
    videoBitrate: '6M',
  },
  'youtube-short': {
    id: 'youtube-short',
    name: 'YouTube Short',
    width: 1080,
    height: 1920,
    fps: 60,
    minDurationSeconds: 15,
    maxDurationSeconds: 60,
    aspectRatio: '9:16',
    safeZone: { top: 100, bottom: 200, left: 40, right: 40 },
    codec: 'h264',
    audioBitrate: '128k',
    videoBitrate: '10M',
  },
  'instagram-story': {
    id: 'instagram-story',
    name: 'Instagram Story',
    width: 1080,
    height: 1920,
    fps: 30,
    minDurationSeconds: 1,
    maxDurationSeconds: 15,
    aspectRatio: '9:16',
    safeZone: { top: 200, bottom: 250, left: 40, right: 40 },
    codec: 'h264',
    audioBitrate: '128k',
    videoBitrate: '6M',
  },
  square: {
    id: 'square',
    name: 'Square (Feed)',
    width: 1080,
    height: 1080,
    fps: 30,
    minDurationSeconds: 3,
    maxDurationSeconds: 60,
    aspectRatio: '1:1',
    safeZone: { top: 0, bottom: 0, left: 0, right: 0 },
    codec: 'h264',
    audioBitrate: '128k',
    videoBitrate: '5M',
  },
  landscape: {
    id: 'landscape',
    name: 'Landscape (16:9)',
    width: 1920,
    height: 1080,
    fps: 30,
    minDurationSeconds: 3,
    maxDurationSeconds: 600,
    aspectRatio: '16:9',
    safeZone: { top: 0, bottom: 0, left: 0, right: 0 },
    codec: 'h264',
    audioBitrate: '192k',
    videoBitrate: '8M',
  },
};
```

### Clip configuration

```typescript
// src/config/clip-config.ts

export type ContentType =
  | 'talking-head'
  | 'montage'
  | 'before-after'
  | 'listicle'
  | 'quote-card'
  | 'product-showcase'
  | 'tutorial-snippet';

export type CaptionStyle = 'pop' | 'highlight' | 'karaoke' | 'subtitle' | 'bounce';

export type TransitionType = 'swipe' | 'zoom-rush' | 'glitch' | 'flash' | 'whip-pan' | 'fade' | 'cut';

export interface SocialClipConfig {
  // --- Identity ---
  title: string;
  description?: string;

  // --- Platform targets ---
  platforms: PlatformId[];         // Which platforms to render for
  primaryPlatform: PlatformId;     // Composition is authored for this, adapted to others

  // --- Content type ---
  contentType: ContentType;

  // --- Duration ---
  durationSeconds: number;         // Total clip duration

  // --- Hook (first 3 seconds) ---
  hook: {
    style: 'bold-text' | 'question' | 'statistic' | 'motion-burst' | 'sound-effect';
    text?: string;                 // Hook text overlay
    soundEffect?: string;          // Path to SFX file (whoosh, ding, bass-drop)
    animation?: 'zoom-in' | 'shake' | 'flash' | 'scale-bounce';
  };

  // --- Scenes ---
  scenes: SocialScene[];

  // --- Captions ---
  captions?: {
    enabled: boolean;
    style: CaptionStyle;
    fontSize?: number;             // Default: 64 for 9:16, 48 for 1:1
    fontFamily?: string;           // Default: 'Inter'
    primaryColor?: string;         // Active word color. Default: '#FFFFFF'
    highlightColor?: string;       // Highlighted word color. Default: '#FFD700'
    backgroundColor?: string;      // Caption background. Default: 'rgba(0,0,0,0.6)'
    position?: 'top' | 'center' | 'bottom'; // Default: 'bottom'
    wordsPerLine?: number;         // Default: 4
  };

  // --- Audio ---
  audio: {
    voiceover?: string;            // Path to voiceover audio file
    voiceroverScript?: string;     // Text to generate voiceover from (uses Qwen3-TTS)
    voiceoverSpeaker?: string;     // Qwen3-TTS speaker name
    voiceoverTone?: string;        // Qwen3-TTS tone
    backgroundMusic?: string;      // Path to background music file
    backgroundMusicVolume?: number; // 0-1, default 0.15
    soundEffects?: Array<{
      file: string;
      startSeconds: number;
      volume?: number;             // 0-1, default 1
    }>;
  };

  // --- Text overlays ---
  textOverlays?: Array<{
    text: string;
    startSeconds: number;
    durationSeconds: number;
    position: 'top' | 'center' | 'bottom' | { x: number; y: number };
    style: 'title' | 'subtitle' | 'callout' | 'label' | 'hashtag';
    fontSize?: number;
    fontWeight?: number;
    color?: string;
    animation?: 'fade-in' | 'slide-up' | 'scale-in' | 'typewriter' | 'bounce-in';
  }>;

  // --- Engagement elements ---
  engagement?: {
    cta?: {
      text: string;                // "Follow for more", "Link in bio", etc.
      position: 'bottom' | 'end-card';
      animation?: 'pulse' | 'slide-in' | 'fade';
    };
    commentPrompt?: {
      text: string;                // "What do you think? Comment below"
      showAt: number;              // Seconds into clip
    };
    countdown?: {
      from: number;                // Start number
      showAt: number;              // Seconds into clip
      style: 'minimal' | 'bold' | 'neon';
    };
    poll?: {
      question: string;
      options: [string, string];
      showAt: number;
      durationSeconds: number;
    };
  };

  // --- Transitions ---
  transitions?: {
    default: TransitionType;       // Default transition between scenes
    durationFrames?: number;       // Default: 8
  };

  // --- Thumbnail / cover frame ---
  thumbnail?: {
    frameSeconds?: number;         // Capture frame at this timestamp
    textOverlay?: string;          // Text to overlay on thumbnail
    style?: 'clean' | 'bold' | 'minimal';
  };

  // --- Auto-reframe (for repurpose mode) ---
  autoReframe?: {
    enabled: boolean;
    sourceAspectRatio?: '16:9' | '4:3'; // Source format
    focusMode: 'center' | 'face-track' | 'motion-track' | 'manual';
    manualRegions?: Array<{
      startSeconds: number;
      endSeconds: number;
      x: number;
      y: number;
      width: number;
      height: number;
    }>;
  };

  // --- Style ---
  style?: {
    colorScheme?: 'dark' | 'light' | 'vibrant' | 'pastel' | 'neon';
    accentColor?: string;
    fontFamily?: string;
    borderRadius?: number;         // For image/video element corners
  };
}

export interface SocialScene {
  type: 'image' | 'video' | 'text-only' | 'split';
  durationSeconds: number;
  media?: {
    src: string;                   // Path to image or video file
    fit?: 'cover' | 'contain' | 'fill';
    animation?: 'ken-burns-in' | 'ken-burns-out' | 'pan-left' | 'pan-right' | 'static' | 'zoom-pulse';
  };
  splitMedia?: {                   // For 'split' type
    left: { src: string; label?: string };
    right: { src: string; label?: string };
  };
  text?: {
    headline?: string;
    body?: string;
    position?: 'top' | 'center' | 'bottom';
  };
  transition?: TransitionType;     // Override default transition to next scene
}
```

---

## 4. Components

### 4.1 `<SocialClip>` -- Main Composition Orchestrator

The root component that reads `SocialClipConfig` and assembles all layers.

```typescript
interface SocialClipProps {
  config: SocialClipConfig;
  platform: PlatformPreset;
}
```

Responsibilities:
- Renders `<TransitionSeries>` of scenes
- Layers audio (voiceover, background music, SFX)
- Overlays captions, text, engagement elements
- Applies hook animation to first 3s
- Respects platform safe zones

### 4.2 `<HookOpener>` -- Scroll-Stopping First 3 Seconds

```typescript
interface HookOpenerProps {
  hook: SocialClipConfig['hook'];
  platform: PlatformPreset;
  durationInFrames: number; // 3 * fps
}
```

Renders the first 3 seconds of the clip with maximum visual impact:
- `bold-text`: Large text with `spring()` scale-in, optional shake
- `question`: Question text with typewriter effect
- `statistic`: Animated counter (interpolate from 0 to value)
- `motion-burst`: Rapid zoom + flash + text reveal
- `sound-effect`: Audio sting with synchronized visual beat

### 4.3 `<CaptionOverlay>` -- TikTok-Style Animated Captions

```typescript
interface CaptionOverlayProps {
  transcriptPath: string;          // Path to Whisper JSON output
  style: CaptionStyle;
  fontSize: number;
  fontFamily: string;
  primaryColor: string;
  highlightColor: string;
  backgroundColor: string;
  position: 'top' | 'center' | 'bottom';
  wordsPerLine: number;
  platform: PlatformPreset;
}
```

Uses Remotion's `createTikTokStyleCaptions()` from `@remotion/captions` to render word-by-word animated captions synced to audio. Styles:

- **pop** -- words scale up from 0 with `spring()` bounce when spoken
- **highlight** -- current word changes to `highlightColor`, others stay `primaryColor`
- **karaoke** -- words fill with color left-to-right as spoken (gradient mask)
- **subtitle** -- traditional subtitle bar at bottom, no per-word animation
- **bounce** -- words drop in from above with gravity-like spring

### 4.4 `<TextOverlay>` -- Animated Text System

```typescript
interface TextOverlayProps {
  text: string;
  style: 'title' | 'subtitle' | 'callout' | 'label' | 'hashtag';
  animation: 'fade-in' | 'slide-up' | 'scale-in' | 'typewriter' | 'bounce-in';
  position: 'top' | 'center' | 'bottom' | { x: number; y: number };
  fontSize: number;
  fontWeight: number;
  color: string;
  platform: PlatformPreset;
}
```

Platform-appropriate font sizes:
- Title: 72px (9:16), 56px (1:1), 48px (16:9)
- Subtitle: 48px (9:16), 36px (1:1), 32px (16:9)
- Callout: 56px with background pill
- Label: 32px uppercase tracking
- Hashtag: 36px with `#` prefix, accent color

### 4.5 `<EngagementOverlay>` -- CTA, Polls, Countdowns

```typescript
interface EngagementOverlayProps {
  engagement: SocialClipConfig['engagement'];
  platform: PlatformPreset;
  totalDurationFrames: number;
}
```

Renders engagement elements with platform-native styling:
- **CTA**: Pulsing button or slide-in bar at bottom. "Follow for more", "Link in bio", etc.
- **Comment prompt**: Text bubble animation with arrow pointing down
- **Countdown**: Circular or numeric countdown with tick animation
- **Poll**: Two-option overlay with animated bars (fake engagement percentages optional)

### 4.6 `<AutoReframe>` -- Intelligent 16:9 to 9:16 Crop

```typescript
interface AutoReframeProps {
  children: React.ReactNode;       // The 16:9 source composition
  sourceWidth: number;
  sourceHeight: number;
  targetWidth: number;
  targetHeight: number;
  focusRegions: Array<{
    startFrame: number;
    endFrame: number;
    x: number;
    y: number;
    width: number;
    height: number;
  }>;
}
```

Wraps a landscape composition and applies an animated crop window that tracks focus regions. Uses `interpolate()` to smoothly pan between regions. Focus regions come from either:
- `tools/auto_reframe.py` (face detection / motion analysis)
- Manual `manualRegions` in config

### 4.7 Content Type Components

Each content type is a self-contained composition pattern:

| Component | Description | Key props |
|---|---|---|
| `<TalkingHead>` | Single speaker with captions, optional PiP | `speakerVideo`, `backgroundImage`, `captions` |
| `<Montage>` | Rapid-cut multi-clip montage | `clips[]`, `cutTiming: 'beat-sync' \| 'even' \| 'custom'` |
| `<BeforeAfter>` | Side-by-side or sequential comparison | `before`, `after`, `layout: 'split' \| 'sequential' \| 'wipe'` |
| `<Listicle>` | Numbered items with animated reveals | `items[]`, `numbering: 'numeric' \| 'emoji' \| 'icon'` |
| `<QuoteCard>` | Styled quote with attribution | `quote`, `attribution`, `background`, `quoteMark` style |
| `<ProductShowcase>` | Product shots with feature callouts | `productImage`, `features[]`, `rotateAnimation` |
| `<TutorialSnippet>` | Quick how-to with step indicators | `steps[]`, `progressBar`, `stepNumberStyle` |

---

## 5. Tools

### 5.1 `tools/transcribe.py` -- Whisper.cpp Transcription

Transcribes audio files to word-level timestamps for caption rendering.

```bash
cd $TOOLKIT
python3 tools/transcribe.py \
  --input projects/PROJECT/public/audio/voiceover.mp3 \
  --output projects/PROJECT/public/captions/transcript.json \
  --model base.en \
  --word-timestamps
```

Output format (compatible with `@remotion/captions`):

```json
{
  "segments": [
    {
      "text": "Here's how to create viral social content",
      "start": 0.0,
      "end": 2.8,
      "words": [
        { "word": "Here's", "start": 0.0, "end": 0.3 },
        { "word": "how", "start": 0.35, "end": 0.5 },
        { "word": "to", "start": 0.52, "end": 0.6 },
        { "word": "create", "start": 0.62, "end": 0.9 },
        { "word": "viral", "start": 0.92, "end": 1.2 },
        { "word": "social", "start": 1.25, "end": 1.6 },
        { "word": "content", "start": 1.62, "end": 2.0 }
      ]
    }
  ]
}
```

Dependencies: `whisper-cpp-python` or `openai-whisper` (Python). Alternatively, uses Remotion's built-in `@remotion/install-whisper-cpp` for native install.

### 5.2 `tools/auto_reframe.py` -- Intelligent Crop Detection

Analyzes a 16:9 video and generates focus region keyframes for 9:16 reframing.

```bash
python3 tools/auto_reframe.py \
  --input source-16x9.mp4 \
  --output focus-regions.json \
  --mode face-track \
  --sample-rate 2   # Analyze every 2nd frame for speed
```

Modes:
- `center` -- static center crop (no analysis needed)
- `face-track` -- OpenCV Haar cascades or MediaPipe face detection, tracks largest face
- `motion-track` -- optical flow (cv2.calcOpticalFlowFarneback) to find area of highest motion
- `rule-of-thirds` -- positions crop at left or right third based on content density

Output:

```json
{
  "sourceWidth": 1920,
  "sourceHeight": 1080,
  "regions": [
    { "startFrame": 0, "endFrame": 90, "x": 660, "y": 0, "width": 608, "height": 1080 },
    { "startFrame": 90, "endFrame": 180, "x": 400, "y": 0, "width": 608, "height": 1080 }
  ]
}
```

Dependencies: `opencv-python`, `mediapipe` (optional for face-track mode).

### 5.3 `tools/extract_clips.py` -- Long-Form to Short-Form Extraction

Analyzes a long-form video and identifies the best segments for short-form clips (repurpose mode).

```bash
python3 tools/extract_clips.py \
  --input long-form-video.mp4 \
  --max-clips 5 \
  --target-duration 30-60 \
  --output clips-manifest.json
```

Analysis approach:
1. Transcribe with Whisper to get content segments
2. Score segments by: audio energy (loud = engaging), speech density (words per second), silence gaps (natural segment boundaries)
3. Identify top N segments by engagement score
4. Output manifest with timestamps and suggested hook text

Dependencies: `whisper`, `librosa`, `numpy`.

### 5.4 `tools/batch_render.sh` -- Multi-Platform Batch Render

Renders the same composition across all target platforms.

```bash
bash tools/batch_render.sh \
  --project projects/my-clip \
  --platforms tiktok,instagram-reel,youtube-short,square \
  --output out/
```

Flow:
1. Reads `clip-config.ts` for platform list
2. For each platform, runs `npx remotion render` with platform-specific composition ID
3. Post-processes with FFmpeg for codec/bitrate optimization
4. Generates thumbnail stills for each platform
5. Outputs all files to `out/{platform}/`

---

## 6. Pipeline

### Create Mode Pipeline

```
User brief / config
        |
        v
[1. Parse config]
  - Validate SocialClipConfig
  - Resolve platform presets
  - Calculate total duration and scene durations
        |
        v
[2. Generate assets] (parallel)
  - Voiceover: Qwen3-TTS (if voiceoverScript provided)
  - Background music: MusicGen or user-provided file
  - Images: FLUX.2 (if AI-generated backgrounds needed)
  - Sound effects: copy to public/audio/sfx/
        |
        v
[3. Transcribe voiceover]
  - Run tools/transcribe.py on voiceover audio
  - Output word-level timestamps to public/captions/
        |
        v
[4. Sync timing]
  - ffprobe all audio files for actual durations
  - Update scene durations to match audio
  - Recalculate total composition duration
        |
        v
[5. Generate Remotion project]
  - Copy template to projects/PROJECT_NAME/
  - Write clip-config.ts with resolved config
  - Register platform compositions in Root.tsx
        |
        v
[6. Preview]
  - npx remotion still for review frames
  - Review hook frame (frame 0-90), middle, CTA
        |
        v
[7. Render]
  - Primary platform: npx remotion render
  - Other platforms: batch_render.sh for all targets
        |
        v
[8. Post-process]
  - FFmpeg: codec optimization, audio normalization
  - Generate thumbnail stills
  - Output: out/{platform}/clip.mp4 + thumbnail.png
```

### Repurpose Mode Pipeline

```
Existing long-form video (MP4)
        |
        v
[1. Analyze source]
  - ffprobe: get resolution, duration, fps
  - tools/extract_clips.py: identify best segments
  - tools/transcribe.py: full transcription
        |
        v
[2. Select clips]
  - Present ranked clip suggestions to user
  - User selects which segments to extract
        |
        v
[3. Extract segments]
  - FFmpeg: frame-accurate trim of selected segments
  - Copy to project public/video/
        |
        v
[4. Auto-reframe] (if source is landscape)
  - tools/auto_reframe.py: generate focus regions
  - Or user provides manual focus overrides
        |
        v
[5. Add social elements]
  - Generate captions from transcription
  - Apply hook to first 3 seconds
  - Add text overlays, CTA, engagement elements
        |
        v
[6. Render & export]
  - Same as Create Mode steps 6-8
```

---

## 7. SKILL.md Draft

```markdown
---
name: social-clip
description: Create short-form social media videos for TikTok, Instagram Reels, YouTube Shorts, and more. Two modes -- create from scratch with a brief, or repurpose long-form video into short clips. Includes TikTok-style animated captions (Whisper + Remotion), auto-reframe (16:9 to 9:16), hook-first structure, engagement overlays, transition library, and batch export across all platforms.
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
permissions:
  - filesystem
  - shell
  - network
  - api
---

# Social Clip

Create short-form social media videos optimized for TikTok, Instagram Reels, YouTube Shorts, and other platforms. Two modes: create from scratch or repurpose existing long-form video.

## Prerequisites

Requires the video-toolkit skill to be installed for AI asset generation (voiceover, images, music).

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT && python3 tools/verify_setup.py
```

Install additional dependencies:

```bash
# Whisper for transcription (choose one)
pip3 install --break-system-packages openai-whisper
# OR use Remotion's built-in Whisper.cpp:
npx remotion install-whisper-cpp

# Auto-reframe (optional -- only for repurpose mode)
pip3 install --break-system-packages opencv-python mediapipe

# Clip extraction (optional -- only for repurpose mode)
pip3 install --break-system-packages librosa numpy
```

## Platform Presets

| Platform | Resolution | FPS | Duration | Aspect |
|---|---|---|---|---|
| TikTok | 1080x1920 | 60 | 15-60s | 9:16 |
| Instagram Reel | 1080x1920 | 30 | 15-90s | 9:16 |
| YouTube Short | 1080x1920 | 60 | 15-60s | 9:16 |
| Instagram Story | 1080x1920 | 30 | 1-15s | 9:16 |
| Square (Feed) | 1080x1080 | 30 | 3-60s | 1:1 |
| Landscape | 1920x1080 | 30 | 3-600s | 16:9 |

Each preset includes platform-specific safe zones to avoid UI overlap (profile icons, captions area, navigation).

## Create Mode

### Step 1: Create Project

```bash
cd $TOOLKIT
cp -r templates/social-clip projects/MY_CLIP
cd projects/MY_CLIP
npm install
```

### Step 2: Write Config

Edit `src/config/clip-config.ts`:

```typescript
import { SocialClipConfig } from './types';

export const clipConfig: SocialClipConfig = {
  title: 'Why devs are switching to terminal video',
  platforms: ['tiktok', 'instagram-reel', 'youtube-short'],
  primaryPlatform: 'tiktok',
  contentType: 'talking-head',
  durationSeconds: 45,

  hook: {
    style: 'bold-text',
    text: 'Stop using video editors.',
    soundEffect: 'audio/sfx/bass-drop.mp3',
    animation: 'zoom-in',
  },

  scenes: [
    {
      type: 'video',
      durationSeconds: 40,
      media: { src: 'video/talking-head.mp4', fit: 'cover' },
    },
    {
      type: 'text-only',
      durationSeconds: 5,
      text: { headline: 'Try it yourself', body: 'Link in bio' },
    },
  ],

  captions: {
    enabled: true,
    style: 'pop',
    highlightColor: '#FFD700',
    position: 'bottom',
    wordsPerLine: 4,
  },

  audio: {
    voiceover: 'audio/voiceover.mp3',
    backgroundMusic: 'audio/bg-lofi.mp3',
    backgroundMusicVolume: 0.12,
  },

  engagement: {
    cta: {
      text: 'Follow for dev tips',
      position: 'end-card',
      animation: 'slide-in',
    },
  },

  transitions: {
    default: 'zoom-rush',
    durationFrames: 8,
  },

  thumbnail: {
    frameSeconds: 1.5,
    textOverlay: 'Stop Using Video Editors',
    style: 'bold',
  },
};
```

### Step 3: Generate Voiceover

```bash
cd $TOOLKIT
python3 tools/qwen3_tts.py \
  --text "Stop using video editors. Here's how I make viral content from my terminal..." \
  --speaker Ryan --tone excited \
  --output projects/MY_CLIP/public/audio/voiceover.mp3 \
  --cloud modal
```

### Step 4: Transcribe for Captions

```bash
cd $TOOLKIT
python3 tools/transcribe.py \
  --input projects/MY_CLIP/public/audio/voiceover.mp3 \
  --output projects/MY_CLIP/public/captions/transcript.json \
  --model base.en --word-timestamps
```

### Step 5: Sync Timing

```bash
cd $TOOLKIT
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  projects/MY_CLIP/public/audio/voiceover.mp3
```

Update `durationSeconds` in config to match actual audio: `ceil(audio_duration + 3)` (3s buffer for hook + CTA).

### Step 6: Preview and Render

```bash
cd $TOOLKIT/projects/MY_CLIP

# Preview hook frame
npx remotion still src/index.ts SocialClip-tiktok --frame=0 --output=/tmp/hook.png

# Preview mid-clip
npx remotion still src/index.ts SocialClip-tiktok --frame=900 --output=/tmp/mid.png

# Render primary platform
npm run render

# Batch render all platforms
bash ../../tools/batch_render.sh \
  --project . \
  --platforms tiktok,instagram-reel,youtube-short \
  --output out/
```

Output: `out/tiktok/clip.mp4`, `out/instagram-reel/clip.mp4`, `out/youtube-short/clip.mp4` + thumbnails.

## Repurpose Mode

### Step 1: Analyze Long-Form Video

```bash
cd $TOOLKIT
python3 tools/extract_clips.py \
  --input path/to/long-form-video.mp4 \
  --max-clips 5 \
  --target-duration 30-60 \
  --output projects/MY_CLIP/clips-manifest.json
```

### Step 2: Auto-Reframe (if source is 16:9)

```bash
python3 tools/auto_reframe.py \
  --input path/to/long-form-video.mp4 \
  --output projects/MY_CLIP/public/focus-regions.json \
  --mode face-track
```

### Step 3: Extract and Configure

Select clips from the manifest and create config with `autoReframe.enabled: true`. The `<AutoReframe>` component reads `focus-regions.json` and applies animated crop.

### Step 4: Add Captions and Render

Same as Create Mode steps 4-6.

## Caption Styles

| Style | Effect | Best for |
|---|---|---|
| `pop` | Words scale up with spring bounce when spoken | High energy, comedy |
| `highlight` | Current word changes color, others stay white | Educational, tutorial |
| `karaoke` | Words fill with color left-to-right | Music, storytelling |
| `subtitle` | Traditional subtitle bar, no per-word animation | Professional, clean |
| `bounce` | Words drop in from above with gravity spring | Playful, casual |

## Transition Library

| Transition | Effect | Best for |
|---|---|---|
| `swipe` | Directional swipe (up/down/left/right) | Scene changes |
| `zoom-rush` | Rapid zoom in then out to next scene | High energy cuts |
| `glitch` | Digital glitch distortion | Tech content, edgy |
| `flash` | White flash between scenes | Photo reveals |
| `whip-pan` | Motion blur simulating camera whip | Fast pacing |
| `fade` | Standard opacity crossfade | Calm transitions |
| `cut` | Hard cut, no transition | Beat-synced montages |

## Content Types

| Type | Description | When to use |
|---|---|---|
| `talking-head` | Single speaker with captions | Advice, opinions, tutorials |
| `montage` | Multi-clip rapid cuts | Showcases, highlights, travel |
| `before-after` | Side-by-side or sequential comparison | Transformations, results |
| `listicle` | Numbered items with animated reveals | Tips, rankings, recommendations |
| `quote-card` | Styled quote with attribution | Motivation, testimonials |
| `product-showcase` | Product shots with feature callouts | Marketing, launches |
| `tutorial-snippet` | Quick how-to with step indicators | Recipes, DIY, code tips |

## Hook Structure (First 3 Seconds)

Every clip must hook within 3 seconds. The `hook` config controls the opening:

- **bold-text** -- Large text slams in with scale + shake. Pair with bass-drop SFX.
- **question** -- Typewriter question engages curiosity. "Did you know...?"
- **statistic** -- Animated counter rolls to a surprising number. "10x faster"
- **motion-burst** -- Flash + zoom + reveal. Maximum visual energy.
- **sound-effect** -- Audio sting with synced visual pulse. Whoosh, ding, dramatic.

## Cost Estimates

| Step | Cost | Notes |
|---|---|---|
| Voiceover (Qwen3-TTS) | ~$0.01 | Per clip, via Modal |
| Background music (MusicGen) | ~$0.02-0.05 | Duration-dependent |
| Image generation (FLUX.2) | ~$0.01/image | If AI backgrounds needed |
| Whisper transcription | Free | Runs locally via whisper.cpp |
| Remotion render | Free | Local render, no license for personal use |
| Auto-reframe analysis | Free | Local OpenCV processing |

**Total per clip:** ~$0.05-0.10 for AI-generated assets. Free if using only user-provided media.

**Batch export:** Rendering 4 platform variants costs zero extra -- same Remotion render with different dimensions.

## Tips

1. **Hook is everything** -- spend 80% of creative effort on the first 3 seconds. If the hook fails, nothing else matters.
2. **Captions are mandatory** -- 85% of social video is watched with sound off. Always enable captions.
3. **Keep text in safe zones** -- each platform overlays UI on the video. Use the preset safe zones to avoid text behind profile icons or navigation.
4. **Match platform pacing** -- TikTok favors cuts every 2-3 seconds. Instagram tolerates slower pacing. YouTube Shorts split the difference.
5. **Use `zoom-rush` sparingly** -- one zoom-rush per clip is impactful, five is nauseating.
6. **End with CTA** -- the last 3-5 seconds should always include a call to action.
7. **Batch render always** -- if you are making a TikTok, render Reel and Short variants too. Nearly free and doubles your reach.
```

---

## 8. Dependencies

### npm packages (Remotion project)

| Package | Version | Purpose |
|---|---|---|
| `remotion` | ^4.x | Core composition engine |
| `@remotion/cli` | ^4.x | Rendering CLI |
| `@remotion/transitions` | ^4.x | Transition presentations |
| `@remotion/captions` | ^4.x | `createTikTokStyleCaptions()` |
| `@remotion/media` | ^4.x | `<Audio>`, `<Video>` components |
| `@remotion/google-fonts` | ^4.x | Font loading (Inter, Montserrat, etc.) |
| `@remotion/install-whisper-cpp` | ^4.x | Optional: local Whisper install |
| `@remotion/media-utils` | ^4.x | `getAudioDuration()`, audio analysis |

### Python packages

| Package | Purpose | Required |
|---|---|---|
| `openai-whisper` | Audio transcription with word timestamps | Yes (or Remotion whisper.cpp) |
| `opencv-python` | Auto-reframe: face detection, motion tracking | Only for repurpose mode |
| `mediapipe` | Auto-reframe: face mesh for precise tracking | Optional (improves face-track) |
| `librosa` | Clip extraction: beat detection, energy analysis | Only for repurpose mode |
| `numpy` | Numerical ops for analysis tools | Yes (transitive) |

### External tools

| Tool | Purpose | Install |
|---|---|---|
| `ffmpeg` / `ffprobe` | Audio probing, post-processing, format conversion | `brew install ffmpeg` |
| `whisper.cpp` | Fast local transcription (alternative to Python whisper) | Via `@remotion/install-whisper-cpp` |

### No external APIs required

All AI generation (voiceover, music, images) goes through existing video-toolkit Modal endpoints. Transcription runs locally. No new API keys needed.

---

## 9. Cost Estimate

### Per-clip cost breakdown

| Scenario | AI Assets | Render | Total |
|---|---|---|---|
| **User-provided media only** (video + audio, add captions) | $0.00 | Free (local) | **$0.00** |
| **Generate voiceover only** | $0.01 | Free | **$0.01** |
| **Generate voiceover + music** | $0.04 | Free | **$0.04** |
| **Full AI generation** (voiceover + music + background images) | $0.08 | Free | **$0.08** |
| **Batch 4 platforms** (same content, 4 renders) | Same as above | Free | **Same** |

### Comparison to competitors

| Tool | Per-clip cost | Monthly cost |
|---|---|---|
| **social-clip (ours)** | $0.00-0.08 | $0.00 (+ Modal free tier) |
| CapCut Pro | Included | $10-20/mo |
| OpusClip | Included | $19-49/mo |
| InVideo AI | Included | $25-60/mo |
| Revid.ai | Included | $19-39/mo |

At 100 clips/month, our cost is ~$0-8 vs $19-60/mo for competitors. Modal's $30/mo free tier covers approximately 300-600 clips worth of AI generation.

---

## 10. Implementation Stories

Ordered by dependency chain and build priority. Effort: S = 1-2 hours, M = 3-6 hours, L = 1-2 days, XL = 3-5 days.

### Phase 1: Foundation (Week 1)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 1 | **Platform presets**: Define `PlatformPreset` type and all 6 presets (TikTok, Reel, Short, Story, Square, Landscape) with safe zones, codec, and bitrate specs. | S | -- |
| 2 | **Config schema**: Define `SocialClipConfig`, `SocialScene`, and all supporting types in TypeScript. Validate with Zod schema for runtime safety. | M | #1 |
| 3 | **Project template scaffold**: Create `templates/social-clip/` with package.json, tsconfig, Root.tsx registering one composition per platform, and placeholder SocialClip component. | M | #1, #2 |
| 4 | **SocialClip orchestrator**: Build `<SocialClip>` component that reads config, creates `<TransitionSeries>` of scenes, layers audio tracks, and renders at platform dimensions. Support image and video scene types. | L | #3 |
| 5 | **TextOverlay component**: Build `<TextOverlay>` with 5 animation types (fade-in, slide-up, scale-in, typewriter, bounce-in) and platform-aware font sizing. | M | #3 |

### Phase 2: Captions (Week 1-2)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 6 | **Whisper transcription tool**: Build `tools/transcribe.py` wrapping Whisper with word-level timestamp output in Remotion-compatible JSON format. | M | -- |
| 7 | **Caption renderer**: Build `<CaptionOverlay>` using `@remotion/captions` `createTikTokStyleCaptions()`. Implement `pop` and `highlight` styles first. | L | #6 |
| 8 | **Additional caption styles**: Add `karaoke`, `subtitle`, and `bounce` caption styles. | M | #7 |

### Phase 3: Hook & Engagement (Week 2)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 9 | **HookOpener component**: Build `<HookOpener>` with `bold-text` and `motion-burst` styles. Includes spring scale-in, shake animation, flash overlay, and SFX sync. | M | #4 |
| 10 | **Additional hook styles**: Add `question` (typewriter), `statistic` (counter), `sound-effect` (audio-synced pulse) hook styles. | M | #9 |
| 11 | **Engagement overlays**: Build `<EngagementOverlay>` with CTA button/bar, comment prompt bubble, countdown timer, and poll overlay. | L | #4, #5 |

### Phase 4: Transitions (Week 2)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 12 | **Transition library**: Implement 5 custom transition presentations for `<TransitionSeries>`: swipe, zoom-rush, glitch, flash, whip-pan. Each uses `interpolate()` and CSS transforms. | L | #4 |

### Phase 5: Content Types (Week 3)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 13 | **TalkingHead content type**: Build `<TalkingHead>` component with speaker video, optional background, and caption integration. | M | #4, #7 |
| 14 | **Montage content type**: Build `<Montage>` with multi-clip rapid cuts, even or custom timing, optional beat-sync hook. | M | #4, #12 |
| 15 | **Listicle content type**: Build `<Listicle>` with animated numbered reveals and progress indicator. | M | #4, #5 |
| 16 | **Remaining content types**: Build QuoteCard, BeforeAfter, ProductShowcase, TutorialSnippet. | L | #4, #5 |

### Phase 6: Auto-Reframe & Repurpose (Week 3-4)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 17 | **Auto-reframe tool**: Build `tools/auto_reframe.py` with center crop and face-track modes using OpenCV. Output focus-region JSON. | L | -- |
| 18 | **AutoReframe component**: Build `<AutoReframe>` wrapper that reads focus-region JSON and applies animated crop via `interpolate()` + CSS `transform` + `overflow: hidden`. | M | #17 |
| 19 | **Clip extraction tool**: Build `tools/extract_clips.py` with Whisper + librosa analysis for identifying engaging segments from long-form video. | L | #6 |

### Phase 7: Batch & Polish (Week 4)

| # | Story | Effort | Depends on |
|---|---|---|---|
| 20 | **Batch render script**: Build `tools/batch_render.sh` that renders all platform variants in sequence with FFmpeg post-processing for codec/bitrate optimization. | M | #4 |
| 21 | **Thumbnail generation**: Add `<ThumbnailFrame>` component and integrate with `npx remotion still` for auto-generating cover frames per platform. | S | #4 |
| 22 | **SKILL.md finalization**: Write final SKILL.md with all instructions, examples, tips, and cost estimates. Integration test with end-to-end create and repurpose workflows. | M | All |

### Total effort estimate

| Phase | Stories | Effort |
|---|---|---|
| Phase 1: Foundation | 5 | ~3 days |
| Phase 2: Captions | 3 | ~2 days |
| Phase 3: Hook & Engagement | 3 | ~2 days |
| Phase 4: Transitions | 1 | ~1-2 days |
| Phase 5: Content Types | 4 | ~3 days |
| Phase 6: Auto-Reframe | 3 | ~3 days |
| Phase 7: Batch & Polish | 3 | ~1-2 days |
| **Total** | **22 stories** | **~15-18 days** |

### Recommended MVP (ship in 1 week)

Stories 1-7, 9, 12, 13, 20 = platform presets + config + orchestrator + text overlays + captions (pop + highlight) + hook (bold-text) + transitions + talking head + batch render. This covers the most common social clip use case: a talking head video with animated captions, rendered across multiple platforms.

---

## Appendix A: Remotion Captions API Reference

The `@remotion/captions` package provides:

```typescript
import { createTikTokStyleCaptions } from '@remotion/captions';

const { pages } = createTikTokStyleCaptions({
  captions: transcriptData.segments.flatMap(s => s.words),
  combineTokensWithinMilliseconds: 800,
});
```

Each `page` contains tokens with timing that the `<CaptionOverlay>` component renders as animated text. The `combineTokensWithinMilliseconds` parameter controls how many words appear per "page" -- lower values = more frequent updates = more TikTok-like feel.

## Appendix B: Safe Zone Reference

Platform UI elements that overlap video content:

- **TikTok**: Username/description bottom-left (bottom 270px), action buttons right side (right 60px), top status bar (top 150px)
- **Instagram Reel**: Username/description bottom-left (bottom 300px), action buttons right side, top search bar (top 120px)
- **YouTube Short**: Title/subscribe bottom (bottom 200px), actions right side, top status (top 100px)
- **Instagram Story**: Reply bar bottom (bottom 250px), story progress top (top 200px)

All text overlays and captions should be positioned within safe zones to remain readable.
