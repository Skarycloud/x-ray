# Verification

Verification answers: **what evidence shows that the outcomes happened and the invariants held?** It's chosen before implementation (SKILL.md step 6) and executed after (step 9).

## Pick methods by tier

| Tier | Minimum | Add when relevant |
| --- | --- | --- |
| **Lightweight** | Nearest relevant test, or lint/typecheck of changed files; read the diff | Quick manual check of the changed output |
| **Integrated** | Test suites covering changed paths and their consumers; build; typecheck; lint | New tests for new behavior; run the app and exercise the path; visual check for UI |
| **Critical** | Everything in Integrated, plus a regression test per invariant | Migration dry-run on a copy; negative/security tests; load or concurrency test; explicit rollback check |

## Method catalog

| Method | Proves | Doesn't prove |
| --- | --- | --- |
| Typecheck / compile | Interfaces line up statically | Runtime behavior, logic |
| Lint | Style rules, some bug patterns | Correctness |
| Unit test | Logic of an isolated unit | Integration, config, real dependencies |
| Integration test | Components work together | Behavior in real deployment environment |
| End-to-end / browser test | User-visible flow works | Coverage of edge cases |
| Manual execution (curl, CLI run, open page) | Real behavior right now, in this environment | Repeatability; other environments |
| Screenshot / visual inspection | Layout and appearance | Behavior, accessibility semantics |
| Diff review | Scope and intent of the change | That it runs |

Pick the cheapest method that would **fail if the claim were false**.

## Writing new tests

- **Bug fix**: write a test that reproduces the bug, watch it fail, then fix. A test that never failed hasn't been shown to catch anything.
- **New behavior**: test the acceptance criteria directly, including at least one edge or failure case.
- **Legacy code you're changing**: add characterization tests for current behavior first (see [invariant-contracts.md](invariant-contracts.md)).
- **Follow existing test conventions**: framework, file location, naming, fixtures.
- **Don't mock the thing under test.** Mock only the boundaries (network, clock, filesystem) when the project already does.

## Running checks honestly

1. **Baseline first.** Run relevant tests before changing code. Record pre-existing failures.
2. **Run the real command.** Use the project's scripts (`npm test`, `make check`, `pytest`) as CI does.
3. **Read the output.** Check counts: "0 tests ran" is not a pass. Check the right files were included.
4. **Fix causes, not symptoms.** Don't add `skip`, loosen assertions, raise timeouts, or delete tests to get green. If a test is genuinely wrong, change it and explain why in the report.
5. **Re-run after the last edit.** Results from before your final change don't count.
6. **Leave the environment alone.** Don't install other package versions, edit import paths, or change config to get a check to pass, unless that's the task. A pass in an environment the project doesn't use proves nothing about the project.

## When to stop

Verification is done when **every** outcome and invariant in the contract has a check that:
- would fail if the claim were false, and
- passed after your last edit.

Then stop. Extra work past that point costs time without adding evidence. Common forms:
- Re-running a suite that already passed with no edits since.
- Rebuilding or re-linting the same unchanged files.
- Adding checks the tier doesn't call for (a browser run for a Lightweight copy change).
- Re-reading the diff in loops instead of once, at the end.

If a new check *would* add evidence (it covers a contract item nothing else covers), it isn't excess. Add it.

## When verification is impossible

Sometimes you can't run tests (missing services, credentials, platform, no browser). Then:
- Do what you can: typecheck, lint, run the subset that works, review the diff carefully.
- State precisely what couldn't be verified and why.
- Suggest the exact command or step a human should run.

Never phrase unverified work as verified. Compare:

> ❌ "Fixed the login bug, everything works."
>
> ✅ "Changed token refresh in `auth/session.ts`. Unit tests pass (`npm test -- auth`: 14 passed). Couldn't run the e2e login flow (needs OAuth credentials); recommend `npm run e2e -- login` before merging."

## Interpreting results

| Result | Meaning | Action |
| --- | --- | --- |
| All relevant tests pass, behavior observed | Outcomes and covered invariants CONFIRMED | Report |
| Pass, but tests don't cover an invariant | That invariant is INFERRED at best | Add test or report gap |
| Failure in code you changed | Your change is wrong or incomplete | Fix |
| Failure that existed at baseline | Not caused by you | Report it; don't fix unless in scope |
| Flaky failure | Unclear | Re-run once; if it persists, investigate or report as UNKNOWN |
