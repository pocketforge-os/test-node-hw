#!/usr/bin/env python3
"""Export and bound every registered carrier title with the locked CAD stack."""

from __future__ import annotations

import argparse
import subprocess
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Sequence

import holder_profiles
import mesh_fingerprint
import qualified_geometry


ROOT = Path(__file__).resolve().parent.parent
TOLERANCE_MM = Decimal("0.0001")


class TitleAuditError(ValueError):
    """A carrier title could not be proved safely inset."""


def _decimal(value: Any) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def title_clearances(
    points: Sequence[mesh_fingerprint.RawPoint],
    title: Mapping[str, Any],
) -> tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal], tuple[Decimal, ...]]:
    if not points:
        raise TitleAuditError("title export contains no mesh points")
    mesh_min = tuple(min(point[axis] for point in points) for axis in range(2))
    mesh_max = tuple(max(point[axis] for point in points) for axis in range(2))
    box_size = tuple(_decimal(value) for value in title["title_box_size_mm"])
    box_center = tuple(
        _decimal(value) for value in title["title_box_center_mm"]
    )
    border_inset = _decimal(title["border_inner_inset_mm"])
    inner_min = tuple(
        box_center[axis] - box_size[axis] / 2 + border_inset
        for axis in range(2)
    )
    inner_max = tuple(
        box_center[axis] + box_size[axis] / 2 - border_inset
        for axis in range(2)
    )
    clearances = (
        mesh_min[0] - inner_min[0],
        inner_max[0] - mesh_max[0],
        mesh_min[1] - inner_min[1],
        inner_max[1] - mesh_max[1],
    )
    return mesh_min, mesh_max, clearances


def _render_title(
    resolved: holder_profiles.ResolvedProfile,
    variant: Mapping[str, Any],
    title: Mapping[str, Any],
    output: Path,
    openscad: str,
) -> None:
    carrier = variant["production_carrier"]
    title_recipe = {
        "source": carrier["source"],
        "part": "title_text",
        "parameters": carrier["parameters"],
    }
    command = holder_profiles.recipe_command(
        resolved,
        title_recipe,
        output,
        openscad=openscad,
        parameter_overrides={
            "EXPECTED_TITLE_BOX_SIZE": title["title_box_size_mm"],
            "EXPECTED_TITLE_BOX_CENTRE": title["title_box_center_mm"],
            "EXPECTED_TITLE_FONT_SIZE": title["title_font_size_mm"],
            "EXPECTED_TITLE_BORDER_INSET": title["border_inner_inset_mm"],
        },
    )
    result = subprocess.run(
        command,
        cwd=resolved.root,
        check=False,
        capture_output=True,
        text=True,
    )
    diagnostics = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    errors = [
        line for line in diagnostics.splitlines() if line.startswith("ERROR:")
    ]
    if result.returncode != 0 or errors:
        raise TitleAuditError(
            f"OpenSCAD title export failed for {variant['device_slug']} "
            f"rc={result.returncode}: {diagnostics}"
        )
    if not output.is_file() or output.stat().st_size == 0:
        raise TitleAuditError(
            f"OpenSCAD produced no title mesh for {variant['device_slug']}"
        )


def audit_all(root: Path, output_dir: Path, openscad: str) -> int:
    qualified_geometry.check_toolchain(
        root / "qualification/cad-toolchain.json",
        openscad,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    audited = 0
    for profile_path in sorted((root / "profiles").glob("*.json")):
        resolved = holder_profiles.validate_profile(root, profile_path)
        title = resolved.document["carrier_title"]
        required = _decimal(title["minimum_text_clearance_mm"])
        for device_slug in sorted(resolved.variants):
            variant = resolved.variants[device_slug]
            output = output_dir / f"{device_slug}.stl"
            _render_title(resolved, variant, title, output, openscad)
            try:
                points = mesh_fingerprint.read_stl_points(output)
            except mesh_fingerprint.StlError as exc:
                raise TitleAuditError(
                    f"invalid title mesh for {device_slug}: {exc}"
                ) from exc
            mesh_min, mesh_max, clearances = title_clearances(points, title)
            if any(value + TOLERANCE_MM < required for value in clearances):
                rendered = ",".join(f"{value:.4f}" for value in clearances)
                raise TitleAuditError(
                    f"carrier_title_inset=fail device={device_slug} "
                    f"clearances_lrtb_mm={rendered} required_mm={required}"
                )
            size = tuple(mesh_max[axis] - mesh_min[axis] for axis in range(2))
            rendered_clearances = ",".join(
                f"{value:.4f}" for value in clearances
            )
            print(
                f"carrier_title_inset=pass device={device_slug} "
                f"font_size_mm={title['title_font_size_mm']} "
                f"mesh_size_mm={size[0]:.4f}x{size[1]:.4f} "
                f"clearances_lrtb_mm={rendered_clearances} "
                f"required_mm={required} output={output}"
            )
            audited += 1
    if audited == 0:
        raise TitleAuditError("no registered carrier titles were found")
    print(f"carrier_title_audit=pass devices={audited}")
    return audited


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "build/checks/carrier-titles",
    )
    parser.add_argument("--openscad", default="openscad")
    args = parser.parse_args()
    audit_all(args.root.resolve(), args.output_dir.resolve(), args.openscad)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
