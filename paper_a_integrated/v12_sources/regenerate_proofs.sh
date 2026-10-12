#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
mkdir -p rederived
python3 verification/rebuild_compact.py rederived >/dev/null
g++ -O3 -std=c++17 verification/cdcl_proof.cpp -o rederived/cdcl_proof
g++ -O3 -std=c++17 verification/check_drup.cpp -o rederived/check_drup
for name in B.antipodal B.mixed A.normal A.special A.antipodal; do
  echo "Regenerating $name"
  rederived/cdcl_proof "rederived/${name}.cnf" "rederived/${name}.drup" 2> "rederived/${name}.solver.log"
  rederived/check_drup "rederived/${name}.cnf" "rederived/${name}.drup"
done
echo 'REGENERATION PASS: all 5 cases'
