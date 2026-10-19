# Claude Code adapter

**Status:** Native skill support documented by the host. **X-RAY not yet tested on Claude Code.**
**Source:** [Claude Code docs: Skills](https://code.claude.com/docs/en/skills) (checked 2026-10-19)

## What the host documents

Claude Code loads skills from directories containing a `SKILL.md`:

| Scope | Path |
| --- | --- |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` |
| Project | `.claude/skills/<skill-name>/SKILL.md` (loaded from the starting directory and each parent up to the repo root) |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md`, invoked as `/plugin-name:skill-name` |

Invocation:
- **Automatic**: Claude matches the request against the skill's `description` and loads the skill when relevant.
- **Manual**: type `/x-ray`.

Frontmatter: Claude Code reads `name` and `description`. It documents `license` and `metadata`, both used by X-RAY, as informational fields it doesn't act on.

## Intended installation (untested)

Personal install:

```bash
# macOS / Linux
git clone https://github.com/Skarycloud/x-ray.git ~/.claude/skills/x-ray
```

```powershell
# Windows (PowerShell)
git clone https://github.com/Skarycloud/x-ray.git "$HOME\.claude\skills\x-ray"
```

Project install: place the skill at `.claude/skills/x-ray/` in the target repository.

## Notes

- Claude Code also reads `CLAUDE.md` for project memory. X-RAY doesn't need one. The workflow itself tells the agent to read existing `CLAUDE.md`/`AGENTS.md` files in the target repo.
- Packaging as a Claude Code plugin is a possible later step; it isn't implemented.

## Test record

_None yet._
