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
trap "rm -f $SEEN_NAMES_FILE" EXIT

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
        if ! echo "$frontmatter" | grep -q "^${field}:"; then
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
    read TOTAL PASSED FAILED ERRORS < "${SEEN_NAMES_FILE}.counts"
    rm -f "${SEEN_NAMES_FILE}.counts"
fi

echo ""
echo "=== Validation Summary ==="
echo "Total skills: $TOTAL"
echo "Passed:       $PASSED"
echo "Failed:       $FAILED"
echo "Errors:       $ERRORS"

if [[ "$ERRORS" -gt 0 ]]; then
    exit 1
else
    echo "All skills valid."
    exit 0
fi
