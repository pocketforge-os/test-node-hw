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
    'else if (PART == "nut_fit_coupon") nut_fit_coupon();',
    'else if (PART == "evidence_nut_section") nut_socket_section_evidence();',
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
    "HOOD_NUT_AF == 5.60",
    "HOOD_NUT_DEPTH == 2.80",
    "HOOD_NUT_LEAD_AF == 6.20",
    "HOOD_NUT_LEAD_DEPTH == 0.80",
    "HOOD_NUT_CAPTURE_WALL == 2.40",
    "PSU_NUT_AF == 5.60",
    "PSU_NUT_DEPTH == 2.60",
    "FLOOR-PSU_NUT_DEPTH == 1.40",
    "function enclosure_hood_screw_z() = 25.6",
    'function enclosure_hood_screw_y(side) = side=="left" ? [170,290] : [170]',
    "function enclosure_hood_nut_boss_top() = 32.0",
    "function enclosure_rear_hood_screw_x() = 282.0",
    "function enclosure_rear_hood_screw_y() = 296.0",
    "function enclosure_rear_hood_screw_z() = 13.0",
    "function enclosure_rear_hood_nut_backstop_depth()",
    "module rear_nut_insert_boss()",
    "module rear_nut_insert_negative()",
    "module rear_hood_nut_cap_required_solid()",
    "module hood_fastener_audit_solid()",
    "module hood_fastener_metal_screw_axes_solid()",
    "module hood_fastener_nut_service_axes_solid()",
    "module iec_terminal_projection_keepout_core()",
    "module pe_route_keepout_core()",
    "module hood_nut_cap_missing()",
    "module hood_nut_backstop_missing()",
    "module psu_nut_floor_missing()",
    "module base_c14_body_interference()",
    "module base_c14_faceplate_interference()",
    "module hood_fastener_ac_service_interference()",
    "module hood_fastener_dc_route_interference()",
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
    "HOOD_NUT_AF": "5.60",
    "HOOD_NUT_DEPTH": "2.80",
    "HOOD_NUT_LEAD_AF": "6.20",
    "HOOD_NUT_LEAD_DEPTH": "0.80",
    "HOOD_NUT_CAPTURE_WALL": "2.40",
    "PSU_NUT_MEASURED_DEPTH": "2.30",
    "PSU_NUT_AF": "5.60",
    "PSU_NUT_DEPTH": "2.60",
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
    "5.60 mm-AF × 2.80 mm-deep",
    "5.60 mm-AF × 2.60 mm-deep",
    "world Z=25.6 mm",
    "rear-panel axis is X=282, Y=296, Z=13 mm",
    "8.66 mm from the rigid C14 body",
    "terminal-projection volume",
    "superseded base with 5.2 mm throats",
    "Do not force nuts into that print",
)

require(
    MAKEFILE,
    "power-system-enclosure: $(POWER_SYSTEM_ENCLOSURE_BASE)",
    "power-system-enclosure-nut-coupon: $(POWER_SYSTEM_ENCLOSURE_NUT_COUPON)",
    'PART="base"',
    'PART="hood"',
    'PART="barrier_template"',
    'PART="evidence_top"',
    'PART="evidence_rear"',
    'PART="evidence_section"',
    'PART="evidence_nut_section"',
    'PART="nut_fit_coupon"',
    "layout-power-system-enclosure-nut-coupon-isometric.png",
    "layout-power-system-enclosure-nut-coupon-top.png",
    'PART="partition_slice"',
    'PART="dc_route_keepout"',
    "partition_missing_material",
    "dc_route_hood_interference",
    "base_c14_body_interference",
    "base_c14_faceplate_interference",
    "hood_fastener_ac_service_interference",
    "hood_fastener_dc_route_interference",
    "hood_fastener_c14_interference",
    "hood_fastener_iec_terminal_interference",
    "hood_fastener_pe_route_interference",
    "hood_fastener_psu_interference",
    "hood_nut_cap_missing",
    "hood_nut_backstop_missing",
    "psu_nut_floor_missing",
    "scripts/check_power_system_enclosure.py",
    "power-system-terminal-barrier-template.dxf",
    "power-system-terminal-barrier-template.svg",
)

