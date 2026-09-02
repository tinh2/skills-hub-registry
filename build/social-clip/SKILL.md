---
name: social-clip
description: "Create short-form social media videos for TikTok, Instagram Reels, YouTube Shorts, and more."
version: "1.0.1"
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

| Platform | Resolution | FPS | Duration | Aspect | Safe Zone (top/bottom/left/right) |
|---|---|---|---|---|---|
| TikTok | 1080x1920 | 60 | 15-60s | 9:16 | 150/270/40/40 |
| Instagram Reel | 1080x1920 | 30 | 15-90s | 9:16 | 120/300/40/40 |
| YouTube Short | 1080x1920 | 60 | 15-60s | 9:16 | 100/200/40/40 |
| Instagram Story | 1080x1920 | 30 | 1-15s | 9:16 | 200/250/40/40 |
| Square (Feed) | 1080x1080 | 30 | 3-60s | 1:1 | 0/0/0/0 |
| Landscape (16:9) | 1920x1080 | 30 | 3-600s | 16:9 | 0/0/0/0 |

Each preset includes platform-specific safe zones (pixels) to avoid UI overlap with profile icons, captions area, and navigation. Keep all text and critical visual elements inside safe zones.

Codec and bitrate per platform:

| Platform | Codec | Video Bitrate | Audio Bitrate |
|---|---|---|---|
| TikTok | H.264 | 8M | 128k |
| Instagram Reel | H.264 | 6M | 128k |
| YouTube Short | H.264 | 10M | 128k |
| Instagram Story | H.264 | 6M | 128k |
| Square (Feed) | H.264 | 5M | 128k |
| Landscape (16:9) | H.264 | 8M | 192k |

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

Scene types: `image`, `video`, `text-only`, `split`.

Scene media animations: `ken-burns-in`, `ken-burns-out`, `pan-left`, `pan-right`, `static`, `zoom-pulse`.

### Step 3: Generate Voiceover

```bash
cd $TOOLKIT
python3 tools/qwen3_tts.py \
  --text "Stop using video editors. Here's how I make viral content from my terminal..." \
  --speaker Ryan --tone excited \
  --output projects/MY_CLIP/public/audio/voiceover.mp3 \
  --cloud modal
```

**Speakers:** `Ryan`, `Aiden`, `Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ono_Anna`, `Sohee`
**Tones:** `neutral`, `warm`, `professional`, `excited`, `calm`, `serious`, `storyteller`, `tutorial`

### Step 4: Generate Background Music (optional)

```bash
cd $TOOLKIT
python3 tools/music_gen.py \
  --preset lofi \
  --duration 50 \
  --output projects/MY_CLIP/public/audio/bg-lofi.mp3 \
  --cloud modal
```

Presets: `corporate-bg`, `upbeat-tech`, `ambient`, `dramatic`, `tension`, `hopeful`, `cta`, `lofi`.

### Step 5: Transcribe for Captions

```bash
cd $TOOLKIT
python3 tools/transcribe.py \
  --input projects/MY_CLIP/public/audio/voiceover.mp3 \
  --output projects/MY_CLIP/public/captions/transcript.json \
  --model base.en --word-timestamps
```

Output format (compatible with `@remotion/captions`):

```json
{
  "segments": [
    {
      "text": "Stop using video editors",
      "start": 0.0,
      "end": 1.8,
      "words": [
        { "word": "Stop", "start": 0.0, "end": 0.3 },
        { "word": "using", "start": 0.35, "end": 0.6 },
        { "word": "video", "start": 0.62, "end": 0.9 },
        { "word": "editors", "start": 0.92, "end": 1.4 }
      ]
    }
  ]
}
```

The `<CaptionOverlay>` component uses `createTikTokStyleCaptions()` from `@remotion/captions` to render word-by-word animated captions synced to the transcript timestamps.

### Step 6: Sync Timing

```bash
cd $TOOLKIT
ffprobe -v error -show_entries format=duration -of csv=p=0 \
  projects/MY_CLIP/public/audio/voiceover.mp3
```

Update `durationSeconds` in config to match actual audio: `ceil(audio_duration + 3)` (3s buffer for hook + CTA).

### Asset Manifest

Each asset gets a manifest entry telling the skill what it contains, its role in the clip, and how prominently to feature it.

