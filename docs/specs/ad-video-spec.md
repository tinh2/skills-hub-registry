# Engineering Spec: `/ad-video` Skill

> Version: 1.0.0 | Date: 2026-03-26 | Status: Draft

---

## 1. Overview

### What it does

The `/ad-video` skill generates platform-optimized video advertisements from a product brief, entirely from the CLI. A user describes their product (name, tagline, features, brand assets) and receives rendered ad variants for every target platform — TikTok, Instagram, YouTube, Facebook, LinkedIn — without opening a video editor or hiring an agency.

### Target user

Startup founders, indie hackers, performance marketers, and small-team product owners who need to run paid video campaigns across platforms but lack the budget or time for agency-produced creative.

### Value proposition

- **One brief, every platform.** Describe your product once; get 9:16, 1:1, 4:5, and 16:9 variants auto-generated.
- **No subscription.** Pay-per-render (~$1-5/video) via Modal or Remotion Lambda, not $20-60/month SaaS.
- **Fully customizable.** Every frame is a React component you own. Fork any template, tweak any animation.
- **Batch at scale.** Feed a CSV of 50 headline/price/audience combos, get 50 personalized videos rendered in parallel.
- **CLI-native.** Fits into developer workflows, CI/CD pipelines, and automation scripts.

### Competitors to beat

| Competitor | Strength | Our edge |
|---|---|---|
| **Shotstack** | JSON API, batch rendering, event triggers | We have Claude generating the composition + script, not just filling templates |
| **Creatomate** | Template + API, A/B variants, multi-format | We offer full React customization, no template lock-in |
| **InVideo AI** | Prompt-based, 16M+ stock assets | We run locally, no subscription, open-source models |
| **Canva Video** | Brand kits, massive template library | We are programmable, scriptable, CI/CD-friendly |
| **Lumen5** | Blog-to-video, NLP scene selection | We generate from structured briefs with proven ad copywriting frameworks |

---

## 2. Architecture

### Relationship to existing skills

The `/ad-video` skill builds on the existing `video-toolkit` infrastructure and the `remotion` skill's composition knowledge.

```
video-toolkit (existing)
  |-- Cloud GPU endpoints (Modal): Qwen3-TTS, FLUX.2, MusicGen, SadTalker
  |-- Remotion render pipeline
  |-- Per-scene audio timing sync (ffprobe)
  |-- Cloudflare R2 file transfer
  |
ad-video (NEW)
  |-- Brand kit system (brand.json)
  |-- Ad brief parser + script generator (Claude)
  |-- Ad template components (Remotion/React)
  |     |-- HookScene, ProblemScene, SolutionScene, CTAScene
  |     |-- ProductShot, KineticText, CTAButton, EndCard, PriceTag, QRCode
  |     |-- PlatformAdapter (auto-reformat to target dimensions)
  |-- Platform format engine (aspect ratios, durations, safe zones)
  |-- Batch personalization engine (CSV/JSON -> variant configs)
  |-- A/B variant generator
  |-- Tools
  |     |-- tools/pexels_search.py (stock footage)
  |     |-- tools/screen_record.py (Playwright product demos)
  |     |-- tools/batch_render.py (parallel variant rendering)
  |     |-- tools/brand_validate.py (brand kit validation + contrast checks)
```

### New directories

```
build/ad-video/
  SKILL.md                          # Skill instructions
projects/ad-template/               # Remotion project template
  src/
    config/
      ad-config.ts                  # Ad brief + brand kit config schema
      platform-specs.ts             # Platform dimension/duration constants
    components/
      scenes/
        HookScene.tsx               # Attention-grabbing opener
        ProblemScene.tsx             # Pain point visualization
        SolutionScene.tsx           # Product as solution
        FeatureScene.tsx            # Feature highlight with animations
        TestimonialScene.tsx        # Quote + avatar
        ComparisonScene.tsx         # Before/after or us-vs-them
        CTAScene.tsx                # Final call-to-action + end card
      overlays/
        CTAButton.tsx               # Animated CTA button
        EndCard.tsx                 # Logo + tagline + CTA + socials
        PriceTag.tsx                # Animated price (with discount strike-through)
        QRCode.tsx                  # Animated QR reveal
        LowerThird.tsx              # Name/title bar
      product/
        ProductShot.tsx             # Product image with parallax/zoom/rotation
        ScreenRecording.tsx         # Embedded Playwright capture
        AppDemo.tsx                 # Animated app screenshots
      text/
        KineticText.tsx             # Animated typography (slide, pop, typewriter, wave)
        StatCounter.tsx             # Animated number counter
        FeatureList.tsx             # Staggered feature bullet animations
      layout/
        PlatformAdapter.tsx         # Wraps any composition, adapts to target format
        SafeZone.tsx                # Platform-specific safe zone overlay (dev mode)
        BrandFrame.tsx              # Consistent brand border/watermark
    lib/
      brand.ts                      # Brand kit loader + validation
      platform.ts                   # Platform format utilities
      variants.ts                   # A/B variant generation logic
      batch.ts                      # Batch data loading (CSV/JSON)
    AdVideo.tsx                     # Root composition
    index.ts                        # Remotion entry point
  public/
    brand/                          # Logo, fonts
    products/                       # Product shots/screenshots
    stock/                          # Downloaded Pexels footage
    audio/                          # Voiceovers, music
    recordings/                     # Playwright screen captures
  package.json
tools/
  pexels_search.py                  # Stock footage/photo search + download
  screen_record.py                  # Playwright browser demo capture
  batch_render.py                   # Parallel variant rendering
  brand_validate.py                 # Brand kit validation
  generate_variants.py              # A/B headline/CTA variant generation
```

---

## 3. Data Model

### Brand Kit (`brand.json`)

