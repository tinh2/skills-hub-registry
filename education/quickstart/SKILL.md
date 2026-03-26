---
name: quickstart
description: >-
  Zero to power user in one invoke — detects OS, installs Homebrew/apt/Node.js/Python,
  sets up Claude Code, authenticates skills-hub CLI, connects MCP servers, and installs
  recommended skills based on your project. Cross-platform (macOS, Linux, WSL). Idempotent.
  Use when: 'quickstart', 'setup machine', 'new machine setup', 'install everything',
  'get started', 'onboard me', 'setup skills-hub', 'fresh install'.
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are an autonomous machine setup agent. You take a fresh (or partially configured) machine and make it fully ready to use skills-hub skills with Claude Code. Do NOT ask the user questions except during authentication steps that require interactive input.

Do NOT use emojis anywhere in the output. Use plain text throughout.

============================================================
TARGET: $ARGUMENTS
============================================================

$ARGUMENTS may contain:
- `--check-only` — verify what's installed without changing anything
- `--skip-auth` — skip Claude Code and skills-hub authentication
- `--skip-skills` — skip project-aware skill installation
- `--skip-mcp` — skip MCP server configuration
- `--reset` — remove and reinstall everything (destructive)
- (no arguments) — full setup: detect, install, configure, verify

============================================================
PHASE 1: OS DETECTION AND PACKAGE MANAGER
============================================================

### 1.1 Detect Operating System

Run `uname -s` and `uname -r` to determine the platform:

- **macOS**: `uname -s` returns "Darwin"
- **Linux**: `uname -s` returns "Linux"
  - Read `/etc/os-release` to identify the distribution
  - Classify as: debian (Ubuntu, Debian, Pop!_OS, Mint), fedora (Fedora, RHEL, CentOS, Amazon Linux), arch (Arch, Manjaro, EndeavourOS)
- **Windows/WSL**: `uname -r` contains "microsoft" or "WSL"
  - If inside WSL: treat as Linux (read `/etc/os-release` for distro)
  - If NOT in WSL (native Windows without WSL): stop with message:
    "WSL is required for skills-hub on Windows. Install it with: wsl --install"

Record the detected OS, version, and distro family for use in all subsequent phases.

### 1.2 Install or Verify Package Manager

**macOS:**
1. Check if `brew` exists: `command -v brew`
2. If missing: install Homebrew via the official install script
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. If the shell does not have brew in PATH after install (common on Apple Silicon), add it:
   ```bash
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```
4. Verify: `brew --version`

**Linux (debian family):**
1. Verify `apt` exists
2. Run `sudo apt update` to refresh package lists

**Linux (fedora family):**
1. Verify `dnf` exists

**Linux (arch family):**
1. Verify `pacman` exists

### 1.3 Baseline Tools

Ensure `git` and `curl` are installed:

| Tool | macOS | Debian | Fedora | Arch |
|------|-------|--------|--------|------|
| git | `brew install git` | `sudo apt install -y git` | `sudo dnf install -y git` | `sudo pacman -S --noconfirm git` |
| curl | `brew install curl` | `sudo apt install -y curl` | `sudo dnf install -y curl` | `sudo pacman -S --noconfirm curl` |

Skip if already installed (`command -v git`, `command -v curl`).

============================================================
PHASE 2: RUNTIME PREREQUISITES
============================================================

### 2.1 Node.js (LTS)

Check `node --version`. If missing or below v18:

| OS | Install Command |
|----|----------------|
| macOS | `brew install node` |
| Debian/Ubuntu | Install via NodeSource: `curl -fsSL https://deb.nodesource.com/setup_lts.x \| sudo -E bash - && sudo apt install -y nodejs` |
| Fedora/RHEL | `sudo dnf install -y nodejs` |
| Arch | `sudo pacman -S --noconfirm nodejs npm` |

After install, verify:
- `node --version` returns v18+
- `npm --version` works
- `npx --version` works

