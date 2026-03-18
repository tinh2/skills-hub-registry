---
name: resume-optimizer
description: Audit a resume builder or optimization tool for ATS compatibility, keyword matching accuracy, formatting standards, achievement quantification, skill extraction, and job-description alignment scoring. Use when reviewing resume software, career platforms, applicant tracking integrations, CV generators, or job application tools.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous resume optimization analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate ATS compatibility, keyword matching, formatting
standards, achievement quantification, skill extraction, and job alignment scoring,
then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "ATS parsing"
or "keyword matching"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (web app, browser extension, API
service, desktop), backend framework, database engine, NLP/ML libraries, PDF
generation library, document parsing engine (PDF, DOCX, plain text), ATS
integration or simulation, job board API integrations, template engine.

Step 1.2 -- Resume Data Model

Read core data structures: resume sections (contact, summary/objective, experience,
education, skills, certifications, projects, publications, volunteer, languages),
experience entries (company, title, dates, achievements/bullets, skills used),
education entries (institution, degree, field, dates, GPA, honors), skills
(categorized, proficiency levels, years of experience), job descriptions (title,
company, requirements, preferred qualifications, responsibilities).

Step 1.3 -- Document Processing Pipeline

Map the resume processing flow: document upload and format detection, text extraction
(OCR for images, PDF parsing, DOCX parsing), section identification and segmentation,
entity extraction (names, dates, companies, titles, skills), data normalization and
storage, template application and rendering, export formats supported (PDF, DOCX,
plain text, HTML).

============================================================
PHASE 2: ATS COMPATIBILITY
============================================================

Step 2.1 -- Format Compliance

Evaluate: ATS-friendly formatting rules enforcement (single-column layout, standard
section headers, no tables or text boxes, no headers/footers for critical content,
standard fonts, no images or graphics in content area), file format output options
(ATS-optimized PDF, DOCX, plain text), encoding handling (UTF-8, special characters),
file size constraints.

Step 2.2 -- Parsing Accuracy

Evaluate: whether the system tests its output against known ATS parsers, section
header recognition by ATS (does the system use standard headers like "Experience"
vs. creative headers like "My Journey"), date format standardization (MM/YYYY
consistently), bullet point character handling (standard bullets vs. special
characters that ATS may misinterpret), contact information extraction accuracy
(phone, email, location, LinkedIn).

Step 2.3 -- ATS Simulation

Evaluate: whether the system can simulate ATS parsing of the generated resume,
parse result preview (what the ATS sees vs. what humans see), parse error detection
and correction suggestions, ATS compatibility score, comparison across major ATS
platforms (Taleo, Workday, Greenhouse, Lever, iCIMS, BambooHR), formatting fallback
recommendations when ATS compatibility conflicts with visual design.

============================================================
PHASE 3: KEYWORD MATCHING ALGORITHMS
============================================================

Step 3.1 -- Keyword Extraction from Job Descriptions

Evaluate: extraction method (regex, NLP entity recognition, TF-IDF, LLM-based),
keyword categorization (hard skills, soft skills, certifications, tools, industry
terms), required vs. preferred keyword distinction, keyword frequency weighting,
contextual extraction (understanding "3+ years of Python" as both a skill and
experience requirement), multi-word keyword handling ("machine learning" as one
keyword, not two).

Step 3.2 -- Resume-to-Job Matching

Evaluate: matching methodology (exact match, semantic similarity, synonym expansion),
match scoring algorithm (binary present/absent, weighted by importance, frequency-
based), skill synonym database quality ("JavaScript" = "JS" = "ECMAScript"),
experience level matching (entry-level resume against senior job -- mismatch
detection), industry context awareness (same skill name different meaning across
industries), negative keyword handling (skills or terms to avoid).

Step 3.3 -- Gap Analysis and Recommendations

Evaluate: missing keyword identification from job description, keyword placement
recommendations (which section to add missing keywords), keyword stuffing detection
and prevention, natural language integration suggestions (not just listing keywords),
priority ordering of missing keywords (required vs. nice-to-have), transferable
skill suggestions (related skills the candidate has that partially match).

============================================================
PHASE 4: FORMATTING AND DESIGN
============================================================

Step 4.1 -- Template Quality

Evaluate: template variety (number, industry-specific, experience-level appropriate),
template responsiveness (content adapts to resume length -- 1-page, 2-page),
typography quality (readable fonts, appropriate sizes, consistent hierarchy),
whitespace and margin handling, print-friendliness, color usage (accessible
contrast, professional appearance), section ordering flexibility.

Step 4.2 -- Content Formatting

Evaluate: bullet point formatting consistency, date alignment, heading hierarchy,
skill section display options (list, grid, proficiency bars, tags), experience
entry layout, education entry layout, multi-column support (when ATS-safe),
page break handling (no orphaned headers, no split entries across pages).

Step 4.3 -- Length Optimization

Evaluate: resume length guidance (1-page for early career, 2-page for experienced),
content prioritization when space is limited, section reordering based on relevance,
achievement condensation suggestions, redundancy detection (same skill listed in
multiple places), content density scoring (too sparse vs. too cramped).

