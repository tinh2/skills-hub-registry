---
name: video-toolkit
description: Create professional videos autonomously using AI -- voiceovers (Qwen3-TTS with voice cloning), image generation (FLUX.2), background music (MusicGen), talking head animation (SadTalker), and Remotion rendering. Uses cloud GPUs via Modal or RunPod. Full pipeline from text brief to rendered MP4.
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

# Video Toolkit

Create professional explainer videos from a text brief. Uses open-source AI models on cloud GPUs (Modal or RunPod) for voiceover, image generation, music, and talking head animation. Remotion (React) handles composition and rendering.

## Setup

### Step 1: Check Current State

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
python3 tools/verify_setup.py
```

### Step 2: Install Dependencies

```bash
cd $TOOLKIT
pip3 install --break-system-packages -r tools/requirements.txt
```

### Step 3: Configure Cloud GPU Endpoints

The toolkit needs Modal endpoint URLs in `.env`:

```bash
pip3 install --break-system-packages modal
python3 -m modal setup   # Opens browser for auth

# Deploy each tool
cd $TOOLKIT
modal deploy docker/modal-qwen3-tts/app.py
modal deploy docker/modal-flux2/app.py
modal deploy docker/modal-music-gen/app.py
modal deploy docker/modal-sadtalker/app.py
modal deploy docker/modal-image-edit/app.py
modal deploy docker/modal-upscale/app.py
modal deploy docker/modal-propainter/app.py
```

Add each URL to `.env`:
```
MODAL_QWEN3_TTS_ENDPOINT_URL=https://...modal.run
MODAL_FLUX2_ENDPOINT_URL=https://...modal.run
MODAL_MUSIC_GEN_ENDPOINT_URL=https://...modal.run
MODAL_SADTALKER_ENDPOINT_URL=https://...modal.run
MODAL_IMAGE_EDIT_ENDPOINT_URL=https://...modal.run
MODAL_UPSCALE_ENDPOINT_URL=https://...modal.run
MODAL_DEWATERMARK_ENDPOINT_URL=https://...modal.run
```

Optional -- Cloudflare R2 for reliable file transfer:
```
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=video-toolkit
```

## Creating a Video

### Step 1: Create Project

```bash
cd $TOOLKIT
cp -r templates/product-demo projects/PROJECT_NAME
cd projects/PROJECT_NAME
npm install
```

Templates: `product-demo` (marketing/explainer), `sprint-review`, `sprint-review-v2` (composable scenes).

### Step 2: Write Config

Edit `projects/PROJECT_NAME/src/config/demo-config.ts`:

```typescript
export const demoConfig: ProductDemoConfig = {
  product: {
    name: 'My Product',
    tagline: 'What it does in one line',
    website: 'example.com',
  },
  scenes: [
    { type: 'title', durationSeconds: 9, content: { headline: '...', subheadline: '...' } },
    { type: 'problem', durationSeconds: 14, content: { headline: '...', problems: ['...'] } },
    { type: 'solution', durationSeconds: 13, content: { headline: '...', highlights: ['...'] } },
    { type: 'stats', durationSeconds: 12, content: { stats: [{value: '99%', label: '...'}] } },
    { type: 'cta', durationSeconds: 10, content: { headline: '...', links: ['...'] } },
  ],
  audio: {
    backgroundMusicFile: 'audio/bg-music.mp3',
    backgroundMusicVolume: 0.12,
  },
};
```

Scene types: `title`, `problem`, `solution`, `demo`, `feature`, `stats`, `cta`.

**Duration rule:** `ceil(word_count / 2.5) + 2`.

### Step 3: Write Voiceover Script

Create `projects/PROJECT_NAME/VOICEOVER-SCRIPT.md`:

```markdown
## Scene 1: Title (9s, ~17 words)
Build videos with AI. The toolkit makes it easy.

