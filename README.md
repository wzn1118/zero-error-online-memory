# Zero-Error Online Memory under Blind Overwrites

Zinan Wang

## Article

`paper.pdf` is the typeset article. `paper.tex` contains the complete LaTeX source; `figures/` contains its vector illustrations. The bibliography is embedded in the source.

## Reproduce the finite checks

Python 3.10 or later is required. All programs use the Python standard library.

```bash
python verify_manifest.py
python run_all.py --full
```

The full suite checks first-phase state-support incidence, the simplex family, deterministic column completion, general bounds, multiround pair counting, finite classifications, and syndrome-atom compatibility graphs. See `REPRODUCIBILITY.md` for the named checks.

## Compile the article

```bash
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The state model uses a public phase index and charges every persistent state label. Erasure recovery is required at each phase; update transitions receive the current label and coordinate assignment.