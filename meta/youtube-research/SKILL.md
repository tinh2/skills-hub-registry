---
name: youtube-research
description: Research pipeline — search YouTube, ingest into NotebookLM, generate deliverables, organize in Obsidian vault
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
triggers:
  - youtube research
  - research with notebooklm
  - notebooklm research
  - deep research
  - research pipeline
---

# YouTube Research Pipeline

You are a research agent that orchestrates Claude Code + NotebookLM + Obsidian into a full research pipeline.

## Prerequisites

- `notebooklm` CLI installed via pipx (`notebooklm-py[browser]`)
- Obsidian vault at `~/personal/research-vault/`
- Authenticated: run `notebooklm login` if not already authenticated

## Pipeline Steps

### Phase 1: YouTube Discovery

1. Ask the user for a research topic (or use the one provided)
2. Use `yt-dlp --flat-playlist "ytsearch20:{topic}"` or web search to find 10-20 relevant YouTube videos
3. Collect video URLs, titles, and channel names

### Phase 2: NotebookLM Ingestion

1. Create a new NotebookLM notebook for the research topic:
   ```bash
   notebooklm create "{topic}"
   ```
2. Capture the notebook ID from the output
3. Set it as active:
   ```bash
   notebooklm use {notebook_id}
   ```
4. Add each YouTube video as a source:
   ```bash
   notebooklm source add "{youtube_url}"
   ```
5. Wait for all sources to be indexed

### Phase 3: Research & Analysis

1. Ask NotebookLM targeted research questions:
   ```bash
   notebooklm ask "What are the key themes across these sources?"
   notebooklm ask "What are the most actionable insights?"
   notebooklm ask "Where do these sources disagree?"
   notebooklm ask "What gaps exist in the current approaches?"
   ```
2. Capture answers with citations

### Phase 4: Generate Deliverables

Generate any combination the user requests (default: audio + report):

```bash
# Audio podcast overview
notebooklm generate audio "make it engaging and actionable" --wait
notebooklm download audio ./artifacts/podcast.mp3

# Written report
notebooklm generate report --format study-guide
notebooklm download report ./artifacts/report.md

# Other options: video, slide-deck, quiz, flashcards, infographic, mind-map, data-table
```

### Phase 5: Obsidian Organization

Organize everything into the vault at `~/personal/research-vault/`:

1. **Source files** — Create `sources/{video-title}.md` for each video:

   ```markdown
   ---
   url: { youtube_url }
   channel: { channel_name }
   added: { date }
   notebook: { notebook_id }
   tags: [research, { topic-tag }]
   ---

   # {Video Title}

   Channel: {channel_name}
   URL: {youtube_url}
   ```

2. **Research file** — Create `research/{topic-slug}.md`:

   ```markdown
   ---
   topic: { topic }
   date: { date }
   notebook: { notebook_id }
   sources: { count }
   tags: [research, { topic-tag }]
   ---

   # {Topic} Research

   ## Sources

   {list of [[wikilinks]] to source files}

   ## Key Themes

   {from notebooklm ask results, with [[wikilinks]] to cited sources}

   ## Actionable Insights

   {from notebooklm ask results}

   ## Gaps & Disagreements

   {from notebooklm ask results}

   ## Artifacts

   - [[artifacts/{topic-slug}-podcast.mp3|Audio Overview]]
   - [[artifacts/{topic-slug}-report.md|Written Report]]
   ```

3. **Artifacts** — Save generated files to `artifacts/` with topic-prefixed names

4. **Index** — Update or create `research/INDEX.md` linking all research topics

## Notes

- NotebookLM auth cookies persist for weeks; re-run `notebooklm login` if expired
- Citation markers `[1]`, `[2]` from NotebookLM map to source order — convert to wikilinks
- All NotebookLM generation is free (runs on Google's infra, no API cost)
- For non-YouTube sources (PDFs, URLs, docs), use `notebooklm source add {path_or_url}`
