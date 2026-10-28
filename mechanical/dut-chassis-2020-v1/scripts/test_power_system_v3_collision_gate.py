#!/usr/bin/env python3
"""Regression matrix for PR86's fail-open collision-result finding."""
from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
import unittest

from power_system_v3_concept import COLLISIONS, clean_empty

EMPTY='Geometries in cache: 2\nTotal rendering time: 0:00:00.001\nCurrent top level object is empty.\n'

class CollisionGate(unittest.TestCase):
    def test_every_selector_and_result_class(self):
        cases=(
            ('clean-empty',1,EMPTY,False,True),
            ('empty-wrong-success-code',0,EMPTY,False,False),
            ('empty-failed-code',2,EMPTY,False,False),
            ('empty-killed',-9,EMPTY,False,False),
            ('missing-empty-proof',1,'',False,False),
            ('warning-before-empty',1,'WARNING: failed geometry\n'+EMPTY,False,False),
            ('error-before-empty',1,'ERROR: failed geometry\n'+EMPTY,False,False),
            ('export-warning',1,EMPTY+'EXPORT-WARNING: invalid mesh\n',True,False),
            ('invalid-zero-volume-file',0,'WARNING: not manifold\n',True,False),
            ('valid-nonempty-file',0,'',True,False),
            ('file-and-empty-message',1,EMPTY,True,False),
            ('unknown-diagnostic',1,'Unrecognized failure\n'+EMPTY,False,False),
        )
        with TemporaryDirectory() as tmp:
            for part in COLLISIONS:
                path=Path(tmp)/(part+'.stl')
                for label,code,log,exists,expected in cases:
                    with self.subTest(selector=part,outcome=label):
                        path.unlink(missing_ok=True)
                        if exists: path.write_text('solid possibly-invalid\nendsolid\n')
                        result=CompletedProcess(['openscad'],code,'',log)
                        self.assertEqual(clean_empty(result,path),expected)
        print(f'PASS collision result gate: {len(COLLISIONS)} selectors x {len(cases)} outcomes; '
              'only clean-empty/code-1/no-file accepts')

if __name__=='__main__': unittest.main()
