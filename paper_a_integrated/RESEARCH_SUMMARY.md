# Paper A — Exact State Alphabets for Blind One-Write Memory

**Zinan Wang — integrated research draft, 12 October 2026**

This branch is an independent integration line. It preserves the repository's earlier `main`, V3, and V5 sources and all existing Zenodo records. The full 18-page typeset paper, editable `paper.tex`, and the 8.3 MB independent CNF/DRUP certificate archive are supplied in the companion research package shared in the conversation; this GitHub note records the research version and its exact theorem statement.

## Model and scope

The encoder initializes a persistent label from a binary record `x∈{0,1}^n`. One update is a coordinate assignment `x_i←b`; the state transition sees only the old label and `(i,b)`, never the overwritten bit. A phase-aware decoder receives the current nonerased coordinates and the label, and must reconstruct up to `q` erasures without error. The minimum number of persistent state labels is `κ₁(n,q)`; the minimum bit cost is `⌈log₂ κ₁(n,q)⌉`.

## Main combined theorem — two-level erasure plateau

For every `n≥7`, and `q∈{n−3,n−2}`:

```
κ₁(n,q) = 2^n − floor(2^(n−1)/n) + 1[n=7].
```

Thus `κ₁(7,4)=κ₁(7,5)=120`; for `n≥8` the formula has an analytic lower bound and explicit Hamming-prefix cubical construction. The optimal rounded bit cost remains `n`.

## Proof architecture

1. **Collision restriction:** if two sources share an initial label, their initial distance exceeds `1+q`.
2. **High-erasure matching normal form:** initial distance-constrained doubletons form a matching; every one-write image forces a valid terminal pair. Residual terminal vertices are paired using maximum matching.
3. **Exact variational principle at `q=n−2`:** initial doubletons are antipodal. For `N=2^n`, `C=\bar C`, `a=|C|/2`, and `Ξ(C)=Σ_{y∉C}max(d_C(y)−1,0)`:
   ```
   κ₁(n,n−2) = min_C max{N−a, N/2+(n−1)a+Ξ(C)/2}.
   ```
4. **Universal converse:** counting distinct forced successor pairs and their Hamming neighborhood yields `κ₁≥N−floor(N/(2n))`. For the `q=n−3` layer, the collision–adjacency inequality `D≤e(C)` yields the same lower bound.
5. **Sharp construction:** for all `n≥8`, Hamming-prefix codewords with suffix subcubes give `a=floor(2^(n−1)/n)` and `Ξ(C)=0`. The `n=13` special suffix packing is handled explicitly.
6. **Finite exception:** five mutually covering CNF cases exclude 119 labels for `n=7,q=4`. Five independently *checked* DRUP refutations contain 50,282 accepted RUP additions in total; an explicit 120-label protocol passes exhaustive write and erasure tests.

## Scientific and verification boundary

The five DRUP files certify unsatisfiability of their corresponding frozen CNFs; the mathematical reduction from arbitrary protocols to these cases, and the general-length inequalities, must be reviewed separately. The entire computer-assisted proof does not amount to formal verification of the full paper.

The seven-stage V12 certificate suite was rerun on 12 October 2026: SHA-256 manifest, 2,046 exact-cardinality tests, byte-identical CNF regeneration, independent proof checking, seven-cube orbit coverage, the explicit protocol, and adversarial certificate corruption tests all passed.

## Follow-on research kept separate

The earlier paper's online/static logarithmic **bit** separation and multiround distance-spectrum inequalities are reserved for Paper B. The fixed-syndrome compatibility and affine-subspace puncturing graph colorings are reserved for Paper C.

## Status

Mathematical-substance provisional score: 89/100; journal submission maturity: 87/100. The branch is a research record, not a peer-reviewed publication or a claim of top-journal acceptance. The complete canonical LaTeX/PDF and DRUP files are distributed in the downloadable research package, not committed to this branch in this initial lightweight GitHub snapshot.

Reference Zenodo V2 DOI: https://doi.org/10.5281/zenodo.23299231

## V13 independent verification addendum (12 October 2026)

The separate research branch now includes `paper_a_integrated/verification/verify_folded_cube_exception.py`, an independently coded no-SAT exhaustive folded-cube check supporting the seven-dimensional exception. In the full downloadable V13 submission package, the updated 21-page article adds a detailed local-predecessor argument, a five-case source-to-CNF implication, expanded prior work, and separately archived frozen five-case CNF/DRUP proofs. The downloadable package is the canonical V13 article; this GitHub branch is a partial source mirror and does not yet contain the exact complete V13 PDF/TeX or frozen proof traces. No mathematical theorem or publication status on `main` has been changed.
