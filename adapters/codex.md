# OpenAI Codex adapter

**Status:** Native skill support documented by the host. **X-RAY not yet tested on Codex.**
**Source:** [Codex docs: Agent Skills](https://developers.openai.com/codex/skills), which redirected to `learn.chatgpt.com/docs/build-skills` when checked on 2026-10-19.

## What the host documents

Codex loads skills from directories containing a `SKILL.md` with required `name` and `description` frontmatter:

| Scope | Path |
| --- | --- |
| Repository | `.agents/skills/` in each directory from the current working directory up to the repository root |
| User | `$HOME/.agents/skills/` |
| Admin | `/etc/codex/skills/` |
| System | Bundled with Codex |

Invocation:
- **Explicit**: run `/skills`, or type `$` to mention a skill, in the Codex CLI or IDE extension.
- **Implicit**: Codex selects a skill when the task matches its `description`.

Optional `agents/openai.yaml` can set UI metadata and invocation policy. X-RAY doesn't ship one.

> Some older third-party guides and an earlier skill-creator sample refer to `~/.codex/skills` (or `$CODEX_HOME/skills`). The current official page lists `$HOME/.agents/skills` for user scope. Follow the official page.

## Intended installation (untested)

```bash
# User scope
git clone https://github.com/Skarycloud/x-ray.git ~/.agents/skills/x-ray

# Repository scope (from the target repo root)
git clone https://github.com/Skarycloud/x-ray.git .agents/skills/x-ray
```

## Notes

- Codex also reads `AGENTS.md` files from the Codex home directory and from each directory between the project root and the working directory ([Codex docs: AGENTS.md](https://developers.openai.com/codex/guides/agents-md), which redirected to `learn.chatgpt.com/docs/agent-configuration/agents-md` when checked). X-RAY's own [`AGENTS.md`](../AGENTS.md) is for contributors to X-RAY, not for target repos.

## Test record

_None yet._
