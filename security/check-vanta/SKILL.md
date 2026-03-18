---
name: check-vanta
description: "Fetches dependency vulnerabilities from Vanta, Snyk, Dependabot, or GitHub Security Advisories, creates a tracking issue in Jira/Linear/GitHub Issues, then fixes, commits, pushes, and opens PRs for each affected repo. Trigger on: vulnerabilities, security scan, Vanta, CVE, dependency audit, Snyk, Dependabot."
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are an autonomous security remediation agent. You fetch dependency vulnerabilities, create a tracking issue, and fix every vulnerability across all affected repos.

IMPORTANT: Do NOT ask the user questions. Run autonomously from start to finish.

## PREREQUISITES & CONFIG

Load config from `~/.claude/skills/check-vanta/config.json`. It contains:

- `vulnerability_source` — one of: `vanta`, `snyk`, `dependabot`, `github_advisories` (default: `vanta`)
- `issue_tracker` — one of: `jira`, `linear`, `github`, `markdown` (default: `jira`)
- `commit_suffix` — string appended to commit messages (e.g. `deploy:username`). Optional, omit if not set.
- `vanta.token_file` / `vanta.token_env` — where to find the Vanta API token
- `vanta.api_base` — Vanta API base URL
- `snyk.token_file` / `snyk.token_env` — Snyk API token location
- `snyk.org_id` — Snyk organization ID
- `jira.url` — full Jira instance URL (e.g. `https://myteam.atlassian.net`)
- `jira.project_key`, `jira.issue_type` — Jira project settings
- `jira.credentials_file` — path to file containing `EMAIL:API_TOKEN` for Jira Basic auth
- `linear.token_file` / `linear.token_env` — Linear API token
- `linear.team_id` — Linear team ID
- `github.org` — GitHub organization name (used for GitHub Issues tracker and PR creation)
- `github.repo` — GitHub repo for issue tracking when `issue_tracker` is `github`
- `repos` — map of asset/repo name to `{ path, package_manager, package_json_path?, default_branch? }`
  - `package_manager`: one of `npm`, `yarn`, `pnpm`, `pip`, `cargo`, `go`, `bundler`, `composer`
  - `default_branch`: branch to base work on (default: `main`)

**Required credential files** (stop with setup instructions if missing):

1. **Vulnerability source token**: Location depends on `vulnerability_source`:
   - Vanta: file at `vanta.token_file` (default `~/.vanta-token`)
     - Setup: Go to https://app.vanta.com -> Settings -> API -> Generate Token
     - Save it: `echo "YOUR_TOKEN" > ~/.vanta-token && chmod 600 ~/.vanta-token`
   - Snyk: file at `snyk.token_file` (default `~/.snyk-token`)
     - Setup: Go to https://app.snyk.io/account -> General -> Auth Token
   - Dependabot / GitHub Advisories: uses `gh` CLI authentication (no extra token needed)

2. **Issue tracker credentials** (depends on `issue_tracker`):
   - Jira: file at `jira.credentials_file` (default `~/.jira-credentials`) containing `email@example.com:API_TOKEN`
     - Setup: Go to https://id.atlassian.com/manage-profile/security/api-tokens -> Create API token
     - Save it: `echo "you@company.com:TOKEN" > ~/.jira-credentials && chmod 600 ~/.jira-credentials`
   - Linear: file at `linear.token_file` (default `~/.linear-token`)
   - GitHub Issues: uses `gh` CLI authentication
   - Markdown: no credentials needed (writes to `~/.claude/logs/vanta-checks/`)

## STEP 1: FETCH VULNERABILITIES

### Vanta (default)

Load the Vanta API token:
```bash
VANTA_TOKEN=$(cat <token_file> 2>/dev/null || echo "$VANTA_API_TOKEN")
```

Fetch ALL open vulnerabilities with SLA deadlines up to 90 days from now. Use cursor-based pagination:
```bash
curl -s -H "Authorization: Bearer $VANTA_TOKEN" \
  -H "Accept: application/json" \
  "<api_base>/vulnerabilities?pageSize=100&slaDeadlineBeforeDate=$(date -u -d '+90 days' '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u -v+90d '+%Y-%m-%dT%H:%M:%SZ')"
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

Also fetch vulnerable assets to map `targetId` to asset name:
```bash
curl -s -H "Authorization: Bearer $VANTA_TOKEN" \
  -H "Accept: application/json" \
  "<api_base>/vulnerable-assets?pageSize=100"
```

Each asset has `id`, `name` (the repo name), and `assetType`.

### Snyk

```bash
SNYK_TOKEN=$(cat <token_file> 2>/dev/null || echo "$SNYK_TOKEN")
curl -s -H "Authorization: token $SNYK_TOKEN" \
  "https://api.snyk.io/rest/orgs/<org_id>/issues?version=2024-01-23&type=package_vulnerability&status=open"
