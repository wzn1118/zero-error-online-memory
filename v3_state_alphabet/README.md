# V3 research revision: sharp state-alphabet deficits

Zinan Wang · 11 October 2026

**Title:** Zero-Error Online Memory under Blind Overwrites: State-Alphabet Deficits, Sharp Storage Gaps, and Syndrome Compatibility.

The existing V2 paper and all original files remain unchanged at the repository root. This folder is an independent V3 development line. The research branch is \`research/v3-state-alphabet-gap\`. The \`main\` branch is unaffected.

## Mathematical results

For a single blind overwrite and \`n>=4\`, the full \`2^n\` state alphabet is necessary exactly when the erasure budget \`q>=n-1\`. For \`q<=n-2\` the new two-antipodal-pair protocol uses at most \`2^n-2\` states.

At the maximal budget permitting any initial collision (\`q=n-2\`) the state deficit \`Delta_n=2^n-kappa_1(n,n-2)\` obeys:
\`\`\`
2^n/[4(n+24)] < Delta_n <= 2^n/(n+1)
Delta_n = Theta(2^n/n).
\`\`\`

The universal construction uses complement-invariant distance-three binary codes with zero-sum parity-check columns. The converse counts forced terminal edges. Perfect Hamming codes improve the constructive constant when \`n=2^r-1\`. The established bit saturation, online/static logarithmic gap, multiround inequalities, and syndrome-graph results remain in the full article.

## Source and reproducibility

\`extension.tex\` contains the new mathematical section, with complete proofs. \`build_v3.py\` produces the integrated \`paper.tex\` from the unchanged V2 root \`paper.tex\`. GitHub Actions compiles \`paper.pdf\` and checks the V2 suite plus the added exhaustive verifier. All files in this directory are isolated from the V2 root publication.

From repository root:

\`\`\`sh
python3 verify_manifest.py
python3 run_all.py --full
python3 v3_state_alphabet/verification/verify_state_deficit.py
python3 v3_state_alphabet/build_v3.py
pdflatex -jobname=paper -output-directory=v3_state_alphabet -interaction=nonstopmode -halt-on-error v3_state_alphabet/paper.tex
pdflatex -jobname=paper -output-directory=v3_state_alphabet -interaction=nonstopmode -halt-on-error v3_state_alphabet/paper.tex
\`\`\`

V2 Zenodo record: https://doi.org/10.5281/zenodo.23299231. The V3 research revision has no DOI until separately deposited.
