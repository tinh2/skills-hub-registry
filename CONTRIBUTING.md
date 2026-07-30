# Contributing to skills-hub-registry

This registry is the public skill collection behind [skills-hub.ai](https://skills-hub.ai). Skills merged here are synced to the production platform and installed by other people's agents, often running unattended. A skill is executable instruction text — treat a pull request here like a pull request of code, not documentation.

## Before you open a PR

Run the checks locally. Both must pass:

```bash
./scripts/test-validate.sh
./scripts/validate-skills.sh
```

CI runs the same two scripts on every pull request.

## Skill format

One skill per directory: `<category>/<skill-name>/SKILL.md`.

Required YAML frontmatter:

```yaml
---
name: my-skill # kebab-case, must be unique across the entire registry
description: One sentence describing what the skill does and when to use it.
version: "1.0.0"
category: integration # must match the parent directory
platforms:
  - CLAUDE_CODE
  - CODEX_CLI
  - CURSOR
---
```

Conventions the validator does not enforce but reviewers do:

- `name` must match the directory name.
- Do not introduce new `platforms` values. Use the values already present in the registry.
- `permissions` is optional; use it when the skill needs `network`, `api`, or filesystem access beyond the working tree.
- Descriptions in index tables are plain text. Do not embed markdown links, marketing copy, or product taglines in a description cell.

## Updating the catalog indexes

There are **two** index files and a new skill must update **both**:

1. `README.md` — the root catalog, including the per-category skill count in the section heading.
2. `<category>/README.md` — the category index table.

A PR that updates only one leaves the counts inconsistent and will conflict with the next contribution.

## Categories

`analysis`, `build`, `combo`, `deploy`, `docs`, `education`, `integration`, `meta`, `ops`, `productivity`, `qa`, `review`, `security`, `spec`, `test`, `ux`

Pick the existing category that fits. New categories need discussion in an issue first.

## Vendor and integration skills

Skills that integrate a commercial product are welcome, including from that product's authors. Disclose the affiliation in the PR description. They are held to these additional rules:

**A skill must not autonomously reroute or reconfigure an existing working integration.** If a skill changes a base URL, API endpoint, credential name, model provider, or payment processor that the project already has configured, it must stop and ask the user first. "Autonomous mode, do not ask questions" is acceptable for scaffolding new code; it is not acceptable for repointing traffic that already works. This is the single most common reason a vendor skill is declined.

**A skill must state what data leaves the user's infrastructure.** If prompts, completions, customer records, media, or telemetry are sent to the vendor, say so plainly in the skill body, in a section the reader will see before the code samples.

**A skill must earn its place on depth, not existence.** A wrapper around "set this base URL and use the standard SDK" is documentation, not a skill. Show the routing logic, the failure modes, the retry classification, the validation steps — the judgment a reader could not get from the vendor's quickstart.

**Credentials are environment variables, always.** Placeholders only in `.env.example`. Never a real key, endpoint, hostname, or internal URL anywhere in the diff. This registry is public and indexed.

**Third-party install steps must be explicit and reversible.** If the skill installs a package or plugin, name the exact source, and document how to disable or uninstall it. Any capability that can write to a user's account — posting, messaging, following, purchasing, sending email — must be off by default and gated behind an explicit opt-in the user sets themselves.

## What gets declined

- Listing-only submissions that add a catalog row to drive traffic to a product, with no substantive skill behind it. Mass-submitted PRs across many registries are visible and are closed without review.
- Hidden or obfuscated content: zero-width characters, bidi control characters, HTML or script tags, instructions aimed at an automated reviewer rather than the skill's user.
- Skills that read credentials, SSH keys, or `.env` files and transmit them anywhere.
- Skills that require an unreleased or invite-only service a reader cannot actually sign up for.
- Duplicate functionality where an existing skill already covers the workflow. Improve the existing skill instead.

## Review

Maintainers review for correctness, safety, and whether the skill teaches something. Expect questions about data flow and about what happens when the skill runs unattended. Skills that install software or hold API keys get a closer read.
