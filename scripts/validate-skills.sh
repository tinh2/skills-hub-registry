#!/usr/bin/env bash
#
# validate-skills.sh — Validate all SKILL.md files in the registry.
#
# Checks:
#   1. YAML frontmatter delimiters (---) are present
#   2. Required fields: name, description, version
#   3. No duplicate skill names
#
# Exit codes:
#   0 — all skills valid
#   1 — one or more violations found

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0
TOTAL=0
PASSED=0
FAILED=0

SEEN_NAMES_FILE=$(mktemp)
trap "rm -f '$SEEN_NAMES_FILE' '${SEEN_NAMES_FILE}.counts'" EXIT

# Collect all SKILL.md files, excluding .claude worktrees and scripts
find "$REPO_ROOT" -name "SKILL.md" -not -path "*/.claude/*" -not -path "*/scripts/*" | sort | while IFS= read -r file; do
    TOTAL=$((TOTAL + 1))
    rel_path="${file#"$REPO_ROOT"/}"
    file_errors=0

    # Check opening frontmatter delimiter
    first_line=$(head -n 1 "$file")
    if [[ "$first_line" != "---" ]]; then
        echo "ERROR: $rel_path — missing opening frontmatter delimiter (---)"
        file_errors=$((file_errors + 1))
    fi

    # Check closing frontmatter delimiter (second occurrence of ---)
    delimiter_count=$(grep -c "^---$" "$file" || true)
    if [[ "$delimiter_count" -lt 2 ]]; then
        echo "ERROR: $rel_path — missing closing frontmatter delimiter (---)"
        file_errors=$((file_errors + 1))
    fi

    # Extract frontmatter (between first and second ---)
    frontmatter=""
    if [[ "$first_line" == "---" ]]; then
        frontmatter=$(sed -n '2,/^---$/p' "$file" | sed '$d')
    fi

    # Check required fields
    for field in name description version; do
        if ! grep -q "^${field}:" <<< "$frontmatter"; then
            echo "ERROR: $rel_path — missing required field: $field"
            file_errors=$((file_errors + 1))
        fi
    done

    # Extract name for duplicate check
    if [[ -n "$frontmatter" ]]; then
        skill_name=$(echo "$frontmatter" | grep "^name:" | head -1 | sed 's/^name:[[:space:]]*//')
        if [[ -n "$skill_name" ]]; then
            prev=$(grep "^${skill_name}	" "$SEEN_NAMES_FILE" 2>/dev/null | head -1 | cut -f2 || true)
            if [[ -n "$prev" ]]; then
                echo "ERROR: $rel_path — duplicate skill name '$skill_name' (first seen in $prev)"
                file_errors=$((file_errors + 1))
            else
                printf '%s\t%s\n' "$skill_name" "$rel_path" >> "$SEEN_NAMES_FILE"
            fi
        fi
    fi

    if [[ "$file_errors" -gt 0 ]]; then
        FAILED=$((FAILED + 1))
        ERRORS=$((ERRORS + file_errors))
    else
        PASSED=$((PASSED + 1))
    fi

    # Write counters to temp files since we're in a subshell (pipe)
    echo "$TOTAL $PASSED $FAILED $ERRORS" > "${SEEN_NAMES_FILE}.counts"
done

# Read counters back from subshell
if [[ -f "${SEEN_NAMES_FILE}.counts" ]]; then
    read -r TOTAL PASSED FAILED ERRORS < "${SEEN_NAMES_FILE}.counts"
    rm -f "${SEEN_NAMES_FILE}.counts"
fi

echo ""
echo "=== Validation Summary ==="
echo "Total skills: $TOTAL"
echo "Passed:       $PASSED"
echo "Failed:       $FAILED"
echo "Errors:       $ERRORS"

# ---------------------------------------------------------------------------
# Check 4 — hidden characters (BLOCKING)
#
# Zero-width, bidi-control, and soft-hyphen characters are invisible in a diff
# but are read by any agent that runs the skill. They are the standard vector
# for smuggling instructions past a human reviewer. No skill in this registry
# legitimately needs one.
# ---------------------------------------------------------------------------
echo ""
echo "=== Hidden Character Scan ==="

