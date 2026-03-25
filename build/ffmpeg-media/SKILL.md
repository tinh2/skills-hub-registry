---
name: ffmpeg-media
description: Process audio and video with FFmpeg -- encoding, format conversion, trimming, concatenation, audio extraction, noise reduction, volume normalization, watermarking, subtitle burning, GIF creation, thumbnail extraction, and hardware-accelerated transcoding. Covers 100+ input/output formats.
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
  - CURSOR
permissions:
  - filesystem
  - shell
---

# FFmpeg Media Processing

Comprehensive FFmpeg skill for video and audio processing tasks. Use this when you need to manipulate media files programmatically.

## Prerequisites

```bash
# Install ffmpeg and ffprobe
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Verify
ffmpeg -version
ffprobe -version
```

## Video Operations

### Format Conversion

```bash
# MP4 to WebM (VP9)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# MP4 to MOV (ProRes for editing)
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le output.mov

# Any format to MP4 (H.264, widely compatible)
ffmpeg -i input.avi -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4

# H.265/HEVC (50% smaller, slower encode)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -c:a aac output_hevc.mp4
```

### Trimming and Cutting

```bash
# Trim from 00:01:30 for 30 seconds (fast, no re-encode)
ffmpeg -ss 00:01:30 -i input.mp4 -t 30 -c copy trimmed.mp4

# Trim with re-encode (frame-accurate)
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:02:00 -c:v libx264 -c:a aac trimmed.mp4

# Remove first 5 seconds
ffmpeg -ss 5 -i input.mp4 -c copy output.mp4
```

### Concatenation

```bash
# Create file list
echo "file 'part1.mp4'" > list.txt
echo "file 'part2.mp4'" >> list.txt
echo "file 'part3.mp4'" >> list.txt

# Concatenate (same codec)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concatenate (different codecs, re-encode)
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### Resize and Scale

```bash
# Scale to 1920x1080
ffmpeg -i input.mp4 -vf "scale=1920:1080" -c:a copy output.mp4

# Scale to width 1280, auto height (maintain aspect ratio)
ffmpeg -i input.mp4 -vf "scale=1280:-2" -c:a copy output.mp4

# Scale to fit within 1920x1080 (add black bars)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### Speed Changes

```bash
# 2x speed (video + audio)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" output.mp4
```

### Watermark and Overlay

```bash
# Add image watermark (bottom-right, 10px margin)
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Add text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='My Video':fontsize=48:fontcolor=white:x=50:y=50" output.mp4
```

### Subtitles

```bash
# Burn subtitles into video
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4

# Burn ASS/SSA subtitles (styled)
ffmpeg -i input.mp4 -vf "ass=subs.ass" output.mp4

# Add subtitle track (soft subs, no burn)
ffmpeg -i input.mp4 -i subs.srt -c copy -c:s mov_text output.mp4
```

### GIF Creation

```bash
# High-quality GIF with palette
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif

# GIF from specific time range
ffmpeg -ss 5 -t 3 -i input.mp4 -vf "fps=15,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### Thumbnail Extraction

```bash
# Single frame at 10 seconds
ffmpeg -ss 10 -i input.mp4 -vframes 1 thumbnail.png

# Thumbnail every 60 seconds
ffmpeg -i input.mp4 -vf "fps=1/60" thumb_%04d.png

# Best thumbnail (most representative frame)
ffmpeg -i input.mp4 -vf "thumbnail=300" -vframes 1 best_thumb.png
```

## Audio Operations

### Extract Audio

```bash
# Extract audio as MP3
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 192k output.mp3

# Extract audio as WAV (lossless)
ffmpeg -i input.mp4 -vn -c:a pcm_s16le output.wav

# Extract audio as AAC
ffmpeg -i input.mp4 -vn -c:a aac -b:a 256k output.m4a
```

### Volume and Normalization

```bash
# Increase volume by 6dB
ffmpeg -i input.mp3 -af "volume=6dB" louder.mp3

# Normalize audio (EBU R128 loudness)
ffmpeg -i input.mp3 -af loudnorm output.mp3

# Detect audio levels first
ffmpeg -i input.mp3 -af "volumedetect" -f null /dev/null
```

### Noise Reduction

```bash
# Simple noise gate
ffmpeg -i input.mp3 -af "afftdn=nf=-25" cleaned.mp3

# High-pass filter (remove low rumble)
ffmpeg -i input.mp3 -af "highpass=f=80" cleaned.mp3

# Combined: high-pass + noise reduction + normalization
ffmpeg -i input.mp3 -af "highpass=f=80,afftdn=nf=-25,loudnorm" cleaned.mp3
```

### Audio Mixing

```bash
# Mix two audio tracks (voice + music)
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first" mixed.mp3

# Add audio to video (replace existing)
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Merge audio into video (keep both tracks)
ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0 -map 1:a output.mp4
```

### Silence Detection

```bash
# Detect silence (threshold -30dB, min 0.5s)
ffmpeg -i input.mp3 -af "silencedetect=noise=-30dB:d=0.5" -f null /dev/null 2>&1 | grep silence

# Remove silence
ffmpeg -i input.mp3 -af "silenceremove=start_periods=1:start_silence=0.5:start_threshold=-30dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_silence=0.5:start_threshold=-30dB:detection=peak,aformat=dblp,areverse" output.mp3
```

## Probe and Analysis

```bash
# Get duration
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp4

# Get resolution
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4

# Get all stream info (JSON)
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Get audio sample rate and channels
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels -of csv=p=0 input.mp3
```

## Hardware Acceleration

```bash
# NVIDIA GPU (NVENC)
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset p4 -crf 23 output.mp4

# Apple Silicon (VideoToolbox)
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# Intel QSV
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv -preset medium output.mp4
```

## Common Patterns for Video Production

### Remotion Post-Processing

```bash
# Add background music to rendered video
ffmpeg -i rendered.mp4 -i bg-music.mp3 \
  -filter_complex "[1:a]volume=0.12[bg];[0:a][bg]amix=inputs=2:duration=first" \
  -c:v copy -c:a aac final.mp4

# Add fade in/out
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=58:d=2" \
  -af "afade=t=in:st=0:d=1,afade=t=out:st=58:d=2" output.mp4
```

### Social Media Export

```bash
# Instagram Reel (9:16, 1080x1920)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy reel.mp4

# Twitter/X (max 2:20, 1280x720)
ffmpeg -i input.mp4 -t 140 -vf "scale=1280:720" -c:a aac twitter.mp4

# YouTube Shorts (9:16, 1080x1920, max 60s)
ffmpeg -i input.mp4 -t 60 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" short.mp4
```

## Tips

1. Use `-c copy` when possible to avoid re-encoding (faster, no quality loss)
2. CRF values: lower = better quality, larger file. 18-23 is good for H.264
3. Always use `-movflags +faststart` for web MP4s (enables streaming)
4. Use `ffprobe` to inspect files before processing
5. Chain filters with commas: `-vf "scale=1280:-2,fps=30"`
