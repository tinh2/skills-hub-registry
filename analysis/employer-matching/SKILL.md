---
name: employer-matching
description: "Audit a job matching platform for relevance, fairness, and candidate experience. Triggers: building or reviewing job boards, ATS matching engines, internal mobility platforms, or workforce marketplaces."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous employer matching analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate matching algorithms, skill alignment, culture
fit modeling, bias detection, geographic handling, salary accuracy, and candidate
experience, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "matching algorithm",
"bias detection", "salary accuracy"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Scan package manifests and config. Identify:
- Platform type: job board, staffing platform, ATS integration, workforce marketplace, internal mobility.
- Backend framework and database engine.
- Search engine: Elasticsearch, Algolia, Solr.
- ML/NLP libraries.
- Recommendation engine.
- Geospatial libraries.
- Salary data providers.
- Communication tools: messaging, email, scheduling.
- Analytics and reporting.

Step 1.2 -- Matching Data Model

Read core data structures:
- Candidate profiles: skills, experience, education, certifications, preferences (location, salary, remote/hybrid/onsite, industry, company size, role type).
- Job postings: title, description, requirements (required vs. preferred), skills, experience level, education, location, salary range, benefits, company culture attributes.
- Employer profiles: industry, size, culture values, benefits, growth stage, tech stack.
- Match records: candidate, job, match score, match components, status, interaction history.

Step 1.3 -- Data Pipeline

Map the end-to-end matching flow:
- Candidate profile creation and enrichment.
- Job posting ingestion: direct entry, ATS import, job board scraping.
- Data normalization: skill standardization, title normalization, location geocoding.
- Matching engine invocation: batch vs. real-time.
- Result ranking and presentation.
- Feedback loop: accept/reject signals back to model.

============================================================
PHASE 2: MATCHING ALGORITHM QUALITY
============================================================

Step 2.1 -- Algorithm Architecture

Evaluate matching approach:
- Method: rule-based filters, weighted scoring, collaborative filtering, content-based filtering, hybrid.
- Feature engineering: what signals feed the match.
- Weighting methodology: fixed weights, learned weights, user-adjustable.
- Threshold configuration: minimum score to show match.
- Scoring transparency: can users understand why they were matched.
- Algorithm versioning and A/B testing.

Step 2.2 -- Match Precision and Recall

Evaluate match quality:
- Precision: are shown matches relevant.
- Recall: are good matches being missed.
- Ranking quality: best matches ranked highest.
- Match volume per candidate: too few is frustrating, too many is overwhelming.
- Match freshness: how quickly new postings appear, how quickly closed postings are removed.
- Duplicate match handling.
- Reciprocal matching: does the candidate also match the job requirements.

Step 2.3 -- Match Signal Processing

Evaluate edge case handling:
- Hard requirement filtering: must-have vs. nice-to-have.
- Deal-breaker handling: candidate excludes certain industries, employer requires specific certification.
- Partial match handling: meets 7 of 10 requirements.
- Overqualification detection: senior candidate matched to junior role.
- Underqualification detection with growth potential scoring.
- Experience equivalency: years of experience vs. demonstrated competency.

============================================================
PHASE 3: SKILL-TO-REQUIREMENT ALIGNMENT
============================================================

Step 3.1 -- Skill Normalization

Evaluate taxonomy quality:
- Skill taxonomy used: proprietary, O*NET, LinkedIn Skills, custom.
- Synonym resolution: "JavaScript" = "JS" = "ECMAScript".
- Skill hierarchy: knows React implies knows JavaScript.
- Skill versioning: Python 2 vs. Python 3.
- Skill ambiguity resolution: context-dependent skill meanings.
- Skill inference from work history.

Step 3.2 -- Requirement Parsing

Evaluate NLP extraction quality:
- NLP extraction from job descriptions: required skills, preferred skills, experience level, education.
- Requirement classification: must-have, nice-to-have, bonus.
- Requirement contradiction detection: entry-level role requiring 5 years experience.
- Implicit requirement identification.
- Requirement weighting by mention position and frequency.

Step 3.3 -- Alignment Scoring

