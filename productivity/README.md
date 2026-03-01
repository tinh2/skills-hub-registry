# Productivity

Developer experience tooling -- dev containers, linting, git hooks, monorepo setup, release automation, and environment configuration.

## Main Skill

**[dx](dx/)** -- Audits developer experience foundations and generates a DX health report with actionable improvement recommendations. Routes to sub-skills based on gaps found.

## Skills (8)

| Skill | Version | Description |
|-------|---------|-------------|
| [dx](dx/) | 1.0.0 | Main orchestrator. Audit developer experience foundations and generate a DX health report with actionable improvements |
| [devcontainer](devcontainer/) | 1.0.0 | Auto-detect stack and generate a production-grade dev container configuration with Codespaces compatibility |
| [env-setup](env-setup/) | 1.0.0 | Detect required tools, install dependencies, configure environment, and verify the project builds and tests pass |
| [git-hooks](git-hooks/) | 1.0.0 | Auto-detect stack and set up pre-commit and commit-msg hooks with conventional commit enforcement |
| [linter](linter/) | 1.0.0 | Auto-detect stack and configure linting, formatting, and editor integration with auto-fix for existing violations |
| [monorepo](monorepo/) | 1.0.0 | Set up or migrate to a monorepo with workspaces, build pipeline, task graph, and local plus remote caching |
| [release](release/) | 1.0.0 | Set up automated release pipeline with semantic versioning, changelog generation, and publishing |
| [vscode](vscode/) | 1.0.0 | Open VS Code in the current working directory |

## Usage

- Full DX health audit: `/dx`
- Generate dev container config: `/devcontainer`
- Set up environment from zero: `/env-setup`
- Configure git hooks and conventional commits: `/git-hooks`
- Set up linting and formatting: `/linter`
- Set up or migrate to a monorepo: `/monorepo`
- Set up automated release pipeline: `/release`
- Open VS Code: `/vscode`