```typescript
interface SocialAsset {
  path: string;                    // relative path to file
  type: 'photo' | 'video' | 'audio' | 'text-card' | 'product-shot' | 'screenshot';
  description: string;             // what this shows — Claude uses for placement
  tags: string[];                  // searchable: ['hook', 'highlight', 'b-roll', 'reaction']
  weight: 1 | 2 | 3 | 4 | 5;     // 1=b-roll flash, 3=standard, 5=hero/hook content
  section?: 'hook' | 'body' | 'cta' | 'outro';  // force into clip section
  platform?: string[];             // limit to: ['tiktok', 'reels'] or omit for all
  trimStart?: number;              // trim video from this second
  trimEnd?: number;                // trim video to this second
  beatSync?: boolean;              // true = cut on beat boundaries
  caption?: string;                // overlay text when this asset is shown
  duration?: number;               // suggested screen time
  notes?: string;                  // special instructions
}

interface SocialManifest {
  assets: SocialAsset[];
  defaults: {
    weight: number;
    durationByWeight: {
      1: number; // 0.5s — flash cut
      2: number; // 1s — quick show
      3: number; // 2s — standard beat
      4: number; // 3s — featured moment
      5: number; // 4s — hero content (hook or climax)
    };
  };
}
```

#### How Weights Work for Social Clips

| Weight | Role | Screen Time | Position | Pacing |
|--------|------|-------------|----------|--------|
| 5 — Hook/Hero | Scroll-stopper | 3-5s | First 3 seconds OR climax | Hold, dramatic entry |
| 4 — Featured | Key moment | 2-3s | Body highlights | Beat-synced emphasis |
| 3 — Standard | Good content | 1.5-2s | Body sequence | Standard beat cuts |
| 2 — Supporting | Context | 0.75-1.5s | Between key moments | Fast cuts |
| 1 — Flash | Texture/energy | 0.3-0.75s | Rapid montage | Flash cuts on beats |

#### Smart Placement Rules

- `weight: 5` + `section: 'hook'` → ALWAYS first 3 seconds. Non-negotiable.
- `weight: 5` without section → hook if no other hook exists, else climax
- `type: 'video'` with `beatSync: true` → cuts land on beat boundaries
- `type: 'text-card'` → shown as animated overlay, not standalone frame
- `weight: 1-2` assets fill rapid-fire montage sections between key moments
- `trimStart`/`trimEnd` → only use this portion of the video
- `platform: ['tiktok']` → only included in TikTok renders (e.g., vertical-optimized clips)
- If total asset duration exceeds clip length, lower-weight assets get dropped first

#### Example

```typescript
const manifest: SocialManifest = {
  assets: [
    {
      path: 'clips/reaction-wow.mp4',
      type: 'video',
      description: 'Friend reacting with genuine surprise and laughter',
      tags: ['hook', 'reaction'],
      weight: 5,
      section: 'hook',
      trimStart: 2.1,
      trimEnd: 4.8,
      notes: 'This is THE scroll-stopper. Use in first 3 seconds.',
    },
    {
      path: 'clips/cooking-montage.mp4',
      type: 'video',
      description: 'Quick cuts of cooking process — chopping, sauteing, plating',
      tags: ['process', 'montage'],
      weight: 3,
      section: 'body',
      beatSync: true,
    },
    {
      path: 'photos/finished-dish.jpg',
      type: 'photo',
      description: 'Beautifully plated final dish with garnish',
      tags: ['result', 'hero'],
      weight: 4,
      section: 'body',
      caption: 'The result speaks for itself',
    },
    {
      path: 'photos/kitchen-candid.jpg',
      type: 'photo',
      description: 'Candid shot laughing in the kitchen',
      tags: ['b-roll', 'personality'],
      weight: 1,
      beatSync: true,
    },
  ],
  defaults: {
    weight: 3,
    durationByWeight: { 1: 0.5, 2: 1, 3: 2, 4: 3, 5: 4 },
  },
};
```

### Step 7: Preview and Render

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

Take an existing long-form video and extract the best segments as short-form social clips.

### Step 1: Analyze Long-Form Video

```bash
cd $TOOLKIT
python3 tools/extract_clips.py \
  --input path/to/long-form-video.mp4 \
  --max-clips 5 \
  --target-duration 30-60 \
  --output projects/MY_CLIP/clips-manifest.json
```

