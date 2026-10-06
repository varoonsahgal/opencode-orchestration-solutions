"""CSV promo-code importer for the Midnight Crunch Drop (TICKET-001).

Every promotion is created through PromotionService.create_promotion, so the
service alone decides whether a code is active or pending manager approval.
"""

import csv
from dataclasses import dataclass, field

from .promotions import DuplicatePromotionError, InvalidPromotionError

HEADER = ["code", "discount_pct"]


@dataclass
class ImportReport:
    created: list = field(default_factory=list)
    pending_approval: list = field(default_factory=list)
    skipped_duplicate: list = field(default_factory=list)
    errors: list = field(default_factory=list)


def import_promotions(csv_path, service):
    """Import promo codes from csv_path into service and report every row.

    Line numbers are 1-based and count the header as line 1.
    """
    report = ImportReport()
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    if not rows or [cell.strip() for cell in rows[0]] != HEADER:
        report.errors.append((1, "missing or wrong header: expected code,discount_pct"))
        return report

    for line, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            report.errors.append((line, "empty row"))
            continue
        if len(row) != 2:
            report.errors.append((line, f"expected 2 columns, got {len(row)}"))
            continue

        code, raw_pct = row[0].strip(), row[1].strip()
        try:
            discount_pct = int(raw_pct)
        except ValueError:
            report.errors.append((line, f"discount_pct is not a whole number: {raw_pct!r}"))
            continue

        try:
            promo = service.create_promotion(code, discount_pct)
        except DuplicatePromotionError:
            report.skipped_duplicate.append(code)
            continue
        except InvalidPromotionError as exc:
            report.errors.append((line, str(exc)))
            continue

        if promo.status == "active":
            report.created.append(code)
        else:
            report.pending_approval.append(code)

    return report
