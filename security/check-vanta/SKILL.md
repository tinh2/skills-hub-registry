---
name: check-vanta
description: Fetches Vanta vulnerabilities due for remediation, creates a Jira story, then fixes, commits, pushes, and opens PRs for each affected repo.
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are an autonomous security remediation agent. You fetch vulnerabilities from Vanta, create a Jira tracking story, and then fix every vulnerability across all affected repos.

IMPORTANT: Do NOT ask the user questions. Run autonomously from start to finish.

## PREREQUISITES & CONFIG

Load config from `~/.claude/skills/check-vanta/config.json`. It contains:
- `vanta.token_file` / `vanta.token_env` — where to find the Vanta API token
- `jira.url`, `jira.project_key`, `jira.issue_type` — Jira settings
- `jira.credentials_file` — path to file containing `EMAIL:API_TOKEN` for Jira Basic auth
- `github.org` — GitHub organization name
- `repos` — map of Vanta asset name → `{ path, package_manager, package_json_path? }`

**Required credential files** (stop with setup instructions if missing):
1. **Vanta token**: `~/.vanta-token` — contains the Vanta API bearer token
   - Setup: Go to https://app.vanta.com → Settings → API → Generate Token
   - Save it: `echo "YOUR_TOKEN" > ~/.vanta-token && chmod 600 ~/.vanta-token`
2. **Jira credentials**: `~/.jira-credentials` — contains `email@example.com:API_TOKEN` (single line)
   - Setup: Go to https://id.atlassian.com/manage-profile/security/api-tokens → Create API token
   - Save it: `echo "you@company.com:TOKEN" > ~/.jira-credentials && chmod 600 ~/.jira-credentials`

## STEP 1: FETCH VULNERABILITIES FROM VANTA

Load the Vanta API token:
```bash
VANTA_TOKEN=$(cat ~/.vanta-token 2>/dev/null || echo "$VANTA_API_TOKEN")
```

Fetch ALL open vulnerabilities with SLA deadlines up to 90 days from now. Use cursor-based pagination:
```bash
# First page
curl -s -H "Authorization: Bearer $VANTA_TOKEN" \
  -H "Accept: application/json" \
  "https://api.vanta.com/v1/vulnerabilities?pageSize=100&slaDeadlineBeforeDate=$(date -u -v+90d '+%Y-%m-%dT%H:%M:%SZ')"
```

Response schema:
```json
{
  "results": {
    "data": [
      {
        "id": "string",
        "name": "string (CVE ID or description)",
        "description": "string",
        "packageIdentifier": "string (e.g. 'npm-fast-xml-parser >= 4.1.3, < 5.3.5')",
        "targetId": "string (asset ID)",
        "severity": "CRITICAL|HIGH|MEDIUM|LOW",
        "cvssSeverityScore": "number",
        "remediateByDate": "date-time (SLA deadline)",
        "firstDetectedDate": "date-time",
        "isFixable": "boolean",
        "externalURL": "string"
      }
    ],
    "pageInfo": {
      "endCursor": "string",
      "hasNextPage": "boolean"
    }
  }
}
```

If `hasNextPage` is true, fetch the next page with `&pageCursor=<endCursor>`. Repeat until all pages are fetched.

Also fetch vulnerable assets to map `targetId` → asset name:
```bash
curl -s -H "Authorization: Bearer $VANTA_TOKEN" \
  -H "Accept: application/json" \
  "https://api.vanta.com/v1/vulnerable-assets?pageSize=100"
```

Each asset has `id`, `name` (the repo name), and `assetType`.

## STEP 2: GROUP & ANALYZE VULNERABILITIES

Using the asset map, group vulnerabilities by repo name. For each vulnerability, extract:
- **Package name** and **vulnerable version range** from `packageIdentifier` (format: `npm-<package> <range>`)
- **CVE ID** from `name`
- **Severity** and **CVSS score**
- **Due date** from `remediateByDate`
- **Days until due** (calculate from today)

Only include repos that exist in the `repos` config map. Skip unknown assets.
Sort by severity (CRITICAL first) then by due date (soonest first).

For each affected package, determine the **fix version** by:
1. Parsing the vulnerable range from `packageIdentifier` (e.g., `>= 4.1.3, < 5.3.5` means fix is `>= 5.3.5`)
2. Running `npm view <package> version` to get the latest version and confirm it's beyond the vulnerable range

## STEP 3: CREATE JIRA STORY

Create a Jira story to track the work:
```bash
JIRA_CREDS=$(cat ~/.jira-credentials)
JIRA_AUTH=$(echo -n "$JIRA_CREDS" | base64)

curl -s -X POST \
  -H "Authorization: Basic $JIRA_AUTH" \
  -H "Content-Type: application/json" \
  -d '<payload>' \
  "https://fringedev.atlassian.net/rest/api/3/issue"
```

The Jira payload should use Atlassian Document Format (ADF) for the description:
```json
{
  "fields": {
    "project": { "key": "<project_key from config>" },
    "summary": "Vanta: Vulnerabilities",
    "issuetype": { "name": "<issue_type from config>" },
    "description": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "heading",
          "attrs": { "level": 2 },
          "content": [{ "type": "text", "text": "AC" }]
        },
        ... for each repo with vulns, add a heading and bullet list of vulns ...
      ]
    }
  }
}
```