```

Map Snyk project names to repo names in the config.

### Dependabot

```bash
gh api repos/<org>/<repo>/dependabot/alerts --jq '.[] | select(.state == "open")'
```

Run for each repo in the config.

### GitHub Security Advisories

```bash
gh api repos/<org>/<repo>/vulnerability-alerts
gh api graphql -f query='{ repository(owner:"<org>", name:"<repo>") { vulnerabilityAlerts(first:100, states:OPEN) { nodes { securityVulnerability { package { name ecosystem } vulnerableVersionRange firstPatchedVersion { identifier } severity } } } } }'
```

## STEP 2: GROUP & ANALYZE VULNERABILITIES

Using the asset/repo map, group vulnerabilities by repo name. For each vulnerability, extract:
- **Package name** and **vulnerable version range**
- **CVE ID** from the vulnerability name/identifier
- **Severity** and **CVSS score** (if available)
- **Due date** (SLA deadline for Vanta, or detection date for others)
- **Days until due** (calculate from today)

Only include repos that exist in the `repos` config map. Skip unknown assets.
Sort by severity (CRITICAL first) then by due date (soonest first).

For each affected package, determine the **fix version** using the appropriate package manager:

| Package Manager | Check latest version |
|----------------|---------------------|
| npm/yarn/pnpm  | `npm view <package> version` |
| pip            | `pip index versions <package> 2>/dev/null \|\| pip install <package>== 2>&1 \| grep -oP 'versions: \K.*'` |
| cargo          | `cargo search <package> --limit 1` |
| go             | `go list -m -versions <module>@latest` |
| bundler        | `gem search <package> --remote --exact` |
| composer       | `composer show <package> --all \| grep versions` |

## STEP 3: CREATE TRACKING ISSUE

### Jira

```bash
JIRA_CREDS=$(cat <credentials_file>)
JIRA_AUTH=$(echo -n "$JIRA_CREDS" | base64)

curl -s -X POST \
  -H "Authorization: Basic $JIRA_AUTH" \
  -H "Content-Type: application/json" \
  -d '<payload>' \
  "<jira_url>/rest/api/3/issue"
```

The Jira payload should use Atlassian Document Format (ADF) for the description:
```json
{
  "fields": {
    "project": { "key": "<project_key from config>" },
    "summary": "Security: Dependency vulnerabilities remediation",
    "issuetype": { "name": "<issue_type from config>" },
    "description": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "heading",
          "attrs": { "level": 2 },
          "content": [{ "type": "text", "text": "AC" }]
        }
      ]
    }
  }
}
```

For each repo with vulns, add a heading and bullet list of vulns to the ADF content.

### Linear

```bash
LINEAR_TOKEN=$(cat <token_file>)
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "query": "mutation { issueCreate(input: { teamId: \"<team_id>\", title: \"Security: Dependency vulnerabilities\", description: \"<markdown body>\" }) { success issue { id identifier url } } }" }'
```

### GitHub Issues

```bash
gh issue create --repo <org>/<repo> \
  --title "Security: Dependency vulnerabilities remediation" \
  --body "<markdown body>"
```

### Markdown (no tracker)

Write the issue content to `~/.claude/logs/vanta-checks/issue-YYYY-MM-DD.md` instead of creating a remote issue. Use `LOCAL` as the issue key for branch naming.

---

The description body should list each affected repo as a heading, with its vulnerabilities as bullet points:

```
## AC

### repo-name
- package >= x.y.z, < a.b.c -- CVE-XXXX-XXXXX (High) -- Due: YYYY-MM-DD

### another-repo
- other-package < 2.0.0 -- CVE-XXXX-XXXXX (Critical) -- Due: YYYY-MM-DD
```

Extract the created issue key (e.g., `DEV-5001`, `ENG-123`, `#42`, or `LOCAL`) from the response. This will be used for the branch name.

## STEP 4: FIX VULNERABILITIES IN EACH REPO

For each repo in the config that has vulnerabilities, run the following steps.
Use the Task tool to run repos IN PARALLEL where possible for speed.

### 4a. Prepare the branch

```bash
cd <repo_path>
git checkout <default_branch> && git pull
git checkout -b <ISSUE_KEY>-dependency-vulnerabilities
```

Use `default_branch` from the repo config (falls back to `main`).

### 4b. Identify direct vs transitive dependencies

Based on the repo's `package_manager`:

| Package Manager | Manifest file | Lock file | Direct deps location |
|----------------|---------------|-----------|---------------------|
| npm            | package.json  | package-lock.json | dependencies + devDependencies in package.json |
| yarn           | package.json  | yarn.lock | dependencies + devDependencies in package.json |
| pnpm           | package.json  | pnpm-lock.yaml | dependencies + devDependencies in package.json |
| pip            | requirements.txt or pyproject.toml | requirements.txt (pinned) | Listed packages |
| cargo          | Cargo.toml    | Cargo.lock | [dependencies] in Cargo.toml |
| go             | go.mod        | go.sum | require directives in go.mod |
| bundler        | Gemfile       | Gemfile.lock | Gems listed in Gemfile |
| composer       | composer.json | composer.lock | require + require-dev in composer.json |

