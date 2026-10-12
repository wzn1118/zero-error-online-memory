# V13 verification status (12 October 2026)

The canonical journal-source TeX and PDF are committed in this directory; the complete frozen research archive is committed as 13 byte-perfect objects in `archive_parts`. Use `bash paper_a_integrated/REBUILD_V13_ARCHIVE.sh --extract` from the repository root, then `cd paper_a_integrated/PaperA_V13`.

`bash RUN_QUICK.sh` passed in the production staging environment. Its tests cover all SHA-256 manifest entries, Q7 folded-cube closure, finite V10 at dimensions 7 and 8, 15 independent CNF input sets, 2,046 gate truth tables, 512 eligible source pairs, 1,792 strong collisions and the 120-state protocol. A separate previous full V12 run checked all five frozen DRUP files and 50,282 RUP steps. Use `bash RUN_ALL.sh` for a fresh full verification.

The DRUP files establish UNSAT of their exact frozen CNFs, not a formal proof of the manuscript-to-CNF reduction. The analytic high-dimensional theorems require ordinary mathematical review, and no fully mechanically checked Lean/Coq proof is claimed.
