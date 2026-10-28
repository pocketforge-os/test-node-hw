#!/usr/bin/env python3
"""Print-orientation evidence, not a printer/material performance guarantee.

Requires trimesh, shapely and matplotlib. Run the mesh and slice audits first.
Uses actual G-code segments and prior-layer mesh sections; it does not infer
support-free geometry from support_material=0. Tray supports are separately
sliced build-plate-only and must be confined to externally removable regions.
"""
import hashlib
import json
import math
import subprocess
import numpy as np
import trimesh
from shapely.geometry import Polygon, GeometryCollection, LineString, Point, box
from shapely import make_valid
from shapely.affinity import rotate, translate
from shapely.ops import unary_union
from power_system_v3_slice_audit import OUT, ROOT, read_paths
from power_system_v3_provenance import CAD_INPUTS, SLICE_INPUTS, PRINT_INPUTS, receipt, require_current


def polygons(g):
    if g.is_empty: return []
    if g.geom_type=='Polygon': return [g]
    if not hasattr(g,'geoms'): return []
    return [p for child in g.geoms for p in polygons(child)]


def section(mesh,z):
    s=mesh.section(plane_origin=[0,0,z+0.0001],plane_normal=[0,0,1])
    area=GeometryCollection()
    if s is not None:
        for loop in s.discrete:
            poly=Polygon(loop[:,:2])
            if not poly.is_valid:
                fixed=make_valid(poly)
                # Resolve self-touching section loops only when the area and
                # boundary are unchanged; never repair a substantive defect.
                if abs(fixed.area-poly.area)>1e-6 or poly.hausdorff_distance(fixed)>1e-6:
                    raise RuntimeError(f'invalid section at {z}')
                poly=unary_union(polygons(fixed))
            # Tangencies may leave lines but no solid cross-section area.
            if poly.area<1e-8: continue
            area=area.symmetric_difference(poly)
    return area


def lines(g):
    if g.is_empty: return []
    if g.geom_type=='LineString': return [g]
    if not hasattr(g,'geoms'): return []
    return [s for c in g.geoms for s in lines(c)]


