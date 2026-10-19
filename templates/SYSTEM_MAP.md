# System map: <task or area>

> Use when the map doesn't fit in a few lines (typical for Critical work). Keep it to the code this change can touch.
> Mark each line CONFIRMED / INFERRED / UNKNOWN / CONTRADICTED and cite a source.
> Delete sections that don't apply.

**Task:** <one sentence>
**Tier:** Lightweight | Integrated | Critical
**Repo state:** <branch / commit>

## Entry points
- <route / command / event / export>: `path:line` [CONFIRMED]

## Execution path
```text
<entry> (path:line)
  → <step> (path:line): <what it does, side effects>
  → <code to change> (path:line)
```

## Consumers of what will change
| Symbol / contract | Consumer | Location | Tested? | State |
| --- | --- | --- | --- | --- |
| | | | | |

## Data flow
- In: <source, format>
- Transformed: <where / how>
- Stored: <table / file / cache>
- Out: <response / event / file>

## Configuration and environment
- <env var / flag / config key>: <effect> [state]

## Existing tests
| Test | What it actually asserts | Baseline result |
| --- | --- | --- |
| | | |

## Open questions
- [UNKNOWN] <question>: resolve by <how>
- [CONTRADICTED] <source A> vs <source B>: trusting <which>, because <why>
