#!/usr/bin/env python3
"""Reproduce mathematical certificates with Python 3.10+ (stdlib only)."""
import argparse
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--full', action='store_true', help='include largest affine hierarchy and all auxiliary finite checks')
args = parser.parse_args()
checks = [
 ('Global support-incidence and exact one-write simplex', ['verify_global_incidence.py', '--max-k','6']),
 ('Exact fourteen-state four-coordinate protocol', ['verification/verify_n4_14_states.py']),
 ('Deterministic all-length simplex completion', ['construct_completed_simplex.py']),
 ('General bounds, encoders, and multiround counts', ['verify_core_bounds.py']),
 ('Distance spectrum', ['verification/verify_spectrum.py']),
 ('Parity capacity and interior saturation', ['verification/verify_parity_upgrade.py']),
 ('General syndrome column criterion', ['verification/verify_general_column_criterion.py']),
 ('Full Hamming syndrome graph', ['verification/verify_hamming.py']),
 ('Shortened Hamming graph', ['verification/verify_shortened_hamming.py']),
 ('Finite five-coordinate classification', ['verification/finite_n5/run_all.py']),
 ('Temporal template synthesis', ['verification/temporal_templates/run_all.py']),
 ('Affine-plane exact coloring', ['verify_affine_plane_exact.py']),
 ('Affine-subspace hierarchy', ['verify_affine_subspace_hierarchy.py', '--max-d', '4' if args.full else '3']),
]
for name, argv in checks:
    print('\n[CHECK]',name,flush=True)
    subprocess.run([sys.executable, str(ROOT/argv[0]), *argv[1:]], cwd=ROOT, check=True)
print('\nPASS: all certificate suites',flush=True)
