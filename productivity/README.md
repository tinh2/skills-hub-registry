# Productivity

Developer experience tooling -- dev containers, linting, git hooks, monorepo setup, release automation, and environment configuration.

## Main Skill

**[dx](dx/)** -- Audits developer experience foundations and generates a DX health report with actionable improvement recommendations. Routes to sub-skills based on gaps found.

## Skills (9)

| Skill | Version | Description |
|-------|---------|-------------|
| [dx](dx/) | 1.0.0 | Main orchestrator. Audit developer experience foundations and generate a DX health report with actionable improvements |
| [devcontainer](devcontainer/) | 1.0.0 | Auto-detect stack and generate a production-grade dev container configuration with Codespaces compatibility |
| [env-setup](env-setup/) | 1.0.0 | Detect required tools, install dependencies, configure environment, and verify the project builds and tests pass |
| [git-hooks](git-hooks/) | 1.0.0 | Auto-detect stack and set up pre-commit and commit-msg hooks with conventional commit enforcement |
| [linter](linter/) | 1.0.0 | Auto-detect stack and configure linting, formatting, and editor integration with auto-fix for existing violations |
| [monorepo](monorepo/) | 1.0.0 | Set up or migrate to a monorepo with workspaces, build pipeline, task graph, and local plus remote caching |
| [release](release/) | 1.0.0 | Set up automated release pipeline with semantic versioning, changelog generation, and publishing |
| [vscode](vscode/) | 1.1.0 | Open VS Code in the current working directory |

## Usage

