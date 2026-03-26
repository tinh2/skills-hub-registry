# Quickstart Skill — Design Spec

**Date:** 2026-03-26
**Status:** Approved
**Scope:** 1 new skill — zero-to-power-user machine setup for skills-hub

## Problem

New users need to install multiple prerequisites (Homebrew, Node.js, Claude Code, skills-hub CLI) and configure MCP servers before they can use skills. This friction slows adoption. There is no single skill that takes a fresh machine and makes it fully ready.

## Design Principles

- **Fully autonomous** — no questions asked, detect everything
- **Cross-platform** — macOS, Linux, Windows (WSL)
- **Idempotent** — safe to re-run; skips anything already installed/configured
- **Project-aware** — recommends and installs skills based on the user's actual project

## Skill Overview

| Skill | Category | Purpose |
|-------|----------|---------|
| `quickstart` | education | Detect OS, install prerequisites, authenticate, configure Claude Code + MCP, install recommended skills |

## Phase 1: OS Detection & Package Manager

Detect the operating system and ensure a package manager is available.

### Detection Logic
- **macOS**: check `uname -s` = Darwin
  - Install Homebrew if `brew` is not found
  - Verify Xcode Command Line Tools (`xcode-select -p`)
- **Linux**: check `uname -s` = Linux
  - Detect distro from `/etc/os-release`
  - Use existing package manager: `apt` (Debian/Ubuntu), `dnf` (Fedora/RHEL), `pacman` (Arch)
- **Windows**: check for WSL via `uname -r` containing "microsoft" or "WSL"
  - If running inside WSL: treat as Linux (use apt)
  - If not in WSL: report that WSL is required and provide install command: `wsl --install`
  - Cannot proceed on native Windows without WSL

### Baseline Tools
Ensure these are installed regardless of OS:
- `git`
- `curl`

## Phase 2: Runtime Prerequisites

Install or verify Node.js (LTS) and Python 3.

### Node.js
- Check `node --version` — if missing or below v18, install:
  - **macOS**: `brew install node`
  - **Debian/Ubuntu**: install via NodeSource LTS repository
  - **Fedora/RHEL**: `dnf install nodejs`
  - **Arch**: `pacman -S nodejs npm`
- Verify `npx --version` works after installation

### Python 3
- Check `python3 --version` — if missing, install:
  - **macOS**: `brew install python3`
  - **Debian/Ubuntu**: `apt install python3`
  - **Fedora/RHEL**: `dnf install python3`
  - **Arch**: `pacman -S python`
- Python is needed by some MCP servers and tools

## Phase 3: Claude Code Setup

Install and authenticate the Claude Code CLI.

### Installation
- Check if `claude` command exists
- If not: `npm install -g @anthropic-ai/claude-code`
- Verify `claude --version`

### Authentication
- Run `claude auth status` or equivalent to check if authenticated
- If not authenticated: this is the ONE interactive step — tell the user to run `claude auth` and wait for completion
- Verify authentication succeeded

## Phase 4: Skills-Hub CLI Authentication

Install and authenticate the skills-hub CLI.

### Installation
- `npx @skills-hub-ai/cli --version` to check if accessible
- If not cached: npx will auto-download on first use

### Authentication
- Run `npx @skills-hub-ai/cli whoami` to check auth status
- If not authenticated: run `npx @skills-hub-ai/cli login`
- Verify with `whoami` after login

## Phase 5: MCP Server Configuration

Detect which MCP servers would be useful and install them.

### Always Install
- **skills-hub**: `claude mcp add skills-hub -- npx @skills-hub-ai/mcp`

### Project-Conditional
Scan the working directory for signals:

| Signal | MCP Server | Install Command |
|--------|-----------|-----------------|
| Any web project (package.json with react/next/vue/svelte) | Playwright | `claude mcp add playwright -- npx @playwright/mcp@latest` |
| `.figma` references, Figma URLs in docs/code | Figma | `claude mcp add figma -- npx figma-mcp` |
| Google Drive references, `.gdoc` files | Google Drive | Guide through Google Drive MCP setup |
| Stitch references, `stitch-designs/` dir | Stitch | `claude mcp add stitch -- npx @_davideast/stitch-mcp proxy` |

