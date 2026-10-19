# Cursor adapter

**Status:** Native skill support documented by the host. **X-RAY not yet tested on Cursor.**
**Source:** [Cursor docs: Agent Skills](https://cursor.com/docs/skills) (checked 2026-10-19)

## What the host documents

| Scope | Paths |
| --- | --- |
| Project | `.agents/skills/`, `.cursor/skills/` |
| User | `~/.agents/skills/`, `~/.cursor/skills/` |
| Compatibility | `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, `~/.codex/skills/` |

Cursor searches skill roots recursively. Nested skill folders inside a repo are scoped to their directory.

Frontmatter: `name` (required, must match folder name) and `description` (required). Optional fields include `paths`, `disable-model-invocation`, and `metadata`.

Invocation:
- **Automatic**: the agent applies the skill when it judges it relevant.
- **Manual**: type `/` in Agent chat and select the skill.

## Intended installation (untested)

Get the skill folder first. The skill lives in `skills/x-ray/` inside the repository:

```bash
git clone https://github.com/Skarycloud/x-ray.git
```

```bash
cp -r x-ray/skills/x-ray ~/.cursor/skills/              # user scope (or ~/.agents/skills/)
cp -r x-ray/skills/x-ray <target-repo>/.cursor/skills/  # project scope
```

## Notes

- A third-party guide reported that Agent Skills were Nightly-only at one point. The official docs page shows no such restriction. Confirm on your Cursor version.
- Before native skills, Cursor projects used rules (`.cursor/rules`). X-RAY doesn't ship a rule file; a rule that points the agent to `SKILL.md` would be a fallback for older Cursor versions, but it isn't written or tested.

## Test record

_None yet._
