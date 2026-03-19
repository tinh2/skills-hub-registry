---
name: ci-health
description: "Monitor and maintain CI runner health — check disk space, clear stale caches (Flutter, Gradle, npm, Docker), prune old worktrees, and report status. Prevents cache corruption failures."
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are an autonomous CI and development environment health agent. Do NOT ask the user questions.
Inspect the local development environment, identify resource problems, clean caches, and report health status.

============================================================
TARGET: $ARGUMENTS
============================================================

Arguments (all optional):
- `--fix`: Automatically clean caches and prune resources (default: report only).
- `--scope <all|disk|cache|worktree|docker|deps>`: Limit checks to specific areas. Default: `all`.
- `--threshold <percent>`: Disk usage warning threshold. Default: `80`.

If no arguments: run a full health report in read-only mode (no cleanup).

============================================================
PHASE 1: DISK SPACE ASSESSMENT
============================================================

1. Check overall disk usage:
   ```bash
   df -h /
   ```
2. Check home directory usage:
   ```bash
   du -sh $HOME 2>/dev/null
   ```
3. Identify the largest directories under `$HOME`:
   ```bash
   du -sh $HOME/*/ 2>/dev/null | sort -rh | head -20
   ```
4. Flag any filesystem above the threshold (default 80%).

============================================================
PHASE 2: CACHE INVENTORY
============================================================

Scan for common development caches and measure their size. Check each only if it exists:

### Flutter / Dart
- `$HOME/.pub-cache/` — Dart package cache
- `$HOME/.dart-tool/` — Dart tool cache
- `$HOME/.flutter/` or Flutter SDK `bin/cache/` — Flutter cache
- `*/build/` directories inside Flutter projects — build artifacts
- `*/.dart_tool/` directories — per-project Dart tool cache

### Gradle / Android
- `$HOME/.gradle/caches/` — Gradle download cache
- `$HOME/.gradle/wrapper/dists/` — Gradle wrapper distributions
- `$HOME/.android/cache/` — Android SDK cache
- `*/android/.gradle/` — per-project Gradle cache
- `*/build/` directories inside Android projects

### Node / npm / pnpm
- `$HOME/.npm/_cacache/` — npm cache
- `$HOME/.pnpm-store/` — pnpm content-addressable store
- `$HOME/.cache/yarn/` — Yarn cache
- `*/node_modules/` — per-project dependencies (flag if stale)

### Python
- `$HOME/.cache/pip/` — pip download cache
- `*/.venv/` — per-project virtual environments

### Rust
- `$HOME/.cargo/registry/` — Cargo registry cache
- `*/target/` — per-project build artifacts

### Go
- `$HOME/go/pkg/mod/cache/` — Go module cache

### Docker
- Docker images: `docker images --format '{{.Size}}\t{{.Repository}}:{{.Tag}}'`
- Docker volumes: `docker system df`
- Dangling images: `docker images -f "dangling=true"`
- Build cache: `docker builder du`

### System Caches
- `$HOME/.cache/` — XDG cache directory
- `$HOME/Library/Caches/` — macOS application caches (report size only, do not auto-clean)

Build a cache inventory:

| Cache | Path | Size | Last Modified | Stale? |
|-------|------|------|---------------|--------|

A cache is "stale" if it hasn't been modified in 30+ days.

============================================================
PHASE 3: WORKTREE AUDIT
============================================================

For each git repo found under common project directories:

1. List worktrees: `git worktree list`
2. Identify orphaned worktrees (pointing to directories that no longer exist)
3. Identify worktrees for branches that have been merged and deleted from remote
4. Check for worktrees older than 30 days with no recent commits

Build a worktree inventory:

| Repo | Worktree | Branch | Status | Age | Last Commit |
|------|----------|--------|--------|-----|-------------|

Status: ACTIVE / ORPHANED / STALE / MERGED

============================================================
PHASE 4: DEPENDENCY HEALTH
============================================================

For each project found:

