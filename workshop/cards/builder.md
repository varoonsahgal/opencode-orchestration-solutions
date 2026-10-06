DO:     Create src/panic_pantry/importer.py with import_promotions(csv_path, service) -> ImportReport, as specified in tickets/TICKET-001.md.
READ:   tickets/TICKET-001.md, src/panic_pantry/promotions.py, src/panic_pantry/models.py, fixtures/promos_clean.csv, fixtures/promos_messy.csv, fixtures/promos_messy.expected.md
RULES:  Criteria 1–9 are final. The service decides approval: never compare to 20 yourself. "Duplicate" includes codes the shop already has (WELCOME10 is one). The header must be exactly `code,discount_pct` (spaces around a name are ignored); anything else → (1, reason) and nothing imported.
TOUCH:  src/panic_pantry/importer.py only.
DONE:   python3 -m unittest tests.test_importer_contract -v → Ran 9 tests, OK, none skipped.
REPORT: files changed · exact command run + its last line · anything you guessed.