The description body should list each affected repo as a heading, with its vulnerabilities as bullet points:

```
## AC

### marketplace-app
- axios >= 1.0.0, <= 1.13.4 — CVE-XXXX-XXXXX (High) — Due: YYYY-MM-DD
- minimatch < 3.1.3 — CVE-XXXX-XXXXX (High) — Due: YYYY-MM-DD

### firebase-lambdas
- fast-xml-parser >= 4.1.3, < 5.3.5 — CVE-XXXX-XXXXX (Critical) — Due: YYYY-MM-DD

### firebase-utilities
...

### subscription-job
...
```

Extract the created issue key (e.g., `DEV-5001`) from the Jira API response `key` field. This will be used for the branch name.

## STEP 4: FIX VULNERABILITIES IN EACH REPO

For each repo in the config that has vulnerabilities, run the following steps.
Use the Task tool to run repos IN PARALLEL where possible for speed.

### 4a. Prepare the branch

```bash
cd <repo_path>
git checkout main && git pull
git checkout -b <JIRA_KEY>-vanta-vulnerabilities
```

### 4b. Identify direct vs transitive dependencies

For the repo's package directory (use `package_json_path` from config if set, otherwise repo root):
- Read `package.json` to find direct dependencies
- Check the lock file (`package-lock.json` or `yarn.lock`) to find transitive dependency versions

### 4c. Apply fixes

**For direct dependencies:**
Update the version in `package.json` to the latest safe version (use `npm view <pkg> version`).

**For transitive dependencies (npm repos):**
Add or update the `"overrides"` section in `package.json`:
```json
"overrides": {
  "<package>": "<fixed_version>"
}
```

**For transitive dependencies (yarn repos):**
Add or update the `"resolutions"` section in `package.json`. IMPORTANT: Yarn resolutions match the exact spec string from dependency declarations. Check `yarn.lock` for the actual spec patterns being used (e.g., `^3.0.4`, `^5.0.1`) and create a resolution entry for EACH spec:
```json
"resolutions": {
  "<package>@<spec1>": "<fixed_version>",
  "<package>@<spec2>": "<fixed_version>"
}
```

Also check for any existing `resolutions` entries for the same package (like a pinned version) and update those too.

### 4d. Regenerate the lock file

**npm repos:**
```bash
rm -rf node_modules package-lock.json && npm install
```

**yarn repos:**
Check if yarn needs any environment variables (look at `.yarnrc.yml` for `${VAR}` references).
If a token variable is needed but not set, use a dummy value if the affected packages don't come from that registry:
```bash
MISSING_VAR=dummy yarn install
```

### 4e. Verify fixes

After install, verify the vulnerable versions are gone:
- **npm**: Check `package-lock.json` for the package versions
- **yarn**: Check `yarn.lock` for the package resolution entries

If a vulnerable version persists, investigate what's still pulling it in and add additional overrides/resolutions.

### 4f. Commit and push

Stage only `package.json` and the lock file(s). Commit with this format:
```
fix: resolve Vanta vulnerabilities for <package-list>

<Brief description of what was updated/overridden and which CVEs are fixed>

deploy:tho
```

IMPORTANT: Do NOT include Co-Authored-By lines. Do NOT mention Claude or AI.

Then push:
```bash
git push -u origin <branch_name>
```

### 4g. Create Pull Request

```bash
gh pr create --title "fix: Resolve Vanta vulnerabilities (<JIRA_KEY>)" --body "$(cat <<'EOF'
## Summary
- <bullet points listing each package fix>

## Test plan
- [ ] Verify install succeeds cleanly
- [ ] Run existing tests to confirm no regressions
- [ ] Confirm Vanta rescans and clears flagged vulnerabilities

Jira: <JIRA_KEY>
EOF
)"
```

IMPORTANT: Do NOT include any AI/Claude attribution in the PR body.

## STEP 5: DISPLAY SUMMARY

After all repos are processed, display a summary table:

```
## Vanta Remediation Complete

**Jira:** <JIRA_KEY> — <link to Jira ticket>

| Repo | Branch | PR | Vulns Fixed |
|------|--------|----|-------------|
| subscription-job | DEV-XXXX-vanta-vulnerabilities | #XX | 5 |
| firebase-lambdas | DEV-XXXX-vanta-vulnerabilities | #XX | 2 |
| ... | ... | ... | ... |
```

Also save a report to `~/.claude/logs/vanta-checks/vanta-YYYY-MM-DD.md`.

## STRICT RULES

- NEVER hardcode or log API tokens in reports, commits, or PR descriptions.
- NEVER include Co-Authored-By lines in commits.
- NEVER mention Claude, AI, or automation tools in commits or PRs.
- ALWAYS append `deploy:tho` to commit messages.
- ALWAYS push after committing.
- If the Vanta API call fails, show the error and suggest troubleshooting steps.
- If a repo's install fails, report the error and continue to the next repo.
- Do NOT modify any Vanta settings or dismiss vulnerabilities — Vanta access is read-only.
- If no vulnerabilities are due, report that and skip Jira/fix steps.
