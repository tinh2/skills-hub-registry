---
name: tutorial-video
description: "Create Fireship-quality developer tutorial videos from annotated markdown and terminal recordings."
version: "0.1.1"
category: build
platforms:
  - CLAUDE_CODE
permissions:
  - filesystem
  - shell
  - network
  - api
---

# Tutorial Video

Create polished developer tutorial videos from markdown and terminal recordings. Write your tutorial as annotated markdown, record your terminal with Asciinema, and get a Fireship-quality MP4.

## Prerequisites

Requires the `video-toolkit` skill to be installed (for voiceover, image generation, talking head, cloud GPU endpoints). Also requires the `remotion` skill for composition patterns.

## Setup

### Step 1: Check State

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
python3 tools/verify_setup.py
```

### Step 2: Install Dependencies

```bash
cd $TOOLKIT
pip3 install --break-system-packages -r tools/requirements-tutorial.txt
npm install -g asciinema  # Or: brew install asciinema
```

### Step 3: Verify Cloud GPU Endpoints

Confirm `.env` in `$TOOLKIT` has Modal endpoint URLs configured (see video-toolkit skill for full setup). At minimum you need `MODAL_QWEN3_TTS_ENDPOINT_URL`. If using AI avatar, also `MODAL_FLUX2_ENDPOINT_URL` and `MODAL_SADTALKER_ENDPOINT_URL`.

### Step 4: Verify Code Hike + Shiki

```bash
cd $TOOLKIT/templates/tutorial
npm install
npx remotion studio  # Should open with sample tutorial
```

## Creating a Tutorial Video

### Step 1: Write Annotated Markdown

Create `tutorial.md` using Code Hike format:

```markdown
!!steps

## Setting Up the Project

Create a new Hono project with the Cloudflare Workers template.

\`\`\`ts ! src/index.ts
import { Hono } from 'hono'

const app = new Hono()

export default app
\`\`\`

## Adding Your First Route

Add a GET route that returns JSON.

\`\`\`ts ! src/index.ts
import { Hono } from 'hono'

const app = new Hono()

// !mark(1:3)
app.get('/', (c) => {
  return c.json({ message: 'Hello Hono!' })
})

export default app
\`\`\`
```

Each `## Heading` becomes a video step. Text below the heading becomes voiceover narration. Code blocks animate between states with Shiki Magic Move.

### Step 2: Record Terminal Demos

```bash
# Record a terminal session
asciinema rec recordings/01-setup.cast

# Replay to verify
asciinema play recordings/01-setup.cast
```

### Step 3: Create Project

```bash
cd $TOOLKIT
cp -r templates/tutorial projects/MY_TUTORIAL
cd projects/MY_TUTORIAL
npm install
```

### Step 4: Write Config

Edit `src/config/tutorial-config.ts`:

```typescript
export const tutorialConfig: TutorialConfig = {
  meta: {
    title: 'Build a REST API with Hono',
    fps: 30, width: 1920, height: 1080,
  },
  steps: [
    {
      id: 'intro',
      type: 'title',
      title: 'Build a REST API with Hono',
      narration: 'In this tutorial, you will build a REST API with Hono.',
      durationSeconds: 6,
      transition: 'fade',
    },
    {
      id: 'setup',
      type: 'terminal',
      title: 'Project Setup',
      narration: 'Start by scaffolding a new Hono project.',
      terminal: {
        castFile: 'recordings/01-setup.cast',
        theme: 'dracula',
        speed: 1.5,
      },
      transition: 'slide-left',
    },
    {
      id: 'first-route',
      type: 'code',
      title: 'Your First Route',
      narration: 'Add a GET route that returns JSON.',
      code: {
        markdownFile: 'tutorial.md',
        language: 'typescript',
        theme: 'github-dark',
        transitionFrames: 25,
      },
      transition: 'slide-left',
    },
  ],
  layout: {
    defaultLayout: 'code-only',
    padding: 40,
    cornerRadius: 12,
    showProgressBar: true,
    progressBarPosition: 'bottom',
    showChapterTitles: true,
    webcam: {
      enabled: true,
      source: 'avatar',
      file: 'webcam/avatar.mp4',
      position: 'bottom-right',
      sizePercent: 15,
      borderRadius: 50,
    },
  },
  audio: {
    voiceover: {
      provider: 'qwen3-tts',
      speaker: 'Ryan',
      tone: 'tutorial',
      stepGap: 0.5,
    },
    backgroundMusic: {
      file: 'audio/bg-music.mp3',
      volume: 0.08,
    },
  },
  theme: {
    codeTheme: 'github-dark',
    terminalTheme: 'dracula',
    backgroundColor: '#0a0a0a',
    accentColor: '#3b82f6',
    textColor: '#ffffff',
    fontFamily: 'Inter',
    codeFontFamily: 'JetBrains Mono',
  },
  export: {
    formats: [
      { name: 'youtube', width: 1920, height: 1080, fps: 30 },
      { name: 'shorts', width: 1080, height: 1920, fps: 30, maxDuration: 60 },
    ],
    outputDir: 'out/',
  },
};
```

