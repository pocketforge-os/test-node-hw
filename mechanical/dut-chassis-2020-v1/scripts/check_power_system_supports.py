#!/usr/bin/env python3
"""Reject support-off hazards in the three V2 power-enclosure meshes."""

from __future__ import annotations

import argparse
import hashlib
import math
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_stl_topology import triangles  # noqa: E402

PARTS = {
    "base": ROOT / "build/power-system-enclosure-base.stl",
    "hood": ROOT / "build/power-system-enclosure-hood.stl",
    "cassette": ROOT / "build/power-system-enclosure-c14-cassette.stl",
}
PROFILE = ROOT / "scripts/prusaslicer-power-system-support-off.ini"
FORBIDDEN_SLICER_WARNINGS = (
    "Floating bridge anchors",
    "Long bridging extrusions",
)

# Exact print-Z bands which contained the verifier's three quantified defects.
# These are additional to the general large-level check below.
RISK_BANDS = {
    "base": (3.5, 4.5, "rear rail gusset underside"),
    "hood": (30.0, 50.0, "seam-lip underside"),
    "cassette": (2.0, 2.8, "cassette-key underside"),
}


def facet_normal_area(facet):
    a, b, c = facet
    u = tuple(b[index] - a[index] for index in range(3))
    v = tuple(c[index] - a[index] for index in range(3))
    normal = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )
    magnitude = math.sqrt(sum(value * value for value in normal))
    return normal, magnitude / 2


def downward_horizontal_levels(facets) -> dict[float, float]:
    levels: dict[float, float] = {}
    for facet in facets:
        normal, area = facet_normal_area(facet)
        magnitude = 2 * area
        if magnitude <= 1e-9 or min(point[2] for point in facet) <= 1e-4:
            continue
        if normal[2] / magnitude < -0.999999:
            level = round(sum(point[2] for point in facet) / 3, 3)
            levels[level] = levels.get(level, 0.0) + area
    return levels


def audit_facets(part: str, facets) -> dict[float, float]:
    levels = downward_horizontal_levels(facets)
    large = {level: area for level, area in levels.items() if area > 50.0}
    if large:
        raise ValueError(f"{part}: downward horizontal level exceeds 50 mm2: {large}")
    low, high, label = RISK_BANDS[part]
    band_area = sum(area for level, area in levels.items() if low <= level <= high)
    if band_area > 0.5:
        raise ValueError(
            f"{part}: {label} remains in print-Z {low:g}..{high:g}: "
            f"{band_area:.3f} mm2"
        )
    return levels


def discover_slicer(explicit: str) -> list[str] | None:
    if explicit:
        return shlex.split(explicit)
    for executable in ("prusa-slicer", "PrusaSlicer"):
        resolved = shutil.which(executable)
        if resolved:
            return [resolved]
    flatpak = shutil.which("flatpak")
    if flatpak:
        probe = subprocess.run(
            [flatpak, "info", "com.prusa3d.PrusaSlicer"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if probe.returncode == 0:
            # Bypass the Flatpak GUI entrypoint so an open single-instance GUI
            # cannot silently swallow an export request.
            return [
                flatpak,
                "run",
                "--command=prusa-slicer",
                "com.prusa3d.PrusaSlicer",
            ]
    return None


def run_slicer(command: list[str], profile: Path) -> None:
    version = subprocess.run(
        command + ["--help"], capture_output=True, text=True, check=False
    )
    version_text = version.stdout + version.stderr
    match = re.search(r"PrusaSlicer-(\d+\.\d+\.\d+)", version_text)
    if version.returncode or not match:
        raise SystemExit("unable to identify PrusaSlicer CLI version")
    if match.group(1) != "2.9.6":
        raise SystemExit(
            f"support-off slicer gate requires PrusaSlicer 2.9.6, got {match.group(1)}"
        )

    profile_hash = hashlib.sha256(profile.read_bytes()).hexdigest()
    audit_dir = ROOT / "build/power-system-support-audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    manifest_lines = [
        f"prusaslicer_version={match.group(1)}",
        f"profile={profile.relative_to(ROOT)}",
        f"profile_sha256={profile_hash}",
    ]
    required_gcode = (
        "; nozzle_diameter = 0.8",
        "; layer_height = 0.4",
        "; support_material = 0",
        "; variable_layer_height = 0",
        "; filament_type = ABS",
    )

    for part, mesh in PARTS.items():
        gcode = audit_dir / f"{part}.gcode"
        log = audit_dir / f"{part}.log"
        gcode.unlink(missing_ok=True)
        invocation = command + [
            "--loglevel",
            "3",
            "--threads",
            "1",
            "--load",
            str(profile),
            "--export-gcode",
            "--output",
            str(gcode),
            str(mesh),
        ]
        result = subprocess.run(invocation, capture_output=True, text=True, check=False)
        output = result.stdout + result.stderr
        log.write_text(output)
        manifest_lines.append(f"{part}_command={shlex.join(invocation)}")
        if result.returncode or not gcode.is_file() or gcode.stat().st_size == 0:
            raise SystemExit(
                f"PrusaSlicer export failed for {part}; see {log.relative_to(ROOT)}"
            )
        found = [warning for warning in FORBIDDEN_SLICER_WARNINGS if warning in output]
        if found:
            raise SystemExit(
                f"support-off slicer gate failed for {part}: {', '.join(found)}"
            )
        gcode_tail = gcode.read_text(errors="replace")[-65536:]
        missing = [line for line in required_gcode if line not in gcode_tail]
        if missing:
            raise SystemExit(f"PrusaSlicer profile drift for {part}: missing {missing}")

    manifest = audit_dir / "manifest.txt"
    manifest.write_text("\n".join(manifest_lines) + "\n")
    print(
        "power_system_support_slicer=pass "
        f"version={match.group(1)} nozzle_mm=0.8 layer_mm=0.4 supports=off "
        f"profile_sha256={profile_hash} parts=3"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, default=PROFILE)
    parser.add_argument("--slicer-command", default=os.environ.get("PRUSA_SLICER", ""))
    parser.add_argument("--allow-missing-slicer", action="store_true")
    args = parser.parse_args()

    for part, mesh in PARTS.items():
        levels = audit_facets(part, triangles(mesh))
        summary = ",".join(f"{level:g}:{area:.3f}" for level, area in sorted(levels.items()))
        print(f"power_system_support_geometry=pass part={part} downward_levels={summary or 'none'}")

    command = discover_slicer(args.slicer_command)
    if command is None:
        if args.allow_missing_slicer:
            print("power_system_support_slicer=skip reason=prusaslicer-2.9.6-unavailable")
            return
        raise SystemExit(
            "PrusaSlicer 2.9.6 is required; install it or set PRUSA_SLICER to its CLI command"
        )
    run_slicer(command, args.profile.resolve())


if __name__ == "__main__":
    main()
