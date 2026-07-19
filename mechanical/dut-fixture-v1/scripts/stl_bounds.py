#!/usr/bin/env python3
"""Report STL mesh bounds and enforce a printer envelope using only stdlib."""

from __future__ import annotations

import argparse
import math
import struct
from pathlib import Path
from typing import Iterable, Iterator, Tuple

Point = Tuple[float, float, float]


def binary_vertices(data: bytes) -> Iterator[Point]:
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    expected = 84 + triangle_count * 50
    if expected != len(data):
        raise ValueError("not a canonical binary STL")
    offset = 84
    for _ in range(triangle_count):
        # Skip 12-byte normal, read 3 vertices, skip 2-byte attribute count.
        values = struct.unpack_from("<12fH", data, offset)
        yield values[3], values[4], values[5]
        yield values[6], values[7], values[8]
        yield values[9], values[10], values[11]
        offset += 50


def ascii_vertices(data: bytes) -> Iterator[Point]:
    for raw_line in data.decode("ascii", errors="strict").splitlines():
        fields = raw_line.strip().split()
        if len(fields) == 4 and fields[0] == "vertex":
            yield tuple(float(value) for value in fields[1:])  # type: ignore[return-value]


def vertices(path: Path) -> Iterable[Point]:
    data = path.read_bytes()
    if len(data) >= 84:
        try:
            yield from binary_vertices(data)
            return
        except ValueError:
            pass
    yield from ascii_vertices(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stl", type=Path)
    parser.add_argument("--max-x", type=float)
    parser.add_argument("--max-y", type=float)
    parser.add_argument("--max-z", type=float)
    args = parser.parse_args()

    points = list(vertices(args.stl))
    if not points or len(points) % 3:
        raise SystemExit(f"invalid STL: vertex_count={len(points)}")
    if not all(math.isfinite(value) for point in points for value in point):
        raise SystemExit("invalid STL: non-finite coordinate")

    mins = tuple(min(point[axis] for point in points) for axis in range(3))
    maxs = tuple(max(point[axis] for point in points) for axis in range(3))
    size = tuple(maxs[axis] - mins[axis] for axis in range(3))
    if any(value <= 0 for value in size):
        raise SystemExit(f"invalid STL: degenerate bounds {size}")

    limits = (args.max_x, args.max_y, args.max_z)
    axes = "XYZ"
    for axis, limit in enumerate(limits):
        if limit is not None and size[axis] > limit + 1e-6:
            raise SystemExit(
                f"oversize: {axes[axis]}={size[axis]:.3f} mm > {limit:.3f} mm"
            )

    signed_volume_mm3 = 0.0
    for offset in range(0, len(points), 3):
        a, b, c = points[offset : offset + 3]
        b_cross_c = (
            b[1] * c[2] - b[2] * c[1],
            b[2] * c[0] - b[0] * c[2],
            b[0] * c[1] - b[1] * c[0],
        )
        signed_volume_mm3 += sum(a[axis] * b_cross_c[axis] for axis in range(3)) / 6
    volume_cm3 = abs(signed_volume_mm3) / 1000

    print(
        f"file={args.stl} triangles={len(points) // 3} "
        f"min={','.join(f'{v:.3f}' for v in mins)} "
        f"max={','.join(f'{v:.3f}' for v in maxs)} "
        f"size={','.join(f'{v:.3f}' for v in size)} "
        f"volume_cm3={volume_cm3:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