```typescript
interface BrandKit {
  name: string;                          // "Acme Corp"
  tagline: string;                       // "Ship faster, break nothing"
  website: string;                       // "https://acme.com"

  logo: {
    primary: string;                     // "brand/logo.svg"
    light: string;                       // "brand/logo-light.svg" (for dark backgrounds)
    dark: string;                        // "brand/logo-dark.svg" (for light backgrounds)
    icon: string;                        // "brand/icon.svg" (square, for small placements)
    minWidth: number;                    // Minimum display width in pixels
    safePadding: number;                 // Minimum padding around logo in pixels
  };

  colors: {
    primary: string;                     // "#2563EB"
    secondary: string;                   // "#7C3AED"
    accent: string;                      // "#F59E0B"
    background: string;                  // "#0F172A"
    surface: string;                     // "#1E293B"
    text: string;                        // "#F8FAFC"
    textMuted: string;                   // "#94A3B8"
    ctaBackground: string;               // "#2563EB"
    ctaText: string;                     // "#FFFFFF"
    gradient?: [string, string];         // ["#2563EB", "#7C3AED"]
  };

  fonts: {
    heading: {
      family: string;                    // "Inter"
      weight: number;                    // 800
      source: 'google' | 'local';       // Where to load from
      file?: string;                     // "brand/fonts/Inter-ExtraBold.woff2"
    };
    body: {
      family: string;                    // "Inter"
      weight: number;                    // 400
      source: 'google' | 'local';
      file?: string;
    };
    accent?: {
      family: string;                    // "Space Grotesk"
      weight: number;
      source: 'google' | 'local';
      file?: string;
    };
  };

  social?: {
    twitter?: string;                    // "@acmecorp"
    instagram?: string;                  // "@acmecorp"
    linkedin?: string;                   // "acme-corp"
    tiktok?: string;                     // "@acmecorp"
    youtube?: string;                    // "@AcmeCorp"
  };
}
```

### Ad Brief (`ad-config.ts`)

```typescript
type AdType =
  | 'product-launch'
  | 'feature-highlight'
  | 'testimonial'
  | 'comparison'
  | 'seasonal-promo'
  | 'app-demo';

type Platform = 'tiktok' | 'instagram-reel' | 'instagram-feed' | 'youtube-preroll' | 'facebook' | 'linkedin';

interface AdBrief {
  type: AdType;
  product: {
    name: string;
    tagline: string;
    description: string;                 // 1-2 sentence product description
    features: string[];                  // Key features (3-6)
    painPoints: string[];                // Problems it solves (2-4)
    pricing?: {
      amount: string;                    // "$29/mo"
      original?: string;                 // "$49/mo" (for discount display)
      trial?: string;                    // "14-day free trial"
    };
  };

  assets: {
    productShots: string[];              // Paths to product images/screenshots
    screenRecording?: {
      url: string;                       // URL to capture
      script: PlaywrightAction[];        // Actions to perform
    };
    stockQueries?: string[];             // Pexels search queries for B-roll
  };

  cta: {
    text: string;                        // "Start Free Trial"
    url: string;                         // "https://acme.com/signup"
    secondary?: string;                  // "Learn More"
    qrCode?: boolean;                    // Generate QR code for CTA URL
  };

  targets: Platform[];                   // Which platforms to generate for

  testimonial?: {                        // For testimonial ad type
    quote: string;
    author: string;
    title: string;
    avatar?: string;                     // Path to avatar image
  };

  comparison?: {                         // For comparison ad type
    competitor: string;
    advantages: Array<{
      dimension: string;                 // "Speed"
      us: string;                        // "50ms"
      them: string;                      // "500ms"
    }>;
  };

  seasonal?: {                           // For seasonal promo type
    event: string;                       // "Black Friday", "Summer Sale"
    discount: string;                    // "50% off"
    deadline: string;                    // "Nov 30"
  };

  voiceover?: {
    enabled: boolean;
    speaker?: string;                    // Qwen3-TTS speaker name
    tone?: string;                       // "excited" | "professional" | "warm"
  };

  music?: {
    preset?: string;                     // MusicGen preset
    file?: string;                       // Path to custom music file
    volume?: number;                     // 0.0-1.0, default 0.15
  };
}
```

### Platform Specs

```typescript
interface PlatformSpec {
  platform: Platform;
  width: number;
  height: number;
  aspectRatio: string;
  fps: number;
  minDuration: number;                   // Seconds
  maxDuration: number;                   // Seconds
  defaultDuration: number;               // Seconds
  safeZone: {                            // Percentage inset from edges
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
  notes: string;
}

const PLATFORM_SPECS: Record<Platform, PlatformSpec> = {
  'tiktok': {
    platform: 'tiktok',
    width: 1080, height: 1920,
    aspectRatio: '9:16', fps: 30,
    minDuration: 15, maxDuration: 60, defaultDuration: 30,
    safeZone: { top: 15, bottom: 20, left: 5, right: 5 },
    notes: 'Bottom 20% obscured by UI. First 3s must hook.',
  },
  'instagram-reel': {
    platform: 'instagram-reel',
    width: 1080, height: 1920,
    aspectRatio: '9:16', fps: 30,
    minDuration: 15, maxDuration: 30, defaultDuration: 15,
    safeZone: { top: 10, bottom: 15, left: 5, right: 5 },
    notes: 'Keep key text in center 70%. Bottom has like/comment UI.',
  },
  'instagram-feed': {
    platform: 'instagram-feed',
    width: 1080, height: 1350,
    aspectRatio: '4:5', fps: 30,
    minDuration: 3, maxDuration: 60, defaultDuration: 15,
    safeZone: { top: 5, bottom: 10, left: 5, right: 5 },
    notes: '4:5 fills more feed space than 1:1. Preferred for ads.',
  },
  'youtube-preroll': {
    platform: 'youtube-preroll',
    width: 1920, height: 1080,
    aspectRatio: '16:9', fps: 30,
    minDuration: 6, maxDuration: 15, defaultDuration: 6,
    safeZone: { top: 5, bottom: 10, left: 5, right: 5 },
    notes: 'Skippable after 5s. CTA must appear by second 4. 6s = non-skippable bumper.',
  },
  'facebook': {
    platform: 'facebook',
    width: 1080, height: 1080,
    aspectRatio: '1:1', fps: 30,
    minDuration: 5, maxDuration: 15, defaultDuration: 15,
    safeZone: { top: 5, bottom: 10, left: 5, right: 5 },
    notes: 'Square performs best in feed. Keep text above 20% of frame.',
  },
  'linkedin': {
    platform: 'linkedin',
    width: 1920, height: 1080,
    aspectRatio: '16:9', fps: 30,
    minDuration: 15, maxDuration: 30, defaultDuration: 30,
    safeZone: { top: 5, bottom: 5, left: 5, right: 5 },
    notes: 'Professional tone. Data/stats perform well. Captions essential (85% watch muted).',
  },
};
```

### Batch Personalization Schema

