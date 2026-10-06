# Orchestrated run notes

> **Reference solution.** The gate log below is a real run of `scripts/gate.sh` against this branch's importer and tests.
> The scorecard rows marked *(your run)* depend on your model, timer and tally, so they're left blank for you.

## Gate log

Written by `bash scripts/gate.sh`. One line per gate run; a FAIL then a later PASS is one repair cycle.

| Time | Gate | Verdict | Evidence |
|---|---|---|---|
| 07:57:48 | builder | PASS | Ran 9: OK (DONE needs OK with none skipped) |
| 07:57:48 | breaker | PASS | without importer.py: Ran 10: OK (skipped=10) (DONE needs OK, every test skipped) |
| 07:57:48 | integration | PASS | whole suite: Ran 33: OK |

## Reviewer dispositions

These findings come from reviewing this importer against the Reviewer checklist. Your Reviewer's findings will differ: what matters is that every one gets a disposition.

| Finding | Severity | Disposition | Reason | Owner |
|---|---|---|---|---|
| Approval bypass: none found. Every row goes through `create_promotion`; the importer never compares to 20, sets a status or calls `approve()` (`importer.py:52`) | — | ACCEPT | Confirmed by the Breaker's spy, reload and `approve()` tests | — |
| Codes and discounts are whitespace-trimmed (`importer.py:44`), so ` SNACK10 ` imports as `SNACK10` | Low | ACCEPT | The ticket is silent; trimming matches how the header is read, and the service still validates the code format | — |
| Bad-code and out-of-range errors reuse the service's exception text as the reason (`importer.py:57`) | Low | ACCEPT | Criterion 4 asks for "a reason"; only blank rows need an exact string | — |
| No Breaker test for a header with an extra column (`code,discount_pct,notes`) | Low | DEFER | The importer already rejects it (`importer.py:32`), but nothing pins that behavior | Breaker, next ticket |

## Scorecard

Measured rows from `bash scripts/score.sh`:

| Row | Module 0: one agent | Module 3: crew |
|---|---|---|
| Model + variant | *(your run)* | *(your run)* |
| Contract tests passing (/9) | *(your run)* | 9/9 |
| Whole suite (last line) | *(your run)* | ran 33 tests: OK |
| Policy source check | *(your run)* | nothing flagged |
| Files changed (product) | *(your run)* | `src/panic_pantry/importer.py`, `tests/test_promo_import.py` |
| Interventions | *(your run)* | *(your run)* |
| Repair cycles (from the gate log) | n/a | 0 |
| Elapsed (of the 15-minute window) | *(your run)* | *(your run)* |
| Rework minutes after the window | n/a | *(your run)* |
| Tokens / cost | *(your run)* | *(your run)* |

## Comparison conclusion

Write this from your own run. A conclusion only this solution can support:

Under the matched 15-minute condition, the crew's result passed all 9 contract tests plus 10 independent Breaker tests. Those Breaker tests catch 5 defects the contract suite misses: a wrong header that still imports, a 3-column row, `20.9` read as 20, the wrong blank-row reason, and a direct write to the JSON store.

What one run does NOT prove: that crews beat single agents in general, or that your crew would produce this code. Model output varies; compare against the gates, not line by line.