Evaluate scoring methodology:
- Skill match scoring: exact match, partial match, related skill, no match.
- Experience level alignment: years and seniority.
- Education alignment: degree level, field relevance.
- Certification and tool/technology match.
- Soft skill assessment: how are inherently subjective skills matched.
- Overall alignment score composition and transparency.

============================================================
PHASE 4: CULTURE FIT MODELING
============================================================

Step 4.1 -- Culture Data Collection

Evaluate data collection quality:
- How employer culture is captured: questionnaire, free text, predefined values, employee reviews.
- Culture dimensions modeled: work-life balance, innovation vs. stability, collaboration vs. autonomy, hierarchy vs. flat, mission-driven vs. profit-driven.
- Culture data validation: is self-reported culture accurate.
- Culture attribute standardization across employers.

Step 4.2 -- Culture Matching

Evaluate matching methodology:
- How candidate culture preferences are captured.
- Matching methodology: dimensional scoring, overall compatibility.
- Culture match weight in overall match score.
- Culture match transparency: can candidates see why they were matched on culture.
- Culture vs. skills trade-off: high culture fit but lower skill match.

Step 4.3 -- Culture Fit Risks

Culture fit is the most common vector for bias in hiring technology. Evaluate:
- Whether culture fit is defined in a way that excludes diverse candidates.
- Whether "culture fit" proxies for demographic homogeneity.
- Whether "culture add" is valued alongside "culture fit".
- Whether culture matching is optional and transparent to candidates.

============================================================
PHASE 5: BIAS DETECTION IN MATCHING
============================================================

Step 5.1 -- Algorithmic Bias Audit

Evaluate bias testing:
- Whether the algorithm has been tested for disparate impact by protected class (race, gender, age, disability, veteran status).
- Bias testing methodology: adverse impact ratio, 4/5ths rule, statistical parity.
- Bias in training data: historical hiring data encodes historical biases.
- Feature audit: are proxy variables for protected classes used (zip code, school name, graduation year).
- Regular bias re-assessment schedule.

Step 5.2 -- Bias Mitigation

Evaluate mitigation techniques:
- Blind matching: name/photo removed.
- Debiased embeddings.
- Fairness constraints in optimization.
- Calibrated scoring across demographic groups.
- Diversity-aware matching without violating discrimination law.
- Inclusion of non-traditional candidates: career changers, employment gaps, non-degree holders.

Step 5.3 -- Bias Monitoring

Evaluate ongoing monitoring:
- Bias monitoring dashboards.
- Outcome tracking by demographic group: match rates, interview rates, hire rates.
- Candidate feedback on match relevance by group.
- Third-party bias audit facilitation.
- Regulatory compliance: EEOC, NYC Local Law 144 for automated employment decision tools, EU AI Act high-risk classification.

============================================================
PHASE 6: GEOGRAPHIC AND REMOTE HANDLING
============================================================

Step 6.1 -- Location Matching

Evaluate geographic matching quality:
- Geocoding accuracy for candidate and job locations.
- Commute time/distance calculation: actual travel time, not just radius.
- Public transit vs. driving considerations.
- Relocation willingness handling.
- Multi-location job support: remote with quarterly on-site.
- International location and time zone handling.
- Cost-of-living adjustment awareness.

Step 6.2 -- Remote Work Classification

Evaluate remote work model:
- Remote category granularity: fully remote, hybrid with specific days, remote with travel, temporarily remote.
- Remote policy accuracy: verified vs. self-reported.
- Time zone compatibility matching for remote roles.
- Remote work equipment and infrastructure requirements.
- State/country work authorization for remote: tax and legal implications.
- Remote-first company identification.

Step 6.3 -- Geographic Preferences

Evaluate preference handling:
- Candidate location preference flexibility: willing to relocate for the right role.
- Employer geographic requirement flexibility.
- Geographic expansion recommendations: wider search yields better matches.
- Location-based salary adjustment: same role, different compensation by location.
- Geographic diversity in match results: not over-indexing on local candidates for remote roles.

============================================================
PHASE 7: SALARY RANGE ACCURACY
============================================================

Step 7.1 -- Salary Data Sources

