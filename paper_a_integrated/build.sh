#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH=1791763200
export FORCE_SOURCE_DATE=1
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > compile1.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > compile2.log
if grep -Eiq 'Overfull \\hbox|undefined references|citation.*undefined' compile2.log; then
  echo "Paper A LaTeX audit warning" >&2
  grep -Ei 'Overfull|undefined references|citation.*undefined' compile2.log >&2
  exit 1
fi
pdfinfo paper.pdf | grep -E 'Title:|Author:|Pages:'
sha256sum paper.tex related_work_expanded.tex new_bibliography.tex v10_local_geometry.tex v12_cnf_correspondence.tex paper.pdf > MANUSCRIPT_SHA256SUMS
sha256sum -c MANUSCRIPT_SHA256SUMS
echo "PASS: canonical uncompressed Paper A sources built and checked"
