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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stl", type=Path)
    parser.add_argument("--expected-components", type=int, required=True)
    args = parser.parse_args()

    facets = triangles(args.stl)
    if not facets:
        raise SystemExit(f"empty STL: {args.stl}")

    normalized = [
        tuple(canonical(point) for point in triangle)
        for triangle in facets
    ]
    edge_counts: Counter[tuple[Point, Point]] = Counter()
    vertex_owner: dict[Point, int] = {}
    components = DisjointSet(len(normalized))
    for index, triangle in enumerate(normalized):
        if len(set(triangle)) != 3:
            raise SystemExit(f"degenerate facet {index}: {triangle}")
        for point in triangle:
            previous = vertex_owner.setdefault(point, index)
            components.union(index, previous)
        for start, finish in (
            (triangle[0], triangle[1]),
            (triangle[1], triangle[2]),
            (triangle[2], triangle[0]),
        ):
            edge_counts[tuple(sorted((start, finish)))] += 1

    invalid_edges = [
        (edge, count) for edge, count in edge_counts.items() if count != 2
    ]
    if invalid_edges:
        examples = ", ".join(
            f"{edge}:{count}" for edge, count in invalid_edges[:3]
        )
        raise SystemExit(
            "mesh is not closed edge-manifold: "
            f"invalid_edges={len(invalid_edges)} examples={examples}"
        )

    component_count = len(
        {components.find(index) for index in range(len(normalized))}
    )
    if component_count != args.expected_components:
        raise SystemExit(
            f"component_count={component_count} "
            f"expected={args.expected_components}"
        )

    print(
        "stl_topology=pass "
        f"file={args.stl} facets={len(normalized)} "
        f"edges={len(edge_counts)} components={component_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
