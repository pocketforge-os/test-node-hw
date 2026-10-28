#!/usr/bin/env python3
"""Reproduce and check the V3 unpowered mechanical fit candidate."""
import argparse
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

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "report.json").unlink(missing_ok=True)
    report = {"status": "unpowered-mechanical-fit-candidate", "parts": {}, "collisions": {}}
    for part in ("tray", "panel", "lid", "bridge"):
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
    for x,y,thickness in ((38,38,1.2),(88,38,1.2),(63,23,1.2),
                          (63,53,1.2),(29,38,4),(97,38,4),
                          (63,16,4),(63,60,4)):
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
    for part in ("collision_parts", "collision_components", "collision_service",
                 "collision_chassis", "collision_plug", "collision_drivers"):
        dest = OUT / f"{part}.stl"
        dest.unlink(missing_ok=True)
        result = export(part, dest)
        log = result.stdout + result.stderr
        if dest.exists():
            # Intentional floor/panel and lid/rim seating contacts produce
            # zero-volume sheets in CGAL, rather than an empty STL.
            overlap = volume(dest)
            if overlap > 0.0001 or "ERROR:" in log:
                raise RuntimeError(f"{part}: overlap={overlap}; see log")
            report["collisions"][part] = {"volume_mm3": overlap,
                "interpretation": "nominal surface contact only"}
            print(f"PASS {part}: contact volume={overlap:.9f} mm3", flush=True)
        elif ("Current top level object is empty" in log and
              "WARNING:" not in log and "ERROR:" not in log):
            report["collisions"][part] = "empty"
            print(f"PASS {part}: empty", flush=True)
        else:
            raise RuntimeError(f"{part}: no usable intersection result; see log")
    if args.render:
        for name, (part, camera) in VIEWS.items():
            result = export(part, OUT / f"{name}.png", (["--render"] if part in ("tray","lid","panel","bridge","panel_section") else []) + ["--imgsize=1600,1200",
                "--projection=o", "--colorscheme=Tomorrow", "--viewall",
                f"--camera={camera}"])
            if result.returncode:
                raise RuntimeError(f"render {name}: see log")
            print(f"PASS render {name}", flush=True)
    (OUT / "report.json").write_text(json.dumps(report, indent=2)+"\n")

if __name__ == "__main__":
    main()
