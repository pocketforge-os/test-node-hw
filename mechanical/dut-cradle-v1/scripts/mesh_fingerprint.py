#!/usr/bin/env python3
"""Create representation-independent fingerprints for printable STL geometry.

The fingerprint intentionally ignores STL headers, facet normals, attribute
bytes, facet ordering, winding, and each facet's starting vertex. Coordinates
are quantized to 0.0001 mm (0.1 micrometre), far below the resolution of the
target FDM process but large enough to make ASCII and binary STL encodings of
the same float geometry compare consistently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

FINGERPRINT_ALGORITHM = "pocketforge-normalized-stl-v1"
COORDINATE_QUANTUM_MM = Decimal("0.0001")
CANONICAL_ASCII_STL_SCHEMA = "pocketforge-canonical-ascii-stl-v1"
SERIALIZATION_MAGIC = (
    b"PocketForge normalized STL\x00"
    b"version=1\x00"
    b"coordinate-quantum-mm=0.0001\x00"
)

RawPoint = tuple[Decimal, Decimal, Decimal]
QuantizedPoint = tuple[int, int, int]
QuantizedTriangle = tuple[QuantizedPoint, QuantizedPoint, QuantizedPoint]


class StlError(ValueError):
    """The input is not a supported, finite STL mesh."""


class _NotBinaryStl(ValueError):
    """Internal signal allowing an ASCII parse fallback."""


def _finite_decimal(value: str) -> Decimal:
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise StlError(f"invalid STL coordinate: {value!r}") from exc
    if not result.is_finite():
        raise StlError(f"non-finite STL coordinate: {value!r}")
    return result


def _decimal_from_float(value: float) -> Decimal:
    if not math.isfinite(value):
        raise StlError(f"non-finite binary STL coordinate: {value!r}")
    return Decimal.from_float(value)


def _binary_points(data: bytes) -> list[RawPoint]:
    if len(data) < 84:
        raise _NotBinaryStl
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    expected_size = 84 + triangle_count * 50
    if expected_size != len(data):
        raise _NotBinaryStl

    points: list[RawPoint] = []
    offset = 84
    for _ in range(triangle_count):
        values = struct.unpack_from("<12fH", data, offset)
        # values[0:3] are the advisory normal and values[12] is the attribute
        # count. Neither describes geometry and neither enters the identity.
        for start in (3, 6, 9):
            points.append(
                (
                    _decimal_from_float(values[start]),
                    _decimal_from_float(values[start + 1]),
                    _decimal_from_float(values[start + 2]),
                )
            )
        offset += 50
    if not points:
        raise StlError("invalid binary STL: no triangles")
    return points


def _ascii_points(data: bytes) -> list[RawPoint]:
    try:
        text = data.decode("ascii", errors="strict")
    except UnicodeDecodeError as exc:
        raise StlError("input is neither a canonical binary nor ASCII STL") from exc

    points: list[RawPoint] = []
    vertices_in_facet: int | None = None
    facet_count = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        fields = raw_line.strip().split()
        if not fields:
            continue
        keyword = fields[0]

        if keyword in {"solid", "endsolid", "outer", "endloop"}:
            continue
        if keyword == "facet":
            if vertices_in_facet is not None:
                raise StlError(f"nested ASCII STL facet at line {line_number}")
            vertices_in_facet = 0
            facet_count += 1
            continue
        if keyword == "vertex":
            if vertices_in_facet is None:
                raise StlError(f"vertex outside ASCII STL facet at line {line_number}")
            if len(fields) != 4:
                raise StlError(f"malformed ASCII STL vertex at line {line_number}")
            points.append(
                (
                    _finite_decimal(fields[1]),
                    _finite_decimal(fields[2]),
                    _finite_decimal(fields[3]),
                )
            )
            vertices_in_facet += 1
            continue
        if keyword == "endfacet":
            if vertices_in_facet != 3:
                raise StlError(
                    "ASCII STL facet must contain exactly three vertices "
                    f"(line {line_number}, found {vertices_in_facet})"
                )
            vertices_in_facet = None
            continue
        raise StlError(f"unsupported ASCII STL record at line {line_number}: {keyword}")

    if vertices_in_facet is not None:
        raise StlError("unterminated ASCII STL facet")
    if facet_count == 0 or len(points) != facet_count * 3:
        raise StlError(
            f"invalid ASCII STL: facets={facet_count} vertices={len(points)}"
        )
    return points


def read_stl_points(path: Path) -> list[RawPoint]:
    """Read finite vertex coordinates from an ASCII or binary STL."""
    data = path.read_bytes()
    try:
        return _binary_points(data)
    except _NotBinaryStl:
        return _ascii_points(data)


def _exact_decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered


def canonicalize_stl(path: Path) -> None:
    """Write deterministic ASCII STL bytes without changing exact geometry.

    Facet order, each facet's cyclic starting vertex, advisory normals, header,
    whitespace, and signed zero are normalized. Vertex winding is retained.
    Unlike the normalized geometry fingerprint, coordinates are not quantized:
    the resulting raw SHA-256 remains an exact distribution-integrity value.
    """
    points = read_stl_points(path)
    if len(points) % 3:
        raise StlError(f"invalid STL vertex count: {len(points)}")
    facets = []
    for offset in range(0, len(points), 3):
        triangle = tuple(points[offset : offset + 3])
        rotations = (
            triangle,
            (triangle[1], triangle[2], triangle[0]),
            (triangle[2], triangle[0], triangle[1]),
        )
        facets.append(min(rotations))

    lines = ["solid PocketForge_Canonical\n"]
    for triangle in sorted(facets):
        lines.append("  facet normal 0 0 0\n")
        lines.append("    outer loop\n")
        for point in triangle:
            coordinates = " ".join(
                _exact_decimal_text(value) for value in point
            )
            lines.append(f"      vertex {coordinates}\n")
        lines.append("    endloop\n")
        lines.append("  endfacet\n")
    lines.append("endsolid PocketForge_Canonical\n")
    path.write_text("".join(lines), encoding="ascii", newline="\n")


def _metric_decimal(value: Any) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise StlError(f"invalid metric number: {value!r}") from exc
    if not result.is_finite():
        raise StlError(f"non-finite metric number: {value!r}")
    return result


def _metric_delta_text(candidate: Any, baseline: Any) -> str:
    return _exact_decimal_text(
        _metric_decimal(candidate) - _metric_decimal(baseline)
    )


def metric_delta(
    baseline: Mapping[str, Any] | None,
    candidate: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    """Describe deterministic numeric/topology deltas between mesh metrics."""
    if baseline is None:
        return None
    bounds_delta = {
        field: [
            _metric_delta_text(
                candidate["bounds_mm"][field][index],
                value,
            )
            for index, value in enumerate(baseline["bounds_mm"][field])
        ]
        for field in ("min", "max", "size")
    }
    topology_delta = {
        field: int(candidate["topology"][field]) - int(value)
        for field, value in sorted(baseline["topology"].items())
    }
    return {
        "bounds_mm": bounds_delta,
        "fingerprint_changed": (
            candidate["fingerprint"] != baseline["fingerprint"]
        ),
        "surface_area_mm2": _metric_delta_text(
            candidate["surface_area_mm2"],
            baseline["surface_area_mm2"],
        ),
        "topology": topology_delta,
        "triangle_count": (
            int(candidate["triangle_count"])
            - int(baseline["triangle_count"])
        ),
        "volume_mm3": _metric_delta_text(
            candidate["volume_mm3"],
            baseline["volume_mm3"],
        ),
    }


def quantize_coordinate(value: Decimal) -> int:
    """Map millimetres to the v1 integer coordinate grid."""
    scaled = (value / COORDINATE_QUANTUM_MM).to_integral_value(
        rounding=ROUND_HALF_EVEN
    )
    result = int(scaled)
    # Decimal("-0") already becomes int(0); keep this explicit as part of the
    # signed-zero normalization contract.
    return 0 if result == 0 else result


def quantize_points(points: Iterable[RawPoint]) -> list[QuantizedPoint]:
    return [
        (
            quantize_coordinate(point[0]),
            quantize_coordinate(point[1]),
            quantize_coordinate(point[2]),
        )
        for point in points
    ]


def triangles(points: Sequence[QuantizedPoint]) -> list[QuantizedTriangle]:
    if not points or len(points) % 3:
        raise StlError(f"invalid STL vertex count: {len(points)}")
    return [
        (points[offset], points[offset + 1], points[offset + 2])
        for offset in range(0, len(points), 3)
    ]


def canonical_triangles(
    mesh_triangles: Iterable[QuantizedTriangle],
) -> list[QuantizedTriangle]:
    """Ignore facet order, winding, and each facet's starting vertex."""
    return sorted(
        tuple(sorted(triangle))  # type: ignore[arg-type]
        for triangle in mesh_triangles
    )


