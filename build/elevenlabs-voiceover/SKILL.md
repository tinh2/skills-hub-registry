---
name: elevenlabs-voiceover
description: "Generate professional AI voiceovers using ElevenLabs TTS for video narration, explainers, and content creation."
version: "1.0.1"
category: build
platforms:
  - CLAUDE_CODE
  - CURSOR
permissions:
  - filesystem
  - shell
  - api
---

# ElevenLabs Voiceover Generation

Generate professional AI voiceovers for Remotion videos using ElevenLabs API.

## Prerequisites

- `ELEVENLABS_API_KEY` in `.env.local`
- Node.js installed
- ffmpeg/ffprobe installed (for timing validation and thumbnail embedding)

## Quick Start

```bash
# Generate voiceover from text
node generate.js --text "Your text here" --output public/audio/voiceover.mp3

# Generate with narrator style (more natural)
node generate.js --text "Your text" --character narrator --output voiceover.mp3

# Generate scenes with request stitching
node generate.js --scenes remotion/scenes.json --output-dir public/audio/project/

# Regenerate a single scene
node generate.js --scenes scenes.json --scene scene2 --new-text "Updated text"

# List available voices and character presets
node generate.js --list-voices
node generate.js --list-characters
```

## Character Presets

Use character presets for more natural voiceovers instead of literal screen text reading:

| Character | Description | Best For |
|-----------|-------------|----------|
| `literal` | Reads text exactly as written | Screen text, quotes |
| `narrator` | Professional storyteller, smooth, engaging | Explainers, documentaries |
| `salesperson` | Enthusiastic, persuasive, energetic | Marketing, ads |
| `expert` | Authoritative, confident, knowledgeable | Legal content, tutorials |
| `conversational` | Casual, friendly, natural | Social media, casual content |
| `dramatic` | Intense, emotional, impactful | Hooks, problem statements |
| `calm` | Soothing, reassuring, gentle | Trust-building, conclusions |

```bash
# Use narrator style globally
node generate.js --scenes scenes.json --character narrator --output-dir public/audio/

# Or set per-scene in scenes.json
{
  "scenes": [
    { "id": "scene1", "text": "Problem statement", "character": "dramatic" },
    { "id": "scene2", "text": "Solution", "character": "calm" }
  ]
}
```

## Scene-Based Generation with Request Stitching

Generate multiple scenes with consistent prosody using ElevenLabs request stitching:

### scenes.json Format

```json
{
  "name": "product-demo",
  "voice": "George",
  "character": "narrator",
  "scenes": [
    {
      "id": "scene1",
      "text": "Generic text-to-speech sounds robotic. Your brand deserves better.",
      "duration": 4.5,
      "character": "dramatic"
    },
    {
      "id": "scene2",
      "text": "With voice cloning, you can use your own voice for unlimited content.",
      "duration": 5.5
    },
    {
      "id": "scene3",
      "text": "Record a short sample. Clone it. Create professional voiceovers in minutes.",
      "duration": 6,
      "delay": 0.3
    }
  ]
}
```

### Generate All Scenes

```bash
node generate.js \
  --scenes remotion/product-demo-scenes.json \
  --output-dir public/audio/product-demo/
```

This creates:
- `product-demo-scene1.mp3` through `sceneN.mp3`
- `product-demo-combined.mp3` (all scenes stitched)
- `product-demo-info.json` (metadata with durations)

### Single Scene Regeneration

```bash
# Regenerate scene2 with new text
node generate.js --scenes scenes.json --scene scene2 --new-text "Updated text" --output-dir public/audio/project/

# Regenerate scene3 with different character
node generate.js --scenes scenes.json --scene scene3 --character salesperson --output-dir public/audio/project/
```

## Thumbnail Embedding

Embed a thumbnail image into MP4 videos for platform previews:

```bash
# Basic usage
node generate.js --embed-thumbnail public/videos/promo.mp4 --thumbnail public/videos/thumbnail.png

# Custom output path
node generate.js --embed-thumbnail promo.mp4 --thumbnail thumbnail.png --output promo-final.mp4
```

## Timing Validation

Automatically validates timing after generation using `ffprobe`:

| Check | Threshold | Description |
|-------|-----------|-------------|
| Duration mismatch | >15% | Warns if actual differs from expected |
| Leading silence | >200ms | Audio starts late |
| Trailing silence | >500ms | Unnecessary silence at end |
| Speaking rate | 2-4.5 wps | Optimal ~3 words/second |

```bash
# Validate all scenes in a project
node generate.js --validate public/audio/product-demo/
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--text`, `-t` | Text to convert to speech | Required (or --file/--scenes) |
| `--file`, `-f` | Read text from file | - |
| `--output`, `-o` | Output file path | `output.mp3` |
| `--output-dir` | Output directory for scenes | `public/audio` |
| `--voice`, `-v` | Voice name or ID | `George` |
| `--model`, `-m` | Model ID | `eleven_multilingual_v2` |
| `--character`, `-c` | Character preset | `literal` |
| `--scenes` | JSON file with scenes | - |
| `--scene` | Regenerate single scene ID | - |
| `--new-text` | New text for scene regen | - |
| `--validate` | Validate existing audio dir | - |
| `--embed-thumbnail` | Video file to embed thumbnail into | - |
| `--thumbnail` | Thumbnail image file (PNG/JPG) | - |

## Recommended Voices

| Voice | Style | Best For |
|-------|-------|----------|
| `George` | Warm, captivating British | Narration, explainers |
| `Antoni` | Professional, warm | Legal content, tutorials |
| `Arnold` | Authoritative, deep | Corporate, serious topics |
| `Josh` | Friendly, conversational | Marketing, casual content |

## Integration with Remotion

```tsx
import { Audio, Sequence, staticFile } from "remotion";

const SCENE_DURATIONS = {
  scene1: 4.5,  // From info.json
  scene2: 5.5,
};

export const VideoWithVoiceover: React.FC = () => {
  const { fps } = useVideoConfig();
  const scene1Frames = Math.round(SCENE_DURATIONS.scene1 * fps);

  return (
    <>
      <Sequence from={0} durationInFrames={scene1Frames}>
        <Audio src={staticFile("audio/project/project-scene1.mp3")} volume={1} />
        <Scene1Visual />
      </Sequence>
      <Sequence from={scene1Frames}>
        <Audio src={staticFile("audio/project/project-scene2.mp3")} volume={1} />
        <Scene2Visual />
      </Sequence>
    </>
  );
};
```

## Tips

1. **Use character presets** -- don't read screen text literally
2. **Punctuation matters** -- periods for pauses, commas for brief breaks
3. **Write out numbers** -- "five hundred" not "500"
4. **Scene-by-scene** -- different scenes can have different characters
5. **Fine-tune** -- use `--scene` to regenerate individual scenes
6. **Request stitching** -- keeps voice consistent across scenes

Source: [maartenlouis/elevenlabs-remotion-skill](https://github.com/maartenlouis/elevenlabs-remotion-skill) (MIT License)
