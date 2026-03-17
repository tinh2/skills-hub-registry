#!/usr/bin/env bash
#
# test-validate.sh — Test suite for validate-skills.sh
#
# Creates temporary fixtures and verifies the validator catches
# all expected errors and passes valid files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALIDATOR="$SCRIPT_DIR/validate-skills.sh"
TMPDIR_BASE=$(mktemp -d)
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

cleanup() {
    rm -rf "$TMPDIR_BASE"
}
trap cleanup EXIT

# Helper: create a minimal repo structure with SKILL.md files
setup_fixture() {
    local fixture_dir="$TMPDIR_BASE/$1"
    mkdir -p "$fixture_dir/scripts"
    # Copy validator to fixture so REPO_ROOT resolves correctly
    cp "$VALIDATOR" "$fixture_dir/scripts/validate-skills.sh"
    echo "$fixture_dir"
}

# Helper: create a SKILL.md file in a fixture
create_skill() {
    local fixture_dir="$1"
    local skill_path="$2"
    local content="$3"
    mkdir -p "$(dirname "$fixture_dir/$skill_path")"
    echo "$content" > "$fixture_dir/$skill_path"
}

# Helper: run validator and capture output + exit code
run_validator() {
    local fixture_dir="$1"
    local output
    local exit_code=0
    output=$("$fixture_dir/scripts/validate-skills.sh" 2>&1) || exit_code=$?
    echo "$output"
    return $exit_code
}

# Test assertion helpers
assert_passes() {
    local test_name="$1"
    local fixture_dir="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    local output
    if output=$(run_validator "$fixture_dir" 2>&1); then
        echo "PASS: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "FAIL: $test_name — expected pass but got exit code $?"
        echo "  Output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_fails() {
    local test_name="$1"
    local fixture_dir="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    local output
    if output=$(run_validator "$fixture_dir" 2>&1); then
        echo "FAIL: $test_name — expected failure but validator passed"
        echo "  Output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    else
        echo "PASS: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    fi
}

assert_output_contains() {
    local test_name="$1"
    local fixture_dir="$2"
    local expected="$3"
    TESTS_RUN=$((TESTS_RUN + 1))
    local output
    output=$(run_validator "$fixture_dir" 2>&1) || true
    if echo "$output" | grep -q "$expected"; then
        echo "PASS: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "FAIL: $test_name — output missing: '$expected'"
        echo "  Output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo "=== Running validate-skills.sh tests ==="
echo ""

# --- Test 1: Valid skill passes ---
fixture=$(setup_fixture "valid")
create_skill "$fixture" "build/ship/SKILL.md" "---
name: ship
description: Fast build loop
version: 1
category: build
---
Instructions here."
assert_passes "Valid skill with all required fields" "$fixture"

# --- Test 2: Missing opening delimiter ---
fixture=$(setup_fixture "no-open")
create_skill "$fixture" "build/bad/SKILL.md" "name: bad
description: Missing delimiter
version: 1
---
Instructions."
assert_fails "Missing opening frontmatter delimiter" "$fixture"
assert_output_contains "Reports missing opening delimiter" "$fixture" "missing opening frontmatter delimiter"

# --- Test 3: Missing closing delimiter ---
fixture=$(setup_fixture "no-close")
create_skill "$fixture" "build/bad/SKILL.md" "---
name: bad
description: Missing closing
version: 1
Instructions."
assert_fails "Missing closing frontmatter delimiter" "$fixture"
assert_output_contains "Reports missing closing delimiter" "$fixture" "missing closing frontmatter delimiter"

# --- Test 4: Missing name field ---
fixture=$(setup_fixture "no-name")
create_skill "$fixture" "build/bad/SKILL.md" "---
description: Has no name
version: 1
---
Instructions."
assert_fails "Missing name field" "$fixture"
assert_output_contains "Reports missing name" "$fixture" "missing required field: name"

# --- Test 5: Missing description field ---
fixture=$(setup_fixture "no-desc")
create_skill "$fixture" "build/bad/SKILL.md" "---
name: test
version: 1
---
Instructions."
assert_fails "Missing description field" "$fixture"
assert_output_contains "Reports missing description" "$fixture" "missing required field: description"

# --- Test 6: Missing version field ---
fixture=$(setup_fixture "no-version")
create_skill "$fixture" "build/bad/SKILL.md" "---
name: test
description: Has no version
---
Instructions."
assert_fails "Missing version field" "$fixture"
assert_output_contains "Reports missing version" "$fixture" "missing required field: version"

# --- Test 7: Duplicate skill names ---
fixture=$(setup_fixture "dupes")
create_skill "$fixture" "build/a/SKILL.md" "---
name: duplicate-name
description: First one
version: 1
---
Instructions."
create_skill "$fixture" "build/b/SKILL.md" "---
name: duplicate-name
description: Second one
version: 1
---
Instructions."
assert_fails "Duplicate skill names detected" "$fixture"
assert_output_contains "Reports duplicate name" "$fixture" "duplicate skill name"

# --- Test 8: Multiple valid skills ---
fixture=$(setup_fixture "multi-valid")
create_skill "$fixture" "build/a/SKILL.md" "---
name: skill-a
description: First skill
version: 1
---
A instructions."
create_skill "$fixture" "build/b/SKILL.md" "---
name: skill-b
description: Second skill
version: 2
---
B instructions."
create_skill "$fixture" "qa/c/SKILL.md" "---
name: skill-c
description: Third skill
version: 1
---
C instructions."
assert_passes "Multiple valid skills all pass" "$fixture"

# --- Test 9: Mix of valid and invalid ---
fixture=$(setup_fixture "mixed")
create_skill "$fixture" "build/good/SKILL.md" "---
name: good-skill
description: Valid skill
version: 1
---
Instructions."
create_skill "$fixture" "build/bad/SKILL.md" "---
description: Missing name
version: 1
---
Instructions."
assert_fails "Mixed valid/invalid fails overall" "$fixture"

# --- Test 10: Empty directory (no skills) ---
fixture=$(setup_fixture "empty")
assert_passes "Empty directory with no skills passes" "$fixture"

# --- Summary ---
echo ""
echo "=== Test Summary ==="
echo "Tests run:    $TESTS_RUN"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [[ "$TESTS_FAILED" -gt 0 ]]; then
    exit 1
else
    echo "All tests passed."
    exit 0
fi
