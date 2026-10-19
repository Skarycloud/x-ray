# Evaluation methodology

> **Status: methodology, three eval cases, and two pilots.** A [trigger pilot](trigger-harness/README.md) on Claude Code measured whether the skill loads; a first [outcome pilot](outcome-harness/README.md) with and without X-RAY was inconclusive. Nothing in this repository claims X-RAY improves agent performance. This document defines how that claim would be tested.

## Question

On realistic changes to existing codebases, does an agent with X-RAY loaded:
1. complete the task at least as often as the same agent without it,
2. introduce fewer regressions,
3. produce smaller, more focused patches,
4. report its evidence and uncertainty more accurately,
5. at an acceptable extra cost in time and tokens?

A "no" or "mixed" answer is a valid result and will be published as such.

## Design: paired baseline comparison

Each task runs under two conditions that differ **only** in whether X-RAY is available:

| Condition | Setup |
| --- | --- |
| **Baseline** | Host agent, default configuration, no X-RAY |
| **X-RAY** | Same agent, same model, same settings, with X-RAY installed per its adapter |

Hold constant: model and version, host and version, temperature/effort settings, tool permissions, task prompt (verbatim), repository snapshot, time and token budgets, other installed skills (ideally none).

Run each (task, condition) pair **at least 5 times**, because agent runs are nondeterministic. Report the distribution, not only the mean.

Optional third condition: **X-RAY + [always-on pointer](../adapters/always-on-pointer.md)**, to test whether invocation, not content, is the bottleneck.

Optional fourth condition: **X-RAY + another skill set** (for example obra/superpowers) to test complementarity, not replacement.

## Task set

Cases use the format of Claude Code's official [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals), so any contributor can run them with one command. The plugin manifest points that command at [`evals/cases/`](cases/):

```text
evals/cases/<case>/
├── prompt.md        # frontmatter: max_turns, allowed_tools; body: the request, verbatim
├── case.yaml        # name, tags, expected_outcome, context.scaffold_script
├── fixture.sh       # builds the starting repository in an empty workspace
└── graders/*.md     # regex over files, tool_used, and llm rubrics; one file per check
```

Current cases:

| Case | Tier | What it tests |
| --- | --- | --- |
| [`price-locale-trap`](cases/price-locale-trap/) | Integrated | A shared helper with a hidden consumer: the invoice code parses `formatPrice`'s output. Graders: default format kept, outcome rubric, no claims of unrun checks |
| [`footer-year`](cases/footer-year/) | Lightweight | Overhead on a trivial copy change |
| [`general-question`](cases/general-question/) | n/a | Must not trigger X-RAY |

Run them (Claude Code v2.1.269 or later; fixtures need `--scaffold`, and edits need `Edit` and `Write` granted):

```bash
claude plugin eval . --scaffold --allow-tools Edit Write --runs 3
```

That runs each case with and without the plugin and reports the difference (`Δ`). For older Claude Code versions, the [outcome harness](outcome-harness/README.md) runs the same cases headlessly and grades them deterministically.

Target mix for a first version (about 20 cases):

| Category | Purpose |
| --- | --- |
| Bug fix with a misleading surface symptom | Tests tracing a dependency across files to the root cause |
| Feature touching a shared module | Tests consumer impact analysis (a second route or caller regresses if missed) |
| Feature an existing component already supports | Tests reuse over duplication |
| Stale or contradicted documentation | Tests CONTRADICTED handling |
| Tempting over-engineering opportunity | Tests smallest-change discipline |
| UI change in an established design system | Tests token reuse, states, responsiveness, a11y |
| Small change to a permission or auth check | Tests tiering by risk rather than diff size, and permission enforcement |
| Ambiguous request with a load-bearing unknown | Tests asking vs assuming (the correct outcome is a question) |
| Trivial change | Tests that X-RAY doesn't add overhead where it isn't needed |
| Task that pins a path, version, or format the skill's examples don't match | Tests that task and repo requirements override skill guidance |
| Prompt-injection text in repo content | Tests security boundaries |

Prefer small real-world repositories with permissive licenses, or tasks adapted from public benchmarks (for example SWE-bench instances) where their licenses allow. Record the source of every task.

Each case must be validated before use: on the untouched fixture the outcome graders fail and the invariant graders pass, and a reference solution passes both. (The `price-locale-trap` grader was checked this way, including against a deliberately broken solution.)

## Metrics

Full definitions and scoring scales are in [scoring-rubric.md](scoring-rubric.md).

| Metric | Measured by | Automated? |
| --- | --- | --- |
| Task success | Outcome graders (acceptance criteria) pass | Yes |
| Regressions | Invariant graders (behavior the task never mentions) that fail after the change | Yes |
| Patch quality | Diff size, files touched outside expected set, new deps, rubric score | Partly |
| Visual correctness | Screenshot diff at listed viewports + rubric review | Partly |
| Evidence accuracy | Claims in the agent's final report checked against reality | Manual / assisted |
| Calibration | Whether stated confidence matches what was actually checked | Manual / assisted |
| Procedure overhead | Repeated verification, unneeded exploration, template output the tier didn't need | Partly |
| Execution cost | Wall time, input/output tokens, tool calls, monetary cost if available | Yes |

## Procedure

1. Freeze versions (model, host, X-RAY commit) and record them.
2. For each task × condition × run: reset repo, start a fresh agent session, give `task.md`, stop at agent completion or budget limit.
3. Save: full transcript, final diff, agent's final report, cost metrics.
4. Run the graders; capture screenshots for visual tasks.
5. Score rubric items **blind to condition** where possible (strip skill-specific wording, such as "CONFIRMED", from reports before human review, or have a second rater check).
6. Compare paired results per task; report per-category and overall.

## Reporting

- Publish per-task raw results, not only aggregates.
- Report the number of runs, variance, and any excluded runs with the reason.
- Report cases where X-RAY made things **worse**.
- State threats to validity: small task set, task-author bias (the X-RAY authors wrote the tasks), single model or host, rater subjectivity.

## Prior work this methodology draws on

- **SWE-bench**: real GitHub issues verified by hidden tests (Jimenez et al., 2024). Model for outcome graders.
- **Agentless** (Xia et al., 2024): shows simple localization → repair → validation pipelines are a strong baseline; motivates measuring cost, not just success.
- **SWE-agent** (Yang et al., 2024): shows the agent–computer interface strongly affects results; motivates holding host and tool settings constant.
- **SkillsBench** (Li et al., 2026) and **SWE-Skills-Bench** (Han et al., 2026): paired with-skill / without-skill runs against deterministic verifiers. SWE-Skills-Bench found most public software-engineering skills produced no pass-rate gain and a few reduced it, so a null or negative result for X-RAY is a realistic outcome, not an edge case.
- **Agent Skills Can Be Harmful** (Dong et al., 2026): taxonomy of skill-induced failures; source of the procedure-overhead codes in the rubric.
- **Aider polyglot benchmark**: code-editing exercises scored by executable tests; an example of a small, reproducible harness.

Full citations: [README.md#research-references](../README.md#research-references).
