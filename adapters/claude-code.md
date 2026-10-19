# Claude Code adapter

**Status:** Native skill support documented by the host. **Plugin install tested locally; trigger pilot and a first outcome pilot run (2026-10-19). No demonstrated benefit yet.** See [Test record](#test-record).
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

## Installation

**Plugin (recommended).** Tested 2026-10-19 with a local copy of the marketplace on Claude Code 2.1.131: the marketplace added, the plugin installed and enabled, and the skill registered as `x-ray:x-ray`. Not yet tested from GitHub.

```text
/plugin marketplace add Skarycloud/x-ray
/plugin install x-ray@x-ray
```

The same from a shell: `claude plugin marketplace add Skarycloud/x-ray`, then `claude plugin install x-ray@x-ray`.

**Plain skill (untested).** Get the skill folder first. The skill lives in `skills/x-ray/` inside the repository:

```bash
git clone https://github.com/Skarycloud/x-ray.git
```

```bash
cp -r x-ray/skills/x-ray ~/.claude/skills/            # personal
cp -r x-ray/skills/x-ray <target-repo>/.claude/skills/  # project
```

```powershell
# Windows (PowerShell)
Copy-Item -Recurse x-ray\skills\x-ray "$HOME\.claude\skills\"
```

## Notes

- Claude Code also reads `CLAUDE.md` for project memory. X-RAY doesn't need one. The workflow itself tells the agent to read existing `CLAUDE.md`/`AGENTS.md` files in the target repo.
- Installed as a plugin, the skill is namespaced: invoke it explicitly with `/x-ray:x-ray`. Installed as a plain skill, it is `/x-ray`.

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

### 2026-10-19: plugin install

With `CLAUDE_CONFIG_DIR` pointed at an empty folder: `claude plugin marketplace add <local copy of this repo>` and `claude plugin install x-ray@x-ray` succeeded, the plugin was enabled at version 0.2.0, and a headless session listed the skill as `x-ray:x-ray`. Installing from GitHub (`Skarycloud/x-ray`) isn't tested yet.

### 2026-10-19: outcome pilot

Case [`price-locale-trap`](../evals/cases/price-locale-trap/), 3 runs with the plugin and 3 without. X-RAY was listed in every "with" run but **invoked in none**; the request was phrased as a feature ("Show prices in German format for our German customers"). The baseline found the hidden invoice consumer in every completed run. No difference between arms is measurable. Details: [evals/outcome-harness/README.md](../evals/outcome-harness/README.md#pilot-2026-10-19-claude-code-21131-claude-opus-4-7).
