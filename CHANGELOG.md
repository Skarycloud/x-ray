# Changelog

All notable changes to X-RAY. Versions follow the `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and the skill's frontmatter.

## 0.2.0 — 2026-10-19

### Changed
- **Layout:** the skill moved from the repository root to [`skills/x-ray/`](skills/x-ray/SKILL.md), the layout used by Anthropic's skills repository, Superpowers, Vercel's agent-skills, and OpenAI's portable plugins. Installs now copy only the skill, and a local clone no longer has to be named `x-ray`.
- **Description** rewritten to lead with when to use the skill, in phrases users type.
- **SKILL.md:** added a "Gotchas" table of tempting shortcuts in both directions (skipping steps, overdoing them), an optional progress checklist, a precedence rule (task and repo over skill examples), and a stop rule for verification.

### Added
- **Claude Code plugin** packaging: [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and [`marketplace.json`](.claude-plugin/marketplace.json). Install with `/plugin marketplace add Skarycloud/x-ray`.
- **Eval cases** in the `claude plugin eval` format under [`evals/cases/`](evals/cases/), and a headless [outcome harness](evals/outcome-harness/README.md) for Claude Code versions without `plugin eval`.
- **Trigger queries** and harness; first Claude Code trigger pilot.
- **CI:** repository checks, the official `skills-ref` validator, and `claude plugin validate`.
- **npm installer** `x-ray-skill` ([`bin/cli.js`](bin/cli.js)): `npx x-ray-skill install` copies the skill into the folders each detected agent reads. Not yet published.
- Optional [always-on pointer](adapters/always-on-pointer.md); [Gemini CLI adapter](adapters/gemini-cli.md); [SECURITY.md](SECURITY.md); issue templates.

## 0.1.0 — 2026-10-19

### Added
- First release: the workflow, references, templates, adapters for Claude Code, Codex, Cursor, and GitHub Copilot, and the evaluation method.
