# Reverse engineering: reconstruct the relevant system

Goal: build an accurate, **task-scoped** model of how the code you're about to change behaves today. You aren't trying to understand the whole repository. Stop when you can predict what your change will affect.

## Procedure

### 1. Anchor on the task
Turn the request into one or more **anchors**: concrete things you can search for.

| Request mentions | Anchor |
| --- | --- |
| A UI element ("the Save button") | Visible text, `aria-label`, test IDs, route path |
| An error ("500 on checkout") | Exact error string, status code, log line |
| An endpoint or command | Route definition, CLI command registration |
| A behavior ("discount applied twice") | Domain term (`discount`, `applyPromo`), related tests |

Search for anchors with exact-string search first (`rg -n "Save changes"`), then symbol search. Searching for exact text beats guessing file names.

### 2. Find the entry point
Work outward from the anchor until you reach where execution starts for this behavior: a route handler, event listener, CLI command, job scheduler, exported public function, or component mounted by a route.

Record it as CONFIRMED with `file:line`.

### 3. Trace the execution path
Follow the call chain from entry point to the code you'll change. For each hop, note:
- Function or module, `file:line`.
- What it receives and returns.
- Side effects: writes, network calls, cache, global state, events emitted.
- Branches that matter: feature flags, environment checks, permission checks, error paths.

Read the code. Don't infer behavior from names. `validateUser()` might also create the user.

### 4. Find the consumers (reverse direction)
For each symbol you'll change, find who depends on it:
- Direct references: `rg -n "\bsymbolName\b"`, IDE "find references", or the language server.
- Indirect references: string-based lookups (dynamic imports, reflection, DI containers, route tables, templates, serialization keys, SQL column names).
- Out-of-repo consumers: published packages, public APIs, webhooks, files other systems read, database columns read by other services. These are usually UNKNOWN; record them as such.

### 5. Map data flow
For data the change touches: where it enters (user input, API, file, DB), how it's transformed and validated, where it's stored, and where it leaves. Pay attention to format boundaries (JSON field names, DB types, timezone handling, encoding) because they break silently.

### 6. Inventory the tests
- Which tests exercise this path? Find them by searching for the symbol and the anchor.
- What do they actually assert? A test that mocks the thing you're changing doesn't protect it.
- Run them once **before** changing anything to get a baseline. Pre-existing failures must be known before you start, not discovered afterward and blamed on your change.

### 7. Check configuration and environment
Look for behavior that differs by environment: env vars, config files, feature flags, build-time constants, platform checks. A change that's correct in dev and wrong in prod usually hides here.

## When to stop

Stop when **all** of these hold:
- You can name the entry point(s) and every in-repo consumer of what you'll change.
- Every remaining UNKNOWN is recorded with how it could be resolved.
- You can describe, in a sentence, how the behavior works today.

Don't keep exploring for completeness. Depth follows the tier set in `SKILL.md`.

## Pitfalls

- **Trusting names**: `isAdmin` might check a feature flag, not a role.
- **Trusting docs**: architecture docs often describe the intended design, not the current one.
- **Missing dynamic dispatch**: plugins, event buses, and string-keyed registries don't show up in "find references."
- **Generated code**: don't edit generated files. Find and change the generator or its source.
- **Dead code**: code with no callers may be invoked dynamically or externally. Confirm before treating it as dead.

## Example (Integrated tier)

> Task: "Orders placed with a 100% discount code fail with a 500."

```text
Anchor: "discount" + 500 on POST /orders
Entry: src/routes/orders.ts:42 createOrder handler            CONFIRMED
Path:  createOrder → pricing.applyDiscount (src/pricing.ts:88)
       → payments.charge (src/payments/stripe.ts:31)            CONFIRMED
Cause: charge() called with amount 0; provider rejects 0-amount
       charges, error is uncaught → 500                         CONFIRMED (reproduced locally, see log)
Consumers of applyDiscount: createOrder, previewCart (src/routes/cart.ts:17),
       invoice export job (jobs/invoice.ts:55)                  CONFIRMED (rg)
Tests: tests/pricing.test.ts covers applyDiscount; no test for
       zero-total orders                                        CONFIRMED
Unknown: does the finance export expect a payment record for
       every order?                                             UNKNOWN → ask / check export consumer
```