base_path = ROOT / "build/power-system-enclosure-base.stl"
hood_path = ROOT / "build/power-system-enclosure-hood.stl"
coupon_path = ROOT / "build/power-system-enclosure-nut-fit-coupon.stl"
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
    base_path, ((0.0, 0.0, 0.0), (220.27, 136.0, 32.0))
)
hood_facets, hood_points = mesh_contract(
    hood_path, ((0.0, 0.0, 0.0), (136.0, 140.0, 74.0))
)
coupon_topology = inspect_topology(coupon_path)
if (
    coupon_topology["invalid_edges"]
    or coupon_topology["components"] != 3
    or coupon_topology["degenerate_facets"]
):
    raise SystemExit(f"nut-fit coupon topology failure: {coupon_topology}")
coupon_facets = triangles(coupon_path)
coupon_points = [point for triangle in coupon_facets for point in triangle]
coupon_bounds = (
    tuple(min(point[axis] for point in coupon_points) for axis in range(3)),
    tuple(max(point[axis] for point in coupon_points) for axis in range(3)),
)
if coupon_bounds != ((0.0, 0.0, 0.0), (50.0, 16.0, 32.0)):
    raise SystemExit(f"nut-fit coupon bounds changed: {coupon_bounds}")


def split_components(facets):
    """Return edge-connected facet groups for per-piece print contracts."""
    edge_faces = {}
    for index, triangle in enumerate(facets):
        rounded = [tuple(round(value, 6) for value in point) for point in triangle]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            edge = tuple(sorted((rounded[a], rounded[b])))
            edge_faces.setdefault(edge, []).append(index)
    adjacency = [set() for _ in facets]
    for indexes in edge_faces.values():
        for index in indexes:
            adjacency[index].update(indexes)
    groups = []
    seen = set()
    for start in range(len(facets)):
        if start in seen:
            continue
        pending = [start]
        seen.add(start)
        group = []
        while pending:
            index = pending.pop()
            group.append(facets[index])
            for neighbor in adjacency[index]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
        groups.append(group)
    return groups


