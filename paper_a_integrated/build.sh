#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Deterministic source reconstruction from the GitHub-tracked compressed blob.
xz -dc manuscript.tex.xz > paper.tex
echo "07ce9a85328a043390c194302a9003aa45efe4ef13d477767fb36f7c4a3aa0b6  paper.tex" | sha256sum -c -

pdflatex -interaction=nonstopmode -halt-on-error paper.tex > compile1.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > compile2.log

if grep -Eiq 'Overfull \\hbox|undefined references|citation.*undefined' compile2.log; then
  echo "LaTeX audit warning found" >&2
  grep -Ei 'Overfull|undefined references|citation.*undefined' compile2.log >&2
  exit 1
fi
pdfinfo paper.pdf | grep -E 'Title:|Author:|Pages:'
sha256sum paper.tex paper.pdf > MANUSCRIPT_SHA256SUMS
echo "PASS: full Paper A source reconstructed and PDF compiled"
