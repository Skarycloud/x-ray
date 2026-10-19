# Adapters

X-RAY ships as one portable skill: [`skills/x-ray/`](../skills/x-ray/SKILL.md), which holds `SKILL.md` plus the files it links to. It follows the [Agent Skills specification](https://agentskills.io/specification). Adapters describe how each host discovers and loads that skill. They don't fork the workflow.

## Status at a glance

Docs last checked: **2026-10-19**. Host behavior changes often, so re-check the linked docs before relying on a path.

| Host | Host documents native `SKILL.md` support | X-RAY tested on this host | Adapter |
| --- | --- | --- | --- |
| Claude Code | Yes | **Plugin install, trigger and outcome pilots** | [claude-code.md](claude-code.md) |
| OpenAI Codex | Yes | **No** | [codex.md](codex.md) |
| Cursor | Yes | **No** | [cursor.md](cursor.md) |
| GitHub Copilot | Yes | **No** | [copilot.md](copilot.md) |
| Gemini CLI | Yes | **No** | [gemini-cli.md](gemini-cli.md) |

For hosts where agents don't invoke the skill reliably, see the optional [always-on pointer](always-on-pointer.md).

"Host documents support" means the host's official docs describe loading Agent Skills from a `SKILL.md` directory. It does **not** mean anyone has run X-RAY on that host and confirmed that it triggers and behaves as intended. That validation is planned (see [evals/README.md](../evals/README.md)).

## Shared layout facts

- The skill is the `skills/x-ray/` folder. Copy that folder, not the whole repository; the README, evals, and CI files aren't part of the skill.
- The Agent Skills spec requires the `name` field to match the skill's folder name. Keep the copied folder named `x-ray`.
- The repository is also a Claude Code plugin marketplace (`.claude-plugin/`), following the layout of Anthropic's own skills repository.
- `.agents/skills/` is documented as a project skill location by Codex, Cursor, GitHub Copilot, and Gemini CLI. `.claude/skills/` is documented by Claude Code, Cursor, and GitHub Copilot. No single path is documented by all five hosts as of the date above.

## Validation checklist for a host (to do before marking "tested")

1. Install using only the steps in that host's adapter file.
2. Confirm the host lists the skill (slash menu, `/skills`, settings, or equivalent).
3. Confirm explicit invocation loads `SKILL.md`.
4. Confirm implicit triggering and non-triggering with the queries in [evals/trigger-queries.md](../evals/trigger-queries.md).
5. Confirm the agent can open a linked reference file (for example `skills/x-ray/references/verification.md`).
6. Record host version, OS, date, and results in the adapter file.