Step types: `title`, `code`, `terminal`, `browser`, `chapter`, `outro`.

Transition types: `fade`, `slide-left`, `slide-right`, `slide-up`, `wipe`, `zoom-in`, `none`.

**Duration rule for narration:** `ceil(word_count / 2.5) + 2` seconds. Terminal and code steps auto-calculate duration from content + voiceover length.

## Asset Manifest

Each asset gets a manifest entry telling the skill what it contains, how important it is, and where it should appear in the tutorial.

```typescript
interface TutorialAsset {
  path: string;                    // relative path to file
  type: 'code' | 'terminal' | 'screenshot' | 'diagram' | 'video' | 'photo';
  description: string;             // what this asset shows — Claude uses this for placement
  tags: string[];                  // searchable: ['setup', 'api', 'database', 'demo']
  step?: number | string;          // which tutorial step this belongs to
  weight: 1 | 2 | 3 | 4 | 5;     // 1=brief flash, 3=standard, 5=key concept (linger)
  zoomRegion?: {                   // auto-zoom to this region when showing
    x: number; y: number;
    width: number; height: number;
  };
  annotations?: string[];          // callouts: ['highlight line 12', 'arrow to submit button']
  duration?: number;               // suggested screen time in seconds
  notes?: string;                  // special instructions
}

interface TutorialManifest {
  assets: TutorialAsset[];
  defaults: {
    weight: number;
    durationByWeight: {
      1: number; // 2s — quick flash
      2: number; // 4s — brief show
      3: number; // 6s — standard explanation
      4: number; // 8s — important concept
      5: number; // 12s — key concept, linger for comprehension
    };
  };
}
```

### How Weights Work for Tutorials

| Weight | Role | Screen Time | Voiceover | Effects |
|--------|------|-------------|-----------|---------|
| 5 — Key Concept | Core lesson, aha moment | 10-15s | Detailed explanation | Slow zoom, highlight, pause |
| 4 — Important | Significant step | 6-10s | Clear walkthrough | Zoom to region, annotations |
| 3 — Standard | Normal tutorial step | 4-6s | Brief narration | Standard code transition |
| 2 — Context | Supporting visual | 2-4s | Quick mention | Quick show, no zoom |
| 1 — Reference | Brief flash | 1-2s | None or "as you can see" | Flash on screen |

### Smart Placement Rules

- Assets tagged `setup` or `install` → early in tutorial (Chapter 1)
- Assets tagged `demo` or `result` → after the code that produces them
- `type: 'terminal'` → played back with typing animation, paused at key outputs
- `type: 'code'` with step numbers → ordered by step, animated transitions between steps
- `type: 'screenshot'` with zoomRegion → auto-zoom + highlight
- `type: 'diagram'` → shown during concept explanation, held longer
- `weight: 5` assets get the voiceover's most detailed explanation
- `weight: 1-2` assets appear in rapid montage sections or are skipped if runtime is tight

### Example

```typescript
const manifest: TutorialManifest = {
  assets: [
    {
      path: 'recordings/npm-install.cast',
      type: 'terminal',
      description: 'Running npm install and seeing the dependency tree',
      tags: ['setup', 'install'],
      step: 1,
      weight: 2,
      duration: 4,
    },
    {
      path: 'code/api-handler.ts',
      type: 'code',
      description: 'The main API route handler showing the GET endpoint',
      tags: ['api', 'core'],
      step: 3,
      weight: 5,
      annotations: ['highlight lines 8-15: this is where the magic happens'],
      notes: 'This is THE key code. Linger here, explain each line.',
    },
    {
      path: 'screenshots/browser-result.png',
      type: 'screenshot',
      description: 'Browser showing the JSON response from our API',
      tags: ['demo', 'result'],
      step: 4,
      weight: 3,
      zoomRegion: { x: 100, y: 200, width: 600, height: 300 },
    },
  ],
  defaults: {
    weight: 3,
    durationByWeight: { 1: 2, 2: 4, 3: 6, 4: 8, 5: 12 },
  },
};
```

