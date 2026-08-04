#!/usr/bin/env python3
"""Regression tests for normalized STL identity and qualification checks."""

from __future__ import annotations

import json
import math
import struct
import tempfile
import unittest
from pathlib import Path

from mesh_fingerprint import (
    CANONICAL_ASCII_STL_SCHEMA,
    COORDINATE_QUANTUM_MM,
    FINGERPRINT_ALGORITHM,
    StlError,
    canonicalize_stl,
    describe_mesh,
)
from qualified_geometry import (
    MANIFEST_SCHEMA,
    QualificationError,
    candidate_manifest,
    check_manifest,
)

Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]

TETRAHEDRON: tuple[Triangle, ...] = (
    ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
    ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0)),
    ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
)


def ascii_stl(
    triangles: tuple[Triangle, ...],
    *,
    normal: str = "0 0 1",
    negative_zero: bool = False,
) -> bytes:
    lines = ["solid test"]
    for triangle in triangles:
        lines.extend((f"  facet normal {normal}", "    outer loop"))
        for point in triangle:
            values = []
            for value in point:
                if negative_zero and value == 0:
                    values.append("-0")
                else:
                    values.append(format(value, ".9g"))
            lines.append(f"      vertex {' '.join(values)}")
        lines.extend(("    endloop", "  endfacet"))
    lines.append("endsolid test")
    return ("\n".join(lines) + "\n").encode("ascii")


def binary_stl(
    triangles: tuple[Triangle, ...],
    *,
    header: bytes = b"test",
    normal: Point = (0.0, 0.0, 1.0),
    attribute: int = 0,
) -> bytes:
    output = bytearray(header.ljust(80, b"\0")[:80])
    output.extend(struct.pack("<I", len(triangles)))
    for triangle in triangles:
        flattened = normal + triangle[0] + triangle[1] + triangle[2]
        output.extend(struct.pack("<12fH", *flattened, attribute))
    return bytes(output)


def rearranged(triangles: tuple[Triangle, ...]) -> tuple[Triangle, ...]:
    return tuple(
        (triangle[1], triangle[0], triangle[2])
        for triangle in reversed(triangles)
    )


class MeshFingerprintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, name: str, data: bytes) -> Path:
        path = self.root / name
        path.write_bytes(data)
        return path

    def digest(self, path: Path) -> str:
        fingerprint = describe_mesh(path)["fingerprint"]
        assert isinstance(fingerprint, dict)
        return str(fingerprint["sha256"])

    def test_ascii_binary_order_winding_and_start_vertex_are_equivalent(self) -> None:
        ascii_path = self.write("mesh-ascii.stl", ascii_stl(TETRAHEDRON))
        changed_representation = tuple(
            (triangle[2], triangle[1], triangle[0])
            for triangle in rearranged(TETRAHEDRON)
        )
        binary_path = self.write(
            "mesh-binary.stl",
            binary_stl(
                changed_representation,
                header=b"a completely different header",
                normal=(99.0, -5.0, 2.0),
                attribute=65535,
            ),
        )
        self.assertEqual(self.digest(ascii_path), self.digest(binary_path))

    def test_normals_headers_attributes_and_signed_zero_do_not_matter(self) -> None:
        positive = self.write("positive.stl", ascii_stl(TETRAHEDRON))
        negative = self.write(
            "negative.stl",
            ascii_stl(
                rearranged(TETRAHEDRON),
                normal="nan -infinity 42",
                negative_zero=True,
            ),
        )
        self.assertEqual(self.digest(positive), self.digest(negative))

    def test_exact_stl_canonicalization_is_byte_deterministic(self) -> None:
        original = self.write("canonical-ascii.stl", ascii_stl(TETRAHEDRON))
        reordered = tuple(
            (triangle[1], triangle[2], triangle[0])
            for triangle in reversed(TETRAHEDRON)
        )
        alternate = self.write(
            "canonical-binary.stl",
            binary_stl(
                reordered,
                header=b"different",
                normal=(9.0, 8.0, 7.0),
                attribute=123,
            ),
        )
        canonicalize_stl(original)
        canonicalize_stl(alternate)
        self.assertEqual(
            "pocketforge-canonical-ascii-stl-v1",
            CANONICAL_ASCII_STL_SCHEMA,
        )
        self.assertEqual(original.read_bytes(), alternate.read_bytes())

    def test_decimal_ascii_and_float32_binary_share_the_quantized_identity(
        self,
    ) -> None:
        decimal_triangle: tuple[Triangle, ...] = (
            (
                (0.1, 17.6332, 0.0),
                (1.25, 0.0, 0.0),
                (0.0, 1.75, 0.5),
            ),
        )
        ascii_path = self.write("decimal-ascii.stl", ascii_stl(decimal_triangle))
        binary_path = self.write(
            "decimal-binary.stl", binary_stl(decimal_triangle)
        )
        self.assertEqual(self.digest(ascii_path), self.digest(binary_path))

    def test_printable_coordinate_mutation_changes_identity(self) -> None:
        original = self.write("original.stl", ascii_stl(TETRAHEDRON))
        mutated_triangles = list(TETRAHEDRON)
        changed = list(mutated_triangles[0])
        changed[0] = (0.001, 0.0, 0.0)
        mutated_triangles[0] = tuple(changed)  # type: ignore[assignment]
        mutated = self.write(
            "mutated.stl", ascii_stl(tuple(mutated_triangles))
        )
        self.assertNotEqual(self.digest(original), self.digest(mutated))

    def test_malformed_and_nonfinite_vertices_are_rejected(self) -> None:
        malformed = self.write(
            "malformed.stl",
            b"""solid bad
facet normal 0 0 1
outer loop
vertex 0 0 0
vertex 1 0 0
endloop
endfacet
endsolid bad
""",
        )
        nonfinite = self.write(
            "nonfinite.stl",
            ascii_stl(TETRAHEDRON).replace(
                b"vertex 0 0 0", b"vertex nan 0 0", 1
            ),
        )
        with self.assertRaises(StlError):
            describe_mesh(malformed)
        with self.assertRaises(StlError):
            describe_mesh(nonfinite)

    def test_metrics_include_closed_manifold_topology(self) -> None:
        path = self.write("tetrahedron.stl", ascii_stl(TETRAHEDRON))
        description = describe_mesh(path)
        self.assertEqual(description["triangle_count"], 4)
        self.assertEqual(
            description["topology"],
            {
                "vertices": 4,
                "edges": 6,
                "facets": 4,
                "components": 1,
                "boundary_edges": 0,
                "nonmanifold_edges": 0,
                "euler_characteristic": 2,
            },
        )
        self.assertEqual(description["volume_mm3"], "0.167")
        self.assertTrue(math.isclose(float(description["surface_area_mm2"]), 2.366))


class QualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "qualification").mkdir()
        (self.root / "build").mkdir()
        self.mesh = self.root / "build" / "part.stl"
        self.mesh.write_bytes(ascii_stl(TETRAHEDRON))
        self.lock = self.root / "qualification" / "toolchain.json"
        self.lock.write_text(
            json.dumps(
                {
                    "schema": "pocketforge-cad-toolchain-v1",
                    "openscad_reported_version": "2021.01",
                }
            ),
            encoding="utf-8",
        )
        self.manifest = self.root / "qualification" / "manifest.json"
        self.manifest.write_text(
            json.dumps(
                {
                    "schema": MANIFEST_SCHEMA,
                    "fingerprint_contract": {
                        "algorithm": FINGERPRINT_ALGORITHM,
                        "coordinate_quantum_mm": str(COORDINATE_QUANTUM_MM),
                    },
                    "toolchain_lock": "qualification/toolchain.json",
                    "qualification": {
                        "status": "physically_accepted",
                        "acceptance_ref": "tsp-test",
                        "accepted_on": "2026-07-21",
                        "accepted_source_revision": "a" * 40,
                        "characterized_source_revision": "b" * 40,
                    },
                    "artifacts": {
                        "part": {
                            "path": "build/part.stl",
                            "make_target": "build/part.stl",
                            "expected": describe_mesh(self.mesh),
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_check_is_read_only_and_mutation_fails(self) -> None:
        original_manifest = self.manifest.read_bytes()
        check_manifest(
            self.root,
            self.manifest,
            openscad="unused",
            verify_toolchain=False,
        )
        self.assertEqual(original_manifest, self.manifest.read_bytes())

        self.mesh.write_bytes(
            ascii_stl(
                (
                    ((0.001, 0.0, 0.0), TETRAHEDRON[0][1], TETRAHEDRON[0][2]),
                    *TETRAHEDRON[1:],
                )
            )
        )
        with self.assertRaises(QualificationError):
            check_manifest(
                self.root,
                self.manifest,
                openscad="unused",
                verify_toolchain=False,
            )

    def test_record_requires_explicit_physical_acceptance(self) -> None:
        with self.assertRaises(QualificationError):
            candidate_manifest(
                self.root,
                self.manifest,
                acceptance_ref="tsp-test",
                accepted_source_revision="a" * 40,
                characterized_source_revision="b" * 40,
                accepted_on="2026-07-21",
                confirmed=False,
            )


if __name__ == "__main__":
    unittest.main()
