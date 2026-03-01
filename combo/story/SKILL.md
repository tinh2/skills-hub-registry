---
name: story
description: Full story lifecycle — chains /arch-review then /story-implementer then /pr. Takes a story from design review through implementation to PR creation.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous story implementation agent. Do NOT ask the user questions.

This skill chains three skills in sequence:
1. `/arch-review` — review the story's design and flag gaps
2. `/story-implementer` — implement the story with tests
3. `/pr` — create a convention-compliant pull request

INPUT: $ARGUMENTS
The Jira story (text, image, or URL), or a description of what to build.

============================================================
PHASE 1: ARCHITECTURE REVIEW
============================================================

Follow the instructions defined in the `/arch-review` skill in Design Review mode.

Pass the input story to the arch-review skill. It will:
- Analyze the story's scope and design
- Check for missing acceptance criteria
- Validate the proposed approach against codebase conventions
- Flag any design gaps or concerns

If the review finds CRITICAL gaps:
- Attempt to resolve them autonomously (adjust the approach, add missing criteria).
- If unresolvable, document them and proceed — the implementation will address them.

Record the review verdict and any adjustments for the implementation phase.

============================================================
PHASE 2: IMPLEMENT
============================================================

Follow the instructions defined in the `/story-implementer` skill.

Pass the original story PLUS any adjustments from the architecture review.

The story-implementer skill will:
- Implement the story following repository conventions
- Write unit tests with full coverage
- Follow the Resource → Service → Repository pattern
- Commit with conventional commit format
- Push after committing

============================================================
PHASE 3: CREATE PR
============================================================

Follow the instructions defined in the `/pr` skill.

The pr skill will:
- Extract the story number from the branch name
- Generate a summary from the commits and changes
- Create a PR with test plan and Jira link
- Enforce all CLAUDE.md conventions (no AI attribution, etc.)

============================================================
OUTPUT
============================================================

## Story Complete

### Architecture Review
- **Verdict:** {approved / approved with adjustments}
- **Adjustments:** {list any changes made to the approach, or "none"}

### Implementation
- **Files changed:** {count}
- **Tests written:** {count}
- **Commits:** {count}

### Pull Request
- **PR:** {URL}
- **Story:** {story number}
- **Title:** {PR title}

NEXT STEPS:
- "Review the PR and merge when ready."
- "Run `/preflight` for pre-deploy verification."
- "Run `/qa` for full QA verification before merging."
