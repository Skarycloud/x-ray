# Evidence ledger

The ledger keeps you honest about what you know versus what you're guessing. It can be a few lines in your reasoning for small tasks, or a table in a change plan for large ones.

## States

| State | Meaning | Required support |
| --- | --- | --- |
| **CONFIRMED** | Directly observed in this session | A source: `file:line`, a command plus its output, a rendered screenshot, a test result |
| **INFERRED** | Concluded from evidence but not observed | The evidence it rests on, and why the inference holds |
| **UNKNOWN** | Not known, and it affects the change | How it could be resolved (command, file, person) |
| **CONTRADICTED** | Two sources disagree | Both sources, and which one you trust and why |

A claim you don't need doesn't belong in the ledger. Record claims that are **load-bearing**: if they're wrong, the change is wrong.

## Entry format

```text
[STATE] claim
  source:  where it came from (file:line, command, URL, person)
  scope:   where it holds (this function / this env / this version)
  checked: when it was last observed (commit or date)
  invalidated if: what would make it false
  recheck: the command or read that re-establishes it
```

`scope`, `checked`, and `invalidated if` keep claims from silently going stale. A claim confirmed before you edited a file may not hold after. Within one task, `checked` and `recheck` are optional; they matter once a claim is reused later (see [Durable ledger](#durable-ledger-optional)).
For UNKNOWN entries, use `resolve:` (how to find out) instead of `source:`.

### Examples

```text
[CONFIRMED] Session tokens expire after 30 minutes.
  source:  src/auth/session.ts:12 (TTL = 30 * 60)
  scope:   production config; dev overrides via SESSION_TTL env var
  checked: a1b2c3d
  invalidated if: session.ts changes, or SESSION_TTL is set in deploy config (not checked)
  recheck: rg -n "TTL|SESSION_TTL" src/auth deploy/

[INFERRED] Nothing outside this repo reads the `legacy_status` column.
  source: no references in repo (rg legacy_status → only migrations + model)
  scope:  this repository only
  invalidated if: another service shares the database

[UNKNOWN] Whether mobile clients older than v3.2 still call /v1/profile.
  resolve: check API access logs, or ask the mobile team

[CONTRADICTED] README says retries are exponential; code uses a fixed 2s delay.
  source: README.md:88 vs src/http/retry.ts:20
  trust:  code (it's what runs); flag the README as stale in the report
```

## Rules

1. **Upgrade only with new evidence.** INFERRED becomes CONFIRMED only when you observe it directly. Repeating an inference doesn't confirm it.
2. **Downgrade on change.** After you edit code, claims about the edited region are stale until rechecked.
3. **Search results are scoped.** "No references found" is CONFIRMED only for what you searched (repo, file types, exact string). Dynamic access and external consumers stay UNKNOWN.
4. **Tool output is evidence; your expectation isn't.** "Tests pass" is CONFIRMED only if you ran them and read the result in this session.
5. **Don't build on load-bearing UNKNOWNs.** Resolve, design around (make the change correct either way), or ask.
6. **Report what's left.** Every unresolved UNKNOWN and CONTRADICTED that affects the result belongs in the final report.

## Decision guide for UNKNOWNs

| Situation | Action |
| --- | --- |
| Resolvable cheaply (one search, one command) | Resolve it now |
| Not resolvable, but change can be made safe for both answers | Do that, note it |
| Not resolvable, affects correctness, low blast radius | Proceed with stated assumption, flag prominently |
| Not resolvable, affects data, security, or public contract | Stop and ask |

## Durable ledger (optional)

By default the ledger lives only in the current task. Keep it across tasks **only** when the repository already has a place for durable agent notes (for example a section of `AGENTS.md` or an existing `docs/` notes file) or the user asks for one. Don't create a new notes file on your own initiative.

What to keep:
- Load-bearing facts that future changes in this area are likely to need: shared consumers, non-obvious invariants, contradicted docs, environment quirks.
- Each entry in the full format above, with `checked` set to a commit hash.

What not to keep:
- INFERRED or UNKNOWN entries stated as facts. Keep them labeled, or leave them out.
- Task narration, plans, or anything the code or git history already records.

When reusing an entry:
1. Treat it as INFERRED until rechecked. A durable entry is a lead, not evidence.
2. If its `invalidated if` condition may have happened since `checked` (for example `git diff <checked> -- <path>` is non-empty), run `recheck` before relying on it.
3. Update `checked` when it still holds; fix or delete it when it doesn't. Don't leave known-wrong entries in place.

## Common mistakes

- Labeling something CONFIRMED because the function name says so.
- Treating a passing CI badge in the README as evidence about the current branch.
- Citing a file without a line, which makes the claim impossible to recheck.
- Recording dozens of trivial facts and hiding the two that matter.