def normalized_mesh_sha256(
    mesh_triangles: Iterable[QuantizedTriangle],
) -> str:
    canonical = canonical_triangles(mesh_triangles)
    digest = hashlib.sha256()
    digest.update(SERIALIZATION_MAGIC)
    digest.update(struct.pack(">Q", len(canonical)))
    for triangle in canonical:
        for point in triangle:
            for coordinate in point:
                try:
                    digest.update(struct.pack(">q", coordinate))
                except struct.error as exc:
                    raise StlError(
                        f"coordinate outside normalized int64 range: {coordinate}"
                    ) from exc
    return digest.hexdigest()


def _point_mm(point: QuantizedPoint) -> tuple[float, float, float]:
    quantum = float(COORDINATE_QUANTUM_MM)
    return tuple(coordinate * quantum for coordinate in point)  # type: ignore[return-value]


def _fixed_decimal(value: float, places: int = 3) -> str:
    return f"{value:.{places}f}"


def _quanta_mm(coordinate: int) -> str:
    return format(Decimal(coordinate) * COORDINATE_QUANTUM_MM, ".4f")


class _DisjointSet:
    def __init__(self, size: int) -> None:
        self.parents = list(range(size))

    def find(self, item: int) -> int:
        while self.parents[item] != item:
            self.parents[item] = self.parents[self.parents[item]]
            item = self.parents[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parents[right_root] = left_root


def _topology(mesh_triangles: Sequence[QuantizedTriangle]) -> dict[str, int]:
    vertices = {point for triangle in mesh_triangles for point in triangle}
    edge_facets: dict[
        tuple[QuantizedPoint, QuantizedPoint], list[int]
    ] = defaultdict(list)

    for facet_index, triangle in enumerate(mesh_triangles):
        for left, right in ((0, 1), (1, 2), (2, 0)):
            edge = tuple(sorted((triangle[left], triangle[right])))
            edge_facets[edge].append(facet_index)  # type: ignore[index]

    sets = _DisjointSet(len(mesh_triangles))
    for facet_indexes in edge_facets.values():
        for facet_index in facet_indexes[1:]:
            sets.union(facet_indexes[0], facet_index)

    boundary_edges = sum(len(facets) == 1 for facets in edge_facets.values())
    nonmanifold_edges = sum(len(facets) > 2 for facets in edge_facets.values())
    components = len({sets.find(index) for index in range(len(mesh_triangles))})

    return {
        "vertices": len(vertices),
        "edges": len(edge_facets),
        "facets": len(mesh_triangles),
        "components": components,
        "boundary_edges": boundary_edges,
        "nonmanifold_edges": nonmanifold_edges,
        "euler_characteristic": len(vertices)
        - len(edge_facets)
        + len(mesh_triangles),
    }


def describe_mesh(path: Path) -> dict[str, object]:
    """Return the normalized identity and stable review metrics for one STL."""
    raw_points = read_stl_points(path)
    quantized = quantize_points(raw_points)
    mesh_triangles = triangles(quantized)
    flattened = [point for triangle in mesh_triangles for point in triangle]

    minimum = tuple(min(point[axis] for point in flattened) for axis in range(3))
    maximum = tuple(max(point[axis] for point in flattened) for axis in range(3))
    size = tuple(maximum[axis] - minimum[axis] for axis in range(3))
    if any(value <= 0 for value in size):
        raise StlError(f"degenerate STL bounds: {size}")

    area_terms: list[float] = []
    volume_terms: list[float] = []
    for triangle in mesh_triangles:
        a, b, c = (_point_mm(point) for point in triangle)
        ab = tuple(b[axis] - a[axis] for axis in range(3))
        ac = tuple(c[axis] - a[axis] for axis in range(3))
        cross = (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0],
        )
        area_terms.append(math.sqrt(sum(value * value for value in cross)) / 2)

        b_cross_c = (
            b[1] * c[2] - b[2] * c[1],
            b[2] * c[0] - b[0] * c[2],
            b[0] * c[1] - b[1] * c[0],
        )
        volume_terms.append(
            sum(a[axis] * b_cross_c[axis] for axis in range(3)) / 6
        )

    return {
        "fingerprint": {
            "algorithm": FINGERPRINT_ALGORITHM,
            "coordinate_quantum_mm": str(COORDINATE_QUANTUM_MM),
            "sha256": normalized_mesh_sha256(mesh_triangles),
        },
        "triangle_count": len(mesh_triangles),
        "bounds_mm": {
            "min": [_quanta_mm(value) for value in minimum],
            "max": [_quanta_mm(value) for value in maximum],
            "size": [_quanta_mm(value) for value in size],
        },
        "surface_area_mm2": _fixed_decimal(math.fsum(area_terms)),
        "volume_mm3": _fixed_decimal(abs(math.fsum(volume_terms))),
        "topology": _topology(mesh_triangles),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stl", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        result = describe_mesh(args.stl)
    except (OSError, StlError) as exc:
        raise SystemExit(f"mesh_fingerprint_error: {exc}") from exc

    print(
        json.dumps(
            result,
            indent=2 if args.pretty else None,
            sort_keys=True,
            separators=None if args.pretty else (",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
