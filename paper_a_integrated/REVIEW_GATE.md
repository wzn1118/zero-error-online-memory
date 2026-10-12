# Replacement review gate — Paper A

- Manuscript: extended related work; explicit V10 local predecessor lemma; V12 complete five-case mapping; careful computational trust boundary.
- V10: 127,232 disjoint legal pair-pair checks at n=7, 653,760 at n=8; zero counterexamples in these finite dimensions.
- V12: 2,046 exact-cardinality gate checks; 512 source pairs; 1,792 strong collisions split 1,344/224/224; 120-state full-phase decoder verification.
- Frozen five-CNF digests are enforced by \`verification/verify_paper_a.py\`.
- Full five DRUP certificate audit was executed on the local archival package. **GitHub CI does not check those DRUP files because only proof generators/checkers, not the 8MB proof bundle, are present on branch.** On-demand regeneration is available.
- Literature positioning explicitly cites Witsenhausen (1976/1979), Ahlswede and Zhang (1989), Chandran et al. (2014), Nakkiran et al. (2014), Hamming graph coloring, and Charpenay et al. (2024).
- Current internal audit estimate: 86/100, subject to independent external proof/priority review; **no journal acceptance or full formalization claim**.
