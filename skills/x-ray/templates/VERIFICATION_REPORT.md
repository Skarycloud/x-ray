# Verification report: <task>

> Report what actually happened. Use real command output, not expectations.
> Lightweight: the short form at the bottom is enough.

## Summary
<One or two sentences: what changed and whether acceptance criteria are met.>

## Changes
| File | Change | Linked to |
| --- | --- | --- |
| `path` | <one line> | AC1 / O1 |

## Evidence
| Claim | Method | Command / observation | Result |
| --- | --- | --- | --- |
| O1 holds | unit test | `<command>` | <e.g. 23 passed, 0 failed> |
| I1 holds | existing suite | `<command>` | |
| UI correct at 375px | visual check | <screenshot / description> | |

Baseline (before change): <pre-existing failures, or "clean">

## Not verified
- <check not run>: <why>; recommended: `<command or step>`

## Remaining risks and unknowns
- [UNKNOWN] <item>
- [CONTRADICTED] <item, e.g. stale doc found at path:line>

## Out-of-scope observations
- <problems noticed but deliberately not fixed>

---

### Short form
```text
Changed: <files and purpose>
Verified: <command> → <actual result>
Not verified / risks: <list or "none">
```