The extraction tool:
1. Transcribes with Whisper to get content segments
2. Scores segments by audio energy (loud = engaging), speech density (words/second), and silence gaps (natural boundaries)
3. Identifies top N segments by engagement score
4. Outputs manifest with timestamps and suggested hook text

### Step 2: Auto-Reframe (if source is 16:9)

```bash
cd $TOOLKIT
python3 tools/auto_reframe.py \
  --input path/to/long-form-video.mp4 \
  --output projects/MY_CLIP/public/focus-regions.json \
  --mode face-track
```

Reframe modes:
- `center` -- static center crop (no analysis needed)
- `face-track` -- OpenCV Haar cascades or MediaPipe face detection, tracks largest face
- `motion-track` -- optical flow to find area of highest motion
- `rule-of-thirds` -- positions crop at left or right third based on content density

The `<AutoReframe>` component reads `focus-regions.json` and applies an animated crop window that smoothly pans between focus regions using `interpolate()`.

### Step 3: Extract and Configure

Select clips from the manifest and create config with `autoReframe.enabled: true`:

```typescript
autoReframe: {
  enabled: true,
  sourceAspectRatio: '16:9',
  focusMode: 'face-track',
},
```

Or provide manual focus region overrides:

```typescript
autoReframe: {
  enabled: true,
  focusMode: 'manual',
  manualRegions: [
    { startSeconds: 0, endSeconds: 10, x: 660, y: 0, width: 608, height: 1080 },
    { startSeconds: 10, endSeconds: 25, x: 400, y: 0, width: 608, height: 1080 },
  ],
},
```

### Step 4: Add Captions and Render

Same as Create Mode steps 5-7. Transcribe the extracted audio, enable captions, and batch render.

## Caption Styles

| Style | Effect | Best for |
|---|---|---|
| `pop` | Words scale up with `spring()` bounce when spoken | High energy, comedy |
| `highlight` | Current word changes to `highlightColor`, others stay white | Educational, tutorial |
| `karaoke` | Words fill with color left-to-right (gradient mask) | Music, storytelling |
| `subtitle` | Traditional subtitle bar at bottom, no per-word animation | Professional, clean |
| `bounce` | Words drop in from above with gravity-like spring | Playful, casual |

Caption config defaults:
- `fontSize`: 64 for 9:16 platforms, 48 for 1:1
- `fontFamily`: Inter
- `primaryColor`: #FFFFFF
- `highlightColor`: #FFD700
- `backgroundColor`: rgba(0,0,0,0.6)
- `position`: bottom
- `wordsPerLine`: 4

## Transition Library

| Transition | Effect | Best for |
|---|---|---|
| `swipe` | Directional swipe (up/down/left/right) | Scene changes |
| `zoom-rush` | Rapid zoom in then out to next scene | High energy cuts |
| `glitch` | Digital glitch distortion | Tech content, edgy |
| `flash` | White flash between scenes | Photo reveals |
| `whip-pan` | Motion blur simulating camera whip (use `@remotion/motion-blur` `<CameraMotionBlur>`) | Fast pacing |
| `fade` | Standard opacity crossfade | Calm transitions |
| `cut` | Hard cut, no transition | Beat-synced montages |

Import custom transitions from `lib/transitions/presentations/` directly, never from barrel files. For additional variety, use GL Transitions (`remotion-gl-transitions`) for trend-matching styles.

## Content Types

| Type | Description | When to use |
|---|---|---|
| `talking-head` | Single speaker with captions, optional PiP | Advice, opinions, tutorials |
| `montage` | Multi-clip rapid cuts with even, custom, or beat-synced timing | Showcases, highlights, travel |
| `before-after` | Side-by-side or sequential comparison with split/wipe layout | Transformations, results |
| `listicle` | Numbered items with animated reveals and progress indicator | Tips, rankings, recommendations |
| `quote-card` | Styled quote with attribution and decorative quote marks | Motivation, testimonials |
| `product-showcase` | Product shots with feature callouts and optional rotation | Marketing, launches |
| `tutorial-snippet` | Quick how-to with step indicators and progress bar | Recipes, DIY, code tips |

## Hook Structure (First 3 Seconds)