1. Check for lockfile freshness (is `package-lock.json` / `pubspec.lock` / `Cargo.lock` up to date?)
2. Check for known vulnerability advisories:
   - Node: `npm audit --json 2>/dev/null`
   - Python: `pip audit 2>/dev/null` (if installed)
   - Rust: `cargo audit 2>/dev/null` (if installed)
3. Count outdated major versions (report only, do not auto-update)

============================================================
PHASE 5: CLEANUP (only if --fix is specified)
============================================================

If `--fix` was NOT specified, skip this phase and present the report with recommendations.

If `--fix` was specified, clean in this order (safest first):

1. **Worktrees:** Remove orphaned and merged worktrees:
   ```bash
   git worktree prune
   git worktree remove <orphaned_path>
   ```

2. **Build artifacts:** Remove `build/`, `target/`, `.dart_tool/` from project directories.

3. **Docker:** Clean dangling images and build cache:
   ```bash
   docker image prune -f
   docker builder prune -f
   ```

4. **Package manager caches:**
   - npm: `npm cache clean --force`
   - Gradle: Remove `$HOME/.gradle/caches/` entries older than 30 days
   - pub: `dart pub cache clean` (if stale)

5. **Stale node_modules:** Remove `node_modules/` from projects not modified in 30+ days.

For each cleanup action, record what was removed and how much space was recovered.

NEVER clean:
- `$HOME/Library/Caches/` (macOS system — can break apps)
- Active worktrees or branches with unmerged work
- Docker containers that are currently running
- Any cache that was modified in the last 7 days (unless disk is critically full >95%)

============================================================
OUTPUT
============================================================

## CI Health Report

### System Overview
- **OS:** {detected OS and version}
- **Disk usage:** {used} / {total} ({percent}%)
- **Status:** {HEALTHY / WARNING / CRITICAL}

### Disk Breakdown

| Location | Size | Notes |
|----------|------|-------|
| Home directory | {size} | |
| Development caches | {total} | See cache inventory |
| Docker | {size} | {N} images, {N} volumes |
| Other | {size} | |

### Cache Inventory

| Cache | Size | Stale? | Recommendation |
|-------|------|--------|----------------|
| {cache name} | {size} | {yes/no} | {keep / clean / review} |

**Total cache size:** {sum}
**Reclaimable space:** {sum of stale/cleanable caches}

### Worktree Status

| Repo | Worktree Count | Orphaned | Stale | Action Needed |
|------|---------------|----------|-------|---------------|

### Dependency Alerts

| Project | Manager | Vulnerabilities | Outdated Major |
|---------|---------|----------------|----------------|

### Cleanup Summary (if --fix was used)

| Action | Space Recovered | Details |
|--------|----------------|---------|
| {action} | {size} | {what was removed} |

**Total space recovered:** {sum}

### Recommendations

Prioritized list of actions to improve environment health:

1. **{action}** — recovers ~{size}, risk: {low/medium}
2. ...

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify disk usage numbers are consistent (parts sum to whole).
3. Verify cleanup actions (if run) actually freed the reported space.
4. If a command failed (permission denied, tool not installed), note it and try alternatives.

IF VALIDATION FAILS:
- Identify which sections are incomplete
- Re-run failed commands with alternative approaches
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what manual steps are needed

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /ci-health — {YYYY-MM-DD}
- Outcome: {SUCCESS | PARTIAL | FAILED}
- Self-healed: {yes — what was healed | no}
- Disk usage: {percent}%
- Space reclaimable: {size}
- Space recovered: {size or "report-only mode"}
- Bottleneck: {phase that struggled or "none"}
- Suggestion: {one-line improvement idea for /evolve, or "none"}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT delete files without explicit `--fix` flag. Default is report-only.
- Do NOT clean macOS system caches (`~/Library/Caches/`).
- Do NOT remove active worktrees or running Docker containers.
- Do NOT auto-update dependencies — only report their status.
- Do NOT hardcode paths, project names, or usernames.
- Do NOT store or log any credentials or secrets found during scanning.
- Do NOT clean caches modified in the last 7 days unless disk is >95% full.
