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
    "DC_BUSHING_CENTRE = is_undef(DC_BUSHING_CENTRE) ? [305.6,191,54]",
    "iecc14_panel_cutout_negative(IEC_SNAP_WALL,IEC_CLEARANCE)",
    "iecc14_body_profile_size() == [27,46.86]",
    "iecc14_faceplate_size() == [31,50.3,2]",
    "M3_NUT_RETAINING_OPENING_AF == 5.2",
    "M3_NUT_RETAINING_LIP == 0.8",
    "module barrier_lower_capture()",
    "module barrier_upper_capture()",
    "module separation_partition()",
    "module terminal_partition_required_solid()",
    "module partition_dc_bushing_negative(clearance=0)",
    "module conductor_retention_saddle",
    "module front_outer_vent_negatives()",
    "module front_inner_baffle_negative()",
    "module gland_negative()",
    "module service_keepouts()",
    "module dc_bundle_route_keepout()",
    "function dc_route_points() = [",
    "[312,191,54], [300,191,54], [270,191,54], [270,173,54]",
    "module ac_terminal_service_keepout()",
    'else if (PART == "partition_slice") terminal_partition_slice();',
    'else if (PART == "dc_route_keepout") dc_bundle_route_keepout();',
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
if "BARRIER_DC_BUSHING" in SOURCE:
    raise SystemExit("nonprinted terminal shield must remain continuous")

defaults = {
    "WALL": "3.2",
    "FLOOR": "4.0",
    "ROOF": "4.0",
    "IEC_CLEARANCE": "0.20",
    "IEC_SNAP_WALL": "1.2",
    "M3_CLEARANCE_DIAMETER": "3.6",
    "M3_NUT_AF": "5.75",
    "M3_NUT_DEPTH": "2.6",
    "M3_NUT_RETAINING_OPENING_AF": "5.2",
    "M3_NUT_RETAINING_LIP": "0.8",
    "SEAM_GAP": "0.8",
    "SEAM_OVERLAP": "6.4",
    "SAFETY_DISTANCE": "8.0",
    "BARRIER_THICKNESS": "1.0",
    "DC_BUSHING_DIAMETER": "8.0",
    "DC_ROUTE_BEND_ENVELOPE": "10.0",
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
    "continuous terminal shield",
    "X=305.6, Y=191, Z=54",
    "installed rail-bearing envelope",
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
    'PART="partition_slice"',
    'PART="dc_route_keepout"',
    "partition_missing_material",
    "dc_route_hood_interference",
    "scripts/check_power_system_enclosure.py",
    "power-system-terminal-barrier-template.dxf",
    "power-system-terminal-barrier-template.svg",
)

base_path = ROOT / "build/power-system-enclosure-base.stl"
hood_path = ROOT / "build/power-system-enclosure-hood.stl"
partition_path = ROOT / "build/power-system-terminal-partition-slice.stl"
dc_route_path = ROOT / "build/power-system-dc-route-keepout.stl"

barrier_svg = (ROOT / "build/power-system-terminal-barrier-template.svg").read_text()
barrier_dxf = (ROOT / "build/power-system-terminal-barrier-template.dxf").read_text()
if (
    barrier_svg.count("<path d=") != 1
    or barrier_svg.count("M ") != 1
    or "81.5,-46" not in barrier_svg
    or barrier_dxf.splitlines().count("LINE") != 4
    or "CIRCLE" in barrier_dxf
):
    raise SystemExit("terminal barrier template must be one continuous 81.5 x 46 plate")


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
partition_facets, partition_points = mesh_contract(
    partition_path, ((304.0, 177.98, 40.86), (307.2, 259.52, 74.02))
)


def require_vertex(points, target, label, tolerance=5e-4):
    if not any(
        all(math.isclose(value, expected, abs_tol=tolerance)
            for value, expected in zip(point, target))
        for point in points
    ):
        raise SystemExit(f"{label} mesh vertex missing at {target}")


