# Engineering Spec: `/tutorial-video` Skill

> Version 0.1.0 | 2026-03-26 | Status: Draft

---

## 1. Overview

### What it does

The `/tutorial-video` skill generates polished developer tutorial videos from annotated markdown and terminal recordings. Write your tutorial as Code Hike-formatted markdown with `!!steps` sections, point at Asciinema `.cast` files for terminal demos, and get a Fireship-quality video rendered via Remotion -- entirely from the CLI.

### Target user

Developer educators, open-source maintainers, DevRel engineers, and content creators who can write markdown but do not want to learn Premiere, After Effects, or spend $29-65/month on Screen Studio or Descript.

### Value proposition

- **One tool, one workflow.** No stitching together OBS + Premiere + ElevenLabs + Canva. Write markdown, record your terminal, run a command, get an MP4.
- **Code transitions that teach.** Shiki Magic Move animates token-level diffs between code states so viewers see exactly what changed, not a wall of new code.
- **Terminal demos baked in.** Asciinema recordings replay inside the video with theme control, speed adjustment, and pause-at-key-moments.
- **Screen Studio-grade zoom effects.** Programmatic auto-zoom follows focus areas with spring physics, smooth Bezier cursor animation, and spotlight dimming.
- **AI voiceover per step.** Qwen3-TTS or ElevenLabs generates narration from your markdown text -- no microphone needed.
- **Social-ready output.** Export 16:9 for YouTube, 9:16 for TikTok/Shorts from the same source.

### Competitive positioning

| Competitor | Price | What we beat them on |
|---|---|---|
| Screen Studio | $9-29/mo | No code animation, no terminal replay, no voiceover, GUI-only |
| Descript | Free-$65/mo | No code animation, no CLI workflow, no Remotion composability |
| Code Hike | Free (OSS) | Code animation only -- no video output, no voiceover, no zoom |
| Guidde | ~$50/mo | Chrome-only capture, no code animation, no terminal replay |
| Synthesia | $18+/mo | Avatar-only, no code, no terminal, no developer workflow |

We combine Code Hike's animated code (unique to us + Code Hike), Asciinema's terminal replay (unique to us), and Screen Studio's zoom effects (replicated programmatically) in a single CLI-driven pipeline. No competitor does all three.

---

## 2. Architecture

### Relationship to existing skills

```
build/video-toolkit/        <-- Existing. Voiceover, image gen, music gen, talking head, cloud GPU.
build/remotion/             <-- Existing. Remotion composition patterns, animations, rendering.
build/ffmpeg-media/         <-- Existing. Post-processing, format conversion, social export.
build/tutorial-video/       <-- NEW. This skill. Tutorial-specific pipeline.
```

The tutorial-video skill **delegates to** video-toolkit for voiceover generation (Qwen3-TTS, ElevenLabs), talking head animation (SadTalker), and cloud rendering (Modal). It **delegates to** remotion for composition patterns (Sequence, spring, interpolate). It **delegates to** ffmpeg-media for post-processing and social format export. It adds no duplicate functionality.

### New components (all in Remotion/React)

| Component | Purpose | Depends on |
|---|---|---|
| `<AnimatedCode>` | Renders Code Hike parsed steps with Shiki Magic Move transitions | `@code-hike/mdx`, `shiki-magic-move` |
| `<TerminalReplay>` | Embeds asciinema-player, seeks per frame | `asciinema-player` |
| `<AutoZoom>` | Spring-based zoom-to-region with focus keyframes | Remotion `spring()`, `interpolate()` |
| `<SmoothCursor>` | Bezier-smoothed cursor movement replay | Remotion `interpolate()` |
| `<FocusHighlight>` | Dims everything outside focus region | CSS overlay |
| `<ProgressBar>` | Timeline with chapter markers and current position | Config-driven |
| `<ChapterTitle>` | Animated chapter title card between steps | Remotion `spring()` |
| `<WebcamPiP>` | Picture-in-picture webcam or AI avatar overlay | `<OffthreadVideo>` or SadTalker |
| `<StepAnnotation>` | Arrows, callouts, highlights overlaid on content | SVG + Remotion animation |
| `<TutorialComposition>` | Root composition wiring all components together | All above |

### New tools (Python/CLI)

| Tool | Purpose |
|---|---|
| `tools/parse_tutorial.py` | Parses Code Hike markdown into JSON step structure |
| `tools/generate_voiceover.py` | Generates per-step voiceover audio via Qwen3-TTS or ElevenLabs |
| `tools/detect_focus.py` | Analyzes code diffs to auto-generate focus region keyframes |
| `tools/cast_to_keyframes.py` | Extracts timing keyframes from `.cast` files for terminal replay |

### Directory structure

```
build/tutorial-video/
  SKILL.md                     # Skill definition (see Section 7)
  templates/
    tutorial/                  # Remotion project template
      src/
        components/
          AnimatedCode.tsx
          TerminalReplay.tsx
          AutoZoom.tsx
          SmoothCursor.tsx
          FocusHighlight.tsx
          ProgressBar.tsx
          ChapterTitle.tsx
          WebcamPiP.tsx
          StepAnnotation.tsx
        compositions/
          TutorialComposition.tsx
        config/
          tutorial-config.ts   # TypeScript config schema
        lib/
          codehike-parser.ts   # Code Hike integration
          shiki-animator.ts    # Shiki Magic Move integration
          asciinema-bridge.ts  # Asciinema player bridge
          zoom-engine.ts       # Auto-zoom calculation
          cursor-smoother.ts   # Bezier cursor smoothing
      public/
        audio/                 # Generated voiceover files
        recordings/            # .cast terminal recordings
        webcam/                # Webcam/avatar video files
      package.json
      tsconfig.json
  tools/
    parse_tutorial.py
    generate_voiceover.py
    detect_focus.py
    cast_to_keyframes.py
    requirements.txt
```

