# Paper A V13 — repository replacement audit
Date: 12 October 2026.

Canonical V13 has replaced the earlier 18-page integrated paper at `paper_a_integrated/paper.tex` and `paper_a_integrated/paper.pdf`. The current version has 21 pages, substantially revised proofs and an extended bibliography. The original complete source and 5 CNF/DRUP pairs are preserved in the V13 ZIP as 13 Git blobs. The historical V12 assets remain accessible in Git history.

Local V13 full-package quick checks passed on 12 October 2026: checksum manifest, independent Q7 folded-cube exhaustive classification, complete n=7 and n=8 V10 finite checks, 15 independent CNF semantic probes, gate semantics, forced-pair geometry, 120-label exhaustive protocol, and two-pass LaTeX compile. Previously frozen full V12 five-case DRUP check passed separately with 50,282 additions; this specific repository update does not represent a new rerun of all five DRUP files inside GitHub Actions.

Build now compiles the committed V13 TeX directly, avoiding accidentally restoring a prior V12 compressed manuscript.

Remaining scholarly obligations: external line-by-line review of the general V10 bound, soundness and completeness of all source-to-CNF cases, an independent verified proof checker, and a systematic recent-priority search. No journal acceptance claim or 100/100 audit score is represented by the repository files.
