#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ARCHIVE="PaperA_V13_Full_Reproducibility_2026-10-12.zip"
mkdir -p artifacts
cat archive_parts/${ARCHIVE}.part{00..12} > "artifacts/${ARCHIVE}"
echo "77097981946fe75c1f227ab43b238d98bdc99545202213da0ca34733298ae61a  artifacts/${ARCHIVE}" | sha256sum -c -
echo "Verified V13 full ZIP at paper_a_integrated/artifacts/${ARCHIVE}"
if [[ "${1:-}" == "--extract" ]]; then
  unzip -qo "artifacts/${ARCHIVE}" -d .
  echo "Extracted into paper_a_integrated/PaperA_V13"
fi