---

## 3. Data Model

### Tutorial config schema (TypeScript)

```typescript
// tutorial-config.ts

export interface TutorialConfig {
  meta: TutorialMeta;
  steps: TutorialStep[];
  layout: LayoutConfig;
  audio: AudioConfig;
  theme: ThemeConfig;
  export: ExportConfig;
}

export interface TutorialMeta {
  title: string;
  subtitle?: string;
  author?: string;
  duration?: number;                    // Override total duration in seconds
  fps: number;                          // Default: 30
  width: number;                        // Default: 1920
  height: number;                       // Default: 1080
}

export interface TutorialStep {
  id: string;                           // Unique step identifier
  type: 'code' | 'terminal' | 'browser' | 'title' | 'chapter' | 'outro';
  title?: string;                       // Chapter/section title
  durationSeconds?: number;             // Override auto-calculated duration
  narration?: string;                   // Text for voiceover generation
  voiceoverFile?: string;               // Pre-recorded voiceover path
  layout?: LayoutMode;                  // Override global layout for this step
  transition?: TransitionType;          // Transition into this step

  // Code step fields
  code?: CodeStepConfig;

  // Terminal step fields
  terminal?: TerminalStepConfig;

  // Browser step fields
  browser?: BrowserStepConfig;

  // Annotations overlaid on this step
  annotations?: Annotation[];

  // Focus/zoom regions for this step
  focusRegions?: FocusRegion[];
}

export interface CodeStepConfig {
  /** Path to Code Hike annotated markdown file */
  markdownFile?: string;
  /** Inline code states (alternative to markdown file) */
  states?: CodeState[];
  /** Programming language for syntax highlighting */
  language: string;
  /** Shiki theme */
  theme?: string;                       // Default: 'github-dark'
  /** Lines to highlight */
  highlights?: LineRange[];
  /** Lines to fold/collapse */
  folds?: LineRange[];
  /** Animation duration between states in frames */
  transitionFrames?: number;            // Default: 20
  /** Font size in pixels */
  fontSize?: number;                    // Default: 18
  /** Show line numbers */
  lineNumbers?: boolean;                // Default: true
}

export interface CodeState {
  code: string;
  filename?: string;                    // Tab/filename display
  highlights?: LineRange[];
  folds?: LineRange[];
  annotations?: InlineAnnotation[];
}

export interface LineRange {
  from: number;
  to: number;
}

export interface InlineAnnotation {
  line: number;
  column?: number;
  text: string;
  type: 'callout' | 'highlight' | 'underline' | 'box';
}

export interface TerminalStepConfig {
  /** Path to .cast (Asciinema) file */
  castFile: string;
  /** Terminal theme */
  theme?: string;                       // Default: 'dracula'
  /** Override terminal dimensions */
  cols?: number;
  rows?: number;
  /** Playback speed multiplier */
  speed?: number;                       // Default: 1.0
  /** Timestamps to pause at (seconds into recording) */
  pauseAt?: PausePoint[];
  /** Maximum idle time between keystrokes (seconds) */
  maxIdleTime?: number;                 // Default: 2.0
  /** Font size in pixels */
  fontSize?: number;                    // Default: 16
}

export interface PausePoint {
  time: number;                         // Seconds into .cast recording
  duration: number;                     // Pause duration in seconds
  annotation?: string;                  // Optional callout text during pause
}

export interface BrowserStepConfig {
  /** Screenshot or screen recording path */
  mediaFile: string;
  /** URL to display in fake browser chrome */
  url?: string;
  /** Browser chrome style */
  browserStyle?: 'macos' | 'windows' | 'minimal' | 'none';
}

export interface Annotation {
  type: 'arrow' | 'callout' | 'highlight' | 'circle' | 'underline' | 'box';
  /** Position as percentage of composition (0-100) */
  x: number;
  y: number;
  /** Size/length for arrows */
  width?: number;
  height?: number;
  /** Arrow direction */
  direction?: 'up' | 'down' | 'left' | 'right';
  /** Callout text */
  text?: string;
  /** Color override */
  color?: string;
  /** When to show (frame offset within step) */
  showAtFrame?: number;
  /** Duration in frames */
  durationFrames?: number;
}

export interface FocusRegion {
  /** Frame offset within step when zoom begins */
  startFrame: number;
  /** Target region as percentage of composition */
  x: number;
  y: number;
  width: number;
  height: number;
  /** Zoom level (1.0 = no zoom, 2.0 = 2x zoom) */
  zoom?: number;                        // Default: auto-calculated from region size
  /** Spring config for zoom animation */
  springConfig?: {
    damping?: number;                   // Default: 200 (smooth, no bounce)
    stiffness?: number;                 // Default: 100
    mass?: number;                      // Default: 1
  };
}

export type LayoutMode =
  | 'code-only'                         // Full-screen code
  | 'terminal-only'                     // Full-screen terminal
  | 'code-terminal'                     // Side-by-side code + terminal
  | 'code-browser'                      // Side-by-side code + browser
  | 'fullscreen'                        // Full-screen media/screenshot
  | 'split-view'                        // 50/50 split (configurable content)
  | 'picture-in-picture';              // Main content + PiP overlay

export type TransitionType =
  | 'fade'
  | 'slide-left'
  | 'slide-right'
  | 'slide-up'
  | 'wipe'
  | 'zoom-in'
  | 'none';

export interface LayoutConfig {
  defaultLayout: LayoutMode;            // Default: 'code-only'
  padding: number;                      // Default: 40
  cornerRadius: number;                 // Default: 12
  showProgressBar: boolean;             // Default: true
  progressBarPosition: 'top' | 'bottom'; // Default: 'bottom'
  showChapterTitles: boolean;           // Default: true
  webcam?: WebcamConfig;
}

export interface WebcamConfig {
  enabled: boolean;
  source: 'file' | 'avatar';
  /** Path to webcam recording or SadTalker output */
  file?: string;
  /** Position of PiP */
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  /** Size as percentage of composition width */
  sizePercent: number;                  // Default: 15
  /** Border radius */
  borderRadius: number;                 // Default: 50 (circle)
  /** Border color */
  borderColor?: string;
}

export interface AudioConfig {
  voiceover: VoiceoverConfig;
  backgroundMusic?: {
    file: string;
    volume: number;                     // Default: 0.08
  };
}

export interface VoiceoverConfig {
  provider: 'qwen3-tts' | 'elevenlabs';
  /** Qwen3-TTS speaker */
  speaker?: string;                     // Default: 'Ryan'
  /** Qwen3-TTS tone */
  tone?: string;                        // Default: 'tutorial'
  /** ElevenLabs voice ID */
  voiceId?: string;
  /** Reference audio for voice cloning */
  refAudio?: string;
  refText?: string;
  /** Silence padding between steps in seconds */
  stepGap: number;                      // Default: 0.5
}

export interface ThemeConfig {
  /** Code editor theme */
  codeTheme: string;                    // Default: 'github-dark'
  /** Terminal theme */
  terminalTheme: string;               // Default: 'dracula'
  /** Background color */
  backgroundColor: string;              // Default: '#0a0a0a'
  /** Accent color for highlights, progress bar, annotations */
  accentColor: string;                  // Default: '#3b82f6'
  /** Text color */
  textColor: string;                    // Default: '#ffffff'
  /** Font family for UI text (not code) */
  fontFamily: string;                   // Default: 'Inter'
  /** Code font family */
  codeFontFamily: string;              // Default: 'JetBrains Mono'
}

export interface ExportConfig {
  formats: ExportFormat[];
  outputDir: string;                    // Default: 'out/'
}

export interface ExportFormat {
  name: string;                         // e.g., 'youtube', 'tiktok', 'shorts'
  width: number;
  height: number;
  fps: number;
  maxDuration?: number;                 // Seconds -- for platform limits
}

// Preset export formats
export const EXPORT_PRESETS = {
  youtube: { name: 'youtube', width: 1920, height: 1080, fps: 30 },
  tiktok: { name: 'tiktok', width: 1080, height: 1920, fps: 30, maxDuration: 180 },
  shorts: { name: 'shorts', width: 1080, height: 1920, fps: 30, maxDuration: 60 },
  square: { name: 'square', width: 1080, height: 1080, fps: 30 },
} as const;
```