### Step 5: Parse Markdown

```bash
cd $TOOLKIT
python3 tools/parse_tutorial.py \
  --input projects/MY_TUTORIAL/tutorial.md \
  --output projects/MY_TUTORIAL/src/config/parsed-steps.json
```

### Step 6: Generate Voiceover

```bash
cd $TOOLKIT
python3 tools/generate_voiceover.py \
  --config projects/MY_TUTORIAL/src/config/tutorial-config.ts \
  --output-dir projects/MY_TUTORIAL/public/audio/voiceover/ \
  --provider qwen3-tts --speaker Ryan --tone tutorial \
  --cloud modal
```

### Step 7: Generate Focus Regions (optional)

Auto-detect zoom regions from code diffs:

```bash
cd $TOOLKIT
python3 tools/detect_focus.py \
  --config projects/MY_TUTORIAL/src/config/tutorial-config.ts \
  --output projects/MY_TUTORIAL/src/config/focus-regions.json
```

### Step 8: Extract Terminal Timing (optional)

Extract timing keyframes from `.cast` files for auto-generated pause points:

```bash
cd $TOOLKIT
python3 tools/cast_to_keyframes.py \
  --input projects/MY_TUTORIAL/recordings/01-setup.cast \
  --speed 1.5 \
  --max-idle 2.0 \
  --output projects/MY_TUTORIAL/src/config/cast-timing.json
```

### Step 9: Generate Background Music (optional)

```bash
cd $TOOLKIT
python3 tools/music_gen.py \
  --preset lofi \
  --duration 300 \
  --output projects/MY_TUTORIAL/public/audio/bg-music.mp3 \
  --cloud modal
```

Presets: `corporate-bg`, `upbeat-tech`, `ambient`, `dramatic`, `tension`, `hopeful`, `cta`, `lofi`.

### Step 10: Preview and Render

```bash
cd $TOOLKIT/projects/MY_TUTORIAL

# Real-time preview
npx remotion studio

# Render YouTube format
npx remotion render TutorialVideo out/tutorial-youtube.mp4

# Render TikTok/Shorts format
npx remotion render TutorialVideoVertical out/tutorial-shorts.mp4

# Instagram Square (1:1)
npx remotion render TutorialVideoSquare out/tutorial-square.mp4
```

### Step 11: Post-Process (optional)

```bash
# Add intro/outro bumper
ffmpeg -f concat -safe 0 -i concat-list.txt -c copy out/final.mp4

# Optimize for web streaming
ffmpeg -i out/tutorial-youtube.mp4 -movflags +faststart out/tutorial-youtube-web.mp4
```

Output: `out/tutorial-youtube.mp4`

## Layout Modes

| Mode | Description | Use when |
|---|---|---|
| `code-only` | Full-screen animated code | Showing code changes |
| `terminal-only` | Full-screen terminal replay | Running CLI commands |
| `code-terminal` | Side-by-side code + terminal | Showing code and its output |
| `code-browser` | Side-by-side code + browser | Web development tutorials |
| `fullscreen` | Full-screen screenshot/image | Architecture diagrams, UI demos |
| `split-view` | 50/50 configurable split | Comparing before/after |
| `picture-in-picture` | Main content + PiP overlay | Webcam or avatar talking head |

## Animated Code Transitions

Code transitions use Shiki Magic Move (token-level FLIP animations):

- **Move:** Tokens that exist in both states animate to their new position
- **Enter:** New tokens fade in and slide from the right
- **Leave:** Removed tokens fade out and slide to the left

Supported annotations in Code Hike markdown:
- `// !mark(1:3)` -- Highlight lines 1-3
- `// !fold(5:10)` -- Collapse lines 5-10
- `// !callout[This is important]` -- Callout annotation

150+ languages supported via Shiki. Themes: `github-dark`, `github-light`, `dracula`, `monokai`, `one-dark-pro`, `vitesse-dark`, etc.

## Terminal Replay

Asciinema recordings play back inside the video with frame-perfect sync:

- **Speed control:** `speed: 1.5` plays back at 1.5x
- **Idle compression:** `maxIdleTime: 2.0` caps gaps between keystrokes at 2 seconds
- **Pause points:** `pauseAt: [{ time: 3.2, duration: 2, annotation: 'Note this output' }]`
- **Themes:** `dracula`, `monokai`, `solarized-dark`, `solarized-light`, `tango`

