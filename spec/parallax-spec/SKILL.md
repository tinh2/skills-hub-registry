---
name: parallax-spec
description: "Turns a Parallax study into an original product spec and a build plan expressed as an obligation ledger: every obligation (parity, differentiator, quality, legal) has an owner, a source E-id or pain item, a testable acceptance check and a verification method, and nothing unknown is silently assumed. Optionally emits REA's formal reconstruction obligation ledger. Triggers: 'write the spec for my version of X', 'build plan from the study', 'obligation ledger', 'what do I need to build', 'parallax spec'."
version: "1.0.0"
category: generate
platforms:
  - CLAUDE_CODE
tags: [spec, build-plan, obligations, clean-room, parallax]
---

# Parallax Spec

The clean-room boundary lives here. Evidence goes in; an original spec in your
own words comes out; the build team (you, in a later step) works from the spec
and the ledger, not from the target.

Requires `parallax/gate.md` (PASS*) and `parallax/study.md`. Uses
`parallax/pain.md` when present.

## Step 1: decide scope

From the study's feature list and pain.md: the core loop, the must-haves, the
differentiators, and an explicit **won't build** list. Critical unknowns that
touch the core loop either get probed now (back to parallax-study) or become a
design decision you own ("we choose X; target behavior unknown, U07").

## Step 2: write the spec in your own words

`parallax/spec.md`: your product's name placeholder (final name comes in
parallax-ship), its screens, flows, data model and rules. Write it from the
*behaviors* in study.md, then improve: your data model is designed for your
product, not mirrored field by field from observed responses. No copied
labels, text, colours, icons or layouts treated as templates. Each section
lists the E-ids or P-ids it satisfies.

## Step 3: the obligation ledger

`parallax/obligations.csv`:

```
id,kind,statement,source,acceptance_check,verify_method,owner,status,evidence_of_done
O001,parity,"User can create a project from the empty state",F01;E012,"e2e: new user creates project in <=3 actions",e2e+screenshot,build,open,
O014,differentiator,"Import 10k-row CSV < 5s",P02,"perf test median < 5s",perf-test,build,open,
O030,quality,"All screens usable at 390px and keyboard-only",spec,"a11y + viewport run",a11y,build,open,
O040,legal,"No asset, copy or code from target in repo",gate,"parallax-verify clean-room scan passes",scan,ship,open,
```

Rules:

- `kind` is parity, differentiator, quality or legal. Always include the legal
  rows (clean-room scan, rename sweep, privacy redaction, ToS re-check).
- Every parity row cites a study E-id or flow; every differentiator a P-id.
- `acceptance_check` must be something a test or capture can decide. "Feels
  fast" is not one.
- `status` is open, built, verified, or waived (with reason). Only
  parallax-verify sets `verified`.
- Unknown target behavior is never a parity obligation; it is a decision row
  citing its U-id.

## Step 4 (optional, Tier A): formal REA ledger

If REA MCP is connected and the study exported an evidence bundle, you can pass
that bundle, the reviewed obligations and a manifest of the reconstruction to
`build_reconstruction_obligation_ledger`. It fails closed on missing owners,
contradictions, unenumerated claims and residual unknowns. Treat its failures
as gaps in the CSV to fix. Its schema is strict; if you cannot satisfy it, keep
the CSV as the source of truth and say so. Do not claim a formal ledger exists
when it did not build.

## Step 5: the build plan

Order obligations into milestones: shell, core loop as a vertical slice, the
remaining must-haves, differentiators, quality, legal. One commit per
obligation group; commit messages reference O-ids. Building uses your normal
workflow; when a builder needs to know how something behaves, they read the
spec or ask for a new probe, never open the target's code or screenshots as a
template.

Hand-off summary: counts by kind, open critical unknowns, milestone list.

Credit: inspired by replica-architect and replica-build in the Replica pack by
Jake Schincariol (MIT). Independent text.
