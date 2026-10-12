# Paper A — Exact State Alphabets for Blind One-Write Memory (V13)

**Canonical version: 12 October 2026**, Zinan Wang.

This independent research article solves an exact state-alphabet problem for one blind overwrite. In the public-phase, zero-error model the theorem states, for all n ≥ 7 and q ∈ {n−3,n−2}:

```
κ₁(n,q) = 2^n − floor(2^(n−1)/n) + 1[n=7].
```

Thus κ₁(7,4)=κ₁(7,5)=120, while dimensions n ≥ 8 have analytic construction and converse proofs. The rounded bit cost is n in both erasure regimes. Paper A unifies the exact variational reduction, near-maximal erasure plateau, Hamming-prefix cube construction, local forced-successor geometry, and exceptional seven-cube finite proof.

The canonical 21-page V13 [TeX](paper.tex) and [PDF](paper.pdf) are tracked directly. The complete 8.7 MiB research bundle is stored in [13 reconstructible parts](archive_parts/) with sha256-checked reassembly. [One-command instructions](README.md).

Independent validation: the folded-cube exception enumerator and two additional V10/V12 audits passed; the frozen five CNF/DRUP certificates have 50,282 accepted RUP additions in total from a completed independent V12 check. Full reruns remain available in the recovered archive. The analysis is a research result awaiting external peer review, not an accepted publication or an end-to-end formally verified proof.

Older V2 multiround results and syndrome-coloring results remain separate prospective papers. Historical `main/paper.tex` retains their prior manuscript; Paper A V13 lives under `paper_a_integrated/`.
