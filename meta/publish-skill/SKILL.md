---
name: publish-skill
description: "Publish a locally installed skill to the skills-hub registry and sync it to the production platform. Use when: 'publish skill X', 'push skill to hub', 'add skill to registry', 'publish to skills hub', 'share this skill', 'make skill available globally'. Runs entirely from the Mac Studio — no VPS needed."
version: "1.3.0"
category: meta
---

You are an autonomous skill publisher. Your job is to take a locally installed skill,
add it to the skills-hub-registry GitHub repo, and sync it to the production platform.

Do NOT ask the user questions. Proceed through all phases automatically.

SKILL TO PUBLISH:
$ARGUMENTS

---

=== PRE-FLIGHT ===

Before starting, verify:

- [ ] `$ARGUMENTS` is provided — this is the skill slug (e.g., "skillify", "my-skill")
- [ ] The skill exists locally at `~/.claude/skills/$ARGUMENTS/SKILL.md`
- [ ] `~/git/skills-hub-registry/` exists and is a git repo
- [ ] `~/git/skills-hub/` exists
- [ ] `~/.claude/state/skills-hub-publish.env` exists and is readable (local-only config;
      it holds the AWS profile, DB coordinates, and registry paths). Source it:
      `set -a; . ~/.claude/state/skills-hub-publish.env; set +a`
- [ ] AWS credentials resolve:
      `AWS_PROFILE=$SKILLS_HUB_AWS_PROFILE AWS_DEFAULT_REGION=$SKILLS_HUB_AWS_REGION aws sts get-caller-identity`

If `$ARGUMENTS` is empty: stop and tell the user "Usage: /publish-skill <skill-slug>"
If the skill file doesn't exist: list `~/.claude/skills/` to show available skills, then stop.
If the config file is missing: tell the user to create it from `references/publish-env.example`.
If AWS creds fail: tell the user to run `aws sso login --profile $SKILLS_HUB_AWS_PROFILE` first.

VALIDATION: All checks must pass before proceeding.
FALLBACK: Report exactly which check failed and what to do to fix it.

=== CROSS-REFERENCE VALIDATION ===
-- Added by /evolve 2026-04-19: skills shipped with broken /slug references hurt users --

After confirming the skill file exists, scan its instructions for cross-references:

1. Extract all `/skill-name` patterns from the SKILL.md:

   ```bash
   grep -oE '/[a-z][a-z0-9-]+' ~/.claude/skills/$ARGUMENTS/SKILL.md | sort -u
   ```

2. For each found reference (e.g., `/ship-pipeline`, `/unit-test`), check if it exists locally:

   ```bash
   ls ~/.claude/skills/<slug>/ 2>/dev/null
   ```

3. Report findings:
   - **Resolved**: skill exists locally — OK to publish
   - **Missing locally**: skill not in `~/.claude/skills/` — warn with: "WARNING: /{slug} referenced in instructions but not installed locally. Verify it exists in the skills-hub registry before publishing."

Do NOT block the publish for missing references — warn only. The referenced skill may exist on the platform even if not installed locally. But missing references are flagged so the user can decide.

VALIDATION: All checks must pass before proceeding.
FALLBACK: Report exactly which check failed and what to do to fix it.

=== TEST PAIRING GATE ===
-- Added by /evolve 2026-07-01: M8=0.00 for 5 consecutive runs in skills-hub-registry;
4 test scripts sat uncommitted across all 5 runs because publish had no test check --

After cross-reference validation, run this check:

1. Check for uncommitted test files in the registry:

   ```bash
   git -C ~/git/skills-hub-registry status --porcelain | grep "^?? scripts/test_"
   ```

   If any untracked test files are found, emit:
   "⚠️ M8 WARNING: Uncommitted test files detected. Commit them NOW before publishing to prevent M8 staying at 0:
   git add scripts/test_<name>.py && git commit -m 'test: add tests for $ARGUMENTS'"

