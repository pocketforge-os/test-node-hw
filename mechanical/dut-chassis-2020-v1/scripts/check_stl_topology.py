#!/usr/bin/env python3
"""Check that an STL is closed, edge-manifold, and has N components."""

from __future__ import annotations

import argparse
import struct
from collections import Counter
from pathlib import Path
from typing import Iterator

Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]


def binary_triangles(data: bytes) -> Iterator[Triangle]:
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    expected = 84 + triangle_count * 50
    if expected != len(data):
        raise ValueError("not a canonical binary STL")
    offset = 84
    for _ in range(triangle_count):
        values = struct.unpack_from("<12fH", data, offset)
        yield (
            (values[3], values[4], values[5]),
            (values[6], values[7], values[8]),
            (values[9], values[10], values[11]),
        )
        offset += 50


def ascii_triangles(data: bytes) -> Iterator[Triangle]:
    vertices: list[Point] = []
    for raw_line in data.decode("ascii", errors="strict").splitlines():
        fields = raw_line.strip().split()
        if len(fields) == 4 and fields[0] == "vertex":
            vertices.append(tuple(float(value) for value in fields[1:]))
    if len(vertices) % 3:
        raise ValueError("ASCII STL vertex count is not divisible by three")
    for offset in range(0, len(vertices), 3):
        yield tuple(vertices[offset : offset + 3])  # type: ignore[return-value]


def triangles(path: Path) -> list[Triangle]:
    data = path.read_bytes()
    if len(data) >= 84:
        try:
            return list(binary_triangles(data))
        except ValueError:
            pass
    return list(ascii_triangles(data))


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def canonical(point: Point) -> Point:
    return tuple(round(value, 6) for value in point)  # type: ignore[return-value]


def inspect_topology(path: Path) -> dict[str, int]:
    """Return stable 1e-6 mm edge-incidence and component metrics."""
    facets = triangles(path)
    if not facets:
        raise ValueError(f"empty STL: {path}")

    normalized = [
        tuple(canonical(point) for point in triangle)
        for triangle in facets
    ]
    edge_counts: Counter[tuple[Point, Point]] = Counter()
    vertex_owner: dict[Point, int] = {}
    components = DisjointSet(len(normalized))
    degenerate_facets = 0
    for index, triangle in enumerate(normalized):
        if len(set(triangle)) != 3:
            degenerate_facets += 1
        for point in triangle:
            previous = vertex_owner.setdefault(point, index)
            components.union(index, previous)
        for start, finish in (
            (triangle[0], triangle[1]),
            (triangle[1], triangle[2]),
            (triangle[2], triangle[0]),
        ):
            edge_counts[tuple(sorted((start, finish)))] += 1

    invalid_edges = sum(count != 2 for count in edge_counts.values())
    component_count = len(
        {components.find(index) for index in range(len(normalized))}
    )
    return {
        "facets": len(normalized),
        "edges": len(edge_counts),
        "components": component_count,
        "invalid_edges": invalid_edges,
        "degenerate_facets": degenerate_facets,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stl", type=Path)
    parser.add_argument("--expected-components", type=int, required=True)
    args = parser.parse_args()

    try:
        result = inspect_topology(args.stl)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if result["degenerate_facets"]:
        raise SystemExit(
            f"mesh has degenerate facets: {result['degenerate_facets']}"
        )
    if result["invalid_edges"]:
        raise SystemExit(
            "mesh is not closed edge-manifold: "
            f"invalid_edges={result['invalid_edges']}"
        )

    if result["components"] != args.expected_components:
        raise SystemExit(
            f"component_count={result['components']} "
            f"expected={args.expected_components}"
        )

    print(
        "stl_topology=pass "
        f"file={args.stl} facets={result['facets']} "
        f"edges={result['edges']} components={result['components']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
