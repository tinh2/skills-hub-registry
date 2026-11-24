---
name: issue-to-qa
description: "Takes one issue all the way to ready for QA: reads the source (Slack thread, Jira/Linear/GitHub issue, alert, meeting notes or text), researches the code, writes lean BE/FE stories, stops once for your approval, files the stories, builds each in its own git worktree, opens PRs, works the review bot rounds until clean, deploys the backend to a dev instance, runs Playwright end to end with screenshots, writes a local HTML report, moves the stories to QA and pings your notification channel. Triggers on: issue to QA, take this to QA, run the full flow, ship this story end to end, turn this Slack thread into stories and PRs, build this ticket, implement and hand off to QA. Use it even when the user only pastes an issue link and says 'do this'."
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
permissions:
  - bash
  - read
  - edit
  - write
  - browser
---

You run a team's story flow from an issue to "ready for QA". You stop once, after the brief and stories. After that you run on your own until QA or a blocker. Merging, approvals, messages to people and anything after QA stay with the user.

Every org specific value comes from the config file. Never guess one.

=== PRE-FLIGHT ===
Before starting, verify:
- [ ] A config exists at `.claude/issue-to-qa.json` in the repo, else `~/.claude/issue-to-qa.json`. If neither exists, run SETUP below, then continue.
- [ ] `git`, `gh` (authenticated) and `jq` are installed. Inside the configured repo, on its default branch.
- [ ] The issue tracker and Slack tools named in the config are connected (MCP or CLI). Missing Slack only disables pings.
- [ ] Playwright (MCP or CLI) is available when any story touches the frontend.
- [ ] A run folder can be created under `config.runs_dir`.
If any check fails:
- Name the missing piece and how to fix it. Do NOT proceed until resolved.

=== SETUP (first run only) ===
Ask the user for each field in one message, offer sensible defaults and write the file:

```json
{
  "repo": { "default_branch": "main", "worktree_path": "../{repo}--{key}-{slug}", "branch": "{key}-{slug}" },
  "tracker": { "type": "jira", "project": "ABC", "issue_type": "Story", "issue_url": "https://example.atlassian.net/browse/{key}", "qa_status": "QA", "assignee": "me" },
  "areas": {
    "backend":  { "paths": ["backend/"],  "test": "make test",  "commit_scope": "api" },
    "frontend": { "paths": ["frontend/"], "test": "yarn vitest run", "install": "yarn install", "commit_scope": "web" }
  },
  "commit_format": "{type}({scope}): {Description} ({key})",
  "review_bot": { "login": "review-bot[bot]", "trigger": "/review", "auto_triggered_on_push": false, "max_rounds": 5 },
  "deploy": { "backend": "./scripts/deploy-dev.sh {tag}", "health_url": "https://api-dev.example.com/health", "image_tag_marker": "image-tag" },
  "preview": { "url": "https://pr-{n}.preview.example.com", "api_switch": "how to point the preview at the dev API, or empty" },
  "testing": { "account_env": "TEST_USER_EMAIL", "db_check": "psql \"$DEV_DB_URL\" -c", "max_e2e_loops": 3 },
  "notify": { "slack_channel_id": "", "push_notifications": true },
  "allow": { "create_issues": true, "transition_to_qa": true, "post_to_notify_channel": true },
  "runs_dir": "~/issue-to-qa-runs",
  "house_rules": ["no code comments", "no stats unless asked"]
}
```

VALIDATION: the file parses with `jq` and every command in it is a real script or alias the user confirmed.
FALLBACK: leave a field empty to skip that step (no preview, no deploy, no Slack). The report lists skipped steps.

=== GROUND RULES ===
- The source wins. Every requirement, AC and PR claim ties to a source (issue, thread, meeting, the user) or becomes an open question. Never add requirements from review tools or guesses.
- Re-check each factual claim against code, data or the source before it goes to the user, the tracker, Slack or a PR.
- Follow the repo's own `CLAUDE.md`, `.claude/rules/` and `config.house_rules`. They beat this skill on code and commit style.
- Only the actions in `config.allow` run automatically. Anything addressed to a person (stakeholder replies, QA notes, lead summaries) is drafted to the clipboard, never sent.
- Only claim what you observed. Skipped or failed steps are named in the PR, the report and the ping.
- Keep `state.md` in the run folder: sources, phase, keys, branches, worktrees, PRs, image tags, deploys, temporary overrides, open questions and each review round's fixes. Update it after every phase. Given a key, run folder or PR with a `state.md`, resume from the recorded phase.

=== PHASE 1: INTAKE AND RESEARCH ===
- Read the source in full, including linked docs, mockups and meeting notes. State the ask in one sentence. If you can't, ask before going further.
- Bugs: find the root cause with evidence (read-only data, logs, code). Features: find what to reuse (tables, components, flags, patterns).
- Verify every endpoint, table, field and component on the default branch. Never write one from memory.
- Search the repo docs for answers before calling anything an open question.
- Decide the split: one backend story, one frontend story or both. Backend and frontend are separate stories and separate PRs.
- Save `research.md` with file paths and line numbers.

VALIDATION: the ask fits in one sentence and every named endpoint or table was found in the code.
FALLBACK: if the source is contradictory, list the contradictions as numbered questions for the stop.

=== PHASE 2: STORIES AND THE ONE STOP ===
Write each story to the run folder (`BE.md`, `FE.md`) in this shape:

```
# BE: <outcome in plain words, under 10 words>

<One plain paragraph: what changes for the user and why.>

Sources: <links>
Depends On: <other story title>   (FE only, when there is one)

## Acceptance Criteria
* **<Group>:**
  * <one testable sentence>

## Decisions
* <choice> (<who>, <date>)

## Open questions
* NEEDS CLARIFICATION: <question> (<who can answer>)

## Dev Notes   (backend, when useful)
* <file and method, what changes>
```

Writing rules: lean, plain language, user-facing names for anything a user sees, no counts or volumes unless they define the work, no requirements without a source. Cut privacy, analytics or "future proofing" ACs nobody asked for.

Then stop and show the user: the ask, a short brief, numbered questions each with your recommendation (include any test step with outside effects such as emails, Slack posts or real third party calls) and the stories. Copy the stories to the clipboard and send a push notification if enabled. Wait.

Apply the answers. Settled ones go to Decisions with the person and date. If `allow.create_issues`, create each story in the tracker, assigned per config, and read it back. Otherwise leave them on the clipboard and wait for the keys.

VALIDATION: the user approved, and each story exists in the tracker with a key.
FALLBACK: if the tracker is unreachable, retry once, then wait for keys pasted by the user.

=== PHASE 3: BUILD, PR AND REVIEW ROUNDS ===
Per story, backend first:
- Fetch, then create the worktree and branch from `origin/<default_branch>` using the config patterns. Never commit on the default branch checkout.
- Implement only what the story says, matching existing patterns. Run the area's install and test commands yourself and fix failures.
- Before the first commit, review the diff for edge cases the story didn't name (partial failures, retries, timezones, empty data, duplicate submits). Fix real ones. Decisions go back to the user as questions, not code.
- Commit with `config.commit_format`. Open the PR with: an opening paragraph (outcome, issue link, why), Behavior, Before launch (flags to create, manual steps), Verification (tests run, dev run, a Step | Result table, overrides reverted, a "Not verified:" line). Frontend PRs name the backend PR to merge first.
- Review rounds: if the bot isn't auto triggered, post `review_bot.trigger`. Poll the bot's summary comment for an update in a background loop. Fix valid findings in one commit, resolve threads without replying. Repeat until the bot reviewed the head commit with no blockers, no unresolved threads, green CI and no merge conflicts, or `max_rounds` is hit.
- When a PR is clean: draft a one-line lead summary (title, issue link, PR link, one sentence on what it does) to the clipboard and post "PR #N is ready for review" plus that summary to the notify channel if allowed.

VALIDATION: each PR is open and clean as defined above.
FALLBACK: at `max_rounds`, stop and report what's left.

=== PHASE 4: DEPLOY AND END-TO-END TEST ===
- Backend PRs: wait for the image built from the head commit, run `deploy.backend` and wait for `health_url` to pass. If the branch adds a migration that the dev deploy won't run, say so and offer a manual path.
- Write `test-plan.md` from the ACs: step, account, data, expected result.
- Frontend or full stack: test on the PR preview pointed at the dev API (`preview.api_switch`), else run the worktree frontend locally. Log in with the account in `testing.account_env`. Do the real action on dev and check the row with `testing.db_check` after each write. Steps with outside effects run only if approved at the stop. Open date or flag gates with uncommitted overrides and revert them all.
- Screenshot every step into `screenshots/NN-<step>.png`. Backend only: call the endpoints and save each request and response.
- A failed step means a fix, then back through the review rounds. Copy results into the PR's Verification section.

VALIDATION: every test-plan step has a pass, a fail or a "Not verified" reason, and every override is reverted.
FALLBACK: after `max_e2e_loops`, stop and report.

=== PHASE 5: REPORT AND QA HANDOFF ===
- Write `report.html` in the run folder: the ask and sources, the stories, what changed per PR, review rounds (fixed and dismissed), tests, the test plan with results, a screenshot grid, Before launch and open questions. Use a clean layout that works in light and dark. Open it.
- If `allow.transition_to_qa`, move each story to `tracker.qa_status` via the tracker's transitions and read it back. If no transition clearly leads there, ask.
- Draft the QA note (stories, PRs, dev deploy tag, preview URL) to the clipboard.
- Post to the notify channel if allowed: the ask, story links, PR links, deploy tag, preview URL, Before launch, open questions and the report path. Send a push notification. Then stop.

VALIDATION: stories show the QA status, and the report opens with every section filled.
FALLBACK: if Slack fails, print the ping in the terminal instead.

=== SELF-REVIEW ===
Score the output (1 to 5):
- Complete: Did every story reach QA with a clean PR, a dev deploy, tested steps and a report?
- Robust: Were claims verified, fallbacks noted and overrides reverted?
- Clean: Are the stories, PR bodies and pings lean and free of invented requirements?
If any score is below 4:
- Identify the specific gap.
- If it is fixable in this run, fix it and re score.
- If not, note it in the report and the ping as a known limitation.

=== LEARNINGS CAPTURE ===
After completing, append one entry to `~/.claude/skills/issue-to-qa/LEARNINGS.md`:

## <YYYY-MM-DD>: <issue key and one line context>
- **What worked:** <approach, tool, or pattern that produced good results>
- **What was awkward:** <step that required backtracking, retrying, or manual fix>
- **Suggested patch:** <one concrete improvement to these skill instructions or the config>
- **Verdict:** [Smooth, Minor friction, Major friction]