### Example config

```typescript
export const tutorialConfig: TutorialConfig = {
  meta: {
    title: 'Build a REST API with Hono in 5 Minutes',
    subtitle: 'From zero to deployed on Cloudflare Workers',
    author: 'Tho Le',
    fps: 30,
    width: 1920,
    height: 1080,
  },
  steps: [
    {
      id: 'intro',
      type: 'title',
      title: 'Build a REST API with Hono',
      narration: 'In this tutorial, you will build and deploy a REST API using Hono and Cloudflare Workers in under five minutes.',
      durationSeconds: 6,
      transition: 'fade',
    },
    {
      id: 'scaffold',
      type: 'terminal',
      title: 'Project Setup',
      narration: 'First, scaffold a new Hono project using the create-hono CLI.',
      terminal: {
        castFile: 'recordings/01-scaffold.cast',
        theme: 'dracula',
        speed: 1.5,
        pauseAt: [
          { time: 3.2, duration: 2, annotation: 'Select the cloudflare-workers template' },
        ],
      },
      transition: 'slide-left',
    },
    {
      id: 'first-route',
      type: 'code',
      title: 'Your First Route',
      narration: 'Hono uses a familiar Express-like routing API. Define a GET route that returns JSON.',
      code: {
        language: 'typescript',
        states: [
          {
            filename: 'src/index.ts',
            code: `import { Hono } from 'hono'\n\nconst app = new Hono()\n\napp.get('/', (c) => {\n  return c.text('Hello Hono!')\n})\n\nexport default app`,
          },
          {
            filename: 'src/index.ts',
            code: `import { Hono } from 'hono'\n\nconst app = new Hono()\n\napp.get('/', (c) => {\n  return c.json({ message: 'Hello Hono!', version: '1.0.0' })\n})\n\napp.get('/users', (c) => {\n  return c.json({ users: [] })\n})\n\nexport default app`,
            highlights: [{ from: 6, to: 6 }, { from: 9, to: 11 }],
          },
        ],
        transitionFrames: 25,
      },
      focusRegions: [
        { startFrame: 0, x: 10, y: 40, width: 80, height: 30, zoom: 1.8 },
        { startFrame: 90, x: 10, y: 55, width: 80, height: 35, zoom: 1.6 },
      ],
      transition: 'slide-left',
    },
    {
      id: 'deploy',
      type: 'terminal',
      title: 'Deploy',
      narration: 'Deploy to Cloudflare Workers with a single command. Your API is live in seconds.',
      terminal: {
        castFile: 'recordings/03-deploy.cast',
        theme: 'dracula',
        speed: 1.0,
        pauseAt: [
          { time: 8.5, duration: 3, annotation: 'Your API is live at this URL' },
        ],
      },
      transition: 'slide-left',
    },
    {
      id: 'outro',
      type: 'outro',
      title: 'Next Steps',
      narration: 'That is it. A deployed REST API in under five minutes. Check the description for the full source code.',
      durationSeconds: 8,
      transition: 'fade',
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
      file: 'audio/bg-lofi.mp3',
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

---

## 4. Components

### 4.1 `<AnimatedCode>`

Renders syntax-highlighted code that animates between states using Shiki Magic Move.

```typescript
interface AnimatedCodeProps {
  states: CodeState[];
  language: string;
  theme: string;
  currentStateIndex: number;        // Driven by frame
  transitionProgress: number;       // 0 to 1, driven by interpolate()
  fontSize: number;
  lineNumbers: boolean;
  fontFamily: string;
  width: number;
  height: number;
}
```

**Implementation notes:**
- Uses `codeToKeyedTokens()` from `shiki-magic-move/core` to tokenize each state
- Uses `createMagicMoveMachine()` to compute token-level FLIP animations (Move, Enter, Leave)
- Each token gets `transform`, `opacity`, and optional `color` interpolation
- Wraps in a container with editor chrome (title bar, dots, filename tab)
- Line highlights render as semi-transparent colored backgrounds
- Line folds collapse with spring animation

### 4.2 `<TerminalReplay>`

Renders an Asciinema recording synchronized to the video timeline.

```typescript
interface TerminalReplayProps {
  castFile: string;                 // Path to .cast file
  theme: string;
  cols: number;
  rows: number;
  speed: number;
  pauseAt: PausePoint[];
  maxIdleTime: number;
  fontSize: number;
  fontFamily: string;
  width: number;
  height: number;
  /** Current frame within this step's Sequence */
  currentFrame: number;
  fps: number;
}
```

**Implementation notes:**
- Parses the `.cast` file (asciicast v2 format: JSON header + newline-delimited event array) at build time
- Each event is `[timestamp, type, data]` where type is "o" (output) or "i" (input)
- Pre-computes a frame-to-terminal-state map: for each video frame, determine which events have fired
- Renders terminal output using a virtual terminal emulator (xterm.js in headless mode or custom renderer)
- Pause points insert dead time: events after the pause timestamp are delayed by `pause.duration` seconds
- Idle compression: consecutive events with gap > `maxIdleTime` are compressed to `maxIdleTime`
- Terminal chrome: rounded container with title bar showing `$ bash` or custom title
- Typing cursor: blinking block cursor positioned at last output position

### 4.3 `<AutoZoom>`

Smoothly zooms the composition to focus on specific regions.

```typescript
interface AutoZoomProps {
  children: React.ReactNode;
  focusRegions: FocusRegion[];
  currentFrame: number;
  fps: number;
  compositionWidth: number;
  compositionHeight: number;
}
```

**Implementation notes:**
- Maintains a "virtual camera" position (x, y, zoom) that interpolates between focus regions
- Uses `spring()` with high damping (200) for smooth, non-bouncy transitions
- When no focus region is active, returns to default (zoom 1.0, centered)
- Applied as CSS `transform: scale() translate()` on a wrapper div
- Zoom level auto-calculated from region size if not specified: `zoom = compositionWidth / (regionWidth * compositionWidth / 100)`
- Easing: starts slow, accelerates, decelerates to stop (spring physics handles this naturally)

### 4.4 `<SmoothCursor>`

Renders a cursor that follows a path with Bezier smoothing.

```typescript
interface SmoothCursorProps {
  keyframes: CursorKeyframe[];
  currentFrame: number;
  fps: number;
  /** Cursor style */
  style?: 'default' | 'pointer' | 'text' | 'dot';
  /** Trail effect */
  showTrail?: boolean;
  /** Click animation */
  showClicks?: boolean;
}

