---
name: parallax-verify
description: "Verifies your product against its Parallax obligation ledger with evidence instead of self-report: re-runs each acceptance check, captures your app's flows and screenshots, checks parity behavior flow by flow, scans the repo for anything copied from the target, and reports coverage with every 'verified' tied to a fresh evidence item. Uses REA coverage/verification and screenshot tools when installed. Triggers: 'how close is my version', 'verify parity', 'is it ready', 'check the obligations', 'did we copy anything', 'parallax verify'."
version: "1.0.0"
category: test
platforms:
  - CLAUDE_CODE
tags: [verification, parity, coverage, clean-room, screenshots, parallax]
---

# Parallax Verify

A row is `verified` only when a check ran in this session and produced an
evidence item you can point to. "I built it" is `built`, not `verified`.

Requires `parallax/gate.md` (PASS*) and `parallax/obligations.csv`. Writes `parallax/verify.md` and
`parallax/evidence/V0NN-*`.

## Step 1: run the acceptance checks

For each open or built obligation, run its `verify_method` against YOUR app
(local or a preview deploy):

- **e2e / flow**: drive the flow (REA `capture_browser_scenario`, Playwright,
  or by hand) and save the capture as a V-id. Compare the observed steps to
  the study's flow: same job done, step count, error handling, persistence.
  Fewer steps than the target is a pass and worth noting.
- **screenshot**: capture each state at 390 and 1440 wide (REA
  `capture_web_screenshot` or your browser tool). Check that every state in
  the obligation exists. Do not chase pixel similarity with the target: your
  brand differs on purpose, and resemblance in look is a legal risk, not a
  goal.
- **perf / a11y / unit**: run the tool, save the output.

Fill `evidence_of_done` with the V-id, set `verified` or record the failure.

## Step 2: regressions with pixel diffs (your app only)

REA `compare_web_screenshots` gives exact changed-pixel ratios between two PNGs.
Use it for your app today vs your app at the last verify run. It is not a
meaningful parity score against the target and is not used as one.

## Step 3: clean-room scan

Prove the legal rows:

- grep the repo for the target's name, product names, domains, CDN hosts and
  distinctive strings noted in the study (case-insensitive)
- no file in the repo whose hash matches any evidence item or raw capture
- no asset fetched from the target's domains at runtime (check your app's own
  network capture)
- no long verbatim UI strings from the study's screenshots (spot-check the
  core flow's labels and empty states)
- `parallax/evidence/raw/` is gitignored and not in history

Any hit fails the legal obligation until fixed.

## Step 4 (optional, Tier A): REA coverage and verification

If the spec built a formal REA ledger, `evaluate_reconstruction_coverage`
reports coverage against a named boundary and `verify_reconstruction` checks
a typed behavioral spec against an evidence bundle. Both are strict: missing,
stale or weak evidence comes back unknown, not pass. Report their verdicts as
given; never upgrade an unknown to a pass. For a second release of the target,
`compare_application_versions` / `compare_web_captures` show what changed, so
you can add new obligations.

## Step 5: report

`parallax/verify.md`:

- coverage: verified / total per kind (parity, differentiator, quality, legal),
  must-have parity verified x of y
- failing and unverified rows, worst first, with what to do
- open unknowns that touch shipped behavior
- clean-room scan result
- a ship verdict: **Ready** only if all must-haves and all legal rows are
  verified; otherwise **Not ready** with the blocking O-ids

Credit: inspired by replica-diff and replica-test in the Replica pack by Jake
Schincariol (MIT). Independent text.