def print_mesh(part):
    mesh=trimesh.load(OUT/f'{part}.stl',force='mesh')
    if part=='tray': mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,0,1]))
    mesh.apply_translation([123.5-mesh.bounds[:,0].mean(),103.5-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
    return mesh


PSU_HOLES=((12.95,86.55),(38.9,66.2),(75,66.2),(75,38.2),(106.6,84.75))
def accessible_support_regions(z):
    regions=[]
    if z<=2.4:
        regions += [Point(p).buffer(3.5) for p in PSU_HOLES]
    if z<=6.9:
        regions += [box(147.5,y-8.5,153.5,y+8.5) for y in (-6.27,150)]
    return unary_union(regions)


def main():
    (OUT/'printability-report.json').unlink(missing_ok=True)
    source=json.loads((OUT/'report.json').read_text())
    sliced=json.loads((OUT/'slice-report.json').read_text())
    require_current(source.get('cad_inputs'),CAD_INPUTS)
    require_current(sliced.get('cad_inputs'),CAD_INPUTS)
    require_current(sliced.get('slice_inputs'),SLICE_INPUTS)
    print_inputs=receipt(PRINT_INPUTS)
    profile=ROOT/'scripts/prusaslicer-power-system-v3-audit.ini'
    if hashlib.sha256(profile.read_bytes()).hexdigest()!=sliced['profile_sha256']:
        raise RuntimeError('slice profile changed since the audit')
    report={'cad_inputs':source['cad_inputs'],'slice_inputs':sliced['slice_inputs'],
            'print_inputs':print_inputs,'profile_sha256':sliced['profile_sha256'],'limits':{'layer_mm':.4,'self_support_lateral_growth_mm':.4,
                     'maximum_residual_straight_segment_mm':{'tray':8.8,'others':1.0}},'parts':{}}
    for part in ('panel','lid','bridge','dc_insert','tray'):
        mesh=print_mesh(part)
        sha=hashlib.sha256((OUT/f'{part}.stl').read_bytes()).hexdigest()
        if sha!=source['parts'][part]['sha256'] or sha!=sliced['parts'][part]['stl_sha256']:
            raise RuntimeError(f'{part}: stale mesh report')
        if hashlib.sha256((OUT/f'{part}.audit.gcode').read_bytes()).hexdigest()!=sliced['parts'][part]['gcode_sha256']:
            raise RuntimeError(f'{part}: stale slice report')
        layers=read_paths(OUT/f'{part}.audit.gcode')
        if not layers: raise RuntimeError(f'{part}: missing toolpaths')
        raw=trimesh.load(OUT/f'{part}.stl',force='mesh')
        cx,cy=raw.bounds[:,:2].mean(axis=0)
        worst=(0,0,[]); islands=0
        previous=None
        for z,segments in sorted(layers.items()):
            current=section(mesh,z-.2)
            if previous is not None:
                polys=polygons(current)
                islands+=sum(not p.intersects(previous) for p in polys if not p.is_empty)
                # A .4 mm lateral offset per .4 mm layer represents a 45°
                # corbel. Beyond this, report actual straight toolpath
                # segments, including perimeter paths (not only bridge infill).
                bearing=previous.buffer(.4,join_style=2)
                if part=='tray':
                    # The generated supports below must independently stay
                    # inside these externally removable zones.
                    allowed=accessible_support_regions(z-.4)
                    allowed=translate(rotate(allowed,90,origin=(0,0)),
                                      xoff=123.5+cy,yoff=103.5-cx)
                    bearing=bearing.union(allowed)
                for x,y,a,b,w,kind in segments:
                    if kind=='Skirt/Brim': continue
                    for run in lines(LineString([(x,y),(a,b)]).difference(bearing)):
                        if run.length>worst[0]: worst=(run.length,z,list(run.coords))
            previous=current
        limit=8.8 if part=='tray' else 1.0
        if islands or worst[0]>limit:
            raise RuntimeError(f'{part}: floating islands={islands}, unsupported run={worst}')
        report['parts'][part]={'stl_sha256':sha,'floating_layer_islands':islands,
            'max_straight_segment_beyond_45_degree_bearing_mm':worst[0], 'worst_layer_z':worst[1],
            'worst_segment':worst[2], 'supports':'accessible base-only supports' if part=='tray' else 'off; short residual bridges only'}
        print(f'PASS {part}: no floating islands; longest residual straight segment {worst[0]:.3f} mm at Z{worst[1]}',flush=True)
    # The base has a continuous floor. Build-plate-only supports exclude all
    # internal baffles, cable tunnels, nut pockets and guard rebates.
    path=OUT/'tray.support.gcode'
    path.unlink(missing_ok=True)
    result=subprocess.run(['flatpak','run','--command=prusa-slicer','com.prusa3d.PrusaSlicer',
        '--load',str(ROOT/'scripts/prusaslicer-power-system-v3-audit.ini'),
        '--support-material','--support-material-auto','--support-material-threshold','45',
        '--support-material-buildplate-only','--dont-support-bridges',
        '--rotate','90','--center','123.5,103.5','--export-gcode','--output',str(path),str(OUT/'tray.stl')],capture_output=True,text=True)
    (OUT/'tray.support.log').write_text(result.stdout+result.stderr)
    if result.returncode or not path.exists(): raise RuntimeError('tray support diagnostic failed')
    if hashlib.sha256((OUT/'tray.stl').read_bytes()).hexdigest()!=report['parts']['tray']['stl_sha256']:
        raise RuntimeError('tray mesh changed during support slicing')
    supports=[(z,s) for z,ss in read_paths(path).items() for s in ss if 'Support' in s[-1]]
    # Inverse of the tray's rotate/centre transform, derive from STL bounds.
    mesh=trimesh.load(OUT/'tray.stl',force='mesh')
    cx,cy=mesh.bounds[:,:2].mean(axis=0)
    if not supports: raise RuntimeError('expected removable base supports were not generated')
    local=[]
    for z,s in supports:
        for x,y in ((s[0],s[1]),(s[2],s[3])):
            local.append([cx+y-103.5,cy-(x-123.5),z])
        a,b=local[-2:]
        footprint=LineString([a[:2],b[:2]]).buffer(s[4]/2)
        if not accessible_support_regions(z).buffer(.01).covers(footprint):
            raise RuntimeError(f'tray support outside removable regions: {a}, {b}')
    # Ensure the two external key regions and all five shallow head recesses
    # are represented, not merely that some unrelated support exists.
    for region in polygons(accessible_support_regions(1.8)):
        if not any(region.covers(Point(p[:2])) for p in local):
            raise RuntimeError('missing support in an expected accessible region')
    report['tray']={'support_path_segments':len(supports),'support_point_bounds':
        [np.min(local,axis=0).tolist(),np.max(local,axis=0).tolist()] if local else [],
        'support_gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'stl_sha256':hashlib.sha256((OUT/'tray.stl').read_bytes()).hexdigest(),
        'all_support_extrusions_with_width_inside_accessible_regions':True}
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    a=np.array(local)
    fig,ax=plt.subplots(figsize=(8,10))
    ax.scatter(a[:,0],a[:,1],c=a[:,2],s=2)
    ax.set_aspect('equal'); ax.set_xlabel('Tray X (mm)'); ax.set_ylabel('Tray Y (mm)')
    ax.set_title('Supports: exposed rail keys and shallow underside screw recesses only')
    fig.savefig(OUT/'tray-support-map.png',dpi=160); plt.close(fig)
    require_current(source['cad_inputs'],CAD_INPUTS)
    require_current(sliced['slice_inputs'],SLICE_INPUTS)
    require_current(print_inputs,PRINT_INPUTS)
    for part,info in report['parts'].items():
        if hashlib.sha256((OUT/f'{part}.stl').read_bytes()).hexdigest()!=info['stl_sha256']:
            raise RuntimeError(f'{part}: mesh changed during audit')
        if hashlib.sha256((OUT/f'{part}.audit.gcode').read_bytes()).hexdigest()!=sliced['parts'][part]['gcode_sha256']:
            raise RuntimeError(f'{part}: toolpaths changed during audit')
    (OUT/'printability-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Tray support paths exported for location/removal inspection:',report['tray']['support_point_bounds'])

if __name__=='__main__': main()