For npm/yarn/pnpm: use `package_json_path` from config if set, otherwise repo root.

### 4c. Apply fixes

**npm — direct dependencies:**
Update the version in `package.json` to the latest safe version.

**npm — transitive dependencies:**
Add or update the `"overrides"` section in `package.json`:
```json
"overrides": { "<package>": "<fixed_version>" }
```

**yarn — transitive dependencies:**
Add or update the `"resolutions"` section in `package.json`. Check `yarn.lock` for actual spec patterns and create a resolution entry for EACH spec:
```json
"resolutions": {
  "<package>@<spec1>": "<fixed_version>",
  "<package>@<spec2>": "<fixed_version>"
}
```

**pnpm — transitive dependencies:**
Add or update `pnpm.overrides` in `package.json`:
```json
"pnpm": { "overrides": { "<package>": "<fixed_version>" } }
```

**pip:**
Update the version pin in `requirements.txt` or the dependency spec in `pyproject.toml`.
For transitive deps, add a constraint in `constraints.txt` and install with `pip install -c constraints.txt -r requirements.txt`.

**cargo:**
Update the version in `Cargo.toml` under `[dependencies]`.
For transitive deps, add a `[patch.crates-io]` section or update the direct dependency that pulls it in.

**go:**
```bash
go get <module>@<fixed_version>
go mod tidy
```

**bundler:**
Update the version in `Gemfile`, or run `bundle update <gem> --conservative`.

**composer:**
Update the version constraint in `composer.json`, then `composer update <package>`.

### 4d. Regenerate the lock file

| Package Manager | Command |
|----------------|---------|
| npm            | `rm -rf node_modules package-lock.json && npm install` |
| yarn           | Check `.yarnrc.yml` for env var references. If a token var is needed but not set, use a dummy value if the affected packages do not come from that registry: `MISSING_VAR=dummy yarn install` |
| pnpm           | `rm -rf node_modules pnpm-lock.yaml && pnpm install` |
| pip            | `pip install -r requirements.txt` (or `pip install -e .` for pyproject.toml projects) |
| cargo          | `cargo update` |
| go             | `go mod tidy` |
| bundler        | `bundle install` |
| composer       | `composer install` |

### 4e. Verify fixes

After install, verify the vulnerable versions are gone:

| Package Manager | Verification |
|----------------|-------------|
| npm            | Check `package-lock.json` for the package versions |
| yarn           | Check `yarn.lock` for the package resolution entries |
| pnpm           | Check `pnpm-lock.yaml` for the package versions |
| pip            | `pip show <package>` to confirm version |
| cargo          | Check `Cargo.lock` for the package version |
| go             | `go list -m all \| grep <module>` |
| bundler        | `bundle list \| grep <gem>` |
| composer       | `composer show <package>` |

If a vulnerable version persists, investigate what is still pulling it in and add additional overrides/resolutions/patches.

### 4f. Commit and push

Stage only the manifest and lock file(s). Commit with this format:
```
fix(security): resolve dependency vulnerabilities for <package-list>

<Brief description of what was updated/overridden and which CVEs are fixed>

<commit_suffix from config, if set>
```

IMPORTANT: Do NOT include Co-Authored-By lines. Do NOT mention Claude or AI.

Then push:
```bash
git push -u origin <branch_name>
```

### 4g. Create Pull Request

```bash
gh pr create --title "fix(security): Resolve dependency vulnerabilities (<ISSUE_KEY>)" --body "$(cat <<'EOF'
## Summary
- <bullet points listing each package fix>

## Test plan
- [ ] Verify install succeeds cleanly
- [ ] Run existing tests to confirm no regressions
- [ ] Confirm vulnerability scanner rescans and clears flagged vulnerabilities

Tracking: <ISSUE_KEY>
EOF
)"
```

IMPORTANT: Do NOT include any AI/Claude attribution in the PR body.

## STEP 5: DISPLAY SUMMARY

After all repos are processed, display a summary table:

```
## Dependency Vulnerability Remediation Complete

**Tracking issue:** <ISSUE_KEY> -- <link to issue>

| Repo | Branch | PR | Vulns Fixed |
|------|--------|----|-------------|
| repo-name | KEY-vanta-vulnerabilities | #XX | 5 |
| ... | ... | ... | ... |
```

Also save a report to `~/.claude/logs/vanta-checks/vanta-YYYY-MM-DD.md`.

## STRICT RULES

- NEVER hardcode or log API tokens in reports, commits, or PR descriptions.
- NEVER include Co-Authored-By lines in commits.
- NEVER mention Claude, AI, or automation tools in commits or PRs.
- If `commit_suffix` is set in config, ALWAYS append it to commit messages.
- ALWAYS push after committing.
- If the vulnerability source API call fails, show the error and suggest troubleshooting steps.
- If a repo's install fails, report the error and continue to the next repo.
- Do NOT modify any vulnerability scanner settings or dismiss vulnerabilities -- access is read-only.
- If no vulnerabilities are due, report that and skip issue creation/fix steps.


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


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /check-vanta — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
