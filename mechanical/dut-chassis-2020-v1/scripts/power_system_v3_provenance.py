#!/usr/bin/env python3
"""Fail-closed source receipts for this bounded CAD producer and its consumers.

The model input set is explicit. Every OpenSCAD export also emits its actual
transitive dependency list; any file outside this set refuses the export.
Adding an import/include therefore requires declaring it here and regenerating.
"""
import hashlib
import json
from pathlib import Path
import shlex

ROOT=Path(__file__).resolve().parents[1]
SCAD_INPUTS=(
    'power-system-v3-concept.scad', 'pocketforge-node-chassis-usb-c.scad',
    'lib/alt-1205t-power-supply.scad', 'lib/iec-c14-fused-switch.scad',
    'lib/pf-2020.scad', 'lib/usb-c-interrupter-bracket.scad',
)
CAD_INPUTS=SCAD_INPUTS+('scripts/power_system_v3_concept.py',
    'scripts/check_stl_topology.py','scripts/power_system_v3_provenance.py')
SLICE_INPUTS=('scripts/power_system_v3_slice_audit.py',
    'scripts/prusaslicer-power-system-v3-audit.ini','scripts/power_system_v3_provenance.py')
PRINT_INPUTS=('scripts/power_system_v3_printability.py','scripts/power_system_v3_provenance.py')


def receipt(inputs,root=ROOT):
    files={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in sorted(inputs)}
    digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'files':files,'sha256':digest}


def require_current(saved,inputs,root=ROOT):
    if saved!=receipt(inputs,root):
        raise RuntimeError('missing/stale source receipt: regenerate CAD, slice and printability evidence in order')


def check_dependencies(path,root=ROOT):
    text=path.read_text().replace('\\\n',' ')
    if ':' not in text: raise RuntimeError('missing OpenSCAD dependency rule')
    names=shlex.split(text.split(':',1)[1])
    actual={(root/n).resolve() for n in names}
    allowed={(root/n).resolve() for n in SCAD_INPUTS}
    if not actual or (root/SCAD_INPUTS[0]).resolve() not in actual or actual-allowed:
        raise RuntimeError(f'undeclared/missing CAD dependencies: {sorted(str(p) for p in actual-allowed)}')
    return actual
