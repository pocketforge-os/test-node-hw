#!/usr/bin/env python3
"""Inspect audit G-code only: geometry evidence, never a printer profile release.

Requires matplotlib for review sheets. Uses the installed PrusaSlicer Flatpak directly. Keeps all machine-specific G-code in the ignored build directory.
"""
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/power-system-v3-concept'

def read_paths(path):
    layers={}
    x=y=e=0.0
    z=0.0
    width=0.9
    kind=''
    for line in path.read_text().splitlines():
        if line.startswith(';Z:'):
            z=round(float(line[3:]),4)
        elif line.startswith(';WIDTH:'):
            width=float(line[7:])
        elif line.startswith(';TYPE:'):
            kind=line[6:]
        elif line.startswith('G92 E'):
            e=float(line[5:])
        elif line.startswith(('G0 ', 'G1 ')):
            words={a:float(b) for a,b in re.findall(r'([XYEF])(-?[\d.]+)',line.split(';')[0])}
            nx,ny,ne=words.get('X',x),words.get('Y',y),words.get('E',e)
            if ne>e+1e-7 and math.hypot(nx-x,ny-y)>1e-7 and kind!='Custom':
                layers.setdefault(z,[]).append((x,y,nx,ny,width,kind))
            x,y,e=nx,ny,ne
    return layers

def covered(segments,point):
    px,py=point
    for x,y,a,b,width,kind in segments:
        if kind=='Skirt/Brim': continue
        dx,dy=a-x,b-y
        t=max(0,min(1,((px-x)*dx+(py-y)*dy)/(dx*dx+dy*dy)))
        if math.hypot(px-x-t*dx,py-y-t*dy)<=width/2+0.015:
            return True
    return False

def main():
    (OUT/'slice-report.json').unlink(missing_ok=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    report={'profile':'0.8 mm nozzle / 0.4 mm layers / ABS geometry audit / supports disabled',
            'profile_sha256':hashlib.sha256((ROOT/'scripts/prusaslicer-power-system-v3-audit.ini').read_bytes()).hexdigest(),
            'parts':{}}
    selections={'tray':[0.4,4,18,26,32,34,42,46.4,48,49.6,54,96],
                'panel':[0.4,0.8,1.2,1.6,4,4.4,8,10],
                'lid':[0.4,4,4.4,8,11.2,11.6,12,14.4],
                'bridge':[0.4,4,4.4,6.4], 'dc_insert':[0.4,2,4,4.4,8,12]}
    for part,heights in selections.items():
        path=OUT/f'{part}.audit.gcode'
        mesh=OUT/f'{part}.stl'
        before=hashlib.sha256(mesh.read_bytes()).hexdigest()
        path.unlink(missing_ok=True)
        result=subprocess.run(['flatpak','run','--command=prusa-slicer',
            'com.prusa3d.PrusaSlicer','--load',str(ROOT/'scripts/prusaslicer-power-system-v3-audit.ini'),
            '--rotate','90' if part=='tray' else '0','--center','123.5,103.5',
            '--export-gcode','--output',str(path),str(mesh)],capture_output=True,text=True)
        (OUT/f'{part}.slice.log').write_text(result.stdout+result.stderr)
        if result.returncode or not path.exists():
            raise RuntimeError(f'{part}: slicing failed; see slice log')
        if hashlib.sha256(mesh.read_bytes()).hexdigest()!=before:
            raise RuntimeError(f'{part}: mesh changed during slicing')
        layers=read_paths(path)
        if not layers: raise RuntimeError(f'{part}: no extrusions')
        paths=[s for layer in layers.values() for s in layer]
        if any('Support' in s[-1] for s in paths): raise RuntimeError(f'{part}: unexpected support')
        bounds=[[min(min(s[i],s[i+2]) for s in paths),max(max(s[i],s[i+2]) for s in paths)] for i in range(2)]
        if bounds[0][0]<0 or bounds[1][0]<0 or bounds[0][1]>247 or bounds[1][1]>207:
            raise RuntimeError(f'{part}: path centres exceed audit bed {bounds}')
        if part=='panel':
            for z in (0.4,0.8,1.2,1.6):
                for px,py in ((38,68),(88,68),(63,53),(63,83)):
                    actual=covered(layers[z],(px+49.5,py+53.5))
                    if actual != (z<=1.2):
                        raise RuntimeError(f'panel island toolpath coverage at {(px,py,z)}: {actual}')
            report['panel_snap_island']='4 probes covered on all 3 layers to 1.2 mm; absent at 1.6 mm'
        fig,axes=plt.subplots(math.ceil(len(heights)/4),4,figsize=(16,4*math.ceil(len(heights)/4)),squeeze=False)
        for ax,z in zip(axes.flat,heights):
            segments=layers[z]
            for bridge,color in ((False,'#176e81'),(True,'#df7723')):
                lines=[((s[0],s[1]),(s[2],s[3])) for s in segments if ('Bridge' in s[-1])==bridge]
                ax.add_collection(LineCollection(lines,colors=color,linewidths=.5))
            ax.set_xlim(bounds[0][0]-2,bounds[0][1]+2); ax.set_ylim(bounds[1][0]-2,bounds[1][1]+2)
            ax.set_aspect('equal'); ax.set_title(f'Z = {z:g} mm'); ax.set_xlabel('mm'); ax.set_ylabel('mm')
        for ax in list(axes.flat)[len(heights):]: ax.axis('off')
        fig.suptitle(f'{part}: actual extrusion paths — orange = bridge infill, teal = other paths',fontsize=14)
        fig.tight_layout(); fig.savefig(OUT/f'{part}-layers.png',dpi=160); plt.close(fig)
        report['parts'][part]={'gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'stl_sha256':hashlib.sha256((OUT/f'{part}.stl').read_bytes()).hexdigest(),
            'layer_count':len(layers),'max_z':max(layers),'path_centre_bounds_including_brim':bounds,
            'support_paths':0,'reviewed_layer_heights':heights}
        print(f'PASS {part}: {len(layers)} layers, bed fit, no support paths')
    (OUT/'slice-report.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__': main()