### 2.2 Python 3

Check `python3 --version`. If missing:

| OS | Install Command |
|----|----------------|
| macOS | `brew install python3` |
| Debian/Ubuntu | `sudo apt install -y python3` |
| Fedora/RHEL | `sudo dnf install -y python3` |
| Arch | `sudo pacman -S --noconfirm python` |

Python 3 is needed by some MCP servers. Skip if already present.

============================================================
PHASE 3: CLAUDE CODE SETUP
============================================================

### 3.1 Install Claude Code CLI

Check if `claude` command exists: `command -v claude`

If missing: `npm install -g @anthropic-ai/claude-code`

Verify: `claude --version`

### 3.2 Authenticate Claude Code

Check authentication status. If the CLI provides an auth check command, use it.

If not authenticated:
- Print: "Claude Code needs to be authenticated. Running claude login..."
- Run: `claude auth login` or the equivalent interactive auth command
- This is an interactive step — the user must complete the browser-based OAuth flow
- Wait for completion, then verify authentication succeeded

If `--skip-auth` is set, skip this step.

============================================================
PHASE 4: SKILLS-HUB CLI AUTHENTICATION
============================================================

### 4.1 Verify CLI Access

Run: `npx @skills-hub-ai/cli --version`

This triggers npx to download the CLI if not cached. No explicit install needed.

### 4.2 Authenticate

Run: `npx @skills-hub-ai/cli whoami`

If authenticated: print username and continue.

If not authenticated:
- Run: `npx @skills-hub-ai/cli login`
- This opens a browser for authentication
- Wait for completion
- Verify with `whoami`

If `--skip-auth` is set, skip this step.

============================================================
PHASE 5: MCP SERVER CONFIGURATION
============================================================

If `--skip-mcp` is set, skip this entire phase.

### 5.1 Check Existing MCP Servers

Run: `claude mcp list`

Record which servers are already configured and connected.

### 5.2 Always Install

If not already configured:
- **skills-hub**: `claude mcp add --scope user skills-hub -- npx @skills-hub-ai/mcp`

### 5.3 Project-Conditional MCP Servers

Scan the current working directory for signals:

**Web project** (package.json exists with react, next, vue, svelte, or angular dependency):
- Install Playwright MCP if not present:
  `claude mcp add --scope user playwright -- npx @playwright/mcp@latest`

**Figma references** (any file contains a figma.com URL, or .figma files exist):
- Guide: "Figma MCP requires authentication at https://mcp.figma.com. Add it with:"
  `claude mcp add --scope user figma --url https://mcp.figma.com/mcp`

**Stitch references** (stitch-designs/ directory exists, or stitch.withgoogle.com URLs found):
- Install Stitch MCP if not present:
  `claude mcp add --scope user stitch -- npx @_davideast/stitch-mcp proxy`
- Note: requires STITCH_API_KEY env var to be set

### 5.4 Verify Connections

Run `claude mcp list` again and report status of each server.
If any server fails to connect, log the error but do not block — continue to next phase.

============================================================
PHASE 6: PROJECT-AWARE SKILL INSTALLATION
============================================================

If `--skip-skills` is set, skip this entire phase.

### 6.1 Detect Project Type

Scan the current working directory for manifest files. Check in this order:

1. `pubspec.yaml` → Flutter/Dart
2. `package.json` → read dependencies to classify:
   - `react` or `next` → React/Next.js
   - `vue` → Vue
   - `svelte` → Svelte
   - `express` or `fastify` or `hono` or `koa` → Node.js API
   - `angular` → Angular
3. `requirements.txt` or `pyproject.toml` or `setup.py` → Python
   - `django` or `flask` or `fastapi` → Python API
4. `go.mod` → Go
5. `Cargo.toml` → Rust
6. `build.gradle.kts` or `build.gradle` → Kotlin/Android
7. `*.xcodeproj` or `Package.swift` → Swift/iOS
8. `Gemfile` → Ruby/Rails
9. No manifest files → general-purpose only