```typescript
interface BatchDataRow {
  // Required
  id: string;                            // Unique variant identifier

  // Text overrides (any field from AdBrief can be overridden)
  headline?: string;
  tagline?: string;
  ctaText?: string;
  price?: string;
  originalPrice?: string;
  discount?: string;

  // Asset overrides
  productShot?: string;                  // Path to variant-specific product image

  // Audience targeting metadata (for file naming, not rendered)
  audience?: string;                     // "developers", "marketers", "founders"
  language?: string;                     // "en", "es", "fr", "de"
  region?: string;                       // "US", "EU", "APAC"
}

interface BatchConfig {
  template: AdBrief;                     // Base template
  data: string;                          // Path to CSV or JSON file
  outputPattern: string;                 // "out/{platform}/{id}-{audience}.mp4"
  parallelism: number;                   // Max concurrent renders (default: 4)
}
```

### A/B Variant Config

```typescript
interface ABConfig {
  variantCount: number;                  // 3-5 variants per element
  elements: Array<'headline' | 'tagline' | 'cta' | 'hook' | 'color-scheme'>;
  strategy: 'claude-generated' | 'manual';
}
```

---

## 4. Components

### Scene Components

Each scene component receives the `BrandKit`, scene-specific content, and platform dimensions via props.

#### `HookScene`

The opening 2-4 seconds that stops the scroll.

```typescript
interface HookSceneProps {
  brand: BrandKit;
  style: 'question' | 'stat' | 'bold-claim' | 'pain-point' | 'curiosity-gap';
  text: string;                          // The hook text
  subtext?: string;                      // Supporting line
  productShot?: string;                  // Optional product image peek
  animation: 'slam' | 'typewriter' | 'reveal' | 'glitch' | 'zoom-in';
  durationInFrames: number;
}
```

Animations:
- `slam` — Text scales from 3x to 1x with spring bounce. High energy.
- `typewriter` — Characters appear one by one with cursor blink.
- `reveal` — Clip-path wipe reveals text left-to-right.
- `glitch` — RGB split + noise flicker, then text stabilizes.
- `zoom-in` — Camera zooms into text with motion blur.

#### `ProblemScene`

Visualizes the pain point the product solves.

```typescript
interface ProblemSceneProps {
  brand: BrandKit;
  headline: string;
  painPoints: string[];                  // 2-3 pain points, staggered entrance
  style: 'list' | 'before-after' | 'frustrated-user' | 'x-marks';
  backgroundImage?: string;              // Stock image or generated
  durationInFrames: number;
}
```

#### `SolutionScene`

Introduces the product as the answer.

```typescript
interface SolutionSceneProps {
  brand: BrandKit;
  headline: string;                      // "Meet [Product]" or "There's a better way"
  productShot: string;
  highlights: string[];                  // 2-3 key benefits
  animation: 'product-reveal' | 'split-transition' | 'zoom-to-product';
  durationInFrames: number;
}
```

#### `FeatureScene`

Highlights a single feature with supporting visual.

```typescript
interface FeatureSceneProps {
  brand: BrandKit;
  feature: string;                       // Feature name
  description: string;                   // One-line benefit
  visual: string;                        // Screenshot, icon, or product shot
  stat?: { value: string; label: string; }; // "10x faster" / "Speed"
  durationInFrames: number;
}
```

#### `TestimonialScene`

Social proof with quote and attribution.

```typescript
interface TestimonialSceneProps {
  brand: BrandKit;
  quote: string;
  author: string;
  title: string;
  avatar?: string;
  rating?: number;                       // 1-5 stars
  style: 'card' | 'full-screen-quote' | 'video-testimonial';
  durationInFrames: number;
}
```

#### `ComparisonScene`

Side-by-side or before/after comparison.

```typescript
interface ComparisonSceneProps {
  brand: BrandKit;
  headline: string;                      // "Why teams switch to [Product]"
  rows: Array<{
    dimension: string;
    us: string;
    them: string;
  }>;
  competitorName: string;
  style: 'table' | 'split-screen' | 'progress-bars';
  durationInFrames: number;
}
```

#### `CTAScene`

Final call-to-action with end card.

```typescript
interface CTASceneProps {
  brand: BrandKit;
  headline: string;                      // "Ready to ship faster?"
  ctaText: string;                       // "Start Free Trial"
  ctaUrl: string;
  pricing?: { amount: string; original?: string; trial?: string; };
  qrCode?: boolean;
  socialLinks?: boolean;                 // Show social handles from brand kit
  style: 'minimal' | 'bold' | 'card' | 'split-logo';
  durationInFrames: number;
}
```

### Overlay Components

#### `CTAButton`

```typescript
interface CTAButtonProps {
  text: string;
  backgroundColor: string;
  textColor: string;
  animation: 'pulse' | 'bounce' | 'glow' | 'slide-in';
  position: 'bottom-center' | 'bottom-right' | 'center';
  size: 'sm' | 'md' | 'lg';
}
```

Renders an animated button shape. Uses `spring()` for entrance, `interpolate()` for pulse/glow loop.

#### `EndCard`

```typescript
interface EndCardProps {
  brand: BrandKit;
  ctaText: string;
  ctaUrl: string;
  showSocials: boolean;
  showQR: boolean;
  style: 'centered' | 'split' | 'minimal';
  durationInFrames: number;
}
```

Full-frame end card with logo, tagline, CTA button, optional QR code, and social handles. Elements animate in with staggered springs.

#### `PriceTag`

```typescript
interface PriceTagProps {
  amount: string;
  originalAmount?: string;               // Shown with strike-through
  label?: string;                        // "per month", "one-time"
  badge?: string;                        // "50% OFF", "LIMITED"
  animation: 'pop' | 'counter' | 'slide';
  colors: { background: string; text: string; badge: string; };
}
```

Animated price display. When `originalAmount` is set, the original price appears first, then gets a strike-through animation, and the new price pops in below.

#### `QRCode`

```typescript
interface QRCodeProps {
  url: string;
  size: number;
  foreground: string;
  background: string;
  logo?: string;                         // Center logo overlay
  animation: 'fade-in' | 'scan-reveal' | 'pixel-build';
}
```

Uses `qrcode` npm package to generate QR data, then renders as SVG with animation. `pixel-build` animates each module appearing one by one. `scan-reveal` simulates a scanning line.

#### `LowerThird`

```typescript
interface LowerThirdProps {
  name: string;
  title: string;
  brand: BrandKit;
  animation: 'slide-left' | 'expand' | 'type';
  durationInFrames: number;
}
```

### Product Components

#### `ProductShot`

```typescript
interface ProductShotProps {
  src: string;
  animation: 'parallax' | 'zoom-rotate' | 'float' | 'tilt-3d' | 'slide-in';
  shadow?: boolean;                      // Drop shadow for depth
  mockup?: 'none' | 'phone' | 'laptop' | 'browser'; // Device frame
  scale?: number;
}
```

