<div align="center">

# X-RAY

**An evidence-based engineering skill for AI coding agents working on existing code.**

Understand the system before changing it. Change only what the task needs. Prove the result with evidence, not confidence.

[![Status: experimental](https://img.shields.io/badge/status-experimental-orange)](#limitations)
[![Version 0.1.0](https://img.shields.io/badge/version-0.1.0-blue)](SKILL.md)
[![Format: Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-6f42c1)](https://agentskills.io/specification)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

> [!IMPORTANT]
> **X-RAY is experimental.** The skill is written, but it hasn't been tested on any host and hasn't been evaluated against a baseline. Nothing in this repository claims it improves agent results. See [Limitations](#limitations) and [Evaluation](#evaluation).

---

## Contents

- [Why X-RAY](#why-x-ray)
- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Usage](#usage)
- [What a run looks like](#what-a-run-looks-like)
- [Design choices driven by published evidence](#design-choices-driven-by-published-evidence)
- [When to use it](#when-to-use-it)
- [Repository layout](#repository-layout)
- [Evaluation](#evaluation)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Research references](#research-references)
- [License](#license)

---

## Why X-RAY

AI coding agents often write plausible code faster than they understand the system they're changing. The failures tend to follow a chain:

1. **Incomplete context.** The agent reads files without reconstructing how they connect.
2. **Wrong assumptions.** It infers behavior from a function name or a stale doc.
3. **A locally plausible change.** The edit looks right in isolation.
4. **An unseen regression.** A caller, data consumer, shared component, or config path breaks elsewhere.
5. **False confidence.** A passing build, or no check at all, gets reported as "fixed".

Other skills already cover planning, TDD, debugging, minimal code, and framework rules well (see [Research references](#research-references)). X-RAY doesn't replace them. Its focus is the part that connects them: **establishing what is true about the existing system, deciding what must not break, and reporting only what was actually verified.**

## How it works

X-RAY is a workflow in [`SKILL.md`](SKILL.md). An agent loads it when a task involves changing existing code.

### 1. Size the task first

Every task is sorted into a risk tier before any investigation. The tier sets how deep every later step goes, in both directions: no shortcuts on risky work, no bureaucracy on trivial work.

| Tier | Typical change | Investigation | Verification |
| --- | --- | --- | --- |
| **Lightweight** | Typo, copy, local style, isolated private function | The touched file and its direct callers | Nearest test or check; read the diff |
| **Integrated** | Feature or fix across modules, shared UI component, new dependency | Callers, data flow, config, and tests for affected paths | Relevant suites, build/typecheck, exercise the changed path |
| **Critical** | Public API, schema, auth, payments, migrations, security fixes | Full impact analysis with recorded evidence | All of the above, plus a regression test per invariant and a rollback note |

The tier depends on **what the change can break, not how small it looks**. A one-line change to an authorization check is Critical.

### 2. Follow ten steps, scaled to the tier

```text
 1. Define the task          goal, checkable acceptance criteria, out of scope
 2. Read the house rules     AGENTS.md / CLAUDE.md / CI config; docs are claims to check
 3. Trace the system         entry point → execution path → callers, data, config, tests
 4. Keep an evidence ledger  label every load-bearing claim (see below)
 5. Write the contract       outcomes that must become true, invariants that must stay true
 6. Choose verification      before editing, so the change can't shape the test
 7. Make the smallest change reuse first; no speculative abstractions or drive-by refactors
 8. Respect the design system tokens, components, states, accessibility, motion
 9. Verify with real results run the checks, read the output, stop when the contract is covered
10. Review and report        read the full diff; report what was and wasn't verified
```

### 3. Separate facts from guesses

Every claim the change depends on gets one of four labels:

| State | Meaning | Required support |
| --- | --- | --- |
| **CONFIRMED** | Observed directly in this session | `file:line`, a command and its output, a test result |
| **INFERRED** | Concluded from evidence, not observed | What it rests on and why the inference holds |
| **UNKNOWN** | Not known, and it matters | How it could be resolved |
| **CONTRADICTED** | Sources disagree (doc vs code, test vs implementation) | Both sources, and which one is trusted and why |

The agent may not present an INFERRED claim as CONFIRMED, and may not build on a load-bearing UNKNOWN.

### 4. Precedence

The user's task comes first, then the target repository's own instructions, versions, and paths, then X-RAY. Examples and templates in this skill are illustrations, never requirements.

## Quick start

> [!NOTE]
> These commands follow each host's official documentation, but **none has been tested with X-RAY yet**. The installed folder **must be named `x-ray`**, because the Agent Skills spec requires the folder name to match the skill's `name` field.

**Claude Code** (personal):

```bash
git clone https://github.com/Skarycloud/x-ray.git ~/.claude/skills/x-ray
```

**OpenAI Codex** (user scope):

```bash
git clone https://github.com/Skarycloud/x-ray.git ~/.agents/skills/x-ray
```

**Cursor** (user scope):

```bash
git clone https://github.com/Skarycloud/x-ray.git ~/.cursor/skills/x-ray
```

**GitHub Copilot** (personal, CLI and local IDE):

```bash
git clone https://github.com/Skarycloud/x-ray.git ~/.copilot/skills/x-ray
```

**Gemini CLI**:

```bash
gemini skills install https://github.com/Skarycloud/x-ray.git
```

Project-scope paths, Windows commands, and the source for each host's behavior are in the adapter files:

| Host | Adapter | Host docs support `SKILL.md` | Tested with X-RAY |
| --- | --- | --- | --- |
| Claude Code | [adapters/claude-code.md](adapters/claude-code.md) | Yes | No |
| OpenAI Codex | [adapters/codex.md](adapters/codex.md) | Yes | No |
| Cursor | [adapters/cursor.md](adapters/cursor.md) | Yes | No |
| GitHub Copilot | [adapters/copilot.md](adapters/copilot.md) | Yes | No |
| Gemini CLI | [adapters/gemini-cli.md](adapters/gemini-cli.md) | Yes | No |

Installing by cloning also brings the README, evals, and adapter docs. Hosts load files other than `SKILL.md` only on demand, so this should be harmless, but it's untested.

## Usage

**Automatic.** Hosts that support Agent Skills read the skill's `description` and load X-RAY when a task matches, for example:

> Fix the 500 error when an order uses a 100% discount code.

> Add an optional `locale` parameter to `formatPrice` without breaking existing callers.

**Explicit.** Invoke it by name where the host supports it: `/x-ray` in Claude Code, `$` or `/skills` in Codex, `/` in Cursor's agent chat.

**Alongside other skills.** If a more specific skill applies (TDD, debugging, a framework guide, a design system), X-RAY tells the agent to use it inside the matching step.

## What a run looks like

A Lightweight change ends with a three-line report (illustrative):

```text
Changed: src/components/Footer.tsx: fixed copyright year typo
Verified: npm test -- Footer → 4 passed, 0 failed
Not verified / risks: none
```

An Integrated or Critical change records its reasoning as it goes. This trace comes from the illustrative example in [references/reverse-engineering.md](references/reverse-engineering.md); it isn't output from a recorded run.

```text
Anchor: "discount" + 500 on POST /orders
Entry: src/routes/orders.ts:42 createOrder handler            CONFIRMED
Path:  createOrder → pricing.applyDiscount (src/pricing.ts:88)
       → payments.charge (src/payments/stripe.ts:31)            CONFIRMED
Cause: charge() called with amount 0; provider rejects 0-amount
       charges, error is uncaught → 500                         CONFIRMED (reproduced locally)
Consumers of applyDiscount: createOrder, previewCart,
       invoice export job                                       CONFIRMED (rg)
Unknown: does the finance export expect a payment record for
       every order?                                             UNKNOWN → ask
```

Full report formats: [templates/VERIFICATION_REPORT.md](templates/VERIFICATION_REPORT.md).

## Design choices driven by published evidence

Recent studies of agent skills shaped several rules. These choices follow from the studies' findings; whether they help X-RAY specifically is untested.

| Finding | X-RAY response |
| --- | --- |
| Most public software-engineering skills produced no pass-rate gain, and a few reduced it, attributed to guidance that conflicted with the project's own context (SWE-Skills-Bench) | Precedence rule: the task and target repo override the skill's examples and templates. The repo's code wins over its docs. |
| The largest source of skill-induced efficiency loss was excessive procedure, led by excessive verification (Dong et al.) | An explicit stop rule for verification; templates only when the work doesn't fit in a few lines; tiers bound depth in both directions. |
| Skills often turned checklists and recipes into mandatory work, and agents changed environments to satisfy them (Dong et al.) | Examples are labeled illustrative; "don't change the environment to make a check pass" is a rule. |
| Focused skills with a few modules outperformed exhaustive bundles (SkillsBench) | A short core workflow (about 120 lines); detail lives in references loaded only when a step needs it. |
| Build evaluations before extensive documentation (Anthropic skill-authoring guidance) | **Not yet followed:** X-RAY was written before its evals. Building them is the top roadmap item. |

## When to use it

| Good fit | Poor fit |
| --- | --- |
| Bug fixes in unfamiliar code | Greenfield prototypes with no existing behavior to preserve |
| Features that touch shared modules or public interfaces | Throwaway scripts |
| Refactors where behavior must stay identical | Pure research or writing tasks |
| UI changes inside an established design system | |
| Changes to data, auth, payments, or migrations (Critical tier) | |

### Principles

- Understand before changing.
- Distinguish confirmed facts from assumptions.
- Trace dependencies and assess change impact.
- Preserve important existing behavior.
- Avoid unnecessary abstractions and dependencies.
- Treat design quality and functional correctness as engineering requirements.
- Verify actual results rather than trusting generated code.
- Report uncertainty and limitations honestly.
- Scale investigation and verification to the risk of the change.

## Repository layout

The repository root **is** the skill folder. `SKILL.md` is the product; everything else supports it.

```text
x-ray/
├── SKILL.md                         The skill: the authoritative, portable workflow
├── references/                      Detailed procedures, loaded on demand
│   ├── reverse-engineering.md       Tracing entry points, call paths, consumers, tests
│   ├── evidence-ledger.md           Evidence states, entry format, durable ledger
│   ├── invariant-contracts.md       Writing outcomes and invariants before editing
│   ├── change-impact-analysis.md    Finding consumers, rating blast radius, safe-change patterns
│   ├── verification.md              Choosing checks by tier, running them honestly, when to stop
│   ├── design-engineering.md        Tokens, states, accessibility, responsiveness, motion
│   └── security-boundaries.md       Permissions, untrusted content, secrets, unsafe actions
├── templates/                       Optional formats, each with a short form
│   ├── SYSTEM_MAP.md
│   ├── CHANGE_PLAN.md
│   └── VERIFICATION_REPORT.md
├── adapters/                        Per-host install and discovery notes, with sources
├── evals/                           Evaluation method and scoring rubric (no results yet)
├── AGENTS.md                        Rules for agents and humans editing this repo
└── CONTRIBUTING.md
```

## Evaluation

X-RAY's claim to usefulness has to come from measurement, not from how well its instructions read. The method is defined in [evals/README.md](evals/README.md):

- **Paired runs.** The same model, host, prompt, and repository snapshot, with and without X-RAY, at least 5 runs per condition.
- **Hidden tests.** Acceptance tests for the task, plus regression tests for behavior the task never mentions.
- **Metrics** ([scoring-rubric.md](evals/scoring-rubric.md)): task success, regressions, patch quality, visual correctness, evidence accuracy (how often the final report claims something false), calibration, procedure overhead, and cost.
- **Tasks chosen to expose harm too:** trivial changes where X-RAY should add no overhead, and tasks where the repo's requirements conflict with the skill's examples.
- **Negative results get published.** A "no gain" result is realistic: in SWE-Skills-Bench, most public software-engineering skills showed none.

**Current status:** the method exists. No tasks, fixtures, or results exist yet.

## Limitations

- **Untested on hosts.** Triggering and behavior on Claude Code, Codex, Cursor, Copilot, and Gemini CLI haven't been checked.
- **Unevaluated.** There's no evidence yet that X-RAY improves outcomes over a baseline.
- **Process skills often don't help.** In SWE-Skills-Bench, 39 of 49 public software-engineering skills produced no pass-rate gain. X-RAY is a process skill and may land in that group; only the evals can tell.
- **Instruction-only.** X-RAY can't force an agent to follow it. Compliance depends on the model and host.
- **Cost.** Investigation and verification cost time and tokens. Tiering and the stop rule are meant to keep trivial tasks cheap; whether they do is unmeasured.
- **No tooling.** No scripts, linters, or CI checks ship with the skill yet.

## Roadmap

Planned, not implemented:

1. **Host validation.** Run the checklist in [adapters/README.md](adapters/README.md) on each host and record the results.
2. **Evaluation v1** (highest priority, since the skill was written before its evals). Start with 3–5 tasks: a trivial change, stale documentation, and a repo requirement that conflicts with the skill's examples. Then grow to about 20 validated tasks, run baseline vs X-RAY, and publish raw results, including negative ones.
3. **Repository checks.** CI for Markdown links, `SKILL.md` frontmatter validation, and length limits.
4. **Packaging.** A slim release containing only skill files; possibly a Claude Code plugin.
5. **Revision from evidence.** Cut or change steps the evals show to be ineffective or costly.

## Contributing

The most useful contributions are **evidence**: host test reports, evaluation tasks with hidden tests, and documented cases where an agent following X-RAY did something wrong or wasteful. See [CONTRIBUTING.md](CONTRIBUTING.md), and read [AGENTS.md](AGENTS.md) before editing: its rules apply to human contributors too.

## Research references

These works informed X-RAY's design. They're cited for attribution. None of them endorses X-RAY, and no text has been copied from them.

<details>
<summary><strong>Skill format and existing skills</strong></summary>

- Agent Skills specification. https://agentskills.io/specification. Skill format, frontmatter rules, progressive disclosure.
- Anthropic. *Skill authoring best practices.* https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices. Conciseness, one-level references, evaluation-driven development.
- Anthropic, *anthropics/skills*. https://github.com/anthropics/skills. Example skills and template structure.
- Jesse Vincent / Prime Radiant, *obra/superpowers* (MIT). https://github.com/obra/superpowers. Its verification-before-completion, test-driven-development, and systematic-debugging skills cover adjacent ground; X-RAY is meant to work alongside them.
- Vercel Labs, *vercel-labs/agent-skills* (MIT). https://github.com/vercel-labs/agent-skills. Focused, domain-specific skills that X-RAY should defer to when they apply.
- *Ponytail* (MIT). https://github.com/DietrichGebert/ponytail. Its "reuse before writing" ladder informed the reuse order in `SKILL.md` step 7 (paraphrased), including the rule that validation, data-loss handling, security, and accessibility are never cut.

</details>

<details>
<summary><strong>Research on agent skills</strong></summary>

- Li et al. *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks.* arXiv:2602.12670, 2026. Paired with/without-skill evaluation; focused skills outperformed exhaustive bundles.
- Han et al. *SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?* arXiv:2603.15401, 2026. Most SWE skills showed no gain; harm traced to guidance conflicting with project context.
- Dong et al. *Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents.* arXiv:2608.11888, 2026. Failure taxonomy; excessive verification and procedure as the main efficiency regressions.
- Hong, Imani, Ahmed. *From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills.* arXiv:2607.01456, 2026. Authoring best-practice violations are near-universal in real skills.

</details>

<details>
<summary><strong>Research on coding agents</strong></summary>

- Jimenez et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. arXiv:2310.06770.
- Zhang et al. *RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation.* EMNLP 2023. arXiv:2303.12570. Repository context matters; motivates task-scoped tracing.
- Yang et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* NeurIPS 2024. arXiv:2405.15793.
- Xia et al. *Agentless: Demystifying LLM-based Software Engineering Agents.* arXiv:2407.01489, 2024. Localize, repair, validate as a strong simple baseline.
- Aider polyglot benchmark. https://aider.chat/docs/leaderboards/. Exercism exercises in six languages, scored by executable tests.

</details>

<details>
<summary><strong>Software engineering and industry research</strong></summary>

- Winters, Manshreck, Wright. *Software Engineering at Google.* O'Reilly, 2020. Hyrum's Law (consumers depend on observable behavior), which underpins the invariant and impact-analysis steps.
- Ousterhout. *A Philosophy of Software Design.* Yaknyam Press, 2018. Complexity as the core cost; caution against shallow, speculative abstractions.
- Hermans. *The Programmer's Brain.* Manning, 2021. How developers read and build models of unfamiliar code; informs the reverse-engineering procedure.
- DORA. *State of AI-assisted Software Development 2025.* Google, 2025. https://dora.dev/research/ai. Finds AI amplifies an organization's existing strengths and weaknesses; X-RAY therefore makes no general productivity claim.

</details>

<details>
<summary><strong>Design and accessibility</strong></summary>

- Emil Kowalski's writing on UI and animation. https://emilkowal.ski. Purposeful, fast, interruptible motion; informs the motion guidance in `references/design-engineering.md`.
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2.* https://www.w3.org/TR/WCAG22/.

</details>

## License

[MIT](LICENSE) © 2026 Sumanth Kumar