## Auto-Zoom Effects

Define focus regions per step to zoom into specific code or terminal areas:

```typescript
focusRegions: [
  { startFrame: 0, x: 10, y: 40, width: 80, height: 30, zoom: 1.8 },
  { startFrame: 90, x: 10, y: 55, width: 80, height: 35, zoom: 1.6 },
]
```

Zoom transitions use Remotion `spring()` with high damping for smooth, non-bouncy motion. Auto-zoom regions can also be auto-generated from code diffs using `tools/detect_focus.py`.

## Focus Highlight

Dims everything outside a focus region (spotlight effect):

```typescript
focusHighlight: {
  enabled: true,
  opacity: 0.6,           // Dim overlay opacity
  borderRadius: 8,
  featheredEdges: true,    // Soft edges via box-shadow blur
}
```

The spotlight window animates with `spring()` when the focus region changes. Used automatically when `focusRegions` are defined on a step.

## Smooth Cursor

Animated cursor overlay with Bezier interpolation between keyframe positions:

```typescript
cursor: {
  enabled: true,
  keyframes: [
    { frame: 0, x: 50, y: 50 },
    { frame: 30, x: 200, y: 100, click: true },
    { frame: 60, x: 400, y: 300 },
  ],
  showTrail: true,
  trailLength: 4,
}
```

- **Bezier interpolation:** Smooth curves between positions (no jerky linear movement)
- **Click ripple:** Expanding ring animation on click events
- **Motion trail:** 3-5 ghost cursors at decreasing opacity following the main cursor

## Webcam / Avatar PiP

Add a talking head overlay:

**Option A: Real webcam recording**
Record separately, reference in config:
```typescript
webcam: {
  enabled: true,
  source: 'file',
  file: 'webcam/recording.mp4',
  position: 'bottom-right',
  sizePercent: 15,
  borderRadius: 50,
}
```

**Option B: AI avatar (SadTalker)**
Generate from a portrait image + voiceover audio:
```bash
cd $TOOLKIT
python3 tools/flux2.py --prompt "Professional developer, dark background" \
  --width 1024 --height 576 --output projects/MY_TUTORIAL/public/webcam/presenter.png --cloud modal

python3 tools/sadtalker.py \
  --image projects/MY_TUTORIAL/public/webcam/presenter.png \
  --audio projects/MY_TUTORIAL/public/audio/voiceover/01-intro.mp3 \
  --preprocess full --still --expression-scale 0.8 \
  --output projects/MY_TUTORIAL/public/webcam/avatar-01.mp4 --cloud modal
```

**SadTalker rules:** ALWAYS use `--preprocess full` and `--still`. Generate per-step clips, NEVER one long video.

## Step Annotations

Overlay arrows, callouts, and highlights on any step:

```typescript
annotations: [
  {
    type: 'arrow',
    x: 45, y: 60,
    direction: 'down',
    text: 'This line is key',
    showAtFrame: 30,
    durationFrames: 90,
  },
  {
    type: 'highlight',
    x: 10, y: 55,
    width: 80, height: 8,
    color: '#3b82f680',
    showAtFrame: 0,
  },
]
```

Types: `arrow`, `callout`, `highlight`, `circle`, `underline`, `box`.

## Progress Bar + Chapter Markers

The progress bar fills proportionally to the current frame and shows chapter markers as dots at step boundaries:

```typescript
layout: {
  showProgressBar: true,
  progressBarPosition: 'bottom',  // 'top' or 'bottom'
  showChapterTitles: true,
}
```

- Chapter markers appear as dots at each step boundary on the progress bar
- Chapter title animates in with a staggered spring at step start, auto-dismisses after 1.5s
- Both components respect theme `accentColor` and `textColor`

## Social Format Export

Export from the same source to multiple formats:

| Format | Resolution | FPS | Max Duration |
|---|---|---|---|
| YouTube | 1920x1080 | 30 | -- |
| TikTok | 1080x1920 | 30 | 180s |
| YouTube Shorts | 1080x1920 | 30 | 60s |
| Square (Instagram) | 1080x1080 | 30 | -- |

Vertical formats auto-reflow: code gets larger font, terminal stacks above narration, PiP moves to top. See Step 10 for render commands.

## Composition Patterns

### Per-Step Audio (1s delay)

```tsx
<Sequence from={30}>
  <Audio src={staticFile('audio/voiceover/01-intro.mp3')} volume={1} />
</Sequence>
```

### Background Music (full duration)

```tsx
<Audio src={staticFile('audio/bg-music.mp3')} volume={0.08} />
```