## Scene 2: Problem (14s, ~30 words)
The problem statement goes here. Keep it punchy and relatable.
```

**Word budget per scene:** `(durationSeconds - 2) * 2.5` words.

### Step 4: Generate Assets

**All commands must run from toolkit root (`$TOOLKIT`).**

#### Background Music

```bash
cd $TOOLKIT
python3 tools/music_gen.py \
  --preset corporate-bg \
  --duration 90 \
  --output projects/PROJECT_NAME/public/audio/bg-music.mp3 \
  --cloud modal
```

Presets: `corporate-bg`, `upbeat-tech`, `ambient`, `dramatic`, `tension`, `hopeful`, `cta`, `lofi`.

#### Voiceover (per-scene)

```bash
cd $TOOLKIT
python3 tools/qwen3_tts.py \
  --text "The voiceover text for scene one." \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal
```

**Speakers:** `Ryan`, `Aiden`, `Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ono_Anna`, `Sohee`
**Tones:** `neutral`, `warm`, `professional`, `excited`, `calm`, `serious`, `storyteller`, `tutorial`

For voice cloning:
```bash
python3 tools/qwen3_tts.py \
  --text "Text to speak" \
  --ref-audio assets/voices/reference.m4a \
  --ref-text "Exact transcript of the reference audio" \
  --output output.mp3 --cloud modal
```

#### Scene Images

```bash
cd $TOOLKIT
python3 tools/flux2.py \
  --prompt "Dark tech background with blue geometric grid" \
  --width 1920 --height 1080 \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal
```

Image presets: `title-bg`, `problem`, `solution`, `demo-bg`, `stats-bg`, `cta`, `thumbnail`, `portrait-bg`

#### Talking Head (optional)

```bash
cd $TOOLKIT
# Generate portrait
python3 tools/flux2.py \
  --prompt "Professional presenter portrait, dark background, facing camera" \
  --width 1024 --height 576 \
  --output projects/PROJECT_NAME/public/images/presenter.png --cloud modal

# Animate per scene
python3 tools/sadtalker.py \
  --image projects/PROJECT_NAME/public/images/presenter.png \
  --audio projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --preprocess full --still --expression-scale 0.8 \
  --output projects/PROJECT_NAME/public/narrator-01.mp4 --cloud modal
```

**SadTalker rules:**
- ALWAYS use `--preprocess full` (default `crop` gives wrong aspect ratio)
- ALWAYS use `--still` (reduces head movement)
- ALWAYS generate per-scene clips, NEVER one long video

### Step 5: Sync Timing

```bash
cd $TOOLKIT
for f in projects/PROJECT_NAME/public/audio/scenes/*.mp3; do
  echo "$(basename $f): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")s"
done
```

Update `durationSeconds` in config to `ceil(actual_audio_duration + 2)`.

### Step 6: Review and Render

```bash
cd $TOOLKIT/projects/PROJECT_NAME
npx remotion still src/index.ts ProductDemo --frame=100 --output=/tmp/review.png
npm run render
```

Output: `out/ProductDemo.mp4`

## Composition Patterns

### Per-Scene Audio (1s delay)

```tsx
<Sequence from={30}>
  <Audio src={staticFile('audio/scenes/01.mp3')} volume={1} />
</Sequence>
```

### Narrator PiP

```tsx
<Sequence from={30}>
  <OffthreadVideo
    src={staticFile('narrator-01.mp4')}
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

## Cost Estimates (Modal)

| Tool | Cost | Notes |
|------|------|-------|
| Qwen3-TTS | ~$0.01/scene | ~20s warm GPU |
| FLUX.2 | ~$0.01/image | ~3s warm |
| MusicGen | ~$0.02-0.05 | Duration-dependent |
| SadTalker | ~$0.05-0.20/scene | ~3-4 min per 10s audio |
| RealESRGAN | ~$0.005/image | Very fast |

**Total 60s video:** ~$1-3. Modal Starter: $30/month free compute.

Source: [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT License)
