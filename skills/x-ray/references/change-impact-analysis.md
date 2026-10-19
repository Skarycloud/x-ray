# Change impact analysis

Answer one question before editing: **if this change is subtly wrong, what breaks, for whom, and would we notice?**

## Procedure

### 1. List what you're changing
Be specific: symbols (functions, types, components, CSS classes), contracts (API shape, DB schema, config keys, CLI flags, events), and behavior (timing, ordering, error handling).

### 2. Find consumers of each item

| Changed item | How to find consumers |
| --- | --- |
| Function / class / type | Language server references; `rg -n "\bName\b"`; check re-exports and barrel files |
| Exported package API | Everything above, plus: is this published? Check `package.json`/`pyproject` exports, public docs, semver policy |
| HTTP/RPC endpoint | Frontend calls, other services, API clients, OpenAPI specs, mobile apps (often external → UNKNOWN) |
| DB column / table | ORM models, raw SQL (`rg` the column name), migrations, analytics/ETL, other services sharing the DB |
| Config key / env var | Config loaders, deploy manifests, CI files, docs, `.env.example` |
| CSS class / design token | Templates and components using it; global stylesheets; tokens used in other themes |
| Event / message | Every subscriber; queue consumers in other repos |
| File format / output | Anything that parses it: scripts, other tools, users |

### 3. Classify each consumer

| Class | Meaning | Required handling |
| --- | --- | --- |
| **In-repo, tested** | Consumer has tests covering the interaction | Run those tests |
| **In-repo, untested** | Consumer exists but nothing checks it | Inspect manually; add a test if Integrated/Critical |
| **External, known** | Another service, client, or user you can identify | Keep backward compatibility or coordinate; flag in report |
| **External, unknown** | Can't enumerate (public API, published package) | Treat contract as frozen unless the task is to change it |

### 4. Rate the blast radius

Combine **reach** (how many consumers) and **severity** (worst plausible failure):

| | Cosmetic | Functional | Data loss / security / money |
| --- | --- | --- | --- |
| **One consumer** | Lightweight | Integrated | Critical |
| **Several** | Integrated | Integrated | Critical |
| **Unknown / external** | Integrated | Critical | Critical |

If this table gives a higher tier than you started with, re-tier and deepen investigation and verification.

### 5. Plan detection
For each significant risk: which test, check, or observation would catch it? If nothing would, that's a gap. Close it (add a test) or report it.

### 6. Plan rollback (Critical only)
How is this undone? Revert commit, flag off, down-migration? Irreversible steps (data deletion, destructive migrations, sent emails) need explicit approval and a backup or dry-run first.

## Safe-change patterns

When a contract must change, prefer patterns that keep old consumers working:

- **Additive change**: add a new optional parameter, field, or endpoint instead of changing an existing one.
- **Expand-contract**: add new → migrate consumers → remove old, across separate changes.
- **Deprecate before delete**: keep old behavior with a warning when consumers are unknown.
- **Feature flag**: ship dark, enable deliberately, keep a kill switch.

Don't apply these by reflex. For a private function with two in-repo callers, just update the callers. The pattern should match the blast radius.

## Example

> Change: rename DB column `users.fullname` → `users.display_name`.

```text
Consumers
  ORM model src/models/user.py:14                  in-repo, tested
  Raw SQL in reports/monthly.sql:22                in-repo, untested
  Analytics ETL (separate repo, reads users table) external, known
  Any BI dashboards                                external, unknown
Blast radius: unknown/external × functional → Critical
Plan: expand-contract. Add display_name, dual-write, backfill; migrate
      in-repo readers; notify analytics owner; drop fullname in a later change.
Detection: model tests; run monthly.sql against fixture DB; ETL owner confirms.
Rollback: column add is reversible; drop step deferred.
```
