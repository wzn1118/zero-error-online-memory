# Paper A — Canonical V13 (12 October 2026)

**Zinan Wang**, *Exact State Alphabets for Blind One-Write Memory: An Erasure Plateau, Sharp Cubical Constructions, and Verified Finite Obstructions*.

The canonical revised paper is [paper.tex](paper.tex), with its 21-page typeset [paper.pdf](paper.pdf). Both have been replaced with the exact V13 distribution versions. The prior V12 manuscript and binary reconstruction input remain accessible through Git history and the earlier research branches.

## Main theorem

For \(n\ge7\), one blind coordinate assignment and either \(q=n-3\) or \(q=n-2\) erased coordinates:

\[
\kappa_1(n,q)=2^n-\left\lfloor\frac{2^{n-1}}{n}\right\rfloor+\mathbf 1_{\{n=7\}}.
\]

The rounded binary storage budget is still \(n\) bits. The article and certificate apply to the finite-state model with a publicly known phase.

## Complete source and certificates

The exact **8.7 MiB comprehensive V13 ZIP** is preserved under [archive_parts/](archive_parts/) in 13 byte-exact binary parts; split upload was necessary because the direct large binary connector transfer failed. Each part is 720,000 bytes except the last. Execute:

```bash
bash paper_a_integrated/REBUILD_V13_ARCHIVE.sh --extract
cd paper_a_integrated/PaperA_V13
bash RUN_QUICK.sh
bash RUN_ALL.sh
```

The reassembly script rejects mismatched SHA-256 before extraction. Its ZIP contains all 5 frozen CNF and DRUP pairs (50,282 checked RUP additions), the V12 independent checker, V13 independent folded-cube and geometry tests, revised 21-page PDF/TeX, manifest and explanatory notes. `RUN_QUICK.sh` checks integrity, finite geometry, partial encoding semantics and LaTeX; `RUN_ALL.sh` independently rechecks all 5 frozen proofs and takes longer. Runtime environment: Python 3.10+, g++, pdflatex, sha256sum and standard Unix commands.

## Verified identifiers

- Canonical source SHA-256: `58a289f787f4fda98327b6619212a4966225f58052529c7f833ede867abfe2c5`
- Canonical PDF SHA-256: `e22c4741904b76e414922dc261791df275268bd4c5e22a3fb73c3e08b417109e`
- Full ZIP SHA-256: `77097981946fe75c1f227ab43b238d98bdc99545202213da0ca34733298ae61a`

See [V13_VERIFICATION_STATUS.md](V13_VERIFICATION_STATUS.md) for the verification scope and remaining trust boundary. Finite DRUP UNSAT claims and their source-to-CNF reduction remain separate mathematical verification obligations.
