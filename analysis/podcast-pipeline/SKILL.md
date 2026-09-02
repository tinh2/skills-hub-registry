---
name: podcast-pipeline
description: "Audio file → full publishing kit pipeline. From a single .mp3 or .wav per episode, generates Whisper-large-v3 transcript with word-level timestamps, automatic chapter detection (audio scene change + topic shift), two show-notes lengths (scannable summary + long-form SEO)."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Podcast Publishing Pipeline

You convert one raw audio file into a complete publishing kit: transcript, chapters, show notes (two formats), SEO blog post, social shorts, quote graphics, and social-thread drafts. Modern podcast SEO requires a per-episode webpage with full transcript + JSON-LD — without it, episodes are invisible to Google and AI Overviews.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Audio file accessible** (mp3, wav, m4a, flac). Local file or accessible URL.
- [ ] **Episode metadata**: number, title, guest(s), publish date, primary topics.
- [ ] **Transcription engine**: Whisper-large-v3 (open source, run locally with GPU/MLX), Deepgram Nova-3 (API, fastest), AssemblyAI Universal-2, OpenAI Whisper API, or Replicate.
- [ ] **Brand kit**: logo, color palette, hosts' photos (for quote graphics + audiogram).
- [ ] **CMS / publish target**: WordPress, Ghost, Squarespace, Substack, custom static site.
- [ ] **Episode duration**: ≤ 90 min runs end-to-end in ~10 min on a Whisper-large GPU; 3+ hours needs chunking.

Recovery:

- If audio quality is poor (heavy background noise), pre-process with `ffmpeg` afftdn / RNNoise before transcription.
- If no GPU available, route to Deepgram or OpenAI Whisper API and surface the per-minute cost.
- For multi-host episodes, prefer Whisper-large + pyannote.audio diarization to get speaker labels right.

============================================================
=== PHASE 1: TRANSCRIPTION ===
============================================================

Generate transcript with word-level timestamps and speaker labels.

**Whisper-large-v3** (preferred, local):

```python
import whisperx  # whisperx adds word-level alignment + diarization

model = whisperx.load_model("large-v3", device="cuda", compute_type="float16")
audio = whisperx.load_audio(episode_path)
result = model.transcribe(audio, batch_size=16, language="en")

# Word-level alignment
align_model, metadata = whisperx.load_align_model(language_code=result["language"], device="cuda")
result = whisperx.align(result["segments"], align_model, metadata, audio, "cuda")

# Diarization (pyannote.audio)
diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device="cuda")
diarize_segments = diarize_model(audio, num_speakers=NUM_SPEAKERS)
result = whisperx.assign_word_speakers(diarize_segments, result)
```

Persist as `transcript.json` with schema:

```json
{
  "segments": [
    {"start": 0.0, "end": 4.2, "speaker": "SPEAKER_00", "text": "Welcome to the show.", "words": [...]},
    ...
  ],
  "metadata": {"language": "en", "duration_s": 3245.6}
}
```

Also export `transcript.srt` (SubRip) and `transcript.vtt` (WebVTT) for video editing / web players.

VALIDATION: Transcript word count is non-trivial (≥ duration_min × 100, since typical speech is 130-150 wpm). Speakers labeled if > 1 voice in audio.

============================================================
=== PHASE 2: CHAPTER DETECTION ===
============================================================

Generate chapter markers in three ways and merge:

1. **Acoustic scene change**: detect ≥ 2s silence + speaker change.
2. **Topic shift**: embed each 60-second window with `all-MiniLM-L6-v2` or `text-embedding-3-small`; cosine-distance peaks = chapter boundary.
3. **LLM pass**: ask Claude / Gemini to read the transcript and propose 5-10 chapter titles with timestamps.

Reconcile the three into 5-12 chapters. Each chapter:

```
00:00 — Cold open
01:23 — Introducing today's guest
04:15 — How {topic} broke open
12:47 — The {key insight}
...
```

Embed as ID3 chapter markers in the mp3 file (for podcast players that support chapters: Apple Podcasts, Overcast, Pocket Casts, Spotify).

VALIDATION: Chapter count 5-12. First chapter starts at 00:00. Title ≤ 60 chars each.

============================================================
=== PHASE 3: SHOW NOTES — TWO FORMATS ===
============================================================

**Format A — Scannable** (≤ 400 words, for podcast player descriptions and listen-page above-fold):

```markdown
{Episode title}

{Guest}, {their title at their company}, joins us to discuss {three sentence hook}.

In this episode, we cover:

- {Beat 1 — verb-led}
- {Beat 2}
- {Beat 3}
- {Beat 4}
- {Beat 5}

## Resources mentioned

- {Book / article / tool}
- {...}

## Find {guest}

- {Twitter / X}
- {LinkedIn}
- {Their company / project}

## Chapters

{from Phase 2}
```

**Format B — Long-form SEO** (1500-2500 words for the episode webpage):