### Narrator PiP

```tsx
<Sequence from={30}>
  <OffthreadVideo
    src={staticFile('webcam/avatar-01.mp4')}
    style={{ width: 320, height: 180, objectFit: 'cover' }}
    muted
  />
</Sequence>
```

ALWAYS use `<OffthreadVideo>`, NEVER `<video>`.

### Transitions

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
```

Import custom transitions from `lib/transitions/presentations/` directly, never from barrel.

## Cost Estimates

| Step | Cost | Notes |
|---|---|---|
| Voiceover (Qwen3-TTS) | ~$0.01/step | ~20s warm GPU via Modal |
| AI avatar (SadTalker) | ~$0.05-0.20/step | ~3-4 min per 10s audio |
| Background music (MusicGen) | ~$0.02-0.05 | Duration-dependent |
| Presenter portrait (FLUX.2) | ~$0.01 | One-time |
| Remotion render | Free (local) | ~2-5 min for 5-min video |

**Total 5-minute tutorial:** ~$0.50-2.00 with AI avatar, ~$0.10-0.50 without.

## Remotion Ecosystem Packages

Install the official Remotion skills for best results: `npx skills i remotion-dev/skills/skills/remotion`. This provides 35 production rules covering animations, audio, transitions, text, 3D, and more.

### Core Packages

| Package | What it does |
|---------|-------------|
| `@remotion/transitions` | fade, slide, wipe, flip, clockWipe, iris |
| `@remotion/captions` | TikTok-style word-by-word captions |
| `@remotion/media-utils` | `visualizeAudio()`, `getAudioData()`, `getAudioDurationInSeconds()` |
| `@remotion/layout-utils` | `measureText()`, `fitText()`, `fillTextBox()` — use for dynamic code block sizing |
| `@remotion/noise` | Procedural noise for film grain |
| `@remotion/google-fonts` | Google Fonts loading |
| `@remotion/shapes` | Geometric shape components — use for overlays in explanations |
| `@remotion/paths` | SVG path animation — use for animated diagrams and flowcharts |
| `remotion-animated` | Declarative `<Animated>` with `Move()`, `Scale()`, `Fade()` |

### Community Packages

| Package | What it does |
|---------|-------------|
| **Remotion Bits** (`npx remotion-bits find/fetch`) | ParticleSystem, AnimatedText (char/word/line stagger), StaggeredMotion — use AnimatedText for step titles |
| **GL Transitions** (`remotion-gl-transitions`) | Hundreds of GLSL shader transitions from gl-transitions.com |
| **remotion-confetti** | Canvas-based confetti with physics |

### AI Services

| Service | What it does | Cost |
|---------|-------------|------|
| **fal.ai** | Single API for video gen (Veo 3.1, Kling 3, Wan 2.2). One key, all models | $0.05-0.50/sec |
| **whisper.cpp** | LOCAL speech-to-text, zero cost. Use for caption generation instead of cloud APIs | Free |
| **Suno** (via KIE) | AI music with vocals. Better than MusicGen for songs with lyrics | $0.03/song |

### Producer Intelligence

**Audio ducking:** Auto-lower music volume when voiceover speaks. Use Remotion's `interpolate()` on volume based on voiceover audio presence.

**Loudness normalization:** Target LUFS per platform: YouTube -14, TikTok -14, Instagram -14, Podcast -16. Post-process:
```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 output.mp4
```

**Film grain via `@remotion/noise`:** Use `noise2D()` or `noise3D()` for procedural film grain instead of CSS overlay.

**Light leaks via `@remotion/light-leaks`:** WebGL overlays for transitions between acts/scenes.

## Key Rules

1. **All animation via `useCurrentFrame()` + `interpolate()`/`spring()`.** No CSS transitions or Tailwind animation classes.
2. **Always `staticFile()`** for assets. Never `require()`.
3. **Always `<OffthreadVideo>`** for webcam/avatar. Never `<video>`.
4. **Always `--preprocess full --still`** for SadTalker.
5. **Generate voiceover per step,** never as one long audio file.
6. **Duration = `ceil(word_count / 2.5) + 2`** for narration-driven steps.
7. **Run all tools from `$TOOLKIT` root,** not from the project directory.

Source: Built on [remotion.dev/templates/code-hike](https://remotion.dev/templates/code-hike), [codehike.org](https://codehike.org), [shikijs/shiki-magic-move](https://github.com/shikijs/shiki-magic-move), [asciinema.org](https://asciinema.org)