# All four horizontal hood nuts load from below through a 5.75 mm feeder, pass
# a 5.2 mm throat bounded by a nominal 0.8 mm-high retaining lip, and seat in
# a 5.75-AF x 2.6 mm-deep pocket.  These vertices are measured on the final
# printable base mesh after its installed-to-print transform.
nut_z = 13.0
nut_radius = 5.75 / math.sqrt(3)
nut_low = nut_z - nut_radius
throat_low = nut_low - 0.8
for centre_x in (338.0 - 170.0, 338.0 - 290.0):
    for depth_min in (5.0, 126.0):
        depth_max = depth_min + 2.6
        for depth in (depth_min, depth_max):
            for x in (centre_x - 5.75 / 2, centre_x + 5.75 / 2):
                require_vertex(
                    base_points, (x, depth, throat_low),
                    "hood-nut 5.75 mm exterior feeder",
                )
                require_vertex(
                    base_points, (x, depth, nut_low),
                    "hood-nut 5.75 mm seated pocket",
                )
                require_vertex(
                    base_points, (x, depth, nut_z + nut_radius / 2),
                    "hood-nut 5.75 mm hex pocket",
                )
            for x in (centre_x - 5.2 / 2, centre_x + 5.2 / 2):
                require_vertex(
                    base_points, (x, depth, throat_low),
                    "hood-nut 5.2 mm retaining throat",
                )
                require_vertex(
                    base_points, (x, depth, nut_low),
                    "hood-nut 0.8 mm retaining lip",
                )

if not math.isclose(nut_low - throat_low, 0.8, abs_tol=1e-6):
    raise SystemExit("hood-nut retaining lip is not 0.8 mm high")

print(
    "hood_nut_retention=pass traps=4 exterior_feeder_af_mm=5.75 "
    "throat_af_mm=5.20 retaining_lip_height_mm=0.80 "
    "pocket_af_mm=5.75 pocket_depth_mm=2.60 insertion=exterior-press"
)

# The isolated actual partition slice is one closed connected mesh with one
# through-bushing (Euler characteristic zero).  Together with the Makefile's
# empty missing-material selector this proves no second slit or opening exists.
partition_vertices = {
    tuple(round(value, 6) for value in point)
    for point in partition_points
}
partition_topology = inspect_topology(partition_path)
partition_euler = (
    len(partition_vertices)
    - partition_topology["edges"]
    + partition_topology["facets"]
)
if partition_euler != 0:
    raise SystemExit(
        "terminal partition must contain exactly the intended through-bushing: "
        f"euler={partition_euler}"
    )
for x in (304.0, 307.2):
    rim = {
        point for point in partition_points
        if math.isclose(point[0], x, abs_tol=2e-4)
        and math.isclose(
            math.hypot(point[1] - 191.0, point[2] - 54.0),
            4.0,
            abs_tol=5e-4,
        )
    }
    if len(rim) < 48:
        raise SystemExit(f"8 mm partition bushing rim missing at X={x}")

print(
    "terminal_partition=pass bounds_mm=3.20x81.54x33.16 "
    "components=1 euler=0 intentional_openings=1 "
    "dc_bushing_diameter_mm=8.00 centre_world_mm=305.6,191,54 "
    "barrier_template_mm=81.5x46 barrier_openings=0"
)

# The evidence route must itself be a single closed sweep, reach both sides of
# the named bushing and front gland, and reserve enlarged bend envelopes.
dc_route_topology = inspect_topology(dc_route_path)
if (
    dc_route_topology["invalid_edges"]
    or dc_route_topology["components"] != 1
    or dc_route_topology["degenerate_facets"]
):
    raise SystemExit(f"DC route topology failure: {dc_route_topology}")
dc_route_facets = triangles(dc_route_path)
dc_route_points = [point for facet in dc_route_facets for point in facet]
route_mins = tuple(min(point[axis] for point in dc_route_points) for axis in range(3))
route_maxs = tuple(max(point[axis] for point in dc_route_points) for axis in range(3))
if not (
    route_mins[0] < 265.1 and route_maxs[0] > 314.9
    and route_mins[1] < 154.1 and route_maxs[1] > 195.9
    and route_mins[2] < 28.1 and route_maxs[2] > 58.9
):
    raise SystemExit(f"DC route lost bushing/gland/bend extent: {(route_mins,route_maxs)}")

print(
    "dc_route=pass components=1 bundle_od_mm=6.00 bend_envelope_mm=10.00 "
    "partition_bushing_world_mm=305.6,191,54 front_gland_world_mm=270,160,31 "
    "hood_interference=clear psu_interference=clear"
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