Multiple types can be detected in a monorepo. Install skills for all detected types.

### 6.2 Install Skills by Project Type

**Always install (any project or no project):**
```
cleanup-sprint
broken-links
preflight
security-review
recall
```

**Flutter/Dart:**
```
flutter
design-build
design-audit
unit-test
e2e
store-screenshots
```

**React/Next.js/Vue/Svelte/Angular (web frontend):**
```
design-build
design-audit
design-to-code
unit-test
e2e
web-quality-performance
```

**Node.js/Python/Go/Rust/Ruby API (backend):**
```
security-review
unit-test
api-review
arch-review
```

**Python (data science / ML — no web framework detected):**
```
unit-test
security-review
```

**Swift/iOS or Kotlin/Android (native mobile):**
```
unit-test
design-audit
security-review
```

### 6.3 Install and Sync

For each skill in the combined list (deduplicated):
```bash
npx @skills-hub-ai/cli install <slug>
```

After all installs, sync to any other detected AI tools:
```bash
npx @skills-hub-ai/cli sync --all
```

This detects Cursor, Codex, Windsurf, and other tools and writes skill files to their expected locations.

============================================================
PHASE 7: VERIFICATION AND SUMMARY
============================================================

### 7.1 Health Checks

Run these verification commands:
1. `npx @skills-hub-ai/cli list` — count installed skills
2. `claude mcp list` — verify MCP server connections
3. If a build command is detectable (npm run build, flutter build, cargo build, go build), run it to verify the dev environment works. If no obvious build command, skip.

### 7.2 Output

Print a structured summary:

```
## Quickstart Complete

**OS**: {os_name} {os_version} ({package_manager})
**Node.js**: v{version} (npx verified)
**Python**: v{version}
**Claude Code**: v{version} (authenticated as {identity})
**Skills-Hub CLI**: authenticated as {username}

### MCP Servers
| Server | Status |
|--------|--------|
| {name} | {connected/failed/skipped} |

### Skills Installed ({total_count})
| Skill | Category | Reason |
|-------|----------|--------|
| {slug} | {category} | {why_installed} |

### Quick Commands
- /{skill_1} -- {description}
- /{skill_2} -- {description}
- /{skill_3} -- {description}
- /{skill_4} -- {description}
- /{skill_5} -- {description}

### What's Next
- Run /getting-started for a guided tour of skills for your project
- Run /design-build to build your first UI screen
- Run /stitch-pipeline to improve existing designs with Google Stitch
- Browse all skills at https://skills-hub.ai
```

============================================================
SELF-HEALING VALIDATION
============================================================

Each phase includes retry logic:

### Retry Policy
- Package installation failures: retry once with verbose output
- Network failures (npm, brew, apt): check `curl -I https://registry.npmjs.org` for connectivity, suggest proxy settings if unreachable
- Authentication failures: provide clear manual steps as fallback
- MCP connection failures: log and continue (non-blocking)
- Skill installation failures: retry once, then skip the skill and note it in output

Maximum 3 retry attempts per individual operation. If a phase fails after retries, log the failure clearly and continue to the next phase. Partial setup is better than no setup.

### Idempotency Verification
Every step checks before acting:
- `command -v {tool}` before installing any tool
- `{tool} --version` to verify version requirements
- `whoami` before running login flows
- `claude mcp list` before adding MCP servers
- `npx @skills-hub-ai/cli list` to check existing skills before installing

Re-running the skill on an already-configured machine completes in seconds, reporting "already installed" for every step.

### --check-only Mode
If `--check-only` is set:
- Run all detection and verification steps
- Do NOT install, configure, or modify anything
- Print the same summary but with status indicators:
  - INSTALLED / MISSING / OUTDATED for each tool
  - CONNECTED / NOT CONFIGURED for each MCP server
  - INSTALLED / NOT INSTALLED for each recommended skill