2. Check if the last 10 commits on main include a `test:` commit for this skill:
   ```bash
   git -C ~/git/skills-hub-registry log --oneline -10 | grep "^.\{8\} test:"
   ```
   If none found, emit:
   "⚠️ M8 WARNING: No paired test: commit found. M8 (Test Coverage Ratio) will remain 0.00
   unless this publish is accompanied by a test commit. Consider:
   git add scripts/test_$ARGUMENTS.py && git commit -m 'test: add smoke tests for $ARGUMENTS skill'"

Do NOT block the publish — warn only. M8 is advisory until a CI gate is wired.


=== SECRET AND PII GATE (BLOCKING) ===
-- Added 2026-07-30 after publish-skill itself was found to have published a production
   RDS endpoint and admin username to a PUBLIC repo for 3.5 months --

The registry is PUBLIC. Anything copied there is world-readable forever, including in git
history after a later fix. Before Phase 2 copies any file, scan every file about to be
published:

```bash
grep -rnE "AWS_PROFILE=[a-z]|[0-9]{12}|\.rds\.amazonaws\.com|\.cache\.amazonaws\.com|[A-Za-z0-9+/]{40}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|/Users/[a-z]+|/home/[a-z]+|[a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,}|apps\.googleusercontent\.com|xox[baprs]-|gh[pousr]_[A-Za-z0-9]{20,}" \
  ~/.claude/skills/$ARGUMENTS/
```

Any hit BLOCKS the publish. Do not sanitize silently and continue — show the user each hit
and the proposed replacement, because deciding what is sensitive is their call.

Replace, never redact-in-place:
- Credentials and hostnames -> a variable sourced from `~/.claude/state/*.env` (local-only)
- Absolute home paths -> `~/` or `$HOME`
- Personal emails, account IDs, org slugs -> a placeholder

A skill that needs environment-specific values must read them from a local config file at
run time. The published skill carries the variable names and an `.example` file; the real
values never leave the machine. This is the "always have a public version" rule: local and
published are the SAME file, and it is safe because it holds no literals.

Note: public AWS service endpoints (e.g. `bedrock-runtime.<region>.amazonaws.com`) are not
secrets. Judge by whether the string identifies YOUR account or infrastructure.

---

=== PHASE 1: DETERMINE REGISTRY CATEGORY ===

Read `~/.claude/skills/$ARGUMENTS/SKILL.md` and extract the `category` from frontmatter.

Map the category to the registry directory:

| Skill category | Registry path |
| -------------- | ------------- |
| meta           | meta/         |
| build          | build/        |
| deploy         | deploy/       |
| analyze        | review/       |
| generate       | spec/         |
| test           | qa/           |
| ops            | deploy/       |
| content        | spec/         |
| security       | security/     |
| ux             | ux/           |
| education      | education/    |

If no match, use `meta/` as default.

Target path: `~/git/skills-hub-registry/<category>/$ARGUMENTS/`

VALIDATION: Category extracted from frontmatter and target path determined.

---

=== PHASE 2: COPY TO REGISTRY ===

1. Create the target directory: `mkdir -p ~/git/skills-hub-registry/<category>/$ARGUMENTS/`
2. Copy all skill files:
   - `~/.claude/skills/$ARGUMENTS/SKILL.md` → registry (required)
   - `~/.claude/skills/$ARGUMENTS/references/` → registry (if exists)
   - `~/.claude/skills/$ARGUMENTS/scripts/` → registry (if exists)
   - `~/.claude/skills/$ARGUMENTS/assets/` → registry (if exists)
   - Do NOT copy `LEARNINGS.md` — that's local usage history, not part of the published skill

3. Update the SKILL.md frontmatter in the registry copy:
   - Ensure `platforms: [CLAUDE_CODE]` is present (add if missing)
   - Ensure `version` is quoted (e.g., `"1.0.0"` not `1.0.0`)
   - Leave all other fields unchanged