interface CursorKeyframe {
  frame: number;
  x: number;
  y: number;
  click?: boolean;
}
```

**Implementation notes:**
- Raw keyframe positions are smoothed using cubic Bezier interpolation between consecutive points
- Click events trigger a ripple animation (expanding circle that fades out)
- Optional motion trail: 3-5 ghost cursors at previous positions with decreasing opacity
- Cursor SVG rendered at native resolution, composited on top of all other content

### 4.5 `<FocusHighlight>`

Dims everything outside a focus region.

```typescript
interface FocusHighlightProps {
  x: number;                        // Percentage
  y: number;
  width: number;
  height: number;
  opacity: number;                  // Dim overlay opacity (0-1), default 0.6
  borderRadius?: number;
  transitionProgress: number;       // For animated entry/exit
}
```

**Implementation notes:**
- Full-screen semi-transparent black overlay with a transparent "window" cut out via CSS `clip-path` or SVG mask
- Window position and size animate with `spring()`
- Feathered edges via box-shadow or SVG filter blur on the mask

### 4.6 `<ProgressBar>`

Shows tutorial progress with chapter markers.

```typescript
interface ProgressBarProps {
  steps: { id: string; title: string; startFrame: number; endFrame: number }[];
  currentFrame: number;
  totalFrames: number;
  position: 'top' | 'bottom';
  accentColor: string;
  height?: number;                  // Default: 4
}
```

**Implementation notes:**
- Thin bar spanning composition width
- Filled portion = `currentFrame / totalFrames`
- Chapter markers: small dots or ticks at each step boundary
- Current chapter title fades in/out above the bar
- Subtle glow on the progress indicator

### 4.7 `<ChapterTitle>`

Animated chapter title card shown at the start of each step.

```typescript
interface ChapterTitleProps {
  title: string;
  stepNumber: number;
  totalSteps: number;
  accentColor: string;
  fontFamily: string;
  animationProgress: number;        // 0 to 1 (spring-driven)
}
```

**Implementation notes:**
- Step number and title animate in with staggered spring (number slides up, title fades in 5 frames later)
- Small accent-colored line or pill behind the step number
- Auto-dismisses after 1.5 seconds with fade-out
- Positioned top-left, does not obstruct content

### 4.8 `<WebcamPiP>`

Picture-in-picture overlay for webcam recording or AI avatar.

```typescript
interface WebcamPiPProps {
  source: string;                   // Video file path
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  sizePercent: number;
  borderRadius: number;
  borderColor?: string;
  borderWidth?: number;
  compositionWidth: number;
  compositionHeight: number;
}
```

**Implementation notes:**
- Uses `<OffthreadVideo>` for rendering performance
- Circular (border-radius: 50%) or rounded rectangle crop
- Subtle drop shadow for depth
- Can be hidden per-step via layout override
- For AI avatar: SadTalker generates per-step talking head videos from a portrait + voiceover audio (same as video-toolkit)

### 4.9 `<StepAnnotation>`

Overlaid annotation (arrow, callout, highlight) on any step.

```typescript
interface StepAnnotationProps {
  annotation: Annotation;
  currentFrame: number;
  fps: number;
  compositionWidth: number;
  compositionHeight: number;
}
```

**Implementation notes:**
- SVG-based rendering for crisp arrows and shapes at any zoom level
- Arrows: SVG `<line>` with arrowhead marker, animated draw-on via `stroke-dashoffset`
- Callouts: rounded rectangle with text, connected to target via leader line
- Highlights: semi-transparent rectangle with accent color
- All annotations spring-animate in and fade out

### 4.10 `<TutorialComposition>`

Root composition that wires everything together.

```typescript
interface TutorialCompositionProps {
  config: TutorialConfig;
}
```

**Implementation notes:**
- Reads config, calculates per-step frame durations from voiceover audio lengths + padding
- Creates a `<TransitionSeries>` with one `<TransitionSeries.Sequence>` per step
- Each sequence contains the appropriate content component (`<AnimatedCode>`, `<TerminalReplay>`, etc.) wrapped in `<AutoZoom>` and `<FocusHighlight>`
- `<ProgressBar>` and `<WebcamPiP>` render as persistent overlays outside the series
- Background music `<Audio>` component spans entire duration
- Per-step voiceover `<Audio>` components aligned to step start frames

---

## 5. Tools

### 5.1 `tools/parse_tutorial.py`

Parses Code Hike annotated markdown into a JSON structure consumable by the Remotion components.

```bash
python3 tools/parse_tutorial.py \
  --input tutorial.md \
  --output src/config/parsed-steps.json
