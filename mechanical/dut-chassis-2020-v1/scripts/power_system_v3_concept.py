#!/usr/bin/env python3
"""Reproduce and check the V3 unpowered mechanical fit candidate."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess

from check_stl_topology import DisjointSet, inspect_topology, triangles

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "power-system-v3-concept.scad"
OUT = ROOT / "build/power-system-v3-concept"
VIEWS = {
    "tray": ("tray", "270,360,280,74,72,20"),
    "lid": ("lid", "270,360,230,74,72,0"),
    "internals": ("internals", "-200,220,380,74,72,42"),
    "dc-section": ("dc_section", "65,-100,30,65,107,30"),
    "dc-insert": ("dc_insert", "100,130,100,26,107,2"),
    "shield": ("shield", "270,360,280,74,72,36"),
    "bridge": ("bridge", "55,70,60,12,12,3"),
    "vent-section": ("vent_section", "300,72,34,39,72,34"),
    "front": ("assembly", "74,-350,34,74,72,34"),
    "left": ("assembly", "-350,72,34,74,72,34"),
    "right": ("assembly", "450,72,34,74,72,34"),
    "top": ("assembly", "74,72,500,74,72,34"),
    "bottom": ("bottom", "-74,72,500,-74,72,0"),
    "assembly": ("assembly", "270,360,230,74,72,30"),
    "open": ("open", "270,360,280,74,72,20"),
    "exploded": ("exploded", "290,400,280,74,90,44"),
    "rear": ("assembly", "74,450,34,74,72,34"),
    "frame": ("frame", "470,600,360,-20,40,20"),
    "frame-open": ("frame_open", "470,600,360,-20,40,20"),
    "chassis": ("chassis", "520,650,420,-5,20,100"),
    "plug-access": ("plug_access", "520,650,420,-5,20,100"),
    "panel": ("panel", "74,34,-250,74,34,0"),
    "panel-section": ("panel_section", "74,-200,20,74,38,4"),
}

def export(part, dest, extra=()):
    cmd = ["openscad", "--hardwarnings", "--check-parameters=true",
           "--check-parameter-ranges=true", "-o", str(dest),
           "-D", f'PART="{part}"', *extra, str(SOURCE)]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    (OUT / f"{dest.stem}.log").write_text(result.stdout + result.stderr)
    return result

def volume(path):
    # Sum absolute volumes per connected shell so disconnected inverted
    # shells cannot cancel a real collision. Zero-volume mating sheets pass.
    facets=triangles(path)
    groups=DisjointSet(len(facets))
    seen={}
    for i,tri in enumerate(facets):
        for point in tri:
            if point in seen:
                groups.union(i,seen[point])
            else:
                seen[point]=i
    totals={}
    for i,(a,b,c) in enumerate(facets):
        root=groups.find(i)
        value=(a[0]*(b[1]*c[2]-b[2]*c[1]) +
               a[1]*(b[2]*c[0]-b[0]*c[2]) +
               a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        totals[root]=totals.get(root,0)+value
    return sum(abs(v) for v in totals.values())

def vertical_hits(path, x, y):
    """Intersect the exported mesh with a Z ray, away from holes/edges."""
    hits = set()
    for a,b,c in triangles(path):
        denom=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(denom)<1e-9:
            continue
        u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/denom
        v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/denom
        if u>=-1e-7 and v>=-1e-7 and u+v<=1+1e-7:
            hits.add(round(u*a[2]+v*b[2]+(1-u-v)*c[2],5))
    return sorted(hits)

COLLISIONS=("collision_parts", "collision_components", "collision_service",
            "collision_chassis", "collision_plug", "collision_drivers", "collision_wires")

def clean_empty(result, dest):
    # OpenSCAD 2021.01 exits 1 for its documented empty-export result. No other
    # failure code, emitted file, warning, error or unexpected log is accepted.
    lines=[line.strip() for line in (result.stdout+result.stderr).splitlines() if line.strip()]
    prefixes=("Geometries in cache:","Geometry cache size in bytes:",
              "CGAL Polyhedrons in cache:","CGAL cache size in bytes:",
              "Total rendering time:")
    return (result.returncode==1 and not dest.exists() and bool(lines) and
            lines[-1]=="Current top level object is empty." and
            all(line.startswith(prefixes) for line in lines[:-1]))

def check_collision_controls():
    for name,empty in (("contact",True),("gap",True),("overlap",False),("thin",False)):
        dest=OUT/f"collision_control_{name}.stl"
        dest.unlink(missing_ok=True)
        result=export(f"collision_control_{name}",dest)
        accepted=clean_empty(result,dest)
        if empty:
            if not accepted: raise RuntimeError(f"collision control {name}: expected clean empty")
        else:
            # Require a successful real solid before asserting the guard
            # rejected it: an exporter failure is not a positive control.
            log=result.stdout+result.stderr
            if result.returncode or "WARNING" in log or "ERROR" in log or not dest.exists():
                raise RuntimeError(f"collision control {name}: invalid export")
            mesh=inspect_topology(dest)
            if mesh["invalid_edges"] or mesh["degenerate_facets"] or volume(dest)<=0 or accepted:
                raise RuntimeError(f"collision control {name}: did not reject a valid overlap")
        print(f"PASS collision control {name}: {'clean empty' if empty else 'real overlap rejected'}",flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--views-only", action="store_true")
    parser.add_argument("--views", nargs="+", choices=list(VIEWS))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.views_only: (OUT / "report.json").unlink(missing_ok=True)
    if args.views_only:
        for name in args.views or VIEWS:
            part,camera=VIEWS[name]
            result=export(part,OUT/f"{name}.png",["--imgsize=1600,1200","--projection=o",
                "--colorscheme=Tomorrow","--viewall",f"--camera={camera}"])
            if result.returncode: raise RuntimeError(f"render {name}: see log")
        return
    report = {"status": "unpowered-mechanical-fit-candidate", "parts": {}, "collisions": {}}
    for part in ("tray", "panel", "lid", "bridge", "dc_insert"):
        dest = OUT / f"{part}.stl"
        result = export(part, dest)
        if result.returncode:
            raise RuntimeError(f"{part}: see {OUT / (part+'.log')}")
        mesh = inspect_topology(dest)
        if (mesh["components"] != 1 or mesh["invalid_edges"] != 0 or
                mesh["degenerate_facets"] != 0):
            raise RuntimeError(f"{part}: {mesh}")
        points = [point for tri in triangles(dest) for point in tri]
        bounds = [[min(p[i] for p in points), max(p[i] for p in points)] for i in range(3)]
        report["parts"][part] = {"topology": mesh, "bounds": bounds,
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}
        print(f"PASS {part}: one closed connected mesh; bounds={bounds}", flush=True)
    for x,y,thickness in ((38,68,1.2),(88,68,1.2),(63,53,1.2),
                          (63,83,1.2),(29,68,4),(97,68,4),
                          (63,46,4),(63,90,4)):
        hits=vertical_hits(OUT/"panel.stl",x,y)
        if hits != [0.0,thickness]:
            raise RuntimeError(f"panel thickness at {(x,y)}: {hits}, expected {thickness}")
    report["panel_thickness"]="four 1.2 mm island probes and four 4 mm frame probes pass"
    print("PASS panel mesh thickness: 1.2 mm island, 4 mm surrounding frame",flush=True)
    for x,y in ((12.95,86.55),(38.9,66.2),(75,66.2),(75,38.2),(106.6,84.75)):
        if vertical_hits(OUT/"tray.stl",x,y) != []:
            raise RuntimeError(f"PSU screw shaft blocked at {(x,y)}")
        hits=vertical_hits(OUT/"tray.stl",x+3,y)
        if hits != [2.4,5.6]:
            raise RuntimeError(f"PSU screw web at {(x,y)}: {hits}")
    report["psu_screw_paths"]="five through shafts; 3.2 mm bearing webs between head and fitting reliefs"
    print("PASS PSU screw shafts, head clearance and 3.2 mm bearing webs",flush=True)
    for part in ("dc_roof_template", "terminal_shield_template"):
        for ext in ("svg","dxf"):
            dest=OUT/f"{part}.{ext}"
            result=export(part,dest)
            if result.returncode or not dest.exists():
                raise RuntimeError(f"{part}: sheet template export failed")
    print("PASS two nonprinted sheet templates, SVG and DXF",flush=True)
    # Probe the actual tray along X at every sampled point across the outlet.
    # This proves an axial obstruction, not a standardized articulated-finger test.
    tray_faces=triangles(OUT/"tray.stl")
    def x_hits(y,z):
        hits=set()
        for tri in tray_faces:
            a,b,c=[(p[1],p[2],p[0]) for p in tri]
            denom=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(denom)<1e-9: continue
            u=((b[1]-c[1])*(y-c[0])+(c[0]-b[0])*(z-c[1]))/denom
            v=((c[1]-a[1])*(y-c[0])+(a[0]-c[0])*(z-c[1]))/denom
            if u>=-1e-7 and v>=-1e-7 and u+v<=1+1e-7:
                hits.add(round(u*a[2]+v*b[2]+(1-u-v)*c[2],5))
        return sorted(hits)
    for y in (100,102,104,106,108,110,112,114,115):
        for z in (22,24,26,28,30):
            hits=x_hits(y,z)
            if 20.0 not in hits or 23.2 not in hits:
                raise RuntimeError(f"DC outlet lost axial baffle at {(y,z)}: {hits}")
    report["dc_exit"]={"axial_baffle_probes":45,"port_mm":[15.8,8.8],
                       "assumed_cables":"one <=8 mm or two <=6 mm jackets; physical fit unverified",
                       "finger_protection_certified":False}
    print("PASS DC outlet: 45 axial mesh rays strike the solid internal baffle",flush=True)
    check_collision_controls()
    report["collision_sample_offset_per_axis_mm"]=0.01
    report["collision_sub_0_02_mm_clearance_qualified"]=False
    report["collision_controls"]="contact/gap clean-empty; 1 mm and 0.02 mm overlap rejected"
    def collision_check(part):
        dest = OUT / f"{part}.stl"
        dest.unlink(missing_ok=True)
        result = export(part, dest)
        if not clean_empty(result,dest):
            raise RuntimeError(f"{part}: nonempty, failed or invalid intersection export; see log")
        return part
    # Separate OpenSCAD processes and output paths; bound memory/CPU use.
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending=[pool.submit(collision_check,part) for part in COLLISIONS]
        for future in as_completed(pending):
            part=future.result()
            report["collisions"][part]="clean empty at 0.01 mm audit tolerance"
            print(f"PASS {part}: clean empty",flush=True)
    if args.render:
        for name, (part, camera) in VIEWS.items():
            result = export(part, OUT / f"{name}.png", (["--render"] if part in ("tray","lid","panel","bridge","panel_section","dc_insert","dc_section") else []) + ["--imgsize=1600,1200",
                "--projection=o", "--colorscheme=Tomorrow", "--viewall",
                f"--camera={camera}"])
            if result.returncode:
                raise RuntimeError(f"render {name}: see log")
            print(f"PASS render {name}", flush=True)
    (OUT / "report.json").write_text(json.dumps(report, indent=2)+"\n")

if __name__ == "__main__":
    main()
