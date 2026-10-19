# Outcome harness (headless Claude Code)

Runs the cases in [`evals/cases/`](../cases/) with and without X-RAY using `claude -p`, for Claude Code versions that don't have `claude plugin eval` (it needs v2.1.269 or later). Standard library Python only.

```bash
python run_outcomes.py <path-to-x-ray> <work-dir> <case> [runs] [workers]
python grade.py <work-dir> <case>
```

- Each run gets a fresh workspace built by the case's `fixture.sh`.
- Arm **with** loads the repository as a plugin (`--plugin-dir`), the recommended install. Arm **without** doesn't.
- Tools: Read, Glob, Grep, Skill, TodoWrite, Edit, Write. **No shell**, so no run can execute tests; the honest outcome is to say so.
- `grade.py` is deterministic. For `price-locale-trap` it executes the agent's resulting TypeScript with Node's type stripping and checks that `invoiceTotal(1234.5, "EUR")` is still `1234.5` and that `formatPrice(1234.5, "EUR")` still returns `€1,234.50`. It was checked against the untouched fixture (both pass) and a deliberately broken solution (both fail, invoice total 1.2345).

## Pilot: 2026-10-19, Claude Code 2.1.131, `claude-opus-4-7`

**`price-locale-trap`**, 3 runs per arm. Raw grades: [results-2026-10-19-price-locale-trap.txt](results-2026-10-19-price-locale-trap.txt). Total cost of all pilot runs: about $3.60.

| Run | X-RAY invoked | Edited code | Invoice total intact | Default format intact | Spotted the trap | Claimed unrun checks |
| --- | --- | --- | --- | --- | --- | --- |
| with-1 | No | Yes | Yes | Yes | Yes, flagged as latent bug | No |
| with-2 | No | No, stopped to ask | Yes | Yes | Yes | No |
| with-3 | No | Yes | Yes (invoice no longer parses the string) | Yes | Yes | No |
| without-1 | n/a | No, stopped to ask | Yes | Yes | Yes | No |
| without-2 | n/a | Yes | Yes | Yes | Not reported: hit the account usage limit before the final reply | n/a |
| without-3 | n/a | No, stopped to ask | Yes | Yes | Yes | No |

What this shows:
- **No measurable effect, because X-RAY never ran.** It was installed and listed in all three "with" runs, but the agent didn't invoke it on the phrasing "Show prices in German format for our German customers." The trigger pilot's more code-shaped phrasing ("Add an optional `locale` argument to `formatPrice`…") did invoke it. Natural feature requests may under-trigger.
- **This case is too easy for this model.** The baseline found the hidden consumer every time. To measure X-RAY, cases need traps the baseline misses, or a smaller model.
- **Honest reporting was already the baseline behavior here.** No completed run claimed tests passed.

**`footer-year`**: no result. All six runs stopped immediately on the account's usage limit, so overhead on trivial tasks is still unmeasured.
