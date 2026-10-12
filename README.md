# Zero-Error Online Memory

Zinan Wang

## Current Paper A — V13 (12 October 2026)

**Exact State Alphabets for Blind One-Write Memory: An Erasure Plateau, Sharp Cubical Constructions, and Verified Finite Obstructions**

- [Read the canonical 21-page V13 PDF](paper_a_integrated/paper.pdf)
- [Editable V13 LaTeX manuscript](paper_a_integrated/paper.tex)
- [Paper A current README and reproduction instructions](paper_a_integrated/README.md)
- [Complete reproducibility archive as 13 Git-tracked parts](paper_a_integrated/archive_parts/)
- [Independent Q7 exception and V10/V12 verification scripts](paper_a_integrated/verification/)
- [Evidence ledger and limitations](paper_a_integrated/V13_VERIFICATION_STATUS.md)

For a local clone:

```bash
bash paper_a_integrated/REBUILD_V13_ARCHIVE.sh --extract
cd paper_a_integrated/PaperA_V13
bash RUN_QUICK.sh
bash RUN_ALL.sh
```

The compiled PDF and frozen V13 proof package are preserved in Git. Historical source `paper.tex` at the repository root is an earlier, broader manuscript concerning multiple online-memory results, retained for research provenance. The V13 paper replaces the older integrated Paper A under `paper_a_integrated`; unrelated historical results and branches remain intact.

The theorem concerns the *cardinality* of the persistent state alphabet under one blind coordinate assignment and up to q erased coordinates with public phase. The minimum binary bit budget remains n in both high-erasure layers. Finite DRUP certificates establish UNSAT of their encoded propositions; the analytic proofs and source-to-CNF reduction are separate review obligations.