============================================================
PHASE 5: ACHIEVEMENT QUANTIFICATION
============================================================

Step 5.1 -- Achievement Detection

Evaluate: whether the system identifies vague bullet points ("Responsible for managing
team" vs. "Led 12-person team that delivered $2M project 3 weeks ahead of schedule"),
action verb detection and suggestion, quantification prompts (revenue, percentages,
team size, time saved, cost reduced), result-oriented language encouragement
(STAR/CAR framework support).

Step 5.2 -- Quantification Assistance

Evaluate: guided quantification workflows (prompts to add numbers to vague bullets),
industry-specific quantification templates, achievement example libraries by role
and industry, before/after bullet comparison, metric suggestion based on job function
(sales: revenue and quota; engineering: system uptime and latency; marketing:
conversion and engagement).

Step 5.3 -- Impact Scoring

Evaluate: bullet impact scoring methodology (weak, moderate, strong), per-bullet
improvement suggestions, overall resume impact score, achievement relevance to
target job, achievement recency weighting (recent achievements weighted more
heavily), leadership and scope indicators.

============================================================
PHASE 6: SKILL EXTRACTION ACCURACY
============================================================

Step 6.1 -- Extraction from Resume Text

Evaluate: skill identification from unstructured text (experience bullets, project
descriptions), extraction accuracy (precision and recall), false positive handling
(mentioning a technology is not the same as proficiency), skill contextualization
(used vs. managed vs. designed with a technology), extraction from non-standard
formats (creative resumes, portfolios).

Step 6.2 -- Skill Normalization

Evaluate: skill synonym resolution, skill hierarchy mapping (React is a JavaScript
framework), skill categorization (programming languages, frameworks, databases,
soft skills, methodologies), skill currency detection (outdated technologies
flagged), proficiency level inference from context ("expert in" vs. "familiar
with" vs. "exposure to").

Step 6.3 -- Skill Gap Visualization

Evaluate: visual comparison of candidate skills vs. job requirements, coverage
percentage by skill category, gap severity weighting (missing required skill vs.
missing preferred skill), skill transferability suggestions, competitive positioning
(how this skill profile compares to typical applicants).

============================================================
PHASE 7: JOB-DESCRIPTION ALIGNMENT SCORING
============================================================

Step 7.1 -- Overall Alignment Score

Evaluate: scoring methodology (weighted keyword match, semantic similarity, experience
level alignment, education match), score components and transparency (can users see
what drives the score), score calibration (does a high score correlate with interview
callbacks), industry-specific scoring adjustments, multi-job comparison (score resume
against multiple jobs simultaneously).

Step 7.2 -- Per-Section Alignment

Evaluate: section-level scoring (how well does each resume section align with the
job), section improvement recommendations prioritized by impact, content reordering
suggestions based on job alignment, tailored summary/objective generation for
specific jobs, experience bullet reordering (most relevant first).

Step 7.3 -- Iterative Optimization

Evaluate: optimization workflow (score, adjust, re-score cycle), score improvement
tracking per revision, diminishing returns detection (further changes won't
significantly improve score), over-optimization warning (resume sounds artificial),
version management (save tailored versions per job application).

Write analysis to `docs/resume-optimizer-analysis.md` (create `docs/` if needed).


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Resume Optimizer Analysis Complete

- Report: `docs/resume-optimizer-analysis.md`
- ATS compatibility factors evaluated: [count]
- Keyword matching methods assessed: [count]
- Formatting standards reviewed: [count]
- Achievement quantification features: [count]
- Skill extraction capabilities analyzed: [count]
- Alignment scoring components reviewed: [count]

**Critical findings:**
1. [finding] -- [job seeker outcome impact]
2. [finding] -- [ATS compatibility concern]
3. [finding] -- [keyword matching accuracy gap]

**Top recommendations:**
1. [recommendation] -- [expected improvement in ATS pass-through rate]
2. [recommendation] -- [expected improvement in job alignment scoring]
3. [recommendation] -- [expected improvement in user experience]

NEXT STEPS:
- "Run `/skill-gap` to analyze the skill taxonomy that feeds resume skill extraction."
- "Run `/employer-matching` to evaluate how resume optimization affects matching outcomes."
- "Run `/security-review` to audit access controls on stored resume and personal data."

DO NOT:
- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real resume content, names, contact information, or employer data in output.
- Do NOT optimize solely for ATS at the expense of human readability -- resumes must pass both.
- Do NOT encourage keyword stuffing -- ATS sophistication is increasing and stuffing triggers rejection.
- Do NOT ignore industry context -- a software engineer resume and a marketing resume have fundamentally different optimization criteria.
- Do NOT treat all ATS platforms as identical -- parsing behavior varies significantly across systems.
- Do NOT conflate resume quality with candidate quality -- the tool should surface what the candidate has done, not fabricate accomplishments.
- Do NOT overlook accessibility -- resume formats should be screen-reader compatible.
- Do NOT assume one resume fits all jobs -- effective optimization requires job-specific tailoring.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /resume-optimizer — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