- Full DX health audit: `/dx`
- Generate dev container config: `/devcontainer`
- Set up environment from zero: `/env-setup`
- Configure git hooks and conventional commits: `/git-hooks`
- Set up linting and formatting: `/linter`
- Set up or migrate to a monorepo: `/monorepo`
- Set up automated release pipeline: `/release`
- Open VS Code: `/vscode`

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [ci-health](ci-health/) | 1.0.0 | Monitor and maintain CI runner health — check disk space, clear stale caches (Flutter, Gradle, npm, Docker), prune old worktrees, and report status. Prevents cache corruption... |
| [daily-standup](daily-standup/) | 1 | >- |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Productivity skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 30 of 30 skills in this folder have a page. You can also [browse the Productivity category on skills-hub.ai](https://skills-hub.ai/browse?category=productivity), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [acp-multi-agent](acp-multi-agent/) | Sets up and orchestrates multi-agent workflows via the Agent Client Protocol (ACP) inside Devin Desktop or any ACP-compatible editor. | [View on skills-hub](https://skills-hub.ai/skills/acp-multi-agent) |
| [ai-spend-optimizer](ai-spend-optimizer/) | Audits your AI coding tool costs across GitHub Copilot, Claude Code, Cursor, Windsurf, and other subscriptions. | [View on skills-hub](https://skills-hub.ai/skills/ai-spend-optimizer) |
| [background-agent-pr-driver](background-agent-pr-driver/) | Configures Claude Code's July 2026 async workflow: background agents that auto-commit, push, and open draft PRs when worktree tasks finish. | [View on skills-hub](https://skills-hub.ai/skills/background-agent-pr-driver) |
| [ci-health](ci-health/) | Monitor and maintain CI runner health — check disk space, clear stale caches (Flutter, Gradle, npm, Docker), prune old worktrees, and... | [View on skills-hub](https://skills-hub.ai/skills/ci-health) |
| [claude-code-hooks-setup](claude-code-hooks-setup/) | Autonomous Claude Code hooks configurator. | [View on skills-hub](https://skills-hub.ai/skills/claude-code-hooks-setup) |
| [claude-model-router](claude-model-router/) | Auto-select the optimal Claude model tier (Haiku 4.5, Sonnet 4.6, or Opus 4.8) for each task based on complexity signals, latency... | [View on skills-hub](https://skills-hub.ai/skills/claude-model-router) |
| [copilot-credits-audit](copilot-credits-audit/) | Audits GitHub Copilot AI Credit usage patterns before the June 2026 flex-billing transition. | [View on skills-hub](https://skills-hub.ai/skills/copilot-credits-audit) |
| [cursor-cloud-agent-workflow](cursor-cloud-agent-workflow/) | Sets up and orchestrates Cursor 3 cloud agent workflows using /in-cloud for isolated VM subagents, /babysit for overnight PR... | [View on skills-hub](https://skills-hub.ai/skills/cursor-cloud-agent-workflow) |
| [cursor-parallel](cursor-parallel/) | Sets up and optimizes parallel task workflows for Cursor Composer 2.5. | [View on skills-hub](https://skills-hub.ai/skills/cursor-parallel) |
| [cursor-seat-optimizer](cursor-seat-optimizer/) | Audits your Cursor Teams usage data and produces a right-sized Standard vs Premium seat assignment plan, saving typical teams 20–40% vs... | [View on skills-hub](https://skills-hub.ai/skills/cursor-seat-optimizer) |
| [daily-standup](daily-standup/) | Cross-repo morning briefing -- recent commits, PR status, CI health, blockers, and suggested priorities for today. | [View on skills-hub](https://skills-hub.ai/skills/daily-standup) |
| [devcontainer](devcontainer/) | Generate a dev container for my project — auto-detect language, framework, and services like PostgreSQL or Redis, create... | [View on skills-hub](https://skills-hub.ai/skills/devcontainer) |
| [dx](dx/) | Audit developer experience and generate a DX health score. | [View on skills-hub](https://skills-hub.ai/skills/dx) |
| [dynamic-skill-loader](dynamic-skill-loader/) | Auto-detects the current project's technology stack and hot-loads context-appropriate skills at session start using Claude Code's... | [View on skills-hub](https://skills-hub.ai/skills/dynamic-skill-loader) |
| [env-setup](env-setup/) | Bootstrap a project from zero to working dev environment. | [View on skills-hub](https://skills-hub.ai/skills/env-setup) |
| [fallback-model-setup](fallback-model-setup/) | Configures Claude Code's fallbackModel chain, --safe-mode troubleshooting protocol, and /cd workspace hygiene for production-resilient... | [View on skills-hub](https://skills-hub.ai/skills/fallback-model-setup) |
| [git-hooks](git-hooks/) | Set up pre-commit hooks for linting, formatting, and type-checking with commit message enforcement using conventional commits. | [View on skills-hub](https://skills-hub.ai/skills/git-hooks) |
| [gpt-5-5-agentic-setup](gpt-5-5-agentic-setup/) | Migrates your agentic coding pipeline to GPT-5.5 — audits the current model config, switches the API endpoint, validates tool-call... | [View on skills-hub](https://skills-hub.ai/skills/gpt-5-5-agentic-setup) |
| [gpt-5-6-tier-routing](gpt-5-6-tier-routing/) | Autonomously selects the right GPT-5.6 tier (Sol / Terra / Luna) for each coding task based on scope, file count, and planning... | [View on skills-hub](https://skills-hub.ai/skills/gpt-5-6-tier-routing) |
| [kiro-quick-plan](kiro-quick-plan/) | Fast single-pass spec-and-execute loop that mirrors Kiro 0.12's Quick Plan Mode. | [View on skills-hub](https://skills-hub.ai/skills/kiro-quick-plan) |
| [linter](linter/) | Configure linting, formatting, and editor integration for any stack. | [View on skills-hub](https://skills-hub.ai/skills/linter) |
| [monorepo](monorepo/) | Set up or migrate to a monorepo with Turborepo, Nx, or pnpm workspaces. | [View on skills-hub](https://skills-hub.ai/skills/monorepo) |
| [plan-to-issues](plan-to-issues/) | Convert a plan, PRD, spec, or roadmap document into tracked GitHub issues with a dependency graph: parses the plan into atomic work... | [View on skills-hub](https://skills-hub.ai/skills/plan-to-issues) |
| [release](release/) | Set up automated releases with semantic versioning, changelog generation, and package publishing. | [View on skills-hub](https://skills-hub.ai/skills/release) |
| [session-handoff](session-handoff/) | Compress the current working session into a handoff document that a fresh session (or another person) can resume from without re-discovery. | [View on skills-hub](https://skills-hub.ai/skills/session-handoff) |
| [session-memory](session-memory/) | Persist, summarize, and reload agent context between sessions — writes a structured session log to CLAUDE.md / AGENTS.md / .hermes.md,... | [View on skills-hub](https://skills-hub.ai/skills/session-memory) |
| [sonnet5-effort-tuner](sonnet5-effort-tuner/) | Audits your active Claude Code sessions and CLAUDE.md projects, then recommends the optimal reasoning effort level (low/medium/high) for... | [View on skills-hub](https://skills-hub.ai/skills/sonnet5-effort-tuner) |
| [terse-mode](terse-mode/) | Install a token-efficiency output contract for the current session and project: writes strict brevity rules into CLAUDE.md (answer-first... | [View on skills-hub](https://skills-hub.ai/skills/terse-mode) |
| [ultracode-effort](ultracode-effort/) | Structured guide for deciding when to invoke Claude Code's ultracode mode, how to run a slice-first pilot, set token budgets, and switch... | [View on skills-hub](https://skills-hub.ai/skills/ultracode-effort) |
| [windsurf-spaces](windsurf-spaces/) | Sets up and manages Windsurf Spaces for multi-agent workflows — discovers project context, creates properly-scoped Space configs, seeds... | [View on skills-hub](https://skills-hub.ai/skills/windsurf-spaces) |
<!-- END GENERATED: skills-hub-index -->
