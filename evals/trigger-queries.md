# Trigger queries

Use these to check whether a host loads X-RAY when it should, and leaves it alone when it shouldn't. They support step 4 of the [host validation checklist](../adapters/README.md#validation-checklist-for-a-host-to-do-before-marking-tested).

**Status:** Pilot run on Claude Code, 1 run per query (2026-10-19): see the [Claude Code test record](../adapters/claude-code.md#test-record). Not yet run on other hosts.

## Method

Adapted from the trigger-evaluation approach in Anthropic's `skill-creator` skill:

1. Start a fresh session in a real repository for each query, with X-RAY installed and no other skills that overlap.
2. Paste the query verbatim. Record whether X-RAY loaded (the host's skill indicator, `/context`, or the transcript).
3. Run each query 3 times. Triggering isn't deterministic.
4. Report the trigger rate for each group. Don't edit the `description` to fit these exact queries; that overfits. If you revise it, hold some queries back to test the revision.

Simple one-step requests may not trigger any skill even when the description matches, because hosts tend to consult skills only for tasks they can't easily handle alone. Record that as a result, not an error.

## Should trigger

| # | Query |
| --- | --- |
| T1 | The checkout endpoint returns a 500 when the cart has a 100% discount code. Can you fix it? |
| T2 | Add an optional `locale` argument to `formatPrice` without breaking the existing callers. |
| T3 | Rename the `fullname` column on users to `display_name`. |
| T4 | Our settings page and the dashboard share the nav bar. Make the nav collapse on mobile. |
| T5 | Why does `validateUser` sometimes create a user? Fix it so it only validates. |
| T6 | Refactor the payment retry logic in `src/payments` so it's easier to follow, same behavior. |
| T7 | Allow team admins, not just org owners, to delete projects. |
| T8 | The README says retries are exponential but they don't seem to be. Make it match. |
| T9 | Bump the session timeout to 60 minutes. |
| T10 | Clean up the old feature flag `new_checkout` now that it's fully rolled out. |

## Should not trigger

Near misses come first; they share vocabulary with code changes but aren't changes to existing code.

| # | Query | Why not |
| --- | --- | --- |
| N1 | Scaffold a new Next.js app with Tailwind and a login page. | Greenfield, no existing behavior |
| N2 | Explain how the auth middleware in this repo works. | Read-only explanation, no change |
| N3 | Write a one-off script that renames these 200 photos by date. | Throwaway script |
| N4 | What's the difference between `useEffect` and `useLayoutEffect`? | General question |
| N5 | Draft release notes from the last 20 commits. | Writing task |
| N6 | Review this PR for security issues. | Review, not a change (another skill may fit better) |
| N7 | Write a haiku about refactoring. | Shares a keyword only |
| N8 | Set up a new Python package with pytest and a CI workflow. | Greenfield |
| N9 | Summarize the open issues labeled `bug`. | No code change |
| N10 | Translate this error message into Spanish for the docs. | Content task |

N2 and N6 are judgment calls: an agent explaining or reviewing code might reasonably use parts of X-RAY. Report their results separately from the clear negatives.

## Result sheet

```text
host, host_version, model, date, xray_commit, query_id, run, triggered (y/n), notes
```