```

**Input:** Markdown file using Code Hike annotations:

```markdown
!!steps

## Setting up the project

First, create a new directory.

```ts ! src/index.ts
const app = new Hono()
```

## Adding a route

Now add a GET route.

```ts ! src/index.ts
const app = new Hono()

app.get('/', (c) => c.json({ hello: 'world' }))
```
```

**Output:** JSON array of step objects with code states extracted, ready to populate `TutorialConfig.steps[].code.states`.

**Implementation:** Uses `@code-hike/mdx`'s `parseRoot()` via a Node.js subprocess (Code Hike is JS-only). The Python script orchestrates the call and reformats output.

### 5.2 `tools/generate_voiceover.py`

Generates voiceover audio for each step's narration text.

```bash
python3 tools/generate_voiceover.py \
  --config src/config/tutorial-config.ts \
  --output-dir public/audio/voiceover/ \
  --provider qwen3-tts \
  --speaker Ryan --tone tutorial \
  --cloud modal
```

**Implementation:** Reads `narration` field from each step in the config. Calls Qwen3-TTS (via existing video-toolkit Modal endpoint) or ElevenLabs API per step. Outputs numbered files: `01-intro.mp3`, `02-scaffold.mp3`, etc. Measures each file's duration via `ffprobe` and prints a timing report.

### 5.3 `tools/detect_focus.py`

Analyzes code state diffs to auto-generate focus region keyframes.

```bash
python3 tools/detect_focus.py \
  --config src/config/tutorial-config.ts \
  --output src/config/focus-regions.json
```

**Implementation:** For each code step, diffs consecutive states to find changed/added lines. Maps changed line ranges to pixel positions based on font size and line height. Outputs `FocusRegion[]` objects that zoom to the changed region. Heuristic: zoom to show changed lines + 3 lines of context above/below.

### 5.4 `tools/cast_to_keyframes.py`

Extracts timing information from Asciinema `.cast` files.

```bash
python3 tools/cast_to_keyframes.py \
  --input recordings/01-scaffold.cast \
  --speed 1.5 \
  --max-idle 2.0 \
  --output src/config/cast-timing.json
