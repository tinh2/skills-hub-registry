---
name: parallax-ship
description: "Pre-launch gate for a product built with Parallax: re-checks the legal gate, runs a brand rename sweep (name, logo, colours, copy, domains, metadata) so nothing can be confused with the original, checks the trademark and domain for your new name, and writes honest comparison and launch copy grounded in verified obligations and real user pain. Refuses to ship while parallax-verify says Not ready. Triggers: 'name my version', 'rebrand before launch', 'ready to launch my clone', 'write the landing page vs X', 'parallax ship'."
version: "1.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
tags: [launch, branding, trademark, positioning, clean-room, parallax]
---

# Parallax Ship

Requires `parallax/verify.md` with verdict Ready. If it says Not ready, list the
blocking O-ids and stop.

## Step 1: re-run the gate

Re-read the target's terms (date changed? new clauses?) and update
`parallax/gate.md`. A new conflict blocks launch until resolved.

## Step 2: name and identity

Propose 5 original names. For each, check and record: trademark search in the
launch markets (USPTO TESS/EUIPO or local office) for the relevant classes,
domain availability, app-store name collisions, and distance from the target's
name (no puns, misspellings or shared distinctive words). Build your own
logo, palette and type; do not start from the target's.

## Step 3: rename sweep

Search the repo, build output and store metadata for the placeholder and the
target's name, product names, domains and colours (case-insensitive, including
package names, bundle IDs, manifest, meta tags, OG images, favicons, emails,
error pages, seed data, test fixtures and commit-visible docs). Fix every hit
except factual comparison text you intend to keep (Step 4). Re-run
parallax-verify's clean-room scan and record the result.

## Step 4: honest launch copy

- Claims come only from `verified` obligations. A differentiator that is not
  verified is not advertised.
- Comparisons with the target name it only factually ("an alternative to X",
  "imports from X"), dated, with no use of its logo and a line saying you are
  not affiliated. Comparative claims about the target must be supportable from
  evidence (an E-id) or its own public docs.
- Positioning comes from pain.md's angle. Reviewer quotes are never used as
  testimonials.

## Step 5: write `parallax/ship.md`

Gate re-check date, chosen name and its checks, rename sweep hits (before /
after), clean-room scan result, launch claims each mapped to an O-id, and
anything still open. Deploying is your normal workflow; smoke a preview of
every route before production.

Credit: inspired by replica-brand and replica-launch in the Replica pack by
Jake Schincariol (MIT). Independent text.