Evaluate data quality:
- Salary data origin: employer-provided, market data integration (BLS, Glassdoor, Levels.fyi, Payscale, proprietary surveys).
- Salary data freshness and update frequency.
- Geographic adjustment methodology.
- Industry and company size adjustments.
- Role level calibration: what "senior" means varies by company.

Step 7.2 -- Salary Matching

Evaluate matching accuracy:
- Candidate salary expectation handling: range vs. single number, base vs. total compensation.
- Employer budget range accuracy: does posted range match actual offers.
- Salary match tolerance: how far apart can expectations and budget be.
- Total compensation modeling: base, bonus, equity, benefits valuation.
- Salary negotiation range estimation.

Step 7.3 -- Salary Transparency

Evaluate compliance and fairness:
- Pay transparency compliance: state and local laws requiring salary ranges.
- Salary range display to candidates.
- Salary comparison tools: how does this range compare to market.
- Salary equity analysis: same role, different pay (pay gap detection).
- Salary progression estimation: where does this role lead financially.

============================================================
PHASE 8: CANDIDATE EXPERIENCE
============================================================

Step 8.1 -- Match Presentation

Evaluate the candidate-facing experience:
- Match result display: score visibility, match reason explanation, job detail summary, company information.
- Result sorting and filtering options.
- Saved searches and alerts.
- Match notification channels: email, push, in-app.
- Match volume management: not overwhelming candidates.
- Expired or filled job handling.

Step 8.2 -- Application Workflow

Evaluate application flow:
- One-click apply functionality.
- Application tracking dashboard.
- Application status visibility.
- Employer response rate and time tracking.
- Application withdrawal capability.
- Resume tailoring and cover letter generation support.
- Interview scheduling integration.

Step 8.3 -- Feedback Loop

A matching algorithm that cannot learn from outcomes will not improve. Evaluate:
- Match relevance feedback mechanism: thumbs up/down, not interested reasons.
- Feedback incorporation into future matching.
- Candidate satisfaction measurement.
- Match-to-hire conversion tracking.
- Time-to-hire measurement.
- Candidate drop-off analysis: where in the process do candidates abandon.

Write analysis to `docs/employer-matching-analysis.md` (create `docs/` if needed).


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

## Employer Matching Analysis Complete

- Report: `docs/employer-matching-analysis.md`
- Matching algorithm components evaluated: [count]
- Skill alignment methods assessed: [count]
- Culture fit factors reviewed: [count]
- Bias detection mechanisms analyzed: [count]
- Geographic/remote handling features: [count]
- Salary accuracy factors assessed: [count]
- Candidate experience elements reviewed: [count]

**Critical findings:**
1. [finding] -- [matching outcome impact]
2. [finding] -- [bias and equity concern]
3. [finding] -- [candidate experience gap]

**Top recommendations:**
1. [recommendation] -- [expected improvement in match relevance]
2. [recommendation] -- [expected improvement in equity and fairness]
3. [recommendation] -- [expected improvement in candidate satisfaction]

NEXT STEPS:
- "Run `/skill-gap` to analyze the skill taxonomy feeding the matching engine."
- "Run `/resume-optimizer` to evaluate candidate profile quality and its effect on matching."
- "Run `/training-path` to assess whether training completers are properly represented in matching."

DO NOT:
- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real candidate names, resumes, employer hiring data, or salary specifics in output.
- Do NOT evaluate matching without bias analysis -- automated matching systems can amplify historical discrimination.
- Do NOT treat culture fit as an unqualified positive -- it is the most common vector for bias in hiring technology.
- Do NOT ignore reciprocal matching -- a great match for the candidate must also be a great match for the employer.
- Do NOT assume salary data is current -- compensation markets shift rapidly and stale data misleads candidates and employers.
- Do NOT overlook the feedback loop -- a matching algorithm that cannot learn from outcomes will not improve over time.
- Do NOT treat all job seekers as identical -- career changers, re-entry workers, and new graduates need different matching approaches.
- Do NOT assess matching accuracy without outcome data -- high match scores are meaningless if they do not predict successful hires.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /employer-matching — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
