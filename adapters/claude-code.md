# Claude Code adapter

**Status:** Native skill support documented by the host. **Trigger pilot run (2026-10-19): the skill loads when it should. Behavior after loading is not yet tested.** See [Test record](#test-record).
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

### 2026-10-19: trigger pilot

- **Setup:** Claude Code 2.1.131, model `claude-opus-4-7`, Windows 11. X-RAY installed as a project skill in a small fake TypeScript shop repo. About 40 unrelated personal skills were also installed, as on a real machine.
- **Method:** the 20 [trigger queries](../evals/trigger-queries.md), **1 run each** (the method calls for 3), headless and read-only, capped at 3 turns. Harness: [evals/trigger-harness/](../evals/trigger-harness/README.md).
- **What this tests:** only whether the skill loads. Not whether the agent then follows it, and not whether results improve.

| Condition | Should trigger | Should not trigger |
| --- | --- | --- |
| Skill only | **10/10** triggered | **0/10** triggered |
| Skill + [always-on pointer](always-on-pointer.md) | **10/10** triggered | **1/10** triggered (N1) |

Observations:
- **No invocation gap on this setup.** Unlike Vercel's January 2026 result, the skill loaded on every matching request without the pointer. Different model, host version, and tasks; this doesn't contradict their result elsewhere.
- **The pointer changed timing, not hit rate.** With the skill alone, T8 and T9 loaded X-RAY only after a couple of exploration calls. With the pointer, all ten loaded it first.
- **The pointer's one extra trigger was N1** ("scaffold a new Next.js app"). The agent noticed the directory already held a project, and loaded X-RAY before risking overwriting it. That is defensible in this fixture, but it is still an extra trigger on a should-not query.
- **N6 ("review this PR for security issues") loaded the host's `security-review` skill**, not X-RAY, in both conditions. That's the intended outcome.
- **Cost:** $5.82 for all 40 runs.

Caveats: one run per query, one model, one tiny fixture, and the 3-turn cap (T8 and T9 triggered on the third call, so a later trigger would have been missed). Treat this as a pilot, not a measurement.
