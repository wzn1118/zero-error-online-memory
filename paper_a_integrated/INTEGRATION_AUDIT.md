# Paper A integration — audit & artifact manifest
Date: 12 October 2026. Author: Zinan Wang.

## Overall assessment
- Mathematical-substance rating: 89/100 (provisional).
- Journal submission maturity: 87/100 (provisional).
- Finite certificate evidence: all five frozen CNF/DRUP cases plus 120-label witness passed the seven-stage local verifier on 12 October 2026.
- CI-independent LaTeX compile: two full passes, 18 pages, no unresolved citations or overfull-box warnings.
- Verdict: suitable for a dedicated research branch and external specialist review; not yet a certified top-journal-ready submission.

## Consolidation
Paper A comprises the V5 exact variational principle, V7 Hamming-prefix cubical constructions, V9 high-erasure matching normal form, V10 collision–adjacency converse, and V12 certified exceptional case. Earlier V2 multiround bounds and syndrome colorings remain separate candidate papers.

## Exact source and artifact hashes (local canonical pack)
```
07ce9a85328a043390c194302a9003aa45efe4ef13d477767fb36f7c4a3aa0b6  paper.tex
c22148c75b33917bad4c02743eda7e149ea66ede1b13c80244e33a635ca90654  paper.pdf
180159fb80db7886c662d9c450da8daeb5b5835542312cb4a3d386e7a3723eb9  V12_Independent_CNF_DRUP_WSL_Fixed.zip
```

## Proof verification
The V12 seven-stage command `bash verify_all.sh` passed: SHA-256 check; 2,046 cardinality-encoding semantic tests; five byte-identical CNFs; 50,282 proof steps checked by RUP; full seven-cube symmetry coverage; complete 120-label decoder tests; negative controls on corrupted proofs.

## Remaining review requirements
1. Independent mathematical audit of the V10 general inequality `D ≤ e(C)`.
2. Independent checking of V7 cubical constructions, including special `n=13`.
3. Expert audit of the mathematical five-case partition and source-to-CNF correspondence. CNF UNSAT certificates prove only the encoded formulas.
4. Systematic novelty assessment against adjacent zero-error coding and online storage models.
5. Deposit final source, PDF and full DRUP supplement in stable public hosting before citing a new version DOI.

## Upload scope
This GitHub branch currently records the integration summary and audit ledger. The complete 18-page canonical PDF, editable TeX and 8.3 MB DRUP archive are available in the conversation's downloadable integration package, but this connector submission did **not** yet transfer their raw bytes to GitHub. Do not represent this branch as containing the complete journal-source tree until its contents have been uploaded and hashes matched.
