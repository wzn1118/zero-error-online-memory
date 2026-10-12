#!/usr/bin/env python3
"""Portable Paper A CI: mathematical structure and frozen CNF byte identity."""
import sys,hashlib,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V12=ROOT/'v12_sources'/'verification'
ME=Path(__file__).resolve().parent
EXPECTED={
'A.antipodal':'b0d22006ce902632023ad0700a5eb5b7fda9ef5a1dff396fa81b8e2de7a07935',
'A.normal':'b36252832359dba8f581f4ce1e73ae47c85dbd0f230e260b6a2801c36e06f31d',
'A.special':'5a3734e9647fc95ad2993f99d2c51daee7efb12431dd769d51298743b794b4ee',
'B.antipodal':'87e88ef8b8edf035af6cbe6e9a5a62829b84ab547237b08e3da1ecd72458a79f',
'B.mixed':'db7ee6de47a519600ab3ecb830d98d99cd3cae0e5dec3541fbe8d66c61efd346',
}
for script in (ME/'audit_v10_pair_geometry.py',V12/'test_encoding_semantics.py',
               V12/'audit_pair_geometry.py',V12/'verify_symmetry_orbits.py',
               V12/'verify_120_protocol.py'):
    print('RUN',script.name,flush=True)
    subprocess.run([sys.executable,str(script)],cwd=ROOT,check=True)
with tempfile.TemporaryDirectory(prefix='paper-a-cnf-') as tmp:
    subprocess.run([sys.executable,str(V12/'rebuild_compact.py'),tmp],cwd=V12,check=True,
                   stdout=subprocess.DEVNULL)
    for name,expected in EXPECTED.items():
        actual=hashlib.sha256((Path(tmp)/(name+'.cnf')).read_bytes()).hexdigest()
        assert actual==expected,(name,actual,expected)
    print('PASS: five frozen CNF SHA-256 values')
print('PASS: Paper A public checks complete; full DRUP proof traces require separate regeneration workflow')
