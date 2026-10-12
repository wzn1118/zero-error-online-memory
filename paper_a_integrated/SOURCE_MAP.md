# Integrated Paper A: proof dependency map

**Research branch:** `research/paper-a-integrated-2026-10-12`.

Main unified theorem: for n≥7 and one blind overwrite, the exact optimal label cardinality is the same at erasure budgets q=n−3 and q=n−2, namely 2^n−⌊2^(n−1)/n⌋+1[n=7].

| Component | Prior source | Claim used | Type of evidence |
|---|---|---|---|
| Online operational model and collision restriction | V2 corrected | source fibers min distance | analytic |
| High-erasure exact matching normal form | V9 | terminal forced-pair matching | analytic |
| Exact complement-invariant variation | V5 | q=n−2 state optimum | analytic + finite |
| Universal alphabet lower bound | V4, V5 | N−⌊N/(2n)⌋ | analytic |
| Hamming-prefix cubical construction | V7 | upper bound for n≥8 (n=13 special) | analytic + finite checks |
| Collision–adjacency converse | V10 | same bound at q=n−3 | analytic + finite checks |
| Seven-cube orbit cases | V11–V12 | reductions of 119-state possibility | analytic finite-case audit |
| Five CNF/DRUP proof tracks | V12 WSL fixed | unsatisfiability of five encoded cases | computational proof |
| 120-state seven-cube protocol | V11–V12 | matching upper bound | exhaustive execution |

Full original fixed certificate archive is available with the independently distributed research package. The GitHub script archive supports regeneration of all five traces from source. Computational proof validity must be distinguished from correctness of mathematical encoding into CNF.

**Local canonical hashes (12 October 2026)**

- paper.tex: `07ce9a85328a043390c194302a9003aa45efe4ef13d477767fb36f7c4a3aa0b6`
- locally compiled paper.pdf: `c22148c75b33917bad4c02743eda7e149ea66ede1b13c80244e33a635ca90654`
- V12 fixed proof archive: `180159fb80db7886c662d9c450da8daeb5b5835542312cb4a3d386e7a3723eb9`

A new GitHub Actions build can produce a different PDF byte hash due to compiler timestamps even when the TeX source is identical; compare its committed source hash first.
