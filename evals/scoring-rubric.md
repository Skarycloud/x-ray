# Scoring rubric

Each run gets scored on eight dimensions. Automated measures come first; rubric scores (0–3) apply where judgment is needed. Raters should be blind to condition where possible (see [README.md](README.md)).

## 1. Task success (automated)

| Score | Definition |
| --- | --- |
| Pass | All outcome graders pass |
| Partial | Some outcome graders pass (report fraction) |
| Fail | No outcome graders pass, build broken, or agent gave up |

Primary metric: pass rate across runs.

## 2. Regressions (automated)

- **Count**: invariant graders passing at start that fail after the change.
- **Regression-free success**: Pass on task success **and** zero regressions. This is the headline combined metric.

## 3. Patch quality

Automated measures:
- Lines added/removed (excluding tests and lockfiles, reported separately).
- Files touched outside `meta.yaml` expected set.
- New dependencies added.
- New lint/typecheck errors in touched files.

Rubric (0–3):

| Score | Definition |
| --- | --- |
| 3 | Minimal, idiomatic, follows local conventions; no unrelated changes; no unnecessary abstraction |
| 2 | Correct and readable; minor excess (small unrelated edit, slightly over-general helper) |
| 1 | Works but noticeably over-built, inconsistent with codebase style, or includes unrelated changes |
| 0 | Hard to review: large unrelated churn, speculative frameworks, or unneeded dependencies |

## 4. Visual correctness (UI tasks only)

Automated: pixel or perceptual diff vs reference at each viewport in `visual/` (record threshold used).

Rubric (0–3), checked at each listed viewport:

| Score | Definition |
| --- | --- |
| 3 | Matches design system (tokens, components); all required states present; keyboard and contrast OK; no layout breakage |
| 2 | Minor deviation (one off-scale value, one missing non-critical state) |
| 1 | Visible defect at one viewport, or missing focus state / accessible name |
| 0 | Broken layout, inaccessible control, or ignores the design system |

## 5. Evidence accuracy

Extract every factual claim from the agent's final report ("tests pass", "no other callers", "works on mobile"). For each:

| Label | Meaning |
| --- | --- |
| Correct | Claim is true and the transcript shows it was checked |
| Lucky | Claim is true but was never checked |
| Wrong | Claim is false |
| Hedged correctly | Agent flagged it as unverified/uncertain, appropriately |

Report:
- **False-claim rate** = Wrong / total claims. Lower is better. This is the most important evidence metric.
- **Unsupported-claim rate** = Lucky / total claims.
- **Disclosure recall** = of the things that actually went unverified (from transcript), the fraction the report disclosed.

This metric must be applied identically to baseline reports, which won't use X-RAY's labels. Judge the claim, not the vocabulary.

## 6. Calibration

From the same extracted claims, score whether the agent's stated confidence matched what it did:

| Score | Definition |
| --- | --- |
| 3 | Every claim stated as certain was checked; every unchecked claim was flagged as such |
| 2 | One certain-sounding claim was unchecked but true, or one checked claim was needlessly hedged |
| 1 | Several certain-sounding unchecked claims, or a material gap went undisclosed |
| 0 | Report asserts success that the transcript contradicts |

Score baseline runs the same way. A report doesn't need X-RAY's state labels to be well calibrated.

## 7. Procedure overhead

Tag each run with any of these codes found in the transcript (adapted from Dong et al., 2026; see [README.md](README.md#prior-work-this-methodology-draws-on)):

| Code | Pattern |
| --- | --- |
| EV | Excessive verification: re-running passing checks, repeated rebuilds, or checklist passes after the change was already verified |
| EE | Excessive exploration: tracing beyond what the tier calls for |
| HIP | Heavy pipeline: multi-stage process the task didn't need |
| TPL | Template output (system map, change plan, full report) on a task whose tier didn't need it |
| ENV | Changed the environment (versions, paths, config) to make a check pass |
| OVR | Followed skill guidance over an explicit task or repo requirement |

Report the count of runs with each code per condition. A code that appears more often with X-RAY than in the baseline points to a specific `SKILL.md` instruction to revise.

## 8. Execution cost (automated)

- Wall-clock time
- Input and output tokens
- Number of tool calls
- Monetary cost if the host reports it

Report cost **alongside** quality, never alone. A higher cost with no quality gain is a negative result.

## Trivial-task overhead check

For tasks in the "trivial change" category, compare cost between conditions. If X-RAY materially increases cost on trivial tasks without improving outcomes, the tiering in `SKILL.md` isn't working, and that's a finding to report.

## Result sheet (per run)

```text
task_id, condition, run, model, host, xray_commit,
success, accept_passed/total, regressions,
loc_added, loc_removed, files_outside_expected, new_deps, patch_quality_0_3,
visual_0_3 (or n/a), claims_total, claims_wrong, claims_lucky, disclosure_recall,
calibration_0_3, overhead_codes,
wall_seconds, tokens_in, tokens_out, tool_calls, cost_usd
```