### Verification
- Run `claude mcp list` and confirm each added server shows as connected
- If any fail to connect, log the error and continue (don't block setup)

## Phase 6: Project-Aware Skill Installation

Scan the current project and install recommended skills.

### Project Detection
Use the same detection logic as the `getting-started` skill — scan for manifest files:
- `package.json` → Node.js/TypeScript
- `pubspec.yaml` → Flutter/Dart
- `requirements.txt` / `pyproject.toml` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `build.gradle.kts` → Kotlin/Android
- `*.xcodeproj` / `Package.swift` → Swift/iOS
- No project files → install general-purpose skills only

### Skill Bundles by Project Type

**Always (any project):**
- `cleanup-sprint` — codebase cleanup
- `broken-links` — link validation
- `preflight` — pre-deploy checks
- `security-review` — security audit
- `recall` — dev timeline analysis

**Flutter/Dart:**
- `flutter` — Flutter development
- `design-build` — UI building
- `design-audit` — accessibility/quality
- `unit-test` — test generation
- `e2e` — end-to-end testing
- `store-screenshots` — app store assets

**React/Next.js/Vue/Svelte (web frontend):**
- `design-build` — UI building
- `design-audit` — accessibility/quality
- `design-to-code` — Figma to code
- `unit-test` — test generation
- `e2e` — end-to-end testing
- `web-quality-performance` — performance optimization

**API/Backend (Express, Fastify, Django, Flask, Rails, Go, Rust):**
- `security-review` — security audit
- `unit-test` — test generation
- `api-review` — API design review
- `arch-review` — architecture review

**Python (data science/ML):**
- `unit-test` — test generation
- `security-review` — security audit

**Mobile (iOS/Android native):**
- `unit-test` — test generation
- `design-audit` — accessibility/quality
- `security-review` — security audit

### Installation
- Install each skill via `npx @skills-hub-ai/cli install <slug>`
- After all installs: `npx @skills-hub-ai/cli sync --all` to sync to any other detected AI tools (Cursor, Codex, etc.)

## Phase 7: Verification & Summary

### Health Checks
1. `npx @skills-hub-ai/cli list` — confirm all skills installed
2. `claude mcp list` — confirm MCP servers connected
3. Run project build command if detectable (`npm run build`, `flutter build`, etc.) — optional, skip if no obvious build command

### Output Format

```
## Quickstart Complete

**OS**: {os} {version} ({package manager})
**Node.js**: v{version} (npx verified)
**Python**: v{version}
**Claude Code**: v{version} (authenticated as {email})
**Skills-Hub CLI**: authenticated as {username}

### MCP Servers
| Server | Status |
|--------|--------|
| skills-hub | connected |
| playwright | connected |

### Skills Installed ({count})
| Skill | Category | Why |
|-------|----------|-----|
| {name} | {category} | {reason} |

### Quick Commands
- /{skill} — {one-line description}
- /{skill} — {one-line description}

### What's Next
- Run `/getting-started` for a guided tour of skills for your project
- Run `/design-build` to build your first UI screen
- Run `/stitch-pipeline` to improve existing designs with Google Stitch
- Visit https://skills-hub.ai to browse all {count}+ skills
```

## Self-Healing

Each phase has built-in retry logic:
- Package installation failures: retry once, then log and continue
- Network failures (npm, brew): check connectivity, suggest proxy settings if needed
- Authentication failures: provide clear manual steps as fallback
- MCP connection failures: log and continue (non-blocking)

Maximum 3 retry attempts per phase. If a phase fails after retries, log the failure and continue to the next phase — partial setup is better than no setup.

## Idempotency

Every step checks before acting:
- `brew --version` before installing Homebrew
- `node --version` before installing Node
- `claude --version` before installing Claude Code
- `whoami` before running login
- `claude mcp list` before adding MCP servers
- `npx @skills-hub-ai/cli list` before installing skills

Re-running the skill on an already-configured machine should complete in seconds with "already installed" for every step.

## Out of Scope

- IDE-specific configuration (VS Code extensions, JetBrains plugins)
- Cloud provider setup (AWS, GCP, Azure credentials)
- Docker installation
- Database setup
- Project-specific environment variables (.env files) — that's what `env-setup` handles
