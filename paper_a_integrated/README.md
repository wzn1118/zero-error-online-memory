# Paper A — reviewed integrated source (12 October 2026)

**Title:** Exact State Alphabets for Blind One-Write Memory: An Erasure Plateau, Sharp Cubical Constructions, and Verified Finite Obstructions.

This folder is the current Paper A draft. The single canonical editable entry point is **paper.tex**. Its four short input modules are \`v10_local_geometry.tex\`, \`v12_cnf_correspondence.tex\`, \`related_work_expanded.tex\`, and \`new_bibliography.tex\`. The stale compressed manuscript and old hard-coded-hash build entry point are superseded.

## Research claims and evidence levels

Under a public phase and deterministic, one-write, zero-error recovery model, the article derives the optimal alphabet size for n>=7 and q in {n−3,n−2}. The dimension-seven exception is a **computer-assisted finite theorem**, conditional on the source-to-CNF mathematical derivation and the independently checked Boolean clause files. The n>=8 analytic results rely on the local collision–adjacency inequality and explicit construction; the finite tests do not prove the universal theorem.

The restored V12 package holds **five frozen CNFs and five matching DRUP traces**, with 50,282 checked proof additions. They are distributed separately in the downloadable reproducibility package. The GitHub branch contains source code capable of regenerating the proof traces; CI does not represent ordinary lightweight tests as a complete DRUP recheck.

## Reproduction

\`\`\`bash
python3 verification/verify_paper_a.py
bash build.sh
\`\`\`

The lightweight verification is Python-standard-library only and validates pairwise geometry in dimensions 7 and 8, 2,046 truth/equivalence cases, all three strong-collision orbits in dimension 7, a full 120-state witness and byte-identical CNF hashes. The long proof generation workflow is in \`.github/workflows/paper-a-v12-regenerate.yml\`, and the original full proof package has its own \`verify_all.sh\` (requires g++). No Docker is required.

## Research boundaries

The exact algebraic and computer-assisted statements are available for specialist review. Publication priority, the universal combinatorial proof, and the source-to-CNF reduction have not been externally peer reviewed or formalized in Lean/Coq. The optimal binary **bit budget remains n** in the stated range, despite the integer state-alphabet saving.

This branch supersedes its previous Paper A draft. The repository main branch, historical research branches and Zenodo deposits are separate.