- Hook lead (60-80 words answering the episode's core question — AI Overview target).
- Full chapter-by-chapter summary with timestamp anchors.
- Quotes block: 3-5 verbatim quotes with attribution.
- Full transcript appended (or linked).
- "Listen to {episode title}" outbound links to Spotify, Apple Podcasts, Overcast, YouTube.
- Author byline + episode date (E-E-A-T signal).

VALIDATION: Format A respects 400-word cap. Format B has lead in first 80 words + full chapter coverage.

============================================================
=== PHASE 4: SEO BLOG POST ===
============================================================

Generate `blog_post.md` (~600-1000 words) — a derivative article driving organic traffic. Structure:

1. **H1** — keyword-optimized title (different from episode title; targets a Google query).
2. **TL;DR** — 50-word answer to the H1 (AEO target).
3. **Background** — 1-2 paragraphs framing the topic.
4. **Key insights from the episode** — 3-5 H2 sections, each anchored to a chapter.
5. **Quote callouts** — 2-3 pull-quotes inline.
6. **Listen to the full episode** — embed player + listen-on-platform links.

Plus `blog_jsonld.json`:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "...",
  "datePublished": "...",
  "author": { "@type": "Person", "name": "..." },
  "image": "...",
  "mainEntityOfPage": "...",
  "associatedMedia": {
    "@type": "PodcastEpisode",
    "name": "...",
    "url": "...",
    "associatedMedia": { "@type": "MediaObject", "contentUrl": "{mp3 url}" },
    "partOfSeries": { "@type": "PodcastSeries", "name": "...", "url": "..." }
  }
}
```

VALIDATION: JSON-LD validates via Rich Results Test. Blog targets a different query than episode title.

============================================================
=== PHASE 5: SOCIAL SHORTS (60-SECOND VERTICAL CLIPS) ===
============================================================

For each chapter or quote, generate a short:

1. **Pick the 3-5 highest-engagement moments** — heuristic: longest applause/laugh pattern, sharpest answer to a question, or a quote-shaped sentence the speaker leaned in on.
2. **Trim to ≤ 60s** via `ffmpeg -ss start -to end`.
3. **Re-encode vertical** (9:16, 1080×1920) with auto-crop centered on speaker or static brand-blur background.
4. **Burn captions** from word-level transcript (highlighted-word style, ~3-4 words at a time, branded color).
5. **Add intro card** (1.5s with episode title + handle) and outro card (1.5s "Full episode → {link}").
6. **Export** as `shorts/short_{n}.mp4` ready for direct upload.

Generate captions per platform:

- TikTok: caption + 3-5 hashtags + handle.
- Instagram Reels: caption + hashtags.
- YouTube Shorts: caption + #Shorts tag.

VALIDATION: Each short is ≤ 60s. Captions burned and word-synced. Vertical aspect ratio confirmed.

============================================================
=== PHASE 6: QUOTE GRAPHICS ===
============================================================

For each of the 3-5 best quotes, generate a 1080×1080 image (Instagram-grid friendly):

- Background: brand color or photo blur.
- Foreground: large quote text (40-60pt), attribution ("— {guest}, {episode N}"), small show logo.
- Output PNG via `Pillow` or `playwright` + HTML template + screenshot.

Each graphic also gets a paired caption file with one-tap social copy.

VALIDATION: Quote text is verbatim from transcript. Attribution correct. Image dimensions exact.

============================================================
=== PHASE 7: SOCIAL THREAD DRAFTS ===
============================================================

Generate X/LinkedIn/Threads multi-post drafts:

- **Post 1 (hook)**: provocative claim from episode + episode link.
- **Posts 2-6 (insights)**: one beat per post, ≤ 280 chars X / ~1200 chars LinkedIn.
- **Post 7 (CTA)**: "Listen to the full episode → {link}".

For LinkedIn, longer single-post format (~1500 chars) is more native than multi-post threads — generate both.

VALIDATION: Character limits respected per platform.

============================================================
=== PHASE 8: PACKAGE & PUBLISH ===
============================================================

Final delivery:

```
episode-{slug}/
├── README.md                    # where each file goes
├── transcript.json
├── transcript.srt
├── transcript.vtt
├── chapters.txt
├── show_notes_short.md
├── show_notes_long.md
├── blog_post.md
├── blog_jsonld.json
├── episode_page.html            # ready to drop into CMS
├── shorts/
│   ├── short_1.mp4 (with caption.txt + hashtags.txt)
│   └── ...
├── graphics/
│   ├── quote_1.png (with caption.txt)
│   └── ...
└── socials/
    ├── x_thread.md
    ├── linkedin_post.md
    └── threads_post.md
```

VALIDATION: Every artifact present. README explains where each goes per CMS (WordPress media library, Ghost post HTML body, Substack import).

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 8 phases produced artifacts?
- **Robust**: Long episodes chunked correctly? Diarization assigned speakers?
- **Clean**: Transcript word count plausible? Chapters at sensible boundaries?
- **Publishing-credible**: Would a podcast producer running 100+ episodes accept this output as "drop-in ready"?

Common gap: trimming shorts at awkward mid-sentence boundaries. Verify start/end snap to sentence boundaries from word-level timestamps.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/podcast-pipeline/LEARNINGS.md`:

## <YYYY-MM-DD> — <episode length, host count, content type>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never publish without a transcript. Episodes without transcripts are invisible to Google + AI search and inaccessible to deaf/HoH listeners.
- Never auto-generate quotes that misattribute. Always pull verbatim with speaker label from diarization.
- Never trim shorts mid-word or mid-sentence. Snap to word boundaries from Whisper alignment.
- Always include JSON-LD PodcastEpisode + BlogPosting. Schema is load-bearing for AI Overview citations.
- Always upload the audio's first 10 seconds intact (player previews; bad opening = drop-off).
