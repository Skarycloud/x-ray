# Gemini CLI adapter

**Status:** Native skill support documented by the host. **X-RAY not yet tested on Gemini CLI.**
**Sources** (checked 2026-10-19):
- [Gemini CLI docs: Agent Skills](https://geminicli.com/docs/cli/skills/)
- [Gemini CLI docs: Creating Agent Skills](https://geminicli.com/docs/cli/creating-skills/)

## What the host documents

Discovery tiers, lowest to highest precedence:

| Tier | Path |
| --- | --- |
| Built-in | Bundled with Gemini CLI |
| Extension | Skills bundled in installed extensions |
| User | `~/.gemini/skills/` or the `~/.agents/skills/` alias |
| Workspace | `.gemini/skills/` or the `.agents/skills/` alias |

On a name collision, the higher tier wins. Within the user or workspace tier, `.agents/skills/` takes precedence over `.gemini/skills/`.

Activation: at session start, Gemini CLI adds each enabled skill's `name` and `description` to the system prompt. When a task matches, the model calls the `activate_skill` tool and the user sees a consent prompt. On approval, the `SKILL.md` body loads and the skill directory becomes readable.

Commands: `/skills list`, `/skills link <path>`, `/skills enable|disable <name>`, `/skills reload`; from the terminal, `gemini skills install <git-url-or-path>` and `gemini skills list --all`.

## Intended installation (untested)

```bash
# User scope, straight from GitHub (--path points at the skill inside the repo)
gemini skills install https://github.com/Skarycloud/x-ray.git --path skills/x-ray

# Workspace scope, from a local clone
gemini skills install ./x-ray/skills/x-ray --scope workspace
```

## Notes

- The consent prompt means X-RAY never loads silently on this host. That affects the implicit-trigger check in the [validation checklist](README.md#validation-checklist-for-a-host-to-do-before-marking-tested): record whether the prompt appeared, not only whether the skill ran.
- Gemini CLI also reads `GEMINI.md` context files. X-RAY doesn't ship one; the workflow tells the agent to read whatever instruction files the target repo has.

## Test record

_None yet._