Renders a product image with cinematic animation. `parallax` uses multi-layer offset on scroll-like motion. `tilt-3d` uses CSS `perspective` + `rotateY`/`rotateX` transforms driven by `spring()`. `float` applies gentle sinusoidal y-offset.

#### `ScreenRecording`

```typescript
interface ScreenRecordingProps {
  src: string;                           // Path to Playwright-captured MP4
  mockup: 'browser' | 'phone' | 'tablet' | 'none';
  zoomRegions?: Array<{
    startFrame: number;
    endFrame: number;
    x: number; y: number;
    width: number; height: number;
  }>;
}
```

Embeds a Playwright-captured screen recording inside a device mockup with optional auto-zoom regions.

### Text Components

#### `KineticText`

```typescript
interface KineticTextProps {
  text: string;
  animation: 'slide-up' | 'pop-word' | 'typewriter' | 'wave' | 'split-reveal' | 'counter';
  fontFamily: string;
  fontSize: number;
  fontWeight: number;
  color: string;
  align: 'left' | 'center' | 'right';
  delay?: number;                        // Frames before animation starts
}
```

Core text animation component. `pop-word` splits text into words and staggers entrance with spring. `wave` applies sinusoidal y-offset per character. `split-reveal` uses clip-path to reveal from center outward. `counter` animates numbers from 0 to target (for stats).

#### `StatCounter`

```typescript
interface StatCounterProps {
  value: number;
  suffix?: string;                       // "%", "x", "K", "M"
  prefix?: string;                       // "$", "#"
  label: string;
  duration: number;                      // Frames to count up
  color: string;
  size: 'sm' | 'md' | 'lg' | 'xl';
}
```

Animated number counter that interpolates from 0 to `value` over `duration` frames. Uses tabular-nums font feature for stable width.

### Layout Components

#### `PlatformAdapter`

```typescript
interface PlatformAdapterProps {
  platform: Platform;
  children: React.ReactNode;
  showSafeZones?: boolean;               // Dev mode: overlay safe zone guides
}
```

Wraps the entire ad composition. Sets width/height/fps from `PLATFORM_SPECS`. Applies platform-specific safe zone padding. Handles layout reflow for vertical vs. horizontal orientations.

The adapter does not simply crop — it re-layouts child components based on orientation:
- **Landscape (16:9):** Side-by-side layouts, horizontal text flow.
- **Portrait (9:16):** Stacked layouts, centered text, larger type for mobile viewing.
- **Square (1:1):** Centered composition, balanced margins.

#### `SafeZone`

```typescript
interface SafeZoneProps {
  platform: Platform;
  visible: boolean;                      // Toggle overlay
}
```

Dev-mode overlay showing red dashed lines for platform-specific safe zones (UI elements, progress bars, action buttons that obscure content).

---

## 5. Tools

### `tools/pexels_search.py` — Stock Footage Integration

```
Usage:
  python3 tools/pexels_search.py \
    --query "startup office team" \
    --type video \
    --orientation landscape \
    --per-page 5 \
    --output projects/ad-template/public/stock/

Requires: PEXELS_API_KEY env var (free at pexels.com/api)
Rate limit: 200 requests/hour, 20,000/month
```

Searches Pexels for photos or videos by keyword. Downloads to project's `public/stock/` directory. Returns JSON metadata (dimensions, duration, photographer, Pexels URL). Supports orientation filter (`landscape`, `portrait`, `square`), color filter, and minimum dimensions.

### `tools/screen_record.py` — Playwright Screen Capture

```
Usage:
  python3 tools/screen_record.py \
    --url "https://app.acme.com/dashboard" \
    --script scripts/demo-flow.json \
    --viewport 1280x720 \
    --device "iPhone 14 Pro" \
    --output projects/ad-template/public/recordings/demo.mp4

Requires: playwright (pip install playwright && playwright install chromium)
```

Executes a scripted browser session and captures frames as MP4. The `--script` JSON defines actions:

```json
[
  { "action": "wait", "duration": 1000 },
  { "action": "click", "selector": "#get-started" },
  { "action": "type", "selector": "#email", "text": "demo@example.com", "delay": 80 },
  { "action": "click", "selector": "#submit" },
  { "action": "wait", "duration": 2000 },
  { "action": "scroll", "y": 500, "duration": 1500 }
]
```

Supports device emulation (mobile, tablet), custom viewport sizes, network throttling, and CSS injection (hide cookie banners, blur PII). Outputs MP4 ready for `<ScreenRecording>` component.

### `tools/batch_render.py` — Parallel Batch Rendering

```
Usage:
  python3 tools/batch_render.py \
    --template projects/ad-template \
    --data variants.csv \
    --platforms tiktok,instagram-reel,facebook \
    --parallelism 4 \
    --output out/batch/

  # Or with Remotion Lambda:
  python3 tools/batch_render.py \
    --template projects/ad-template \
    --data variants.csv \
    --renderer lambda \
    --output s3://my-bucket/ads/
```

Reads a CSV or JSON data file, merges each row with the base ad config, and renders all variants across all target platforms. Supports local multi-process rendering or Remotion Lambda for cloud-scale parallelism.

Output structure:
```
out/batch/
  tiktok/
    variant-001-developers.mp4
    variant-002-marketers.mp4
  instagram-reel/
    variant-001-developers.mp4
    variant-002-marketers.mp4
  facebook/
    variant-001-developers.mp4
    variant-002-marketers.mp4
```

### `tools/brand_validate.py` — Brand Kit Validation

```
Usage:
  python3 tools/brand_validate.py --brand brand.json

Checks:
  - All referenced files exist (logo SVGs, font files)
  - Color contrast ratios (WCAG AA: 4.5:1 for text, 3:1 for large text)
  - CTA button contrast (ctaText on ctaBackground)
  - Font file validity
  - Logo dimensions meet minimum size requirements
  - Gradient readability (text on gradient endpoints)
```

### `tools/generate_variants.py` — A/B Variant Generator

```
Usage:
  python3 tools/generate_variants.py \
    --config ad-config.ts \
    --elements headline,cta,hook \
    --count 5 \
    --output variants.json

Strategy:
  - Uses Claude to generate variant copy based on the product brief
  - Headlines: different angles (benefit, curiosity, social proof, urgency, comparison)
  - CTAs: different actions (Start, Try, Get, Discover, Claim)
  - Hooks: different openers (question, stat, bold claim, pain point)
```

