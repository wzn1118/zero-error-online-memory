#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "58a289f787f4fda98327b6619212a4966225f58052529c7f833ede867abfe2c5  paper.tex" | sha256sum -c -
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > compile1.log
pdflatex -interaction=nonstopmode -halt-on-error paper.tex > compile2.log
if grep -Eiq 'Overfull \\hbox|undefined references|citation.*undefined' compile2.log; then
 echo "LaTeX audit warning"; exit 1
fi
pdfinfo paper.pdf | grep -E 'Pages:|Page size:'
echo "PASS canonical V13 manuscript compiled"
