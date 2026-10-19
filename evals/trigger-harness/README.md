# Trigger harness (Claude Code)

Runs the [trigger queries](../trigger-queries.md) headlessly with `claude -p` and records whether the `x-ray` skill was invoked. Standard library Python only.

```bash
python make_fixture.py <path-to-x-ray> <fixtures-dir>        # builds two copies of a small fake shop repo
python run_triggers.py ../trigger-queries.md <fixtures-dir> <results-dir> [runs] [workers]
python score.py <results-dir>
```

- `make_fixture.py` builds `skill-only` (X-RAY installed at `.claude/skills/x-ray`) and `skill-plus-pointer` (the same, plus the [always-on pointer](../../adapters/always-on-pointer.md) as `CLAUDE.md`).
- `run_triggers.py` runs each query in each fixture. Sessions are read-only: `--permission-mode dontAsk` with only `Read Grep Glob Skill` allowed, `--max-turns 3`.
- `score.py` marks a run `Y` if a `Skill` tool call named `x-ray` appears, and `!` if the session hit the turn cap (expected with the cap).

**Limit:** the 3-turn cap keeps cost down, but a skill invoked after turn 3 counts as not triggered. That can under-count for both groups.

Results: [results-2026-10-19-claude-code.txt](results-2026-10-19-claude-code.txt). Analysis: [adapters/claude-code.md](../../adapters/claude-code.md#test-record).
