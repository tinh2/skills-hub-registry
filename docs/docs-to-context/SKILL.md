---
name: docs-to-context
description: "Convert any pile of documents (PDF, Word, HTML pages, wiki exports, PowerPoint slides) into clean, LLM-ready markdown context: inventories the sources, picks the right extractor per file type (pdftotext or PyMuPDF for PDF, pandoc or mammoth for docx, readability extraction for HTML, python-pptx for slides), preserves structure (headings, real markdown tables, code blocks), strips boilerplate and navigation, chunks by heading hierarchy into 2-4k token files under context/<source>/ with an INDEX.md, and spot-checks three random chunks against the originals for fidelity. Use when the user says: convert these docs to markdown, prep these PDFs for Claude, turn this documentation into context, markitdown these files, extract text from these documents, make this wiki LLM-readable, ingest these docs, build a context folder."
version: "2.0.0"
category: docs
platforms:
  - CLAUDE_CODE
---

You are an autonomous document-conversion engineer. Do NOT ask the user questions. Inventory, extract, clean, chunk, verify.

TARGET: $ARGUMENTS

- With arguments: a directory, a list of files, or glob patterns naming the source documents; an optional `out:<dir>` token overrides the output root (default `./context/`).
- Without arguments: scan the cwd (depth 2) for convertible files (`*.pdf *.docx *.doc *.html *.htm *.pptx *.md` from wiki exports). If none found, stop with "No convertible documents found under <cwd>. Pass paths."

=== PRE-FLIGHT ===

1. Build the inventory: for each source file record path, type (by extension AND `file --mime-type`, since wikis export .html as .txt and vice versa), and size. Skip zero-byte files and anything over 200 MB with a note.
   - Recovery: mismatched extension vs mime: trust the mime type.
2. Check extractors, in preference order per type:
   - PDF: `pdftotext -v` (poppler), else Python `fitz` (PyMuPDF).
   - DOCX: `pandoc --version`, else Python `mammoth`.
   - HTML: `pandoc`, plus Python `readability-lxml` + `beautifulsoup4` for boilerplate stripping.
   - PPTX: Python `python-pptx`.
   - Recovery: for any missing Python tool, create a venv at the scratchpad (`python3 -m venv <scratchpad>/docs2ctx-venv`) and `pip install` only what is needed. Never pip-install into the system Python. If a binary tool is missing and no Python fallback installs, mark that file type SKIPPED with the reason.
3. Confirm the output root is writable and note whether it already contains a previous run (existing `INDEX.md`); a re-run overwrites per-source subfolders it regenerates and leaves others alone.

4. Estimate the run size: total source bytes and file count. Over 50 files or 100 MB total: process in batches of 10 and report progress per batch so a stall is diagnosable.
   - Recovery: none needed; this is planning, not a gate.

=== PHASE 1: EXTRACT WITH STRUCTURE ===

Per file, into a raw intermediate at `<scratchpad>/raw/<source-name>.md`:

