#!/usr/bin/env python3
"""
Enhance all skills in the registry with:
1. Self-healing validation blocks
2. Self-evolving telemetry blocks
3. Subagent spawning for parallelizable skills (combo category)
"""
import os
import re

REGISTRY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Self-healing blocks by category
SELF_HEALING = {
    "analysis": """
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
""",
    "build": """
============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention
""",
    "combo": """
============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes
""",
    "deploy": """
============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available
""",
    "docs": """
============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations
""",
    "integration": """
============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the integration, validate:

1. Run the project's test suite to verify the integration works end-to-end.
2. Run build/compile to confirm no breakage.
3. Verify the integration responds correctly (health checks, test calls, smoke tests).
4. If failures occur, diagnose from error output and apply minimal fixes.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Document the integration state and what's blocking
- Include error output and attempted fixes
""",
    "meta": """
============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify the analysis consumed sufficient data.
2. Verify all output sections have substantive content (not just headers).
3. Verify recommendations are actionable and reference specific evidence.

IF VALIDATION FAILS:
- Identify data gaps and attempt alternative data sources
- Re-generate incomplete sections with expanded analysis
- Repeat up to 2 iterations
""",
    "productivity": """
============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing, validate the output was produced correctly:

1. Verify generated files exist and are syntactically valid.
2. Run any available validation (lint, type-check, dry-run).
3. If the skill produces configuration, verify it parses without errors.

IF VALIDATION FAILS:
- Diagnose from error context and re-generate the failing artifact
- Repeat up to 2 iterations
""",
    "qa": """
============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate your work:

1. Re-run the specific checks that originally found issues.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes
""",
    "review": """
============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the review, validate completeness and consistency:

1. Verify all required output sections are present and non-empty.
2. Verify every finding references a specific file or code location.
3. Verify recommendations are actionable (not vague).
4. Verify severity ratings are justified by evidence.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack specificity
- Re-analyze the deficient areas
- Repeat up to 2 iterations
""",
    "security": """
============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the security analysis, validate thoroughness:

1. Verify every category in the audit was actually checked (not skipped).
2. Verify every finding has a specific file:line location.
3. Verify severity ratings are justified by impact assessment.
4. Verify no false positives by re-reading flagged code in context.

IF VALIDATION FAILS:
- Re-audit skipped categories or vague findings
- Verify or remove false positives
- Repeat up to 2 iterations
""",
    "test": """
============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After generating and running tests, validate:

1. All generated test files compile/parse without syntax errors.
2. Run the generated tests — capture pass/fail results.
3. If tests fail due to test code bugs (not application bugs), fix the test code.
4. Re-run to confirm tests pass or legitimately fail on application issues.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Separate test failures into: test bugs vs application bugs
- Fix test bugs, document application bugs
""",
    "ux": """
============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate:

1. Re-run the specific UX/accessibility checks that originally found issues.
2. Run the project's test suite to verify fixes didn't break functionality.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat up to 3 iterations.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
""",
}

# Universal telemetry block
TELEMETRY = """
============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /{skill_name} — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
"""

