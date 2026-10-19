# AGENTS.md

Guidance for AI agents (and humans) working **on this repository**. To use X-RAY on another codebase, see [SKILL.md](SKILL.md).

## What this repo is

A Markdown-only Agent Skill. The repo root is the skill directory. `SKILL.md` is the product; everything else supports it.

## Rules

- **`SKILL.md` stays concise.** It must stay under 500 lines per the Agent Skills spec (target: well under 200). Put detail in `references/`, linked one level deep from `SKILL.md`.
- **Frontmatter must stay spec-valid**: `name: x-ray` (matches the directory), `description` ≤ 1024 characters and says what *and* when.
- **One source of truth.** Workflow steps live in `SKILL.md`. References expand on a step; they don't redefine it. If you change a step, check the matching reference and template.
- **No unverified claims.** Don't write that X-RAY works on a host, improves results, or beats an alternative unless a recorded test or eval shows it. Mark planned work as planned.
- **Cite, don't copy.** When an idea comes from another project or paper, paraphrase it and add it to the README's Research references. Respect source licenses.
- **No dependencies or frameworks** without a concrete need agreed in an issue.
- **Every mandatory step needs a reason.** Studies of skill-induced failures found excessive procedure (especially repeated verification) to be the main cost skills add. Don't add a required step, check, or template unless an observed failure or eval result calls for it; prefer conditional wording ("when X, do Y").
- **Concrete over motivational.** Reference content should be procedures, decision tables, and examples.

## Checks before finishing a change

1. Run `python tools/validate.py .`. It checks frontmatter, relative links and anchors, and terminology. CI runs it on every push.
2. CI also runs the official `skills-ref validate` ([agentskills/skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)). Locally, pass the folder path from its parent (`skills-ref validate x-ray`); `skills-ref validate .` reports a false directory-name mismatch.
3. If you change the `description`, re-run [evals/trigger-queries.md](evals/trigger-queries.md) on at least one host, or say you didn't.
4. Terminology is consistent: tier names (Lightweight / Integrated / Critical) and evidence states (CONFIRMED / INFERRED / UNKNOWN / CONTRADICTED).
5. Adapter docs cite official sources and a "checked" date.
6. Say which checks you ran and which you didn't.
