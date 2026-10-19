# Always-on pointer (optional, experimental)

**Status:** Untested. Whether this helps X-RAY is an open question for the [evals](../evals/README.md).

## Why this exists

Skills load only when the agent decides to invoke them, and agents often don't. In Vercel's Next.js evals (January 2026), the agent never invoked the available skill in 56% of cases, and the skill scored the same as having no docs at all. An explicit pointer in an always-loaded file raised invocation, but the wording mattered: "You MUST invoke the skill" made agents anchor on the skill and miss project context, while "explore the project first, then invoke the skill" worked better.

Always-loaded files have a cost too. An ETH Zurich study of `AGENTS.md`-style context files found they did not generally improve task success and raised inference cost by over 20% on average. So the pointer below is deliberately tiny, and it adds a reminder, not the workflow.

## The pointer

Paste this into the target repository's always-loaded instruction file: `AGENTS.md` (Codex, Cursor, Copilot), `CLAUDE.md` (Claude Code), or `GEMINI.md` (Gemini CLI). It assumes X-RAY is already installed as a skill.

```markdown
## Changing existing code
Before editing existing code, explore the relevant files first. Then use the `x-ray` skill:
size the change by what it could break, check claims against the code, and report only
what you actually verified. Skip it for trivial edits where nothing else can break.
```

## When not to use it

- The repository already has a long instruction file. Adding more always-loaded text is the pattern the ETH study found costly.
- Agents on your host already invoke X-RAY reliably. Check with the trigger queries in [evals/trigger-queries.md](../evals/trigger-queries.md) first.

## Sources (checked 2026-10-19)

- Vercel, *AGENTS.md outperforms skills in our agent evals*, 2026-01-27. https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* arXiv:2602.11988, 2026.