VALIDATION: `~/git/skills-hub-registry/<category>/$ARGUMENTS/SKILL.md` exists and contains `platforms`.
FALLBACK: If copy fails, check file permissions and retry.

---

=== PHASE 3: COMMIT AND PUSH TO REGISTRY ===

```bash
cd ~/git/skills-hub-registry
git add <category>/$ARGUMENTS/
git commit -m "feat(<category>): add $ARGUMENTS skill v<version>"
git push origin main
```

VALIDATION: `git push` exits with code 0.
FALLBACK: If push fails, run `git pull --rebase origin main` then retry push.

---

=== PHASE 4: SYNC TO PRODUCTION PLATFORM ===

This syncs the registry into the live skills-hub database.

Run the following (all in one shell context so env vars persist):

```bash
# 1. Fetch prod DB credentials
set -a; . ~/.claude/state/skills-hub-publish.env; set +a
DB_PASS=$(AWS_PROFILE=$SKILLS_HUB_AWS_PROFILE AWS_DEFAULT_REGION=$SKILLS_HUB_AWS_REGION \
  aws secretsmanager get-secret-value --secret-id "$SKILLS_HUB_DB_SECRET_ID" \
  --query SecretString --output text)

# 2. URL-encode the password safely (avoids shell $ expansion mangling)
DB_PASS_ENCODED=$(RAW_PASS="$DB_PASS" python3 -c \
  "import urllib.parse, os; print(urllib.parse.quote(os.environ['RAW_PASS'], safe=''))")

# 3. Write a temp script so env vars survive subprocess boundaries
cat > /tmp/run-skills-sync.sh << SCRIPT
#!/bin/bash
export DATABASE_URL="postgresql://${SKILLS_HUB_DB_USER}:${DB_PASS_ENCODED}@${SKILLS_HUB_DB_HOST}:${SKILLS_HUB_DB_PORT}/${SKILLS_HUB_DB_NAME}?schema=public"
export NODE_ENV=production
cd ~/git/skills-hub/apps/api
# Pull latest registry so the sync picks up the new skill
cd ~/git/skills-hub && git pull --ff-only 2>/dev/null || true
cd ~/git/skills-hub/apps/api
npx tsx prisma/seed-external.ts --sync
SCRIPT
chmod +x /tmp/run-skills-sync.sh
bash /tmp/run-skills-sync.sh
```

The sync will print one line per external source showing created/updated/skipped counts.
Look for the `$SKILLS_HUB_SOURCE_SLUG` source line — that's the registry with your skills.

VALIDATION: Sync exits 0 and prints summary lines without "failed > 0".
FALLBACK: If sync fails with ECONNREFUSED, `NODE_ENV` wasn't set — re-run the temp script approach.
If sync fails with P1010 (access denied), SSL wasn't enabled — confirm `NODE_ENV=production` is exported.
If sync fails with an AWS error, run `aws sso login --profile $SKILLS_HUB_AWS_PROFILE` and retry.

---

=== SELF-REVIEW ===

Score the result (1–5):

- Complete: Did the skill land in registry AND sync to production?
- Robust: Were all pre-flight checks run? Were fallbacks needed?
- Clean: Is the registry SKILL.md properly formatted with platforms field?

If any score < 4: identify the gap, fix it, re-score.

---

=== OUTPUT SUMMARY ===

```
## Published: /<skill-name>

**Registry path:** ~/git/skills-hub-registry/<category>/<skill>/SKILL.md
**GitHub commit:** <short SHA>
**Production sync:** <created N / updated N from the registry source line>

The skill is now available on skills-hub.ai and installable via:
  /install <skill-name>
```

---

## STRICT RULES

- Never copy LEARNINGS.md to the registry — it's local history, not public content.
- Always use the temp-script pattern for the sync step (PHASE 4). Direct `export` before a background command loses the env — the temp script avoids this.
- The sync re-processes ALL skills in the registry, not just the new one. That's expected and harmless.
- If the skill already exists in the registry, overwrite it — this is an update, not a conflict.