```

**Implementation:** Parses asciicast v2 format. Applies speed multiplier and idle compression. Outputs total adjusted duration and a list of "interesting moments" (command executions, long outputs) suitable for auto-generating pause points or focus regions.

---

## 6. Pipeline

End-to-end flow from authoring to rendered MP4.

### Step 1: Author content

User creates:
- `tutorial.md` -- Code Hike annotated markdown with `!!steps`, code blocks, and narration text per step
- `recordings/*.cast` -- Asciinema terminal recordings (`asciinema rec recordings/01-scaffold.cast`)
- Optional: `webcam/talking-head.mp4` -- webcam recording
- Optional: Pre-recorded voiceover audio files

### Step 2: Create project

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
cp -r templates/tutorial projects/MY_TUTORIAL
cd projects/MY_TUTORIAL
npm install
```

### Step 3: Parse markdown

```bash
cd $TOOLKIT
python3 tools/parse_tutorial.py \
  --input projects/MY_TUTORIAL/tutorial.md \
  --output projects/MY_TUTORIAL/src/config/parsed-steps.json
```

### Step 4: Write config

Edit `projects/MY_TUTORIAL/src/config/tutorial-config.ts` using the parsed steps JSON as a starting point. Add terminal step references, layout preferences, theme, and export formats.

### Step 5: Generate voiceover

```bash
cd $TOOLKIT
python3 tools/generate_voiceover.py \
  --config projects/MY_TUTORIAL/src/config/tutorial-config.ts \
  --output-dir projects/MY_TUTORIAL/public/audio/voiceover/ \
  --provider qwen3-tts --speaker Ryan --tone tutorial \
  --cloud modal
```

### Step 6: Generate focus regions (optional)

```bash
cd $TOOLKIT
python3 tools/detect_focus.py \
  --config projects/MY_TUTORIAL/src/config/tutorial-config.ts \
  --output projects/MY_TUTORIAL/src/config/focus-regions.json
```

### Step 7: Generate AI avatar (optional)

```bash
cd $TOOLKIT
# Generate presenter portrait
python3 tools/flux2.py \
  --prompt "Professional developer, dark background, facing camera, friendly expression" \
  --width 1024 --height 576 \
  --output projects/MY_TUTORIAL/public/webcam/presenter.png --cloud modal

# Generate per-step talking head clips
for f in projects/MY_TUTORIAL/public/audio/voiceover/*.mp3; do
  BASENAME=$(basename "$f" .mp3)
  python3 tools/sadtalker.py \
    --image projects/MY_TUTORIAL/public/webcam/presenter.png \
    --audio "$f" \
    --preprocess full --still --expression-scale 0.8 \
    --output "projects/MY_TUTORIAL/public/webcam/avatar-${BASENAME}.mp4" \
    --cloud modal
done
```

### Step 8: Generate background music (optional)

```bash
cd $TOOLKIT
python3 tools/music_gen.py \
  --preset lofi \
  --duration 300 \
  --output projects/MY_TUTORIAL/public/audio/bg-music.mp3 \
  --cloud modal
```

### Step 9: Preview

```bash
cd $TOOLKIT/projects/MY_TUTORIAL
npx remotion studio
# Opens browser at localhost:3000 with real-time preview
```

### Step 10: Render

```bash
cd $TOOLKIT/projects/MY_TUTORIAL

# YouTube (16:9)
npx remotion render TutorialVideo out/tutorial-youtube.mp4

# TikTok/Shorts (9:16)
npx remotion render TutorialVideoVertical out/tutorial-shorts.mp4
```

### Step 11: Post-process (optional)

```bash
# Add intro/outro bumper
ffmpeg -f concat -safe 0 -i concat-list.txt -c copy out/final.mp4

# Optimize for web streaming
ffmpeg -i out/tutorial-youtube.mp4 -movflags +faststart out/tutorial-youtube-web.mp4
```

---

## 7. SKILL.md Draft

```markdown
---
name: tutorial-video
description: Create Fireship-quality developer tutorial videos from annotated markdown and terminal recordings. Animated code transitions (Code Hike + Shiki Magic Move), terminal replay (Asciinema), auto-zoom effects, AI voiceover (Qwen3-TTS or ElevenLabs), progress bar with chapters, webcam/avatar PiP, step annotations, and social format export. Full pipeline from markdown to rendered MP4 via Remotion.
version: 0.1.0
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

### Step 3: Verify Code Hike + Shiki

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
    },
    {
      id: 'setup',
      type: 'terminal',
      narration: 'Start by scaffolding a new Hono project.',
      terminal: {
        castFile: 'recordings/01-setup.cast',
        theme: 'dracula',
        speed: 1.5,
      },
    },
    {
      id: 'first-route',
      type: 'code',
      narration: 'Add a GET route that returns JSON.',
      code: {
        markdownFile: 'tutorial.md',
        language: 'typescript',
        theme: 'github-dark',
        transitionFrames: 25,
      },
    },
  ],
  layout: {
    defaultLayout: 'code-only',
    padding: 40,
    cornerRadius: 12,
    showProgressBar: true,
    progressBarPosition: 'bottom',
    showChapterTitles: true,
  },
  audio: {
    voiceover: {
      provider: 'qwen3-tts',
      speaker: 'Ryan',
      tone: 'tutorial',
      stepGap: 0.5,
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
    formats: [{ name: 'youtube', width: 1920, height: 1080, fps: 30 }],
    outputDir: 'out/',
  },
};
```

**Duration rule for narration:** `ceil(word_count / 2.5) + 2` seconds. Terminal and code steps auto-calculate duration from content + voiceover length.

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

### Step 7: Preview and Render

```bash
cd $TOOLKIT/projects/MY_TUTORIAL

# Real-time preview
npx remotion studio

# Render YouTube format
npx remotion render TutorialVideo out/tutorial.mp4

# Render TikTok/Shorts format
npx remotion render TutorialVideoVertical out/tutorial-shorts.mp4
```

Output: `out/tutorial.mp4`

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

## Social Format Export

Export from the same source to multiple formats:

| Format | Resolution | FPS | Max Duration |
|---|---|---|---|
| YouTube | 1920x1080 | 30 | -- |
| TikTok | 1080x1920 | 30 | 180s |
| YouTube Shorts | 1080x1920 | 30 | 60s |
| Square (Instagram) | 1080x1080 | 30 | -- |

Vertical formats auto-reflow: code gets larger font, terminal stacks above narration, PiP moves to top.

## Cost Estimates

| Step | Cost | Notes |
|---|---|---|
| Voiceover (Qwen3-TTS) | ~$0.01/step | ~20s warm GPU via Modal |
| AI avatar (SadTalker) | ~$0.05-0.20/step | ~3-4 min per 10s audio |
| Background music (MusicGen) | ~$0.02-0.05 | Duration-dependent |
| Presenter portrait (FLUX.2) | ~$0.01 | One-time |
| Remotion render | Free (local) | ~2-5 min for 5-min video |

**Total 5-minute tutorial:** ~$0.50-2.00 with AI avatar, ~$0.10-0.50 without.

## Key Rules

1. **All animation via `useCurrentFrame()` + `interpolate()`/`spring()`.** No CSS transitions or Tailwind animation classes.
2. **Always `staticFile()`** for assets. Never `require()`.
3. **Always `<OffthreadVideo>`** for webcam/avatar. Never `<video>`.
4. **Always `--preprocess full --still`** for SadTalker.
5. **Generate voiceover per step,** never as one long audio file.
6. **Duration = `ceil(word_count / 2.5) + 2`** for narration-driven steps.
7. **Run all tools from `$TOOLKIT` root,** not from the project directory.

Source: Built on [remotion.dev/templates/code-hike](https://remotion.dev/templates/code-hike), [codehike.org](https://codehike.org), [shikijs/shiki-magic-move](https://github.com/shikijs/shiki-magic-move), [asciinema.org](https://asciinema.org)
```

---

## 8. Dependencies

### npm packages (in template `package.json`)

| Package | Version | Purpose |
|---|---|---|
| `remotion` | ^4.x | Core video framework |
| `@remotion/cli` | ^4.x | Rendering CLI |
| `@remotion/transitions` | ^4.x | Transition effects |
| `@remotion/media` | ^4.x | Audio/Video components |
| `@remotion/google-fonts` | ^4.x | Font loading (Inter) |
| `@code-hike/mdx` | ^1.x | Markdown parsing with code annotations |
| `shiki` | ^1.x | Syntax highlighting engine |
| `shiki-magic-move` | ^0.x | Token-level FLIP animations |
| `xterm` | ^5.x | Terminal emulation for rendering .cast output |
| `xterm-addon-serialize` | ^0.x | Serialize terminal state to HTML |
| `react` | ^18.x | React (Remotion dependency) |
| `typescript` | ^5.x | TypeScript |
| `zod` | ^3.x | Config validation |

### Python packages (in `requirements-tutorial.txt`)

| Package | Version | Purpose |
|---|---|---|
| `requests` | ^2.x | HTTP calls to Modal endpoints |
| `python-dotenv` | ^1.x | .env file loading |

### External tools

| Tool | Install | Purpose |
|---|---|---|
| `asciinema` | `brew install asciinema` | Terminal recording |
| `ffmpeg` / `ffprobe` | `brew install ffmpeg` | Audio duration measurement, post-processing |
| `node` | ^18+ | Remotion runtime, Code Hike parsing |

### External APIs / services

| Service | Required? | Purpose | Cost |
|---|---|---|---|
| Modal (cloud GPU) | Yes (for AI features) | Qwen3-TTS, FLUX.2, SadTalker, MusicGen | ~$0.01-0.20/call |
| ElevenLabs | Optional (alternative to Qwen3-TTS) | High-quality voiceover | $5-22/mo |

---

## 9. Cost Estimate

### Per-video costs (5-minute tutorial, 8 steps)

| Component | Unit Cost | Units | Total |
|---|---|---|---|
| Voiceover generation (Qwen3-TTS) | $0.01/step | 8 | $0.08 |
| AI avatar generation (SadTalker) | $0.10/step | 8 | $0.80 |
| Presenter portrait (FLUX.2) | $0.01 | 1 | $0.01 |
| Background music (MusicGen) | $0.03 | 1 | $0.03 |
| Remotion local render | $0.00 | 1 | $0.00 |
| **Total with AI avatar** | | | **~$0.92** |
| **Total without avatar** | | | **~$0.12** |

### Comparison to competitors

| Solution | Monthly cost | Per-video cost (amortized) |
|---|---|---|
| **tutorial-video skill** | $0 subscription | $0.12-0.92/video |
| Screen Studio + ElevenLabs | $29 + $22 = $51/mo | $5.10/video (10 videos/mo) |
| Descript | $24-65/mo | $2.40-6.50/video |
| Guidde | ~$50/mo | $5.00/video |

---

## 10. Implementation Stories

Ordered by dependency chain. Each story is independently shippable and testable.

### Phase 1: Foundation (Week 1-2)

#### Story 1: Project template scaffold
**Effort:** S (2-4 hours)

Create `templates/tutorial/` with package.json, tsconfig, Remotion root, placeholder composition, and the full TypeScript config schema with Zod validation. Verify `npx remotion studio` launches with a "Hello Tutorial" placeholder.

**Acceptance criteria:**
- `cp -r templates/tutorial projects/test && cd projects/test && npm install && npx remotion studio` works
- Config schema validates with Zod, rejects invalid input with clear errors
- Placeholder composition renders a static frame

#### Story 2: AnimatedCode component (Code Hike + Shiki Magic Move)
**Effort:** L (2-3 days)

Build `<AnimatedCode>` that renders syntax-highlighted code and animates between states using Shiki Magic Move. Integrate `@code-hike/mdx` `parseRoot()` for markdown parsing. Support 150+ languages, line highlights, line folds, editor chrome (title bar, filename tabs).

**Acceptance criteria:**
- Given two TypeScript code states, component smoothly animates token-level transitions (Move, Enter, Leave)
- Line highlights render as colored backgrounds
- Editor chrome shows filename and colored dots
- Works with `github-dark`, `dracula`, and `monokai` themes
- `parse_tutorial.py` extracts steps from Code Hike markdown and outputs valid JSON

#### Story 3: TerminalReplay component
**Effort:** L (2-3 days)

Build `<TerminalReplay>` that parses `.cast` files and renders terminal output synchronized to video frames. Support speed control, idle compression, pause points with annotations, and terminal themes.

**Acceptance criteria:**
- Given a `.cast` file, component replays terminal output in sync with video timeline
- Speed multiplier works (1.5x plays faster)
- Idle gaps exceeding `maxIdleTime` are compressed
- Pause points insert dead time with optional annotation overlay
- Terminal chrome renders (rounded container, title bar)
- `cast_to_keyframes.py` outputs correct timing JSON

### Phase 2: Effects (Week 2-3)

#### Story 4: AutoZoom + FocusHighlight
**Effort:** M (1-2 days)

Build `<AutoZoom>` with spring-based zoom transitions between focus regions, and `<FocusHighlight>` with animated spotlight dimming. Build `detect_focus.py` for auto-generating focus regions from code diffs.

**Acceptance criteria:**
- Zoom transitions are smooth (no jank, no bounce with damping=200)
- Zoom level auto-calculated from region size when not specified
- FocusHighlight dims non-focus area with feathered edges
- `detect_focus.py` generates valid focus regions from code state diffs

#### Story 5: SmoothCursor
**Effort:** S (4-8 hours)

Build `<SmoothCursor>` with Bezier interpolation between keyframe positions, click ripple animation, and optional motion trail.

**Acceptance criteria:**
- Cursor movement is smooth (no jerky linear interpolation)
- Click events show expanding ripple
- Trail effect renders 3-5 ghost cursors at decreasing opacity

#### Story 6: ProgressBar + ChapterTitle
**Effort:** S (4-8 hours)

Build `<ProgressBar>` with chapter markers and current chapter title display. Build `<ChapterTitle>` with staggered spring entrance animation.

**Acceptance criteria:**
- Progress bar fills proportionally to current frame
- Chapter markers visible as dots at step boundaries
- Chapter title animates in at step start, auto-dismisses after 1.5s
- Both components respect theme colors

### Phase 3: Integration (Week 3-4)

#### Story 7: Voiceover pipeline + audio timing
**Effort:** M (1-2 days)

Build `generate_voiceover.py` that reads config, generates per-step audio via Qwen3-TTS or ElevenLabs, and outputs a timing report. Wire voiceover audio into the composition with correct per-step alignment.

**Acceptance criteria:**
- Generates one MP3 per step with narration text
- Measures duration via ffprobe, prints timing report
- Composition auto-calculates step durations from voiceover length + padding
- Background music plays at configured volume beneath voiceover

#### Story 8: WebcamPiP + StepAnnotation
**Effort:** M (1-2 days)

Build `<WebcamPiP>` supporting real webcam recording and SadTalker AI avatar. Build `<StepAnnotation>` with SVG-based arrows, callouts, and highlights.

**Acceptance criteria:**
- PiP renders in configured corner with correct size and border radius
- SadTalker per-step avatar clips align with voiceover timing
- Annotations animate in with spring, support all 6 types
- Arrow draw-on animation via stroke-dashoffset

#### Story 9: TutorialComposition (root wiring)
**Effort:** M (1-2 days)

Build `<TutorialComposition>` that reads the full config and wires all components together. TransitionSeries with per-step sequences, persistent overlays (progress bar, PiP), audio layers, and layout mode switching.

**Acceptance criteria:**
- Full tutorial renders end-to-end from config
- Layout modes switch correctly per step
- Transitions between steps work (fade, slide-left, etc.)
- All overlays (progress bar, PiP, annotations) render on top of content

### Phase 4: Social Export + Polish (Week 4-5)

#### Story 10: Social format export (vertical 9:16)
**Effort:** M (1-2 days)

Add vertical composition variant that reflows content for 9:16. Code gets larger font, terminal stacks vertically, PiP moves to top.

**Acceptance criteria:**
- `TutorialVideoVertical` composition renders at 1080x1920
- Code is readable at phone size (larger font, narrower)
- Terminal content visible (may need font size increase)
- PiP repositions to top of frame

#### Story 11: SKILL.md + documentation
**Effort:** S (2-4 hours)

Write final SKILL.md with complete usage instructions, matching video-toolkit and remotion skill conventions. Add to registry `.skills.json`.

**Acceptance criteria:**
- SKILL.md matches frontmatter format of existing skills
- All commands documented with working examples
- Registered in `.skills.json`

#### Story 12: End-to-end validation
**Effort:** M (1-2 days)

Build a real 3-5 minute tutorial video using the skill to validate the full pipeline. Fix all issues found. Record the process as a meta-tutorial.

**Acceptance criteria:**
- A complete tutorial video renders without manual intervention beyond config authoring
- Video quality matches Fireship production level (smooth animations, clear audio, readable code)
- Pipeline completes in under 10 minutes (excluding cloud GPU wait times)

### Total effort estimate

| Phase | Stories | Effort |
|---|---|---|
| Phase 1: Foundation | Stories 1-3 | ~1.5 weeks |
| Phase 2: Effects | Stories 4-6 | ~1 week |
| Phase 3: Integration | Stories 7-9 | ~1 week |
| Phase 4: Polish | Stories 10-12 | ~1 week |
| **Total** | **12 stories** | **~4.5 weeks** |

---

## Appendix: Key Technical References

- **Code Hike docs:** https://codehike.org/docs
- **Code Hike Remotion template:** https://remotion.dev/templates/code-hike
- **Shiki Magic Move:** https://github.com/shikijs/shiki-magic-move
- **Shiki Magic Move FLIP technique:** https://shiki-magic-move.netlify.app
- **Asciinema:** https://asciinema.org
- **Asciicast v2 format:** https://docs.asciinema.org/manual/asciicast/v2/
- **Remotion spring():** https://www.remotion.dev/docs/spring
- **Remotion interpolate():** https://www.remotion.dev/docs/interpolate
- **Remotion TransitionSeries:** https://www.remotion.dev/docs/transitions/transitionseries
- **Screen Studio (auto-zoom reference):** https://www.screen.studio
