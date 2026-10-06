# Plan — TICKET-001

Contract (frozen): tickets/TICKET-001.md, criteria 1–9.
Above 20% → pending_approval.
Exactly 20% → active.
Header: the first line must be exactly `code,discount_pct` (spaces around a name are ignored). Anything else → `(1, reason)` and nothing is imported.

Logical workflow:
freeze contract
→ Builder + Breaker can work independently
→ combine both results
→ run every test
→ review evidence
→ make final decision

Lab execution note:
In this workshop we run Builder and Breaker one after another so their behavior
is easy to observe. Logically, neither depends on the other's implementation.

| Card    | Writes                       | Done when                                                                      |
|---------|------------------------------|--------------------------------------------------------------------------------|
| builder | src/panic_pantry/importer.py | python3 -m unittest tests.test_importer_contract -v → 9 tests OK, none skipped |
| breaker | tests/test_promo_import.py   | python3 -m unittest tests.test_promo_import -v → OK, every test skipped until importer.py exists |

Kept by me: settling any unclear rule in the ticket before agents start, and trivial edits (like renaming one variable) that cost more to delegate than to do.
Also mine: freezing the contract, integrating the results, reviewing evidence,
and making the final GO / NO-GO decision.
