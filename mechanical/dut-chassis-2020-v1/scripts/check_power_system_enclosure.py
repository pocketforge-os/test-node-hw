#!/usr/bin/env python3
"""Focused source/mesh contracts for the pre-DUT02 power enclosure."""

from pathlib import Path
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "power-system-enclosure.scad").read_text()
DOC = (ROOT / "POWER_SYSTEM_ENCLOSURE.md").read_text()
MAKEFILE = (ROOT / "Makefile").read_text()
sys.path.insert(0, str(ROOT / "scripts"))
from check_stl_topology import inspect_topology, triangles  # noqa: E402


def require(text: str, *fragments: str) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise SystemExit(f"power enclosure contract missing: {missing}")


require(
    SOURCE,
    "include <lib/alt-1205t-power-supply.scad>",
    "include <lib/iec-c14-fused-switch.scad>",
    'PART = is_undef(PART) ? "assembly" : PART;',
    'if (PART == "base") printable_base();',
    'else if (PART == "hood") printable_hood();',
    'else if (PART == "barrier_template") barrier_template_2d();',
    'else if (PART == "assembly") assembly_evidence(false);',
    'else if (PART == "installed_preview") installed_preview();',
    "function enclosure_outer_min() = [190, 160, 0]",
    "function enclosure_outer_max() = [326, 300, 78]",
    "function enclosure_rail_min() = [322.8, 117.73, 0]",
    "function enclosure_rail_max() = [326, 338, 20]",
    "[[125.73,10], [149.73,10], [306,10], [330,10]]",
    "function enclosure_psu_origin() = [194, 257.5, 4]",
    "function enclosure_psu_rotation() = [0,0,-90]",
    "function enclosure_psu_keepout_min() = [194,180,4]",
    "function enclosure_psu_keepout_max() = [304,257.5,40.86]",
    "alt1205t_upper_left_m3_centre() == [4.95,4.95]",
    "alt1205t_lower_left_m3_centre() == [6.75,98.6]",
    "[[25.3,30.9],[25.3,67],[53.3,67]]",
    "function enclosure_c14_origin() = [308,300,49.15]",
    "function enclosure_c14_rotation() = [90,0,0]",
    "function enclosure_c14_face_direction() = [0,1,0]",
    "iecc14_panel_cutout_negative(IEC_SNAP_WALL,IEC_CLEARANCE)",
    "iecc14_body_profile_size() == [27,46.86]",
    "iecc14_faceplate_size() == [31,50.3,2]",
    "M3_NUT_RETAINING_OPENING_AF < M3_NUT_AF",
    "module barrier_lower_capture()",
    "module barrier_upper_capture()",
    "module separation_partition()",
    "module conductor_retention_saddle",
    "module front_outer_vent_negatives()",
    "module front_inner_baffle_negative()",
    "module gland_negative()",
    "module service_keepouts()",
    "AC_TERMINAL_PROJECTION = is_undef(AC_TERMINAL_PROJECTION)",
    "AC_WIRE_BEND_RADIUS = is_undef(AC_WIRE_BEND_RADIUS)",
    "IEC_TERMINAL_PROJECTION = is_undef(IEC_TERMINAL_PROJECTION)",
    "PE_LUG_SERVICE_DIAMETER = is_undef(PE_LUG_SERVICE_DIAMETER)",
    "DC_CONDUCTOR_COUNT = is_undef(DC_CONDUCTOR_COUNT)",
    "DC_CONDUCTOR_GAUGE_AWG = is_undef(DC_CONDUCTOR_GAUGE_AWG)",
    "DC_BUNDLE_OD = is_undef(DC_BUNDLE_OD)",
    "DC_GLAND_CUTOUT_DIAMETER = is_undef(DC_GLAND_CUTOUT_DIAMETER)",
    "SAFETY_DISTANCE >= 8",
    "SEAM_GAP <= 1.0",
    "SEAM_OVERLAP >= 2*WALL",
    "VENT_SLOT <= 1.6",
    "VENT_PLENUM >= 10",
    "enclosure_psu_keepout_min().x-(enclosure_outer_min().x+WALL) >= 0.8",
)

if "text(" in SOURCE:
    raise SystemExit("printable enclosure source must contain no text geometry")

defaults = {
    "WALL": "3.2",
    "FLOOR": "4.0",
    "ROOF": "4.0",
    "IEC_CLEARANCE": "0.20",
    "IEC_SNAP_WALL": "1.2",
    "M3_CLEARANCE_DIAMETER": "3.6",
    "M3_NUT_AF": "5.75",
    "M3_NUT_DEPTH": "2.6",
    "SEAM_GAP": "0.8",
    "SEAM_OVERLAP": "6.4",
    "SAFETY_DISTANCE": "8.0",
    "BARRIER_THICKNESS": "1.0",
    "BARRIER_DC_BUSHING_DIAMETER": "8.0",
    "DC_CONDUCTOR_COUNT": "2",
    "DC_CONDUCTOR_GAUGE_AWG": "18",
    "DC_BUNDLE_OD": "6.0",
    "DC_GLAND_CUTOUT_DIAMETER": "12.5",
    "VENT_SLOT": "1.6",
    "VENT_PLENUM": "10.0",
}
for name, expected in defaults.items():
    pattern = rf"{name} = is_undef\({name}\) \? ([0-9.]+) : {name};"
    match = re.search(pattern, SOURCE)
    if not match or match.group(1) != expected:
        raise SystemExit(f"{name} must remain overridable with default {expected}")