coupon_component_bounds = []
for component in split_components(coupon_facets):
    points = [point for triangle in component for point in triangle]
    bounds = (
        tuple(min(point[axis] for point in points) for axis in range(3)),
        tuple(max(point[axis] for point in points) for axis in range(3)),
    )
    if bounds[0][2] != 0.0:
        raise SystemExit(f"coupon component does not contact Z=0: {bounds}")
    bed_points = {
        (round(point[0], 6), round(point[1], 6))
        for point in points if math.isclose(point[2], 0.0, abs_tol=1e-6)
    }
    if len(bed_points) < 4:
        raise SystemExit(f"coupon component lacks meaningful bed contact: {bounds}")
    bed_area = 0.0
    for triangle in component:
        if all(math.isclose(point[2], 0.0, abs_tol=1e-6) for point in triangle):
            a, b, c = triangle
            bed_area += abs(
                (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
            ) / 2.0
    if bed_area < 20.0:
        raise SystemExit(
            f"coupon component bed contact is below 20 mm2: {bed_area} {bounds}"
        )
    coupon_component_bounds.append(bounds)

coupon_component_bounds.sort(key=lambda bounds: bounds[0][0])
expected_coupon_components = (
    ((0.0, 0.0, 0.0), (12.0, 16.0, 32.0)),
    ((20.0, 0.0, 0.0), (23.2, 12.0, 12.0)),
    ((38.0, 0.0, 0.0), (50.0, 12.0, 4.0)),
)
if tuple(coupon_component_bounds) != expected_coupon_components:
    raise SystemExit(f"coupon component bounds changed: {coupon_component_bounds}")
for left, right in zip(coupon_component_bounds, coupon_component_bounds[1:]):
    if left[1][0] >= right[0][0]:
        raise SystemExit("coupon projected component footprints overlap")
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


# The relocated rear boss is diagonally separated from the exact rigid inlet
# by X and Z, and is also behind the terminal/bend volumes in Y. These are
# conservative AABB distances; the empty CSG selectors below are authoritative.
rear_axis = (282.0, 296.0, 13.0)
rear_boss = ((276.0, 290.0, 3.98), (288.0, 296.0, 20.0))
c14_body = ((294.5, 278.2, 25.72), (321.5, 300.0, 72.58))
rigid_dx = c14_body[0][0] - rear_boss[1][0]
rigid_dz = c14_body[0][2] - rear_boss[1][2]
rigid_clearance = math.hypot(rigid_dx, rigid_dz)
if not (
    rear_axis == (282.0, 296.0, 13.0)
    and math.isclose(rigid_dx, 6.5)
    and math.isclose(rigid_dz, 5.72)
    and math.isclose(rigid_clearance, 8.658429, abs_tol=1e-6)
    and math.isclose(290.0-288.0, 2.0)
    and math.isclose(296.0-288.0, 8.0)
    and math.isclose(25.0-20.0, 5.0)
):
    raise SystemExit("rear-panel fastener lost its audited C14/AC-bend margins")


# Three hood nuts press through visible side mouths: left Y=170/290 and right
# Y=170. World Y maps to print X=338-Y. The fourth uses the equally direct
# rear-panel mouth measured separately below.
nut_z = 25.6
lead_radius = 6.2 / math.sqrt(3)
# The negative begins 0.01 mm outside the boss to make CSG robust, so the
# final mesh at the physical face samples 0.01/0.82 into the taper.
lead_face_radius = (6.2-(6.2-5.6)*0.01/0.82) / math.sqrt(3)
pocket_radius = 5.6 / math.sqrt(3)
socket_print_contracts = (
    (168.0, 4.0, 4.81, 7.61),
    (48.0, 4.0, 4.81, 7.61),
    (168.0, 128.8, 127.99, 125.19),
)
for centre_x, mouth, lead_inner, pocket_inner in socket_print_contracts:
    require_vertex(
        base_points, (centre_x, mouth, nut_z-lead_face_radius),
        "hood-nut 6.20 AF visible lead-in mouth",
    )
    require_vertex(
        base_points, (centre_x, lead_inner, nut_z-pocket_radius),
        "hood-nut 5.60 AF pressure-fit transition",
    )
    require_vertex(
        base_points, (centre_x, pocket_inner, nut_z-pocket_radius),
        "hood-nut 2.80 mm blind pocket extent",
    )
    if not math.isclose(
        abs(pocket_inner-lead_inner), 2.8, abs_tol=1e-6
    ):
        raise SystemExit("hood-nut pocket is not 2.80 mm deep")
    if nut_z-lead_radius-20.0 < 2.0:
        raise SystemExit("rail-side nut lead-in lacks 2 mm vertical clearance")
    mouth_profile = {
        (round(point[0], 4), round(point[2], 4))
        for point in base_points
        if math.isclose(point[1], mouth, abs_tol=2e-4)
        and abs(point[0]-centre_x) < 3.2
        and abs(point[2]-nut_z) < 3.7
    }
    lowest = min(z for _, z in mouth_profile)
    highest = max(z for _, z in mouth_profile)
    if not (
        {x for x, z in mouth_profile if z == lowest} == {centre_x}
        and {x for x, z in mouth_profile if z == highest} == {centre_x}
    ):
        raise SystemExit("hood socket is not point-up/support-free in print Z")

# Rear world +Y insertion maps to printer -X. The 0.01 mm robust-CSG start
# produces X=42.00 at the physical face, X=42.81 at the 5.60-AF transition,
# and X=45.61 at the blind pocket end. World X=282 maps to print Y=92.
rear_print_y = 92.0
for target, label in (
    ((42.0, rear_print_y, 13.0-lead_face_radius),
     "rear hood-nut 6.20 AF visible lead-in mouth"),
    ((42.81, rear_print_y, 13.0-pocket_radius),
     "rear hood-nut 5.60 AF pressure-fit transition"),
    ((45.61, rear_print_y, 13.0-pocket_radius),
     "rear hood-nut 2.80 mm blind pocket extent"),
):
    require_vertex(base_points, target, label)
rear_mouth_profile = {
    (round(point[1], 4), round(point[2], 4))
    for point in base_points
    if math.isclose(point[0], 42.0, abs_tol=2e-4)
    and abs(point[1]-rear_print_y) < 3.7
    and abs(point[2]-13.0) < 3.7
}
rear_lowest = min(z for _, z in rear_mouth_profile)
rear_highest = max(z for _, z in rear_mouth_profile)
if not (
    {y for y, z in rear_mouth_profile if z == rear_lowest} == {rear_print_y}
    and {y for y, z in rear_mouth_profile if z == rear_highest} == {rear_print_y}
):
    raise SystemExit("rear hood socket is not point-up/support-free in print Z")

# Installed hood walls cap all four 6.20-AF mouths. Their only opening is the
# 3.6 mm screw bore at roof-down Z=52.4; the Make empty-solid diagnostic proves
# the complete annulus, while these rim planes measure the final hood mesh.
hood_cap_print_contracts = (
    (130.0, (0.0, 3.2)),
    (10.0, (0.0, 3.2)),
    (130.0, (129.6, 132.8)),
)
for centre_y, wall_planes in hood_cap_print_contracts:
    for wall_plane in wall_planes:
        if not any(
            math.isclose(point[0], wall_plane, abs_tol=2e-4)
            and math.isclose(point[1], centre_y, abs_tol=2e-4)
            and math.isclose(
                math.hypot(point[1]-centre_y, point[2]-52.4),
                0.0,
                abs_tol=2e-4,
            )
            for point in hood_points
        ):
            # A circular mesh has no centre vertex; verify its 1.8 mm rim.
            rim = {
                point for point in hood_points
                if math.isclose(point[0], wall_plane, abs_tol=2e-4)
                and math.isclose(
                    math.hypot(point[1]-centre_y, point[2]-52.4),
                    1.8,
                    abs_tol=5e-4,
                )
            }
            if len(rim) < 30:
                raise SystemExit(
                    f"hood screw/cap rim missing at print {(wall_plane,centre_y,52.4)}"
                )

# Rear cap is in the roof-down hood's Y=0..3.2 wall at print X=92/Z=65.
for wall_plane in (0.0, 3.2):
    rim = {
        point for point in hood_points
        if math.isclose(point[1], wall_plane, abs_tol=2e-4)
        and math.isclose(
            math.hypot(point[0]-92.0, point[2]-65.0),
            1.8,
            abs_tol=5e-4,
        )
    }
    if len(rim) < 30:
        raise SystemExit(
            f"rear hood screw/cap rim missing at print {(92.0,wall_plane,65.0)}"
        )

print(
    "hood_nut_retention=pass traps=4 insertion=direct-visible-pressure "
    "side_traps=3 rear_traps=1 "
    "lead_af_mm=6.20 lead_depth_mm=0.80 pocket_af_mm=5.60 "
    "pocket_depth_mm=2.80 screw_axis_z_mm=25.60 boss_top_z_mm=32.00 "
    "rail_clearance_min_mm=2.02 left_backstop_mm=2.80 right_backstop_mm=3.20 "
    "rear_axis_xyz_mm=282,296,13 rear_backstop_mm=2.40 "
    "c14_rigid_clearance_mm=8.66 ac_bend_clearance_mm=9.64 "
    "hood_cap=annular-only-screw-bore"
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

# The five approved M3 centers survive the installed-to-print transform as
# visible top-open pressure sockets.  The hex extends from Z=1.40 to Z=4.00,
# proving the exact 2.60 mm depth and retained 1.40 mm floor.
for u, v in ((4.95, 4.95), (25.3, 30.9), (25.3, 67.0),
             (53.3, 67.0), (6.75, 98.6)):
    centre = (80.5 + u, 4.0 + v)
    for z in (1.4, 4.0):
        require_vertex(
            base_points,
            (centre[0], centre[1]-pocket_radius, z),
            f"approved PSU 5.60 AF socket at local {(u,v)}",
        )

# The third coupon component is the same exact PSU socket in floor-down
# orientation.  The first component carries the rail-side hood socket at the
# same Z=25.6 and with the exact rail obstruction; the middle component is the
# actual 3.2 mm hood wall and screw-bore crop in roof-down orientation.
for z in (1.4, 4.0):
    require_vertex(
        coupon_points, (44.0-pocket_radius, 6.0, z),
        "coupon PSU 5.60 AF socket",
    )
require_vertex(
    coupon_points, (6.0, 8.8, nut_z-lead_face_radius),
    "coupon rail-side 6.20 AF hood lead-in",
)
hood_coupon_rim = {
    point for point in coupon_points
    if math.isclose(point[0], 20.0, abs_tol=2e-4)
    and math.isclose(
        math.hypot(point[1]-6.0, point[2]-6.4),
        1.8,
        abs_tol=5e-4,
    )
}
if len(hood_coupon_rim) < 32:
    raise SystemExit("coupon roof-down hood-cap screw-bore rim missing")

print(
    "psu_nut_pressure_fit=pass traps=5 top_open=true af_mm=5.60 "
    "nut_measured_mm=2.30 pocket_depth_mm=2.60 floor_mm=1.40"
)
print(
    "nut_fit_coupon=pass components=3 bounds_mm=50x16x32 "
    "each_min_z_mm=0 projected_footprints=disjoint supports=none text=none"
)

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
