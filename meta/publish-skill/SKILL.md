---
name: publish-skill
description: "Publish a locally installed skill to the skills-hub registry and sync it to the production platform. Use when: 'publish skill X', 'push skill to hub', 'add skill to registry', 'publish to skills hub', 'share this skill', 'make skill available globally'. Runs entirely from the Mac Studio — no VPS needed."
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
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
- [ ] AWS credentials are available: `AWS_PROFILE=recipeai AWS_DEFAULT_REGION=us-east-1 aws sts get-caller-identity`

If `$ARGUMENTS` is empty: stop and tell the user "Usage: /publish-skill <skill-slug>"
If the skill file doesn't exist: list `~/.claude/skills/` to show available skills, then stop.
If AWS creds fail: tell the user to run `aws sso login --profile recipeai` first.

VALIDATION: All checks must pass before proceeding.
FALLBACK: Report exactly which check failed and what to do to fix it.

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
DB_PASS=$(AWS_PROFILE=recipeai AWS_DEFAULT_REGION=us-east-1 aws secretsmanager \
  get-secret-value --secret-id "skills-hub/prod/db-password" \
  --query SecretString --output text)

# 2. URL-encode the password safely (avoids shell $ expansion mangling)
DB_PASS_ENCODED=$(RAW_PASS="$DB_PASS" python3 -c \
  "import urllib.parse, os; print(urllib.parse.quote(os.environ['RAW_PASS'], safe=''))")

# 3. Write a temp script so env vars survive subprocess boundaries
cat > /tmp/run-skills-sync.sh << SCRIPT
#!/bin/bash
export DATABASE_URL="postgresql://skillshub_admin:${DB_PASS_ENCODED}@skills-hub-prod.c6tii4e8ymqj.us-east-1.rds.amazonaws.com:5432/skillshub?schema=public"
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
Look for the `tinh2` source line — that's the registry with your skills.

VALIDATION: Sync exits 0 and prints summary lines without "failed > 0".
FALLBACK: If sync fails with ECONNREFUSED, `NODE_ENV` wasn't set — re-run the temp script approach.
If sync fails with P1010 (access denied), SSL wasn't enabled — confirm `NODE_ENV=production` is exported.
If sync fails with AWS error, run `aws sso login --profile recipeai` and retry.

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
**Production sync:** <created N / updated N from tinh2 source line>

The skill is now available on skills-hub.ai and installable via:
  /install <skill-name>
```

---

## STRICT RULES

- Never copy LEARNINGS.md to the registry — it's local history, not public content.
- Always use the temp-script pattern for the sync step (PHASE 4). Direct `export` before a background command loses the env — the temp script avoids this.
- The sync re-processes ALL skills in the registry, not just the new one. That's expected and harmless.
- If the skill already exists in the registry, overwrite it — this is an update, not a conflict.