---

## 6. Pipeline

### Step-by-step flow: Brief to rendered ad variants

```
STEP 1: Initialize Project
  User runs: /ad-video "SaaS product launch for Acme, targeting developers"

  Claude:
    a. Creates project from ad-template
    b. Prompts for brand kit (or reads existing brand.json)
    c. Prompts for product details, features, CTA
    d. Generates ad-config.ts from brief

STEP 2: Generate Ad Script
  Claude writes the ad script using Hook/Problem/Solution/CTA framework:
    a. Analyzes product brief
    b. Writes hook (2-4s) — attention-grabbing opener
    c. Writes problem (3-5s) — pain point the audience feels
    d. Writes solution (4-8s) — product as the answer, feature highlights
    e. Writes CTA (2-4s) — clear next action
    f. Allocates duration per scene based on platform constraints
    g. Adjusts script density for platform (YouTube 15s vs. TikTok 30s)

STEP 3: Gather Assets
  Sequential, with parallelism where possible:
    a. Validate brand kit: python3 tools/brand_validate.py --brand brand.json
    b. In parallel:
       - Download stock B-roll: python3 tools/pexels_search.py --query "..." --output public/stock/
       - Capture screen recording: python3 tools/screen_record.py --url "..." --output public/recordings/
       - Generate voiceover: python3 tools/qwen3_tts.py --text "..." --output public/audio/vo.mp3
       - Generate background music: python3 tools/music_gen.py --preset upbeat-tech --output public/audio/bg.mp3
       - Generate AI images (if needed): python3 tools/flux2.py --prompt "..." --output public/images/
    c. Sync timing: ffprobe each audio file, update scene durations in config

STEP 4: Compose Remotion Project
  Claude writes/updates the Remotion composition:
    a. Maps ad script scenes to React components
    b. Wires brand kit into all components
    c. Sets up platform variants as separate Compositions
    d. Configures transitions between scenes (fade, wipe, slide based on energy)
    e. Layers audio: background music (volume 0.12-0.15) + voiceover (volume 1.0)

STEP 5: Generate Platform Variants
  For each target platform:
    a. PlatformAdapter sets dimensions, fps, duration from PLATFORM_SPECS
    b. Scenes re-layout for aspect ratio (stacked for 9:16, side-by-side for 16:9)
    c. Text sizes adjust (larger for mobile-first vertical, smaller for landscape)
    d. Safe zones applied (no key content in platform UI overlay areas)
    e. Duration trimmed/expanded to platform constraints

STEP 6: A/B Variants (optional)
  If requested:
    a. python3 tools/generate_variants.py generates 3-5 headline/CTA combos
    b. Each variant gets a separate Composition with overridden text
    c. File naming: {platform}/{ad-type}-{variant-letter}.mp4

STEP 7: Batch Personalization (optional)
  If CSV/JSON data file provided:
    a. python3 tools/batch_render.py reads data file
    b. Merges each row with base config
    c. Renders all variants x all platforms in parallel
    d. Outputs organized by platform/variant

STEP 8: Render
  a. Preview: npx remotion studio (local browser preview)
  b. Render all:
     for platform in targets:
       npx remotion render src/index.ts Ad-${platform} out/${platform}.mp4
  c. Or batch: python3 tools/batch_render.py --template . --platforms all

STEP 9: Validate Output
  Claude verifies:
    a. All platform variants rendered successfully
    b. File sizes are within platform upload limits
    c. Duration within platform constraints
    d. Resolution matches platform spec
```

### Duration Allocation by Platform

| Platform | Total | Hook | Problem | Solution | CTA |
|---|---|---|---|---|---|
| TikTok (30s) | 30s | 3s | 7s | 14s | 6s |
| Instagram Reel (15s) | 15s | 2s | 3s | 7s | 3s |
| YouTube Pre-roll (6s) | 6s | 1.5s | — | 2.5s | 2s |
| YouTube Pre-roll (15s) | 15s | 2s | 3s | 7s | 3s |
| Facebook (15s) | 15s | 2s | 3s | 7s | 3s |
| LinkedIn (30s) | 30s | 3s | 7s | 14s | 6s |

YouTube 6s bumper ads skip the Problem scene entirely — they are Solution + CTA only.

---

## 7. SKILL.md Draft

```markdown
---
name: ad-video
description: Generate platform-optimized video ads from a product brief. Supports brand kits, 6 ad types, 6 platform formats (TikTok, Instagram, YouTube, Facebook, LinkedIn), batch personalization, A/B variants, stock footage, screen recordings, and AI voiceover. ~$1-5/video.
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
permissions:
  - filesystem
  - shell
  - network
  - api
tags: [video, advertising, marketing, remotion, batch, brand-kit, social-media]
author: skills-hub
---

# Ad Video

Create platform-optimized video ads from a product brief. Describe your product, get ads for TikTok, Instagram, YouTube, Facebook, and LinkedIn — rendered and ready to upload.

## Setup

### Step 1: Check Prerequisites

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
python3 tools/verify_setup.py
```

The ad-video skill extends the video-toolkit. Ensure video-toolkit is installed and configured first.

### Step 2: Install Additional Dependencies

```bash
cd $TOOLKIT
pip3 install --break-system-packages playwright qrcode[pil] Pillow
playwright install chromium
```

### Step 3: Configure API Keys

Add to `.env`:
```
PEXELS_API_KEY=...    # Free at pexels.com/api (stock footage)
```

Voiceover and music use existing video-toolkit Modal endpoints (Qwen3-TTS, MusicGen).

## Creating an Ad

### Step 1: Create Project

```bash
cd $TOOLKIT
cp -r templates/ad-template projects/MY_AD
cd projects/MY_AD
npm install
```

### Step 2: Define Brand Kit

Create or edit `brand.json`:

```json
{
  "name": "Acme Corp",
  "tagline": "Ship faster, break nothing",
  "website": "https://acme.com",
  "logo": {
    "primary": "brand/logo.svg",
    "light": "brand/logo-light.svg",
    "dark": "brand/logo-dark.svg",
    "icon": "brand/icon.svg",
    "minWidth": 120,
    "safePadding": 16
  },
  "colors": {
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "accent": "#F59E0B",
    "background": "#0F172A",
    "surface": "#1E293B",
    "text": "#F8FAFC",
    "textMuted": "#94A3B8",
    "ctaBackground": "#2563EB",
    "ctaText": "#FFFFFF"
  },
  "fonts": {
    "heading": { "family": "Inter", "weight": 800, "source": "google" },
    "body": { "family": "Inter", "weight": 400, "source": "google" }
  }
}
```

