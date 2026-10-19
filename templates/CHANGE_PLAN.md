# Change plan: <task>

> Write before editing. If the plan fits in a few lines (most Lightweight and many Integrated tasks), the short version at the bottom is enough.

**Tier:** Lightweight | Integrated | Critical, because <reason>

## Goal and acceptance criteria
- Goal: <one or two sentences>
- AC1: <observable, checkable>
- AC2:
- Out of scope: <what this change will not do>

## Contract
| ID | Type | Statement | Verified by |
| --- | --- | --- | --- |
| O1 | Outcome | | |
| I1 | Invariant | | |

## Impact
| Changed item | Consumers | Risk | Detection |
| --- | --- | --- | --- |
| | | | |

## Approach
- What changes, file by file, and why this is the smallest safe option.
- Alternatives rejected: <option>, because <reason>
- New dependencies: none | <name>, because <reason; alternative rejected>

## Load-bearing assumptions
- [INFERRED / UNKNOWN] <assumption>: <how it's handled if wrong>

## Rollback (Critical only)
- <revert / flag off / down-migration>; irreversible steps: <none | list, with approval status>

---

### Lightweight version
```text
Change: <what and where>
Must not break: <the one thing that matters>
Check: <command or observation>
```
