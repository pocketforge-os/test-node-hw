#!/usr/bin/env python3
"""Verify the four straight reference faces on a right-angle checker STL."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from check_stl_topology import Triangle, triangles

COORD_TOLERANCE = 1e-4
AREA_TOLERANCE_MM2 = 0.05


def triangle_area(triangle: Triangle) -> float:
    a, b, c = triangle
    ab = tuple(b[axis] - a[axis] for axis in range(3))
    ac = tuple(c[axis] - a[axis] for axis in range(3))
    cross = (
        ab[1] * ac[2] - ab[2] * ac[1],
        ab[2] * ac[0] - ab[0] * ac[2],
        ab[0] * ac[1] - ab[1] * ac[0],
    )
    return math.sqrt(sum(value * value for value in cross)) / 2


def reference_face_area(
    facets: list[Triangle],
    *,
    fixed_axis: int,
    fixed_value: float,
    span_axis: int,
    span_start: float,
    span_end: float,
    thickness: float,
) -> float:
    area = 0.0
    for triangle in facets:
        if not all(
            abs(point[fixed_axis] - fixed_value) <= COORD_TOLERANCE
            for point in triangle
        ):
            continue
        if not all(
            span_start - COORD_TOLERANCE
            <= point[span_axis]
            <= span_end + COORD_TOLERANCE
            and -COORD_TOLERANCE
            <= point[2]
            <= thickness + COORD_TOLERANCE
            for point in triangle
        ):
            continue
        area += triangle_area(triangle)
    return area


def require_close(actual: float, expected: float, description: str) -> None:
    if abs(actual - expected) > AREA_TOLERANCE_MM2:
        raise SystemExit(
            f"{description}: area={actual:.6f} expected={expected:.6f}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stl", type=Path)
    parser.add_argument("--leg-length", type=float, required=True)
    parser.add_argument("--arm-width", type=float, required=True)
    parser.add_argument("--thickness", type=float, required=True)
    parser.add_argument("--inside-relief", type=float, required=True)
    parser.add_argument("--outside-chamfer", type=float, required=True)
    args = parser.parse_args()

    facets = triangles(args.stl)
    if not facets:
        raise SystemExit(f"empty STL: {args.stl}")

    points = [point for triangle in facets for point in triangle]
    mins = tuple(min(point[axis] for point in points) for axis in range(3))
    maxs = tuple(max(point[axis] for point in points) for axis in range(3))
    expected_mins = (0.0, 0.0, 0.0)
    expected_maxs = (
        args.leg_length,
        args.leg_length,
        args.thickness,
    )
    for axis, (actual, expected) in enumerate(zip(mins, expected_mins)):
        if abs(actual - expected) > COORD_TOLERANCE:
            raise SystemExit(
                f"unexpected minimum {'XYZ'[axis]}={actual:.6f}; "
                f"expected={expected:.6f}"
            )
    for axis, (actual, expected) in enumerate(zip(maxs, expected_maxs)):
        if abs(actual - expected) > COORD_TOLERANCE:
            raise SystemExit(
                f"unexpected maximum {'XYZ'[axis]}={actual:.6f}; "
                f"expected={expected:.6f}"
            )

    outside_length = args.leg_length - args.outside_chamfer
    inside_start = args.arm_width + args.inside_relief
    inside_length = args.leg_length - inside_start
    expected_outside_area = outside_length * args.thickness
    expected_inside_area = inside_length * args.thickness

    outer_horizontal = reference_face_area(
        facets,
        fixed_axis=1,
        fixed_value=0.0,
        span_axis=0,
        span_start=args.outside_chamfer,
        span_end=args.leg_length,
        thickness=args.thickness,
    )
    outer_vertical = reference_face_area(
        facets,
        fixed_axis=0,
        fixed_value=0.0,
        span_axis=1,
        span_start=args.outside_chamfer,
        span_end=args.leg_length,
        thickness=args.thickness,
    )
    inner_horizontal = reference_face_area(
        facets,
        fixed_axis=1,
        fixed_value=args.arm_width,
        span_axis=0,
        span_start=inside_start,
        span_end=args.leg_length,
        thickness=args.thickness,
    )
    inner_vertical = reference_face_area(
        facets,
        fixed_axis=0,
        fixed_value=args.arm_width,
        span_axis=1,
        span_start=inside_start,
        span_end=args.leg_length,
        thickness=args.thickness,
    )

    require_close(
        outer_horizontal,
        expected_outside_area,
        "outer horizontal reference face is interrupted",
    )
    require_close(
        outer_vertical,
        expected_outside_area,
        "outer vertical reference face is interrupted",
    )
    require_close(
        inner_horizontal,
        expected_inside_area,
        "inner horizontal reference face is interrupted",
    )
    require_close(
        inner_vertical,
        expected_inside_area,
        "inner vertical reference face is interrupted",
    )

    print(
        "right_angle_geometry=pass "
        f"file={args.stl} angle_deg=90.000 "
        f"outside_reference_mm={outside_length:.3f} "
        f"inside_reference_mm={inside_length:.3f} "
        f"bounds_mm={args.leg_length:.3f}x{args.leg_length:.3f}x"
        f"{args.thickness:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
