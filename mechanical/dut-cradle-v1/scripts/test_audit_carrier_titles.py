#!/usr/bin/env python3
"""Unit tests for the all-device carrier-title inset audit."""

from __future__ import annotations

import unittest
from decimal import Decimal

import audit_carrier_titles as audit


class CarrierTitleAuditTests(unittest.TestCase):
    def test_clearance_uses_inner_border_edges_on_all_four_sides(self) -> None:
        title = {
            "title_box_size_mm": [Decimal("20"), Decimal("10")],
            "title_box_center_mm": [Decimal("10"), Decimal("5")],
            "border_inner_inset_mm": Decimal("1.2"),
        }
        points = [
            (Decimal("3.6"), Decimal("3.6"), Decimal("3.2")),
            (Decimal("16.4"), Decimal("6.4"), Decimal("3.2")),
            (Decimal("3.6"), Decimal("6.4"), Decimal("4.4")),
        ]
        mesh_min, mesh_max, clearances = audit.title_clearances(points, title)
        self.assertEqual((Decimal("3.6"), Decimal("3.6")), mesh_min)
        self.assertEqual((Decimal("16.4"), Decimal("6.4")), mesh_max)
        self.assertEqual(
            tuple(Decimal("2.4") for _ in range(4)),
            clearances,
        )

    def test_empty_export_is_rejected(self) -> None:
        with self.assertRaisesRegex(audit.TitleAuditError, "no mesh points"):
            audit.title_clearances([], {})


if __name__ == "__main__":
    unittest.main()
