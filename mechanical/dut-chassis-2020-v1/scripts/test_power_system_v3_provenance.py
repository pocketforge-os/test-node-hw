#!/usr/bin/env python3
"""Property sweep: stale inputs must fail before either consumer starts work.

Run with the same Python environment as the printability audit. Copies only
source files into disposable trees; never edits the real worktree's inputs.
The actual successful producer/consumer path is exercised by the CAD workflow.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from power_system_v3_provenance import (
    ROOT, CAD_INPUTS, SLICE_INPUTS, PRINT_INPUTS, SCAD_INPUTS,
    receipt, require_current, check_dependencies,
)


class ProvenanceTests(unittest.TestCase):
    def make_tree(self,directory):
        root=Path(directory)
        for name in set(CAD_INPUTS+SLICE_INPUTS+PRINT_INPUTS):
            target=root/name; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/name,target)
        out=root/'build/power-system-v3-concept';out.mkdir(parents=True)
        cad=receipt(CAD_INPUTS,root); sliced=receipt(SLICE_INPUTS,root)
        (out/'report.json').write_text(json.dumps({'cad_inputs':cad}))
        (out/'slice-report.json').write_text(json.dumps({'cad_inputs':cad,'slice_inputs':sliced}))
        return root,out

    def consumer_rejects(self,root,consumer):
        result=subprocess.run([sys.executable,str(root/'scripts'/consumer)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('missing/stale source receipt',result.stderr)
        self.assertFalse((root/'build/power-system-v3-concept/printability-report.json').exists())

    def test_every_cad_input_blocks_both_consumers(self):
        for name in CAD_INPUTS:
            for consumer in ('power_system_v3_slice_audit.py','power_system_v3_printability.py'):
                with self.subTest(input=name,consumer=consumer), tempfile.TemporaryDirectory() as tmp:
                    root,out=self.make_tree(tmp)
                    path=root/name; path.write_bytes(path.read_bytes()+b'\n')
                    self.consumer_rejects(root,consumer)

    def test_every_slice_input_blocks_print_consumer(self):
        for name in SLICE_INPUTS:
            with self.subTest(input=name), tempfile.TemporaryDirectory() as tmp:
                root,out=self.make_tree(tmp)
                path=root/name;path.write_bytes(path.read_bytes()+b'\n')
                self.consumer_rejects(root,'power_system_v3_printability.py')

    def test_legacy_reports_rejected_by_both_consumers(self):
        for consumer in ('power_system_v3_slice_audit.py','power_system_v3_printability.py'):
            with self.subTest(consumer=consumer), tempfile.TemporaryDirectory() as tmp:
                root,out=self.make_tree(tmp)
                (out/'report.json').write_text('{}')
                self.consumer_rejects(root,consumer)

    def test_receipt_integrity_and_end_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root,out=self.make_tree(tmp)
            for inputs in (CAD_INPUTS,SLICE_INPUTS,PRINT_INPUTS):
                original=receipt(inputs,root)
                require_current(original,inputs,root)  # unchanged PASS path
                for bad in (None,{}, {'files':original['files'],'sha256':'wrong'}):
                    with self.assertRaises(RuntimeError):require_current(bad,inputs,root)
            for name in PRINT_INPUTS:
                original=receipt(PRINT_INPUTS,root)
                path=root/name;before=path.read_bytes();path.write_bytes(before+b'\n')
                with self.assertRaises(RuntimeError): require_current(original,PRINT_INPUTS,root)
                path.write_bytes(before)

    def test_actual_dependency_receipts(self):
        with tempfile.TemporaryDirectory(prefix='psu deps ') as tmp:
            root,out=self.make_tree(tmp);dep=out/'model.d'
            # Make escapes in paths, including spaces in the execution root.
            dep.write_text('out.stl: \\\n'+ ' \\\n'.join(str(root/n).replace(' ','\\ ') for n in SCAD_INPUTS)+'\n')
            self.assertEqual(len(check_dependencies(dep,root)),len(SCAD_INPUTS))
            dep.write_text(dep.read_text()+' '+str(root/'undeclared.stl').replace(' ','\\ '))
            with self.assertRaises(RuntimeError):check_dependencies(dep,root)
            dep.write_text('out.stl:\n')
            with self.assertRaises(RuntimeError):check_dependencies(dep,root)

if __name__=='__main__':unittest.main()
