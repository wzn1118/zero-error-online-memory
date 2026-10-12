# Paper A V13 — proof-to-source map

Canonical journal manuscript: `paper_a_integrated/paper.tex` (21 pages; SHA-256 58a289f787f4fda98327b6619212a4966225f58052529c7f833ede867abfe2c5).

| Mathematical component | Source | Verification |
| --- | --- | --- |
| One-write high-erasure matching normal form | analytic manuscript; V9 | general proof |
| Complement-invariant variational theorem | analytic manuscript; V5 | small n examples |
| Sharp finite length bound | analytic manuscript; V4–V5 | finite audits |
| Hamming-prefix cubical packing, n=13 exceptional packing | analytic manuscript; V7 | finite construction check |
| Collision–adjacency D≤e(C) for n−3 layer | analytic manuscript; V10 | `verification/independent_v10_audit.py` at n=7,8 |
| Seven-cube folded quotient classification | analytic manuscript; V7–V12 | `verification/verify_folded_cube_exception.py` |
| 119-label nonexistence for (7,1,4) | V12 independent CNF + DRUP | `PaperA_V13/v12_certificates/verify_all.sh` after archive reassembly |
| Finite encoding tests and 120-label upper bound | V12 | `verification/independent_v12_encoding_audit.py` and V12 suite |

The full V13 reproducibility ZIP, including all canonical sources, compiled PDF, 5 frozen CNFs, 5 frozen DRUP proofs and verification logs, can be recovered from `archive_parts` with `REBUILD_V13_ARCHIVE.sh --extract`.

A checked unsatisfiable CNF is not by itself a proof that all counterexamples satisfy that encoding. The general geometric inequalities and the five-case reduction remain independent mathematical proof obligations.