Every clip must hook within 3 seconds. The `hook` config controls the opening:

- **bold-text** -- Large text slams in with `spring()` scale + shake. Pair with bass-drop SFX.
- **question** -- Typewriter question engages curiosity. "Did you know...?"
- **statistic** -- Animated counter rolls to a surprising number with `interpolate()`. "10x faster"
- **motion-burst** -- Flash + zoom + reveal. Maximum visual energy.
- **sound-effect** -- Audio sting with synced visual pulse. Whoosh, ding, dramatic.

Hook animations: `zoom-in`, `shake`, `flash`, `scale-bounce`.

## Engagement Overlays

### CTA (Call to Action)

```typescript
engagement: {
  cta: {
    text: 'Follow for more',    // or "Link in bio", "Subscribe", etc.
    position: 'end-card',       // 'bottom' for persistent, 'end-card' for last 3-5s
    animation: 'pulse',         // 'pulse', 'slide-in', 'fade'
  },
},
```

### Comment Prompt

```typescript
engagement: {
  commentPrompt: {
    text: 'What do you think? Comment below',
    showAt: 20,                 // Seconds into clip
  },
},
```

### Countdown

```typescript
engagement: {
  countdown: {
    from: 5,
    showAt: 10,
    style: 'bold',              // 'minimal', 'bold', 'neon'
  },
},
```

### Poll

```typescript
engagement: {
  poll: {
    question: 'Which do you prefer?',
    options: ['Terminal', 'GUI Editor'],
    showAt: 15,
    durationSeconds: 5,
  },
},
```

## Text Overlays

```typescript
textOverlays: [
  {
    text: '#DevTips',
    startSeconds: 0,
    durationSeconds: 10,
    position: 'top',
    style: 'hashtag',           // 'title', 'subtitle', 'callout', 'label', 'hashtag'
    animation: 'fade-in',       // 'fade-in', 'slide-up', 'scale-in', 'typewriter', 'bounce-in'
  },
],
```

Platform-appropriate font sizes:
- Title: 72px (9:16), 56px (1:1), 48px (16:9)
- Subtitle: 48px (9:16), 36px (1:1), 32px (16:9)
- Callout: 56px with background pill
- Label: 32px uppercase tracking
- Hashtag: 36px with `#` prefix, accent color

## Style Configuration

```typescript
style: {
  colorScheme: 'dark',          // 'dark', 'light', 'vibrant', 'pastel', 'neon'
  accentColor: '#FFD700',
  fontFamily: 'Inter',
  borderRadius: 12,             // For image/video element corners
},
```

## Batch Multi-Platform Export

Render one piece of content across all target platforms in a single command:

```bash
bash tools/batch_render.sh \
  --project projects/MY_CLIP \
  --platforms tiktok,instagram-reel,youtube-short,square \
  --output out/
```

The batch render script:
1. Reads `clip-config.ts` for the platform list
2. For each platform, runs `npx remotion render` with platform-specific composition ID
3. Post-processes with FFmpeg for codec/bitrate optimization per platform specs
4. Generates thumbnail stills for each platform
5. Outputs all files to `out/{platform}/clip.mp4` + `out/{platform}/thumbnail.png`

## Composition Patterns

### Audio Layering

```tsx
// Voiceover with 1s delay for hook
<Sequence from={fps * 3}>
  <Audio src={staticFile('audio/voiceover.mp3')} volume={1} />
</Sequence>

// Background music (full duration, low volume)
<Audio src={staticFile('audio/bg-lofi.mp3')} volume={0.12} />

// Sound effect at specific time
<Sequence from={0}>
  <Audio src={staticFile('audio/sfx/bass-drop.mp3')} volume={0.8} />
</Sequence>
```