Validate: `python3 tools/brand_validate.py --brand brand.json`

### Step 3: Write Ad Config

Edit `src/config/ad-config.ts`:

```typescript
export const adConfig: AdBrief = {
  type: 'product-launch',
  product: {
    name: 'Acme Deploy',
    tagline: 'Ship faster, break nothing',
    description: 'One-click deployments with automatic rollbacks and zero-downtime.',
    features: [
      'One-click deploy',
      'Automatic rollbacks',
      'Zero-downtime migrations',
    ],
    painPoints: [
      'Deployments take hours and break production',
      'Rollbacks are manual and terrifying',
    ],
    pricing: { amount: '$29/mo', trial: '14-day free trial' },
  },
  assets: {
    productShots: ['products/dashboard.png', 'products/deploy-screen.png'],
    stockQueries: ['developer coding', 'server room'],
  },
  cta: {
    text: 'Start Free Trial',
    url: 'https://acme.com/signup',
    qrCode: true,
  },
  targets: ['tiktok', 'instagram-reel', 'youtube-preroll', 'facebook', 'linkedin'],
  voiceover: { enabled: true, speaker: 'Ryan', tone: 'excited' },
  music: { preset: 'upbeat-tech', volume: 0.12 },
};
```

Ad types: `product-launch`, `feature-highlight`, `testimonial`, `comparison`, `seasonal-promo`, `app-demo`.

### Step 4: Gather Assets

**Stock footage:**
```bash
cd $TOOLKIT
python3 tools/pexels_search.py \
  --query "developer coding" --type video --orientation landscape \
  --output projects/MY_AD/public/stock/
```

**Screen recording (optional):**
```bash
python3 tools/screen_record.py \
  --url "https://app.acme.com/dashboard" \
  --script projects/MY_AD/scripts/demo-flow.json \
  --viewport 1280x720 \
  --output projects/MY_AD/public/recordings/demo.mp4
```

**Voiceover:**
```bash
python3 tools/qwen3_tts.py \
  --text "Tired of deployments that break production? Meet Acme Deploy." \
  --speaker Ryan --tone excited \
  --output projects/MY_AD/public/audio/vo.mp3 --cloud modal
```

**Background music:**
```bash
python3 tools/music_gen.py \
  --preset upbeat-tech --duration 30 \
  --output projects/MY_AD/public/audio/bg.mp3 --cloud modal
```

### Step 5: Generate Composition

Claude reads the ad config and brand kit, then generates the Remotion composition. The composition includes:

1. **HookScene** — Attention-grabbing opener (question, stat, or bold claim)
2. **ProblemScene** — Visualize the pain point
3. **SolutionScene** — Product reveal with key highlights
4. **CTAScene** — Call-to-action with end card

Each scene uses KineticText for headlines, ProductShot for product images, and brand-consistent colors/fonts from brand.json.

**Ad script structure:** Hook (stop scrolling) > Problem (empathy) > Solution (product demo) > CTA (next action).

### Step 6: Render All Platforms

```bash
cd $TOOLKIT/projects/MY_AD

# Preview
npx remotion studio

# Render all platforms
npx remotion render src/index.ts Ad-tiktok out/tiktok.mp4
npx remotion render src/index.ts Ad-instagram-reel out/instagram-reel.mp4
npx remotion render src/index.ts Ad-youtube-preroll out/youtube-preroll.mp4
npx remotion render src/index.ts Ad-facebook out/facebook.mp4
npx remotion render src/index.ts Ad-linkedin out/linkedin.mp4
```

Output: one MP4 per platform in `out/`.

### Step 7: A/B Variants (Optional)

Generate variant headlines and CTAs for testing:

```bash
cd $TOOLKIT
python3 tools/generate_variants.py \
  --config projects/MY_AD/src/config/ad-config.ts \
  --elements headline,cta \
  --count 3 \
  --output projects/MY_AD/variants.json
```

Then render each variant:
```bash
cd $TOOLKIT/projects/MY_AD
npx remotion render src/index.ts Ad-tiktok-A out/tiktok-A.mp4
npx remotion render src/index.ts Ad-tiktok-B out/tiktok-B.mp4
npx remotion render src/index.ts Ad-tiktok-C out/tiktok-C.mp4
```

### Step 8: Batch Personalization (Optional)

Create a CSV with variant data:

```csv
id,headline,ctaText,price,audience
dev-us,"Deploy in 60 seconds","Start Free Trial","$29/mo",developers
mktg-us,"Marketing teams ship 3x faster","Try It Free","$29/mo",marketers
dev-eu,"Ship code with confidence","Start Now","€27/mo",developers-eu
```

Render all:
```bash
cd $TOOLKIT
python3 tools/batch_render.py \
  --template projects/MY_AD \
  --data projects/MY_AD/variants.csv \
  --platforms tiktok,instagram-reel,facebook \
  --parallelism 4 \
  --output projects/MY_AD/out/batch/
```

Output: `out/batch/{platform}/{id}.mp4` — one video per row per platform.

## Platform Specs

| Platform | Aspect | Resolution | FPS | Duration | Notes |
|---|---|---|---|---|---|
| TikTok | 9:16 | 1080x1920 | 30 | 15-60s | Bottom 20% obscured by UI |
| Instagram Reel | 9:16 | 1080x1920 | 30 | 15-30s | Keep text in center 70% |
| Instagram Feed | 4:5 | 1080x1350 | 30 | 3-60s | 4:5 fills more feed space |
| YouTube Pre-roll | 16:9 | 1920x1080 | 30 | 6-15s | Skippable after 5s |
| Facebook | 1:1 | 1080x1080 | 30 | 5-15s | Square performs best in feed |
| LinkedIn | 16:9 | 1920x1080 | 30 | 15-30s | Data/stats perform well |

## Ad Script Framework

Every ad follows the **Hook > Problem > Solution > CTA** structure:

1. **Hook (2-4s):** Stop the scroll. Use a question, shocking stat, bold claim, or pain point. Must grab attention in the first 1.5 seconds.
2. **Problem (3-7s):** Show empathy. Describe the pain the audience feels. Use animated text, frustrated-user visuals, or before/after.
3. **Solution (4-14s):** Reveal the product. Show it in action (screenshots, screen recording, product shots). Highlight 2-3 key features with animated text + stats.
4. **CTA (2-6s):** Clear next action. Animated button, QR code, pricing, and end card with logo + tagline.

