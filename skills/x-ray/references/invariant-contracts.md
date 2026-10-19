# Invariant contracts

Before editing, write down two lists: what must **change** and what must **not**. Most regressions come from the second list never being written.

## Contract structure

```text
Required outcomes (must become true)
  O1. <observable behavior after the change>

Invariants (must remain true)
  I1. <existing behavior that must be preserved>

Verification
  O1 → <how it will be checked>
  I1 → <how it will be checked>
```

Each item must be **observable**: someone could check it with a test, a command, or by looking. "Code is clean" isn't observable. "No new lint warnings in changed files" is.

## Where invariants come from

Go through this checklist for the code you're changing. Skip categories that don't apply.

| Category | Ask | Example invariant |
| --- | --- | --- |
| Public interface | Who calls this, and what do they rely on? | `getUser(id)` still returns `null` (not throws) for unknown IDs |
| Data format | What reads what this writes? | JSON field `created_at` stays ISO-8601 UTC |
| Error semantics | What errors do callers catch or display? | Invalid input still returns 400 with `{error: {code}}` shape |
| Persistence | Can existing stored data still be read? | Rows written before this change still deserialize |
| Permissions | Who can do this today? | Non-admins still can't access `/admin/*` |
| Performance | Are there hot paths or limits? | Search stays one DB query per request (no N+1) |
| Ordering / idempotency | Does order or retry matter? | Re-sending the webhook doesn't double-credit |
| UI | What do users see elsewhere? | Header layout unchanged at 320px and 1440px |
| Accessibility | What do assistive-tech users rely on? | Dialog still traps focus and closes on Esc |
| Configuration | What env/flag combos exist? | Behavior with `FEATURE_X=off` unchanged |

## Strength of verification

Not every invariant needs a new test. Pick the cheapest method that would **actually fail** if the invariant broke:

1. Existing test already asserts it → run it. Confirm it would fail by reading the assertion.
2. Type system enforces it → typecheck.
3. No coverage, and it's important → add a focused test (characterization test if the behavior is legacy).
4. Not automatable here (visual, external system) → manual check with recorded evidence, or mark unverified.

A **characterization test** pins current behavior before you change code, even behavior that looks odd. If the odd behavior is actually a bug you're fixing, the test changes intentionally, and you say so.

## Example

> Task: add optional `locale` parameter to `formatPrice(amount, currency)`.

```text
Required outcomes
  O1. formatPrice(1234.5, "EUR", "de-DE") → "1.234,50 €"
Invariants
  I1. formatPrice(amount, currency) with no locale returns exactly what it returns today
      for all currencies used in fixtures
  I2. Signature remains backward-compatible (existing 2-arg call sites compile unchanged)
  I3. No new runtime dependency (Intl is available on all supported targets)
Verification
  O1 → new unit test
  I1 → existing tests/price.test.ts (12 cases) + snapshot of current outputs before change
  I2 → typecheck
  I3 → diff of package.json is empty
```

## Anti-patterns

- Writing invariants after the change. You'll unconsciously pick ones that still hold.
- Invariants so broad they're unverifiable ("nothing else breaks").
- Skipping invariants because "it's a small change." Small changes to shared code have wide blast radius; let the impact analysis decide.
