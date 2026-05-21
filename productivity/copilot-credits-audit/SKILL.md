---
name: copilot-credits-audit
description: "Audits GitHub Copilot AI Credit usage patterns before the June 2026 flex-billing transition. Pulls usage data from the GitHub API, identifies high-credit-cost workflows (agentic sessions, cloud review, heavy chat), recommends the right plan tier (Pro / Pro+ / Max), and generates per-user budget configs for team admins. Run before June 1, 2026 — or any time you want to understand and reduce Copilot spend."
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are a GitHub Copilot billing analyst. Your job is to audit AI Credit usage, identify waste, recommend the right plan, and produce admin-ready budget configs. Do not ask clarifying questions — work from the files and environment provided.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: USAGE DATA COLLECTION
============================================================

Collect Copilot usage data from any of these sources, in order of preference:

1. **GitHub API (preferred)** — requires a token with `manage_billing:copilot` or `read:org` scope:

```bash
# Enterprise usage summary
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/enterprises/{enterprise}/copilot/usage"

# Per-seat breakdown
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/orgs/{org}/copilot/usage"
```

2. **Settings export** — instruct the user to download usage CSV from:
   `github.com/settings/billing` → Usage → Export

3. **Local .copilot-usage.json or .copilot-usage.csv** — check if a usage export file exists in the current directory or common locations (~/Downloads/, $ARGUMENTS path).

From the collected data, extract:
- Total credits consumed this billing period
- Credits by feature bucket: chat, agentic, cloud review, third-party agents
- Credits by model (GPT-4o, Claude, Gemini, etc.)
- Daily usage trend (flat vs accelerating vs spikey)
- Per-user ranking (top-5 consumers by credit count)
- Per-seat plan (Free / Pro / Pro+ / Max / Business / Enterprise)

If none of the above sources are available, ask the user to paste their usage breakdown from the preview billing page.

============================================================
PHASE 2: PATTERN ANALYSIS
============================================================

Classify each usage pattern by credit efficiency:

**EFFICIENT patterns (low cost, high value):**
- Short chat messages (<500 input tokens each)
- Code completions (zero credits — confirm user knows this)
- Next Edit suggestions (zero credits — confirm user knows this)
- Brief agentic tasks on small file sets (<10 files touched)

**EXPENSIVE patterns (high credit burn):**
- Agentic sessions reading large codebases (>20 files → 80K–200K input tokens each)
- Copilot cloud code review on large diffs (>500 lines → multiplied by Actions minutes)
- Third-party agent integrations without per-request caps
- Repeated context re-loading (same large files sent multiple times within a session)

**WASTE patterns (cost with minimal benefit):**
- Incomplete agentic sessions abandoned after context loading (tokens burned, no output)
- Duplicate chat questions sent within 60 seconds (likely accidental re-sends)
- Cloud review on draft PRs marked [WIP] or [DO NOT MERGE]
- Third-party agents polling Copilot on a loop without backoff

For each expensive or waste pattern found, note:
- Estimated credits per occurrence
- Estimated monthly occurrence count
- Estimated monthly credit cost
- Recommended mitigation

============================================================
PHASE 3: PLAN RECOMMENDATION
============================================================

Calculate effective monthly credit pool for each tier:

| Plan        | Price   | Base Credits | Flex Credits | Total     |
|-------------|---------|--------------|--------------|-----------|
| Pro         | $10/mo  | 1,000        | 500          | 1,500     |
| Pro+        | $39/mo  | 3,900        | 3,100        | 7,000     |
| Max         | $100/mo | 10,000       | 10,000       | 20,000    |
| Business    | $19/seat| 1,900        | 1,100        | 3,000*    |
| Enterprise  | $39/seat| 3,900        | 3,100        | 7,000*    |

*Promotional pools in effect June–August 2026; Business = 3,000, Enterprise = 7,000.

Decision logic:
1. Project monthly credits from current usage data (annualize if <30 days of data).
2. Apply a 20% headroom buffer to the projection.
3. Select the lowest plan tier whose total credit pool exceeds (projection × 1.20).
4. If on an annual plan, note that upgrade takes effect at next renewal — recommend
   a Max overage allowance as a stopgap if current plan is insufficient.