Duration varies by platform — see the allocation table in the engineering spec.

## Composition Patterns

### Brand-Consistent Text

ALWAYS load fonts from brand kit. NEVER hardcode font families.

```tsx
const { fontFamily: headingFont } = loadFont({
  family: brand.fonts.heading.family,
  weight: brand.fonts.heading.weight,
});
```

### Product Shot with Animation

```tsx
<ProductShot
  src={staticFile('products/dashboard.png')}
  animation="tilt-3d"
  mockup="browser"
  shadow
/>
```

### Animated CTA Button

```tsx
<CTAButton
  text="Start Free Trial"
  backgroundColor={brand.colors.ctaBackground}
  textColor={brand.colors.ctaText}
  animation="pulse"
  position="bottom-center"
  size="lg"
/>
```

### Platform-Aware Layout

```tsx
<PlatformAdapter platform="tiktok">
  <HookScene brand={brand} style="stat" text="87% of deploys fail" animation="slam" />
  <ProblemScene brand={brand} headline="Deployment is broken" painPoints={[...]} />
  <SolutionScene brand={brand} headline="Meet Acme Deploy" productShot="..." />
  <CTAScene brand={brand} ctaText="Start Free Trial" ctaUrl="..." />
</PlatformAdapter>
```

## Cost Estimates

| Component | Cost | Notes |
|---|---|---|
| Voiceover (Qwen3-TTS) | ~$0.01 | Per scene, ~20s warm GPU |
| Background music (MusicGen) | ~$0.02-0.05 | Duration-dependent |
| Stock footage (Pexels) | Free | 200 req/hr, no attribution needed |
| Screen recording (Playwright) | Free | Local execution |
| AI images (FLUX.2) | ~$0.01/image | If needed for backgrounds |
| Remotion render (local) | Free | ~30s per 30s video |
| Remotion render (Lambda) | ~$0.01-0.10 | Per render, massively parallel |

**Single ad, all 5 platforms:** ~$1-3 total
**Batch of 50 variants x 5 platforms (250 videos):** ~$5-25 total (Lambda) or free (local, ~2 hours)

## Key Rules

1. **Brand kit first** — always validate brand.json before composing
2. **Platform specs are law** — never exceed duration limits, always respect safe zones
3. **Hook in 1.5 seconds** — the first scene MUST grab attention immediately
4. **All motion via useCurrentFrame()** — no CSS animations, no Tailwind animate classes
5. **Always staticFile()** for assets — never require() or import
6. **Always OffthreadVideo** — never raw <video> tags
7. **CTA on every variant** — every ad must end with a clear call-to-action
8. **Test at 1x speed** — preview at actual playback speed before rendering