# Subagent blocks for combo skills that chain other skills
SUBAGENT_PATTERNS = {
    "polish": """
PARALLEL EXECUTION: Use the Agent tool to run both tracks simultaneously.
- Agent A (UX Specialist): "Run /ux skill instructions on this project. Audit accessibility, design standards, and usability. Fix all issues found. Return a summary of changes made."
- Agent B (Scale Analyst): "Run /scale-audit skill instructions on this project. Analyze scalability concerns. Return findings — do NOT modify code (read-only analysis)."
- Wait for both agents to complete.
- Merge Agent A's code changes (already applied) with Agent B's recommendations.
- Apply any high-priority scalability fixes from Agent B that don't conflict with Agent A's changes.
""",
    "full-test": """
PARALLEL EXECUTION: Use the Agent tool to run both phases concurrently.
- Agent A (E2E Tests): "Run /e2e skill instructions on this project. Auto-detect the stack, generate and run exhaustive integration tests. Apply self-healing for failures. Return: test results, coverage summary, issues found."
- Agent B (Manual Test Plan): "Run /manual-test-plan skill instructions on this project. Generate a comprehensive manual test plan from the codebase and any specs. Return: the complete test plan document."
- Wait for both agents to complete.
- Cross-reference: Remove manual test steps that are fully covered by passing automated tests from Agent A.
- Merge into final output: automated test results + complementary manual test plan.
""",
    "cleanup-sprint": """
PARALLEL EXECUTION: Use the Agent tool to spawn cleanup specialists for independent categories.
- Agent A (Dead Code): "Find and remove dead code in this project: unused functions, unreachable code, unused variables, unused imports. Run tests after each removal to verify safety. Return: files modified, lines removed, test results."
- Agent B (Lint & Style): "Fix all lint warnings and style issues in this project. Run the project's linter/formatter. Organize imports. Return: files modified, issues fixed, categories."
- Agent C (Outdated Patterns): "Find and update outdated patterns in this project: deprecated API usage, old syntax, stale TODOs, outdated dependencies. Return: patterns found, updates applied, files modified."
- Wait for all agents to complete.
- Run the full test suite to verify all changes integrate cleanly.
- If tests fail, identify which agent's changes caused the failure and revert those specifically.
""",
    "research": """
PARALLEL EXECUTION: Use the Agent tool to run competitive analysis and feature discovery concurrently when both are independent.
- Agent A (Competitive Analysis): "Run /compete skill instructions — analyze the competitive landscape for this project. Return competitive gaps and opportunities."
- Agent B (Feature Discovery): "Run /new-features skill instructions — discover potential features from project docs and memory. Return feature candidates with priority."
- Wait for both agents to complete.
- Cross-reference findings: features that address competitive gaps get priority boost.
""",
    "retro": """
PARALLEL EXECUTION: After /recall completes and produces findings, use the Agent tool to run follow-up analyses concurrently.
- Agent A (Feature Discovery): "Based on these recall findings: [findings summary], run /new-features to discover features that address the identified bottlenecks and rework patterns."
- Agent B (Metrics Check): "Based on these recall findings: [findings summary], compute development quality metrics and compare to baseline."
- Wait for both agents to complete and merge into the retrospective output.
""",
    "review-implement": """
PARALLEL EXECUTION: When review findings span both backend and frontend, use the Agent tool to fix them concurrently.
- Agent A (Backend Fixes): "Fix the following backend review findings: [backend findings]. Run backend tests after each fix. Return: files modified, tests pass/fail."
- Agent B (Frontend Fixes): "Fix the following frontend review findings: [frontend findings]. Run frontend tests after each fix. Return: files modified, tests pass/fail."
- Wait for both agents to complete.
- Run the full test suite to verify integration.
""",
    "secure-ship": """
PARALLEL EXECUTION: Use the Agent tool to run security audit and pre-deploy checks concurrently.
- Agent A (Security Audit): "Run comprehensive security analysis on this project — OWASP Top 10, dependency scan, secrets check. Return findings with severity."
- Agent B (Pre-deploy Gate): "Run pre-deploy verification — tests, build, migrations, commit conventions. Return READY or NOT READY with blockers."
- Wait for both agents to complete.
- If security findings are CRITICAL, block deployment regardless of pre-deploy gate.
""",
    "compliance-suite": """
PARALLEL EXECUTION: Use the Agent tool to run compliance checks concurrently.
- Agent A (Security Compliance): "Run security compliance audit — check auth, encryption, access controls, audit logging."
- Agent B (Regulatory Compliance): "Run regulatory compliance check — GDPR, HIPAA, SOC2, PCI-DSS as applicable."
- Agent C (Code Quality): "Run code quality compliance — coding standards, documentation coverage, test coverage thresholds."
- Wait for all agents to complete and merge into unified compliance report.
""",
}


def bump_version(content):
    """Bump version in frontmatter."""
    # Match version in YAML frontmatter
    def bump(m):
        ver = m.group(1).strip('"').strip("'")
        if "." in ver:
            parts = ver.split(".")
            parts[0] = str(int(parts[0]) + 1)
            new_ver = ".".join(parts)
        else:
            new_ver = str(int(ver) + 1)
        return f'version: "{new_ver}"'

    return re.sub(r'version:\s*["\']?([^"\'\n]+)["\']?', bump, content, count=1)


def has_section(content, section_name):
    """Check if a section already exists in the content."""
    return section_name.upper() in content.upper()


