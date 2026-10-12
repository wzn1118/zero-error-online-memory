# Paper A V13 audit and reproducibility upgrade — 12 October 2026

Research branch: \`research/paper-a-v13-verification-upgrade-2026-10-12\`.

## Scientific claim and limitations
The candidate main theorem is the two-level exact state alphabet
\(\kappa_1(n,q)=2^n-\lfloor2^{n-1}/n\rfloor+\mathbf1_{n=7}\)
for \(n\ge7,\;q\in\{n-3,n-2\}\), with one blind coordinate assignment and public phase. Its rounded bit cost remains \(n\).

The V12 full frozen CNF/DRUP package was retrieved and fully executed in a Linux environment on 12 October 2026, passing all seven stages. Its five RUP proofs have 801, 32,062, 4,860, 5,706 and 6,853 accepted additions respectively, a total of 50,282. The canonical full frozen proofs are supplied in the downloadable comprehensive V13 research package, not all mirrored into this lightweight GitHub branch.

## New independent reproduction
Run \`python3 paper_a_integrated/verification/verify_folded_cube_exception.py\`.

This separate implementation exhaustively certifies that a complement-invariant 18-point subset of \(Q_7\) must have \(\Xi(C)\ge6\). The enumerator reports 7,549 closed sets for zero exterior excess, 26 for excess one, and 1,721 across 1,358 exhaustive cases for excess two. It does not invoke a SAT solver or the existing V12 proof machinery.

The V10 inequality was independently tested for all 127,232 admissible disjoint pair-pair combinations at \(n=7\) and 653,760 at \(n=8\); no finite counterexamples arose. Those tests are in the downloadable full research package.

## Remaining trust boundary
The universal V10 inequality and cubical packing proof require general mathematical reasoning; finite tests do not establish all \(n\). CNF/DRUP UNSAT validates only the encoded cases; source-to-CNF correctness and orbit coverage require their separate mathematical and source-level arguments. An independently verified LRAT kernel and a Lean/Coq end-to-end proof are not currently available. No 100/100 or acceptance guarantee is claimed.

The previous \`main\`, historical research branches and Zenodo deposits remain unchanged.