Source: Built on [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT License)
```

---

## 8. Dependencies

### npm Packages (Remotion project)

| Package | Purpose | Version |
|---|---|---|
| `remotion` | Core video composition | ^4.x |
| `@remotion/cli` | Rendering CLI | ^4.x |
| `@remotion/transitions` | Scene transitions (fade, wipe, slide) | ^4.x |
| `@remotion/media` | Audio/Video embedding | ^4.x |
| `@remotion/google-fonts` | Font loading | ^4.x |
| `@remotion/lambda` | Cloud rendering (optional) | ^4.x |
| `@remotion/light-leaks` | Transition overlays | ^4.x |
| `qrcode` | QR code generation for CTA overlays | ^1.x |
| `react` | UI framework | ^18.x |
| `react-dom` | DOM rendering | ^18.x |
| `typescript` | Type safety | ^5.x |

### Python Packages (tools)

| Package | Purpose |
|---|---|
| `requests` | Pexels API calls |
| `playwright` | Browser automation for screen recording |
| `Pillow` | Image processing, QR code rendering |
| `qrcode` | QR code data generation |
| `python-dotenv` | Environment variable loading |

### External APIs

| API | Cost | Purpose |
|---|---|---|
| **Pexels** | Free (200 req/hr) | Stock photos and videos for B-roll |
| **Modal** (existing) | Pay-per-second (~$0.01-0.20/call) | Qwen3-TTS, FLUX.2, MusicGen GPU endpoints |
| **Remotion Lambda** (optional) | ~$0.01-0.10/render | Cloud-scale parallel rendering |
| **ElevenLabs** (optional) | $5-22/month | Premium voiceover alternative to Qwen3-TTS |

---

## 9. Cost Estimate

### Per-video cost (single platform, single variant)

| Item | Low | High | Notes |
|---|---|---|---|
| Voiceover (Qwen3-TTS) | $0.01 | $0.03 | 1-3 scenes |
| Background music (MusicGen) | $0.02 | $0.05 | 15-60s generation |
| Stock footage (Pexels) | $0.00 | $0.00 | Free API |
| AI images (FLUX.2) | $0.00 | $0.03 | 0-3 generated backgrounds |
| Screen recording | $0.00 | $0.00 | Local Playwright |
| Render (local) | $0.00 | $0.00 | ~30-60s wall time |
| Render (Lambda) | $0.01 | $0.10 | Optional cloud render |
| **Total per video** | **$0.03** | **$0.21** | |

### Per-campaign cost (5 platforms, 1 variant each)

| Scenario | Cost | Time |
|---|---|---|
| Local render, Qwen3 voiceover | ~$0.15-1.00 | ~5-10 min |
| Lambda render, Qwen3 voiceover | ~$0.50-2.00 | ~2-3 min |
| Lambda render, ElevenLabs voiceover | ~$1.00-5.00 | ~2-3 min |

### Batch cost (50 variants x 5 platforms = 250 videos)

| Scenario | Cost | Time |
|---|---|---|
| Local render (4 parallel) | ~$2-5 (voiceover only) | ~2-3 hours |
| Lambda render (50 parallel) | ~$10-25 | ~10-15 min |

### Comparison to competitors

| Solution | Cost for 5-platform campaign | Monthly commitment |
|---|---|---|
| **ad-video (ours)** | $0.15-5.00 | $0/month |
| Shotstack | ~$5-15 | $25-99/month |
| Creatomate | ~$3-10 | $24-99/month |
| InVideo AI | Unlimited (within plan) | $25-60/month |
| Canva Video | Unlimited (within plan) | $13-20/month |
| Lumen5 | Unlimited (within plan) | $29-199/month |

---

## 10. Implementation Stories

Ordered by dependency. Effort: S = 1-2 days, M = 3-5 days, L = 1-2 weeks.

### Phase 1: Foundation (Week 1-2)

| # | Story | Effort | Dependencies |
|---|---|---|---|
| 1 | **Brand kit system** — Define `BrandKit` TypeScript interface, create `brand.json` schema, build `brand.ts` loader with font resolution (Google Fonts + local), write `brand_validate.py` with color contrast checks (WCAG AA). | M | None |
| 2 | **Platform spec engine** — Define `PlatformSpec` constants for all 6 platforms (dimensions, fps, duration bounds, safe zones). Build `PlatformAdapter` component that sets Composition dimensions and applies safe zone insets. Build `SafeZone` debug overlay. | S | None |
| 3 | **Ad config schema** — Define `AdBrief`, `AdType`, `Platform`, `BatchDataRow`, `ABConfig` TypeScript types. Build config parser that validates brief against platform duration constraints. | S | #2 |
| 4 | **KineticText component** — Implement all 6 text animation modes (slide-up, pop-word, typewriter, wave, split-reveal, counter). All animations via `useCurrentFrame()` + `interpolate()` + `spring()`. | M | None |
| 5 | **StatCounter component** — Animated number counter with tabular-nums, prefix/suffix support. | S | #4 |

### Phase 2: Scene Components (Week 2-3)

| # | Story | Effort | Dependencies |
|---|---|---|---|
| 6 | **HookScene component** — 5 animation styles (slam, typewriter, reveal, glitch, zoom-in). Brand-aware colors and fonts. Platform-aware text sizing. | M | #1, #4 |
| 7 | **ProblemScene component** — 4 styles (list, before-after, frustrated-user, x-marks). Staggered pain point animations. | M | #1, #4 |
| 8 | **SolutionScene component** — Product reveal with ProductShot integration. 3 animation modes. | M | #1, #4, #10 |
| 9 | **CTAScene + EndCard** — Animated CTA button, end card with logo/tagline/socials, QR code generation. | M | #1, #4, #11, #12 |
| 10 | **ProductShot component** — 5 animation modes (parallax, zoom-rotate, float, tilt-3d, slide-in). Device mockup frames (phone, laptop, browser). Drop shadow. | M | None |

### Phase 3: Overlay & Specialty Components (Week 3-4)

| # | Story | Effort | Dependencies |
|---|---|---|---|
| 11 | **CTAButton component** — Animated button with pulse, bounce, glow, slide-in. Configurable position and size. | S | #1 |
| 12 | **QRCode component** — Generate QR from URL, render as SVG, 3 animation modes (fade-in, scan-reveal, pixel-build). | S | None |
| 13 | **PriceTag component** — Animated price with discount strike-through. Counter animation for numbers. | S | #5 |
| 14 | **LowerThird component** — Name/title bar with 3 animation styles. | S | #1 |
| 15 | **FeatureScene component** — Single feature highlight with stat counter, screenshot, and animated description. | M | #1, #4, #5, #10 |
| 16 | **TestimonialScene component** — Quote card, full-screen quote, star rating animation. | M | #1, #4 |
| 17 | **ComparisonScene component** — Table, split-screen, and progress-bar comparison styles. | M | #1, #4 |

### Phase 4: Tools & Pipeline (Week 4-5)

| # | Story | Effort | Dependencies |
|---|---|---|---|
| 18 | **Pexels stock search tool** — `tools/pexels_search.py` with keyword search, orientation/color filters, download to project directory, JSON metadata output. | M | None |
| 19 | **Playwright screen recording tool** — `tools/screen_record.py` with scripted actions (click, type, scroll, wait), device emulation, viewport config, MP4 output. | M | None |
| 20 | **ScreenRecording component** — Embed Playwright MP4 in device mockup with optional zoom regions. | S | #19 |
| 21 | **Ad composition root** — `AdVideo.tsx` that reads ad-config.ts + brand.json, maps ad type to scene sequence, creates per-platform Compositions via PlatformAdapter. | M | #1-#17 |
| 22 | **Ad template project** — Complete `templates/ad-template/` with package.json, tsconfig, Remotion config, example brand.json, example ad-config.ts, render scripts. | M | #21 |

### Phase 5: Scale & Automation (Week 5-6)

| # | Story | Effort | Dependencies |
|---|---|---|---|
| 23 | **A/B variant generator** — `tools/generate_variants.py` that uses Claude API to generate headline/CTA/hook variants from the product brief. Outputs variant configs. | M | #3 |
| 24 | **Batch personalization engine** — `tools/batch_render.py` that reads CSV/JSON, merges with base config, renders all variants x all platforms. Local multi-process support. | L | #21, #22 |
| 25 | **Remotion Lambda integration** — Add Lambda as a render backend option in `batch_render.py`. Deploy script, S3 output, cost tracking. | L | #24 |
| 26 | **SKILL.md + documentation** — Write the final SKILL.md with all instructions, validate the end-to-end flow, create example configs for each ad type. | M | All |

### Total effort estimate

| Phase | Stories | Effort |
|---|---|---|
| Phase 1: Foundation | 5 | ~2 weeks |
| Phase 2: Scene Components | 5 | ~2 weeks |
| Phase 3: Overlays & Specialty | 7 | ~1.5 weeks |
| Phase 4: Tools & Pipeline | 5 | ~2 weeks |
| Phase 5: Scale & Automation | 4 | ~2 weeks |
| **Total** | **26 stories** | **~9-10 weeks** |

### Critical path

```
Brand Kit (#1) --> Scene Components (#6-9) --> Ad Composition (#21) --> Template (#22) --> SKILL.md (#26)
                                                     ^
Platform Specs (#2) --> PlatformAdapter (#2) --------+
KineticText (#4) --> All Scene Components (#6-9) ----+
ProductShot (#10) --> SolutionScene (#8) -------------+
```

Stories #18 (Pexels), #19 (Playwright), #23 (A/B), #24 (Batch) can run in parallel with scene component development.

---

## Appendix: Ad Type Scene Maps

### Product Launch
Hook (bold-claim) > Problem (list) > Solution (product-reveal) > Feature x2 > CTA

### Feature Highlight
Hook (curiosity-gap) > Feature (full scene) > Demo (screen recording) > CTA

### Testimonial
Hook (stat/social-proof) > Testimonial (full-screen-quote) > Solution (product-reveal) > CTA

### Comparison
Hook (question) > Comparison (table or split-screen) > Solution (highlights) > CTA

### Seasonal Promo
Hook (urgency) > PriceTag (discount reveal) > Feature (quick highlights) > CTA (deadline)

### App Demo
Hook (pain-point) > ScreenRecording (product in action) > Feature x2 > CTA