def find_output_section(content):
    """Find the position of the OUTPUT section."""
    # Look for ===...OUTPUT...=== or ## Output
    patterns = [
        r'\n={3,}\n\s*OUTPUT\s*\n={3,}',
        r'\n## Output\b',
        r'\nOUTPUT\n={3,}',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            return m.start()

    # Look for NEXT STEPS section as fallback
    patterns_next = [
        r'\n={3,}\n\s*NEXT STEPS\s*\n={3,}',
        r'\n## Next Steps\b',
    ]
    for pat in patterns_next:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            return m.start()

    return None


def find_end_position(content):
    """Find the end of the instructions (before DO NOT section or end of file)."""
    # Look for DO NOT section
    patterns = [
        r'\n={3,}\n\s*DO NOT\s*\n={3,}',
        r'\n## DO NOT\b',
        r'\nSTRICT RULES:?\s*\n',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            return m.start()

    return len(content)


def get_category(filepath):
    """Extract category from file path."""
    # Path is like: registry_root/category/skill-name/SKILL.md
    parts = filepath.split(os.sep)
    for i, part in enumerate(parts):
        if part in SELF_HEALING:
            return part
    return None


def get_skill_name(filepath):
    """Extract skill name from file path."""
    parts = filepath.split(os.sep)
    return parts[-2]  # parent directory name


def process_skill(filepath):
    """Process a single skill file."""
    with open(filepath, "r") as f:
        content = f.read()

    original = content
    category = get_category(filepath)
    skill_name = get_skill_name(filepath)

    if not category:
        print(f"  SKIP (no category): {filepath}")
        return False

    # Bump version
    content = bump_version(content)

    # Determine if we're in frontmatter-instructions format or body format
    has_frontmatter = content.startswith("---")

    # Check if self-healing already exists
    has_healing = has_section(content, "SELF-HEALING")

    # Find insertion points
    output_pos = find_output_section(content)
    end_pos = find_end_position(content)

    # Add self-healing before OUTPUT (if not already present)
    if not has_healing and category in SELF_HEALING:
        healing_block = "\n" + SELF_HEALING[category].rstrip() + "\n"
        if output_pos:
            content = content[:output_pos] + healing_block + content[output_pos:]
            # Recalculate end_pos since we inserted content
            end_pos = find_end_position(content)
        else:
            # No OUTPUT section found, insert before end
            content = content[:end_pos] + healing_block + content[end_pos:]
            end_pos = find_end_position(content)

    # Add telemetry at the end (before DO NOT section if it exists)
    if not has_section(content, "SELF-EVOLUTION TELEMETRY"):
        telemetry = TELEMETRY.replace("{skill_name}", skill_name)
        telemetry_block = "\n" + telemetry.rstrip() + "\n"
        end_pos = find_end_position(content)
        content = content[:end_pos] + telemetry_block + content[end_pos:]

    # Add subagent patterns for combo skills
    if skill_name in SUBAGENT_PATTERNS and not has_section(content, "PARALLEL EXECUTION"):
        subagent_block = "\n" + SUBAGENT_PATTERNS[skill_name].rstrip() + "\n"
        # Insert after PHASE 1 header for most combo skills
        phase1_match = re.search(
            r'(PHASE 1[^\n]*\n={3,}\n)', content, re.IGNORECASE
        )
        if phase1_match:
            insert_pos = phase1_match.end()
            content = content[:insert_pos] + "\n" + subagent_block + "\n" + content[insert_pos:]
        else:
            # Insert near the top of instructions, after the first paragraph
            # Find end of first paragraph after frontmatter
            if has_frontmatter:
                fm_end = content.find("---", 3)
                if fm_end > 0:
                    first_blank = content.find("\n\n", fm_end + 3)
                    if first_blank > 0:
                        insert_pos = first_blank
                        content = (
                            content[:insert_pos]
                            + "\n"
                            + subagent_block
                            + content[insert_pos:]
                        )

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        return True
    return False


def main():
    skills_modified = 0
    skills_skipped = 0
    skills_total = 0

    for root, dirs, files in os.walk(REGISTRY_ROOT):
        # Skip scripts and hidden directories
        if "scripts" in root or "/." in root:
            continue
        for f in files:
            if f == "SKILL.md":
                filepath = os.path.join(root, f)
                skills_total += 1
                try:
                    if process_skill(filepath):
                        skills_modified += 1
                    else:
                        skills_skipped += 1
                except Exception as e:
                    print(f"  ERROR: {filepath}: {e}")
                    skills_skipped += 1

    print(f"\nDone: {skills_modified} modified, {skills_skipped} skipped, {skills_total} total")


if __name__ == "__main__":
    main()