1. PDF: `pdftotext -layout` first; if headings and tables come out mangled (all text same weight, columns interleaved), switch to PyMuPDF and reconstruct headings from font-size clusters (largest 2-3 size tiers become #/##/###). Tables: reconstruct as markdown tables when column alignment is detectable; otherwise keep as fenced text blocks labeled `table (unstructured)`.
2. DOCX: `pandoc -f docx -t gfm --wrap=none`; mammoth fallback emits HTML, pipe through `pandoc -f html -t gfm`.
3. HTML: run readability extraction to isolate the article body, then `pandoc -f html -t gfm --wrap=none`. Keep `<pre>/<code>` as fenced code blocks with a language tag when the class hints one.
4. PPTX: per slide emit `## Slide N: <title>`, bullet text as list items, speaker notes under `> Notes:` blockquotes, table shapes as markdown tables.
5. Record per file: extractor used, heading count, table count, code-block count.

VALIDATION: Every non-skipped source produced a raw .md with non-trivial length (at least 1% of source bytes or 200 chars) and at least one heading (synthesize `# <filename>` if the format truly has none).
FALLBACK: If an extractor crashes on a file, try the next extractor in the preference chain; if all fail, mark the file FAILED with the error's first line and continue. Never let one bad file kill the run.

=== PHASE 2: CLEAN ===

1. Strip repeated boilerplate: lines occurring on 3+ pages of the same PDF (headers/footers/page numbers), nav/menu/cookie/footer remnants in HTML, "Confidential" stamps.
   Detect repeats mechanically (sort raw lines, count duplicates above a length threshold) rather than by eyeballing.
2. Dedupe: if two sources are near-identical (same title and over 80% identical lines), keep the newer one and note the drop.
3. Normalize: collapse 3+ blank lines to one, strip trailing whitespace, fix mid-word hyphen linebreaks from PDFs ("infor-\nmation" -> "information"), demote skipped heading levels so the hierarchy is contiguous.
4. Do NOT rewrite sentences, summarize, or "improve" wording. Cleaning is subtractive only.

VALIDATION: Cleaned length is within 40-100% of raw length (bigger cuts mean you probably deleted content, not boilerplate); heading hierarchy has no jumps (no # straight to ###).
FALLBACK: If a file lost more than 60%, diff raw vs cleaned, restore the largest removed non-repeating block, and re-check.

=== PHASE 3: CHUNK AND INDEX ===

1. Split each cleaned document at heading boundaries, greedily packing sibling sections until a chunk reaches roughly 2-4k tokens (estimate: words x 1.33). Never split inside a table or code fence; oversize atomic sections become a single oversized chunk with a note.
2. Write chunks to `context/<source-name-slug>/NN-<section-slug>.md`. Each chunk starts with a provenance header:

```markdown
<!-- source: <original path> | section: <heading trail> | chunk NN/<total> -->
```

3. Write `context/INDEX.md`: one section per source with source path, extractor, chunk table (file, heading trail, ~tokens), plus a top summary line "N sources, N chunks, ~N total tokens" and a list of SKIPPED/FAILED files with reasons.

VALIDATION: Every chunk is 200 tokens to ~5k tokens (flag outliers), every chunk file listed in INDEX.md exists on disk and vice versa.
FALLBACK: Merge sub-200-token fragments into their preceding sibling; regenerate INDEX.md after any merge.

=== PHASE 4: FIDELITY SPOT-CHECK ===

1. Pick 3 random chunks (or all, if fewer than 3 exist) spanning different sources.
2. For each, locate the corresponding passage in the ORIGINAL document (re-extract that page/section directly) and compare: are the facts, numbers, table values, and code intact and in order?
3. Score each PASS/FAIL with a one-line finding.

VALIDATION: 3/3 PASS.
FALLBACK: On any FAIL, re-extract that source with the alternate extractor, re-clean, re-chunk that source only, and re-check it. If it still fails, mark the source LOW-FIDELITY in INDEX.md so a consumer knows to trust the original.

=== OUTPUT ===

```
DOCS -> CONTEXT: <out-dir>
Sources: <n> converted, <n> skipped, <n> failed
Chunks: <n> files, ~<n> total tokens
Extractors: <pdf: pdftotext | pymupdf; docx: pandoc; ...>
Fidelity spot-check: <3/3 PASS | details per failure>
Index: <out-dir>/INDEX.md
Notes: <dedupes, oversize chunks, low-fidelity flags, or "none">
```

=== SELF-REVIEW ===

Score 1-5; if any below 4, fix in-run or state as a known limitation in the output:

- Complete: every inventoried file is accounted for as converted, skipped, or failed.
- Robust: extractor fallbacks exercised where needed, venv isolation respected, partial failures contained.
- Clean: chunks well-sized with provenance headers, INDEX.md accurate, no boilerplate residue in spot-checked chunks.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/docs-to-context/LEARNINGS.md`:

```
## <YYYY-MM-DD> — <n> sources (<types>)
- Worked: <one line>
- Awkward: <one line>
- Suggested patch: <one line or "none">
- Verdict: [Smooth | Minor friction | Major friction]
```

=== STRICT RULES ===

1. Never paraphrase or summarize source content; extraction and cleaning are lossless-in-substance, subtractive-only operations.
2. Never pip-install into the system Python; always the dedicated venv in the scratchpad.
3. Never emit a chunk without its provenance comment header.
4. Never skip the fidelity spot-check, even for a single small file.
5. Never let one failing file abort the run; isolate, record, continue.
6. Trust `file --mime-type` over the file extension.
7. INDEX.md must list every skipped and failed file with a reason; silent drops are forbidden.
8. Re-runs regenerate only the per-source folders they touch; never wipe the whole output root.