### Scene Transitions

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
// Custom transitions from lib/transitions/presentations/
import { swipe } from './lib/transitions/presentations/swipe';
import { zoomRush } from './lib/transitions/presentations/zoom-rush';
```

ALWAYS use `<OffthreadVideo>`, NEVER `<video>`.

## Cost Estimates

| Step | Cost | Notes |
|---|---|---|
| Voiceover (Qwen3-TTS) | ~$0.01 | Per clip, via Modal |
| Background music (MusicGen) | ~$0.02-0.05 | Duration-dependent |
| Image generation (FLUX.2) | ~$0.01/image | If AI backgrounds needed |
| Whisper transcription | Free | Runs locally via whisper.cpp — preferred over cloud APIs |
| Remotion render | Free | Local render, no license for personal use |
| Auto-reframe analysis | Free | Local OpenCV processing |

**Total per clip:** ~$0.05-0.10 for AI-generated assets. Free if using only user-provided media.

**Batch export:** Rendering 4 platform variants costs zero extra -- same Remotion render with different dimensions.

## Remotion Ecosystem Packages

Install the official Remotion skills for best results: `npx skills i remotion-dev/skills/skills/remotion`. This provides 35 production rules covering animations, audio, transitions, text, 3D, and more.

### Core Packages

| Package | What it does |
|---------|-------------|
| `@remotion/transitions` | fade, slide, wipe, flip, clockWipe, iris |
| `@remotion/captions` | TikTok-style word-by-word captions |
| `@remotion/media-utils` | `visualizeAudio()`, `getAudioData()`, `getAudioDurationInSeconds()` |
| `@remotion/layout-utils` | `measureText()`, `fitText()`, `fillTextBox()` |
| `@remotion/motion-blur` | `<Trail>` and `<CameraMotionBlur>` — use for whip-pan transitions |
| `@remotion/noise` | Procedural noise for film grain |
| `@remotion/google-fonts` | Google Fonts loading |
| `@remotion/shapes` | Geometric shape components |
| `@remotion/paths` | SVG path animation |
| `remotion-animated` | Declarative `<Animated>` with `Move()`, `Scale()`, `Fade()` |

### Community Packages

| Package | What it does |
|---------|-------------|
| **Remotion Bits** (`npx remotion-bits find/fetch`) | ParticleSystem (confetti, rain, starfields) for engagement effects, AnimatedText, StaggeredMotion |
| **GL Transitions** (`remotion-gl-transitions`) | Hundreds of GLSL shader transitions from gl-transitions.com — use for trend-matching transition styles |
| **remotion-confetti** | Canvas-based confetti with physics |

### AI Services

| Service | What it does | Cost |
|---------|-------------|------|
| **fal.ai** | Single API for video gen (Veo 3.1, Kling 3, Wan 2.2). One key for AI clip generation | $0.05-0.50/sec |
| **whisper.cpp** | LOCAL speech-to-text, zero cost. Use for transcription instead of cloud APIs | Free |
| **Suno** (via KIE) | AI music with vocals. Better than MusicGen for songs with lyrics | $0.03/song |

### Producer Intelligence

**Audio ducking:** Auto-lower music volume when voiceover speaks. Use Remotion's `interpolate()` on volume based on voiceover audio presence. Essential for voiceover clips.

**Loudness normalization:** Target LUFS per platform: YouTube -14, TikTok -14, Instagram -14, Podcast -16. Post-process:
```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 output.mp4
```

**Film grain via `@remotion/noise`:** Use `noise2D()` or `noise3D()` for procedural film grain instead of CSS overlay.

**Light leaks via `@remotion/light-leaks`:** WebGL overlays for transitions between scenes.

## Tips

1. **Hook is everything** -- spend 80% of creative effort on the first 3 seconds. If the hook fails, nothing else matters.
2. **Captions are mandatory** -- 85% of social video is watched with sound off. Always enable captions.
3. **Keep text in safe zones** -- each platform overlays UI on the video. Use the preset safe zones to avoid text behind profile icons or navigation.
4. **Match platform pacing** -- TikTok favors cuts every 2-3 seconds. Instagram tolerates slower pacing. YouTube Shorts split the difference.
5. **Use `zoom-rush` sparingly** -- one zoom-rush per clip is impactful, five is nauseating.
6. **End with CTA** -- the last 3-5 seconds should always include a call to action.
7. **Batch render always** -- if you are making a TikTok, render Reel and Short variants too. Nearly free and doubles your reach.
8. **Duration rule** -- for scenes with voiceover, set `durationSeconds` to `ceil(audio_duration + 3)` (3s buffer for hook + CTA).
9. **Test the hook first** -- use `npx remotion still --frame=0` to preview the opening frame before full render.
10. **Sound effects sell it** -- a bass-drop or whoosh on the hook frame increases perceived production quality dramatically.
