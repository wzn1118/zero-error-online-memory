# Independent V12 DRUP Reconstruction (no GitHub push)

**Status:** Certified five-case **computer-assisted** refutation of a 119-label protocol for `(n,T,q)=(7,1,4)`, paired with a fully enumerated 120-label protocol. The earlier original `.native.drup` files were lost; the five files in `proofs/` are newly generated and checked against the new `cnf/` files. Do **not** mix them with an older CNF or treat them as byte-identical copies of the missing V12 proof traces.

The completed computation supports **κ₁(7,4)=120**, subject to the correctness of the explicitly stated finite encoding equivalence and the independent proof checker's small trusted code base. This is a machine-checkable propositional certificate, *not* a Lean or Coq proof of the full mathematical reduction or a peer-reviewed publication.

## One-command verification

On Linux/macOS or Windows PowerShell with WSL, using Python 3.10+, `g++`, `sha256sum` and no external Python dependencies:

```sh
bash verify_all.sh
```

The script checks immutable SHA-256 hashes, exhaustively tests the cardinality-gate semantics, regenerates all five DIMACS CNFs and compares them byte-for-byte, recompiles the independent C++ checker, validates all five DRUP refutations (final empty clause required), audits the 7-cube pair geometry and symmetry orbits, verifies all source/write/erasure histories of a constructive 120-state protocol, and tests that intentionally corrupted/truncated proofs are rejected.

To independently regenerate the **proof traces** themselves (takes longer):

```sh
bash regenerate_proofs.sh
```

The generator (`verification/cdcl_proof.cpp`) is *not* a trusted component of proof validation. The verifier (`verification/check_drup.cpp`) independently validates every proof addition using Boolean unit propagation under negated assumptions. Both use integer arithmetic, no floating-point MILP tolerances, Docker, network or external SAT tool.

## Mathematical encoding map

There are exactly 512 eligible initial pairs of seven-bit vectors at distance 6 or 7. A hypothetical protocol with at most 119 labels necessarily uses exactly nine pair-fibers. Let `C` be their 18 distinct endpoints, `D` the forced successor-pair duplication count, `e(C)` the induced cube-edge count, and `Xi(C)` the exterior one-neighborhood overlap. The lower bound is

`K >= max(128-a, 64+6a+e(C)-D+ceil(Xi(C)/2))`, with `D<=e(C)`.

With `a=9`, the critical requirement is `e-D+ceil(Xi/2)<=1`, so either

- `B`: `Xi=0`, with a fixed distance-6 pair (mixed case) or a fixed antipodal pair (antipodal-only case); or
- `A`: `e-D=0`, `Xi<=2`, and at least one strong forced-pair collision. There are exactly three isometry orbits of such collision pairs, represented by normal distance-6, special distance-6, and antipodal translations.

Each CNF encodes the exact-nine cardinality, pair disjointness, selected word variables, the relevant constraints and symmetry seed. In case A, every conflicting initial pair-pair combination with positive `e-D` is forbidden; the exterior-neighborhood excess is encoded using exact Boolean threshold gates. In case B, every exterior word is forbidden from having two selected neighbors. Fully equivalent Tseitin definitions are used throughout.

See `docs/FORMAL_RECONSTRUCTION.tex` and `docs/V11_five_case_reduction_prior.tex` for the full derivation, together with `verification/` scripts.

## Research integrity and publication

No remote action was taken. All existing GitHub branches and Zenodo records remain unchanged. A strict independent referee should still review the paper-to-CNF reduction and the source-level C++ verifier. The computation alone does not establish originality relative to the literature.

## Windows / WSL linker-output fix (2026-10-12)

The portable `verify_all.sh` creates `.v12-check.XXXXXXXX/` under the
**extracted repository directory** rather than relying on WSL `/tmp`. The
temporary directory is cleaned at exit. This avoids a reported WSL linker
error (`cannot open output file /tmp/tmp.*/check_drup: No such file or directory`).
This patch changes only the verifier's temporary build path and documents
Windows steps; the five CNF files, five DRUP files and source-level mathematical
checkers are byte-for-byte unchanged.

In PowerShell, after extracting the ZIP to a normal writable folder:

```powershell
cd "C:\Users\10847\Downloads\Online_Memory_V12_WSL_Fix_UNPUSHED_2026-10-12"
wsl bash ./verify_all.sh
```

If `g++: command not found`, inside WSL install a C++ toolchain
(`sudo apt update && sudo apt install -y g++` in Ubuntu), then rerun.
The WSL `localhost` proxy and systemd warnings do not by themselves
indicate verification failure. Verify that the final output ends in `COMPLETE`.
If the script stops, quote the **first line containing `FAIL` or `error`**,
not only the WSL startup warnings.

See `WINDOWS_WSL_FIX.md` for the diagnosis and alternate one-file patch.
