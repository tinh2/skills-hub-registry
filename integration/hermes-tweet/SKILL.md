---
name: hermes-tweet
description: Install and operate the Hermes Tweet plugin for Hermes Agent X/Twitter explore, read, and explicitly gated action workflows.
version: 1.0.0
category: integration
platforms:
  - CLAUDE_CODE
  - CODEX_CLI
  - CURSOR
permissions:
  - network
  - api
---

# Hermes Tweet

Use Hermes Tweet when a Hermes Agent user needs X/Twitter research, social listening, account reads, trend checks, monitor setup, or tightly controlled posting from a native Hermes plugin.

Source: https://github.com/Xquik-dev/hermes-tweet

## Install

Prefer the native Hermes plugin installer:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
hermes plugins list
hermes tools list
```

If the Git installer is unavailable, install the PyPI package into the Hermes Agent virtual environment:

```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python hermes-tweet
hermes plugins enable hermes-tweet
hermes tools list
```

## Configuration

- `tweet_explore` is available without network access or an API key.
- `tweet_read` requires `XQUIK_API_KEY`.
- `tweet_action` requires `XQUIK_API_KEY` and `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Keep `HERMES_TWEET_ENABLE_ACTIONS=false` for public research, public monitoring, support triage, and unattended sessions that do not require private or action-only routes.
- Enable actions only for sessions where the user explicitly asks to post, reply, send DMs, follow, run private reads, manage webhooks, manage monitors, run extraction jobs, draw giveaways, or change media.

If `XQUIK_API_KEY` is added to `~/.hermes/.env` during an active Hermes CLI session, run `/reload` before using `tweet_read`.

## Operating Procedure

1. Run `tweet_explore` first to find the exact endpoint and required arguments.
2. Use `tweet_read` for catalog-listed read-only routes.
3. Use `tweet_action` only after confirming the request is private, write-like, or otherwise action-only, and action gating is enabled.
4. Do not call private or write-like routes through `tweet_read`.
5. Do not enable actions for cron or gateway jobs unless the workflow requires private reads or action-only operations.

## Smoke Test

```bash
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Expected behavior:

- Without `XQUIK_API_KEY`, Hermes exposes `tweet_explore` only.
- With `XQUIK_API_KEY`, `tweet_read` can call `/api/v1/account`.
- `tweet_action` stays unavailable or disabled unless `HERMES_TWEET_ENABLE_ACTIONS=true`.

## References

- Repository guide: https://github.com/Xquik-dev/hermes-tweet#readme
- PyPI package: https://pypi.org/project/hermes-tweet/
- Hermes plugins guide: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/
- Build a Hermes plugin: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin/
