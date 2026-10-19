# GitHub Copilot adapter

**Status:** Native skill support documented by the host. **X-RAY not yet tested on any Copilot surface.**
**Sources** (checked 2026-10-19):
- [GitHub Docs: Creating agent skills for Copilot](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-skills)
- [Microsoft Learn: Copilot agent skills in Visual Studio](https://learn.microsoft.com/visualstudio/ide/copilot-agent-skills)

## What the host documents

GitHub Docs list agent-skill support for Copilot cloud agent, Copilot code review, Copilot CLI, the GitHub Copilot app, and agent mode in VS Code.

| Scope | Paths (GitHub Docs) |
| --- | --- |
| Project | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` |
| Personal | `~/.copilot/skills/` or `~/.agents/skills/` |

The Microsoft Learn page for Visual Studio also lists `~/.claude/skills/` as a personal location.

Frontmatter: `name` (required, lowercase with hyphens, typically matching the directory) and `description` (required). `license` and `allowed-tools` are optional.

Activation: in agent mode, Copilot decides when a skill is relevant and loads it.

## Intended installation (untested)

```bash
# Project scope (works for repo-based surfaces such as cloud agent)
git clone https://github.com/Skarycloud/x-ray.git .github/skills/x-ray

# Personal scope (CLI / local IDE)
git clone https://github.com/Skarycloud/x-ray.git ~/.copilot/skills/x-ray
```

Cloning a repo inside another repo creates a nested Git repository. For a committed project install, copy the files or use a submodule instead.

## Notes

- Copilot also supports repository instructions (`.github/copilot-instructions.md`), and GitHub's changelog says the coding agent reads `AGENTS.md` ([changelog](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions)). X-RAY relies on skills, not those files.
- The `gh skill` command mentioned in GitHub Docs was in public preview when checked; this adapter doesn't depend on it.

## Test record

_None yet._