require(
    DOC,
    "pre-DUT02 mechanical prototype",
    "not a certified mains",
    "Always unplug",
    "X=190..326, Y=160..300, Z=0..78",
    "0.8 mm nominal side clearance",
    "1.2 mm",
    "true +0.20 mm contour clearance",
    "Fuse remains",
    "TBD",
    "protective-earth",
    "Printed parts and hood",
    "screws are never part of protective-earth bonding",
    "No PSU chassis bonding hole",
    "M12/PG7-class",
    "flammability",
    "full-load thermal/ventilation test",
    "No certification or powered-use approval",
)

require(
    MAKEFILE,
    "power-system-enclosure: $(POWER_SYSTEM_ENCLOSURE_BASE)",
    'PART="base"',
    'PART="hood"',
    'PART="barrier_template"',
    'PART="evidence_top"',
    'PART="evidence_rear"',
    'PART="evidence_section"',
    "scripts/check_power_system_enclosure.py",
    "power-system-terminal-barrier-template.dxf",
    "power-system-terminal-barrier-template.svg",
)

base_path = ROOT / "build/power-system-enclosure-base.stl"
hood_path = ROOT / "build/power-system-enclosure-hood.stl"


def mesh_contract(path: Path, expected_bounds: tuple[tuple[float, ...], tuple[float, ...]]):
    topology = inspect_topology(path)
    if topology["invalid_edges"] or topology["components"] != 1 or topology["degenerate_facets"]:
        raise SystemExit(f"mesh topology failure for {path.name}: {topology}")
    facets = triangles(path)
    points = [point for triangle in facets for point in triangle]
    mins = tuple(min(p[axis] for p in points) for axis in range(3))
    maxs = tuple(max(p[axis] for p in points) for axis in range(3))
    if (mins, maxs) != expected_bounds:
        raise SystemExit(
            f"mesh bounds changed for {path.name}: expected={expected_bounds} got={(mins,maxs)}"
        )
    return facets, points


base_facets, base_points = mesh_contract(
    base_path, ((0.0, 0.0, 0.0), (220.27, 136.0, 20.0))
)
hood_facets, hood_points = mesh_contract(
    hood_path, ((0.0, 0.0, 0.0), (136.0, 140.0, 74.0))
)

# The five approved M3 centers survive the installed-to-print transform.  The
# library's -0.01 overlap can create both 3.99 and 4.00 rim planes.
for u, v in ((4.95, 4.95), (25.3, 30.9), (25.3, 67.0),
             (53.3, 67.0), (6.75, 98.6)):
    centre = (80.5 + u, 4.0 + v)
    rim = {
        point for point in base_points
        if math.isclose(
            math.hypot(point[0] - centre[0], point[1] - centre[1]),
            1.8,
            abs_tol=5e-4,
        )
    }
    if len(rim) < 60 or not {3.99, 4.0}.issubset({point[2] for point in rim}):
        raise SystemExit(f"approved PSU M3 rim missing at local {(u,v)} / print {centre}")

# Four rail holes remain exactly on their existing Y/Z axes; print rotation
# maps world Y to X and the world X hole axis to printer Y.
for world_y in (125.73, 149.73, 306.0, 330.0):
    centre_xz = (338.0 - world_y, 10.0)
    rim = {
        point for point in base_points
        if point[1] > 132.7
        and math.isclose(
            math.hypot(point[0] - centre_xz[0], point[2] - centre_xz[1]),
            1.8,
            abs_tol=5e-4,
        )
    }
    if len(rim) < 60 or {132.8, 136.0} != {point[1] for point in rim}:
        raise SystemExit(f"rail M3 axis changed at world Y={world_y}")

# In roof-down hood coordinates the approved clearanced C14 contour spans
# print Y=0..1.2 through the local snap island.  The six contour corners are
# inherited from the reusable component negative.
c14_vertices = (
    (104.3, 52.48), (104.3, 11.1498),
    (109.9139, 5.22), (126.0861, 5.22),
    (131.7, 11.1498), (131.7, 52.48),
)
hood_points_set = set(hood_points)
for x, z in c14_vertices:
    for y in (0.0, 1.2):
        if not any(
            math.isclose(px, x, abs_tol=2e-4)
            and math.isclose(py, y, abs_tol=2e-4)
            and math.isclose(pz, z, abs_tol=2e-4)
            for px, py, pz in hood_points_set
        ):
            raise SystemExit(f"approved C14 snap-island contour missing at {(x,y,z)}")

# No exterior vent aperture is wider than 1.6 mm in Z, and the inner bank is
# explicitly half a pitch out of alignment with the outer bank.
if "enclosure_front_vent_z0()+VENT_PITCH/2" not in SOURCE:
    raise SystemExit("inner vent bank lost its half-pitch labyrinth offset")


def signed_volume(facets) -> float:
    total = 0.0
    for a, b, c in facets:
        total += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
    return abs(total)


base_volume = signed_volume(base_facets)
hood_volume = signed_volume(hood_facets)
if base_volume <= 0 or hood_volume <= 0:
    raise SystemExit("printable enclosure mesh volume must be positive")

print(
    "power_system_enclosure_contract=pass "
    "parts=2 topology=closed-connected print_text=none "
    "world_bounds_mm=190..326x160..300x0..78 "
    "psu_side_clearance_mm=0.8 c14_profile_mm=27x46.86 "
    "c14_clearance_per_side_mm=0.20 c14_snap_wall_mm=1.2 "
    "rail_axes_y_mm=125.73,149.73,306,330 "
    f"base_volume_mm3={base_volume:.3f} hood_volume_mm3={hood_volume:.3f}"
)