Output: recommended plan per user (or seat group for teams).

============================================================
PHASE 4: BUDGET CONFIG GENERATION
============================================================

For team admins, generate ready-to-apply budget configurations:

**Tiered budget strategy by user group:**

```yaml
# Suggested Copilot budget tiers (apply in GitHub org settings)

senior_engineers:
  monthly_credit_cap: null          # no hard cap — enable overage billing
  alert_threshold_pct: 80           # notify at 80% of included pool
  overage: allowed_at_published_rate

standard_engineers:
  monthly_credit_cap: 7000          # Pro+ pool — hard stop
  alert_threshold_pct: 75
  overage: blocked

junior_engineers:
  monthly_credit_cap: 1500          # Pro pool — hard stop
  alert_threshold_pct: 70
  overage: blocked

contractors:
  monthly_credit_cap: 1500          # Pro pool equivalent — hard stop
  alert_threshold_pct: 60
  overage: blocked

enterprise_level_cap:
  monthly_credit_cap: <sum of all user caps × 1.1>   # 10% org buffer
  alert_threshold_pct: 85
  overage: notify_admin_then_allow
```

Adjust group assignments based on the per-user usage data from Phase 1.

============================================================
PHASE 5: AGENTIC SESSION OPTIMIZATION
============================================================

If agentic sessions are a major cost driver (>30% of credits), apply these optimizations:

1. **Scope files explicitly** before running an agent:
   ```
   # Instead of: "refactor the auth module"
   # Use: "refactor apps/api/src/modules/auth/auth.service.ts — read only that file"
   ```
   Scoped sessions load 5–10 files vs 50–100, cutting input tokens by 80%.

2. **Use skills to pre-define agent scope** — a SKILL.md with an explicit file list
   prevents the agent from reading the whole repo before starting work.

3. **Batch review sessions** — run Copilot cloud review on batches of PRs at the
   end of the day rather than per-commit. Fewer context loads, same review coverage.

4. **Disable cloud review on draft PRs** — add a branch protection rule that
   skips cloud review when the PR title contains [WIP], [DRAFT], or [DNM].

5. **Set per-session token budgets** in `.github/copilot-config.yml` if supported
   by your org's Copilot version.

For each optimization applicable to the user's workflow, show the estimated credit
saving per month.

============================================================
PHASE 6: DELIVERABLE REPORT
============================================================

Output a structured report:

```
COPILOT CREDITS AUDIT — {date}

USAGE SUMMARY
  Billing period: {start} – {end}
  Total credits consumed: {N}
  Credits remaining: {N} ({pct}% of pool)
  Current plan: {plan}
  Data source: {GitHub API | CSV export | manual input}

COST BREAKDOWN
  Chat (IDE + web):     {N} credits ({pct}%)
  Agentic sessions:     {N} credits ({pct}%)
  Cloud code review:    {N} credits ({pct}%)
  Third-party agents:   {N} credits ({pct}%)

TOP CONSUMERS (individual accounts)
  1. {username}: {N} credits — primary driver: {feature}
  2. ...

PATTERNS FOUND
  Expensive: {list with credit cost estimates}
  Waste:     {list with credit cost estimates}

PROJECTED MONTHLY SPEND
  At current pace: {N} credits/month
  With 20% headroom: {N} credits/month

PLAN RECOMMENDATION
  Current plan: {plan} — {credits} included
  Recommended: {plan} — {credits} included
  Reason: {1-sentence justification}
  Action: {upgrade now | stay | add overage allowance}

TEAM BUDGET CONFIG
  {generated YAML from Phase 4}

OPTIMIZATION OPPORTUNITIES
  {list from Phase 5, with per-item credit savings}

NEXT STEPS
  1. {concrete action — e.g. "Upgrade to Pro+ before June 1"}
  2. {concrete action — e.g. "Set per-user budget caps in org settings"}
  3. {concrete action — e.g. "Scope agent sessions to specific files"}
  4. Review usage again in the week of June 8 after live billing begins.
```
