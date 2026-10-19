# Security policy

## What X-RAY contains

The skill in [`skills/x-ray/`](skills/x-ray/SKILL.md) is Markdown only. It ships no scripts, hooks, MCP servers, or `allowed-tools` grants, and the Claude Code plugin declares no components besides the skill. The npm installer, [`bin/cli.js`](bin/cli.js), has no dependencies and only copies `skills/x-ray/` into agent skill folders; it refuses to overwrite a folder that isn't X-RAY unless you pass `--force`. The Python files under `tools/` and `evals/` are for developing and testing this repository; the skill never tells an agent to run them.

Skills run with the permissions of the agent that loads them, so read what you install, and install only from this repository: https://github.com/Skarycloud/x-ray.

## Reporting a problem

If you find something in X-RAY that could lead an agent to act unsafely, such as instructions that weaken the security boundaries in [`references/security-boundaries.md`](skills/x-ray/references/security-boundaries.md), or a supply-chain concern about this repository:

1. Use GitHub's private vulnerability reporting (**Security** tab → **Report a vulnerability**) if it's enabled for this repository.
2. Otherwise, open an issue that says you have a security report, **without** exploit details, and ask for a private contact.

Expect an acknowledgement within a week. This is a small, volunteer-maintained project, so there is no bounty.