HIDDEN_OUT=$(find "$REPO_ROOT" -name "SKILL.md" -not -path "*/.claude/*" -not -path "*/scripts/*" -print0 \
    | python3 -c '
import sys, pathlib
BAD = {
    0x200B: "ZERO WIDTH SPACE",        0x200C: "ZERO WIDTH NON-JOINER",
    0x200D: "ZERO WIDTH JOINER",       0x200E: "LEFT-TO-RIGHT MARK",
    0x200F: "RIGHT-TO-LEFT MARK",      0xFEFF: "BYTE ORDER MARK",
    0x202A: "LRE", 0x202B: "RLE", 0x202C: "PDF", 0x202D: "LRO", 0x202E: "RIGHT-TO-LEFT OVERRIDE",
    0x2066: "LRI", 0x2067: "RLI", 0x2068: "FSI", 0x2069: "PDI",
    0x00AD: "SOFT HYPHEN",             0x2060: "WORD JOINER",
}
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
violations = 0
for raw in sys.stdin.read().split("\0"):
    if not raw:
        continue
    p = pathlib.Path(raw)
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"ERROR: {raw} - unreadable: {exc}")
        violations += 1
        continue
    try:
        rel = p.relative_to(root)
    except ValueError:
        rel = p
    for lineno, line in enumerate(text.splitlines(), 1):
        for col, ch in enumerate(line, 1):
            if ord(ch) in BAD:
                print(f"ERROR: {rel}:{lineno}:{col} - hidden character "
                      f"{BAD[ord(ch)]} (U+{ord(ch):04X}). Delete it; skills must "
                      f"contain no invisible characters.")
                violations += 1
print(f"__VIOLATIONS__{violations}")
' "$REPO_ROOT")

HIDDEN_COUNT=$(grep -o '__VIOLATIONS__[0-9]*' <<< "$HIDDEN_OUT" | tail -1 | sed 's/__VIOLATIONS__//')
HIDDEN_COUNT="${HIDDEN_COUNT:-0}"
grep -v '__VIOLATIONS__' <<< "$HIDDEN_OUT" | grep -v '^$' || true

if [[ "$HIDDEN_COUNT" -gt 0 ]]; then
    echo "Hidden characters: $HIDDEN_COUNT violation(s)"
    ERRORS=$((ERRORS + HIDDEN_COUNT))
else
    echo "No hidden characters found."
fi

# ---------------------------------------------------------------------------
# Check 5 — catalog index coverage for NEW skills (ADVISORY)
#
# A new skill must appear in BOTH the root README.md catalog and its
# category README.md. Scoped to skills added relative to the base ref, because
# the existing catalog has known gaps (see CONTRIBUTING.md); a repo-wide
# version would fail on unrelated pre-existing debt.
#
# ADVISORY: warns without failing. Promote to blocking per the CI gate rule
# (5 consecutive green runs on main, zero spurious failures) by moving
# INDEX_WARNINGS into ERRORS below.
# ---------------------------------------------------------------------------
echo ""
echo "=== Catalog Index Coverage (new skills, advisory) ==="

BASE_REF="${BASE_REF:-origin/main}"
INDEX_WARNINGS=0

if ! git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
    echo "SKIP: not a git working tree."
elif ! git -C "$REPO_ROOT" rev-parse --verify --quiet "$BASE_REF" >/dev/null 2>&1; then
    echo "SKIP: base ref '$BASE_REF' not found (set BASE_REF to override)."
else
    MERGE_BASE=$(git -C "$REPO_ROOT" merge-base "$BASE_REF" HEAD 2>/dev/null || echo "$BASE_REF")
    ADDED=$(git -C "$REPO_ROOT" diff --name-only --diff-filter=A "$MERGE_BASE"...HEAD -- '*/SKILL.md' 2>/dev/null || true)

    if [[ -z "$ADDED" ]]; then
        echo "No new skills added relative to $BASE_REF."
    else
        while IFS= read -r skill_path; do
            [[ -z "$skill_path" ]] && continue
            skill_dir=$(dirname "$skill_path")
            category="${skill_dir%%/*}"
            skill_name=$(basename "$skill_dir")

            if ! grep -q "($skill_dir/)" "$REPO_ROOT/README.md" 2>/dev/null; then
                echo "WARN: $skill_dir - not listed in root README.md."
                echo "      Add a row linking ($skill_dir/) to the '$category' table,"
                echo "      and increment the skill count in that section heading."
                INDEX_WARNINGS=$((INDEX_WARNINGS + 1))
            fi

            if [[ ! -f "$REPO_ROOT/$category/README.md" ]]; then
                echo "WARN: $category/README.md does not exist; cannot index $skill_name."
                INDEX_WARNINGS=$((INDEX_WARNINGS + 1))
            elif ! grep -q "($skill_name/)" "$REPO_ROOT/$category/README.md" 2>/dev/null; then
                echo "WARN: $skill_dir - not listed in $category/README.md."
                echo "      Add a row linking ($skill_name/) to that category table."
                INDEX_WARNINGS=$((INDEX_WARNINGS + 1))
            fi
        done <<< "$ADDED"

        if [[ "$INDEX_WARNINGS" -eq 0 ]]; then
            echo "All new skills are listed in both catalog indexes."
        else
            echo "Index coverage: $INDEX_WARNINGS warning(s) (advisory, not failing the build)."
        fi
    fi
fi

echo ""
if [[ "$ERRORS" -gt 0 ]]; then
    echo "FAILED: $ERRORS error(s)."
    exit 1
else
    echo "All skills valid."
    exit 0
fi
