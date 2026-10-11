# Sharp first-order alphabet-deficit theorem (V4)

**Author:** Zinan Wang.  **Status:** Independent research extension of V3.

Let \(\kappa_1(n,n-2)\) denote the smallest persistent state alphabet for a deterministic one-overwrite protocol with at most \(n-2\) erased coordinates, and put \(\Delta_n=2^n-\kappa_1(n,n-2)\).

## Main theorem

For every \(n\ge 4\),
\[
\Delta_n\le\left\lfloor\frac{2^n}{2n}\right\rfloor.
\]
For every \(n\ge1024\), writing \(\ell=\lceil\log_2 n\rceil\),
\[
\left(1-\frac{2}{\ell^2}\right)\frac{2^n}{2n}
\le \Delta_n\le
\left\lfloor\frac{2^n}{2n}\right\rfloor.
\]
Consequently the **exact first-order limit** is
\[
\boxed{\displaystyle \lim_{n\to\infty}
\frac{2n(2^n-\kappa_1(n,n-2))}{2^n}=1.}
\]

### Proof of the finite-length converse

At phase zero every nonsingleton fiber is an antipodal pair, since any two words sharing an initial label must have distance at least \(q+T+1=n\). Let \(a\) be the number of such pairs, \(C\) their \(2a\) endpoints, and \(e(C)\) the number of distance-one edges induced by \(C\) in the binary \(n\)-cube. Let \(\mathcal F\) be the set of forced successor pairs produced by all writes from these initial pairs.

Each source pair has \(2n\) forced successor pairs, all of distance \(n-1\). A forced pair can originate from at most two source antipodal pairs. Two source pairs generate the same forced pair precisely when their members are adjacent in the cube. Counting the resulting duplicated pairs yields
\[
|\mathcal F|=2na-e(C).
\]
The union of the members of \(\mathcal F\) is exactly the closed radius-one neighborhood \(B_1(C)\). Double-counting incidences \((c,y)\) with \(c\in C\) and \(y\in B_1(c)\) gives
\[
|B_1(C)|\le (n+1)|C|-2e(C)=2(n+1)a-2e(C).
\]
A phase-one label can contain at most two current words because \(A(n,n-1)=2\) for \(n\ge4\). Every forced pair requires its own label and every word outside \(B_1(C)\) is phase-one reachable and cannot use a forced-pair label. Therefore
\[
K\ge |\mathcal F|+\frac{2^n-|B_1(C)|}{2}
\ge 2^{n-1}+(n-1)a.
\]
Phase zero requires \(K\ge2^n-a\). Minimizing the maximum of these two affine bounds over \(a\ge0\) yields
\[
K\ge 2^n-\frac{2^n}{2n}.
\]
Integer rounding proves the claimed converse.

### Proof of the constructive asymptotic lower bound

Let \(m<n\), \(p=n-m\), and let \(A\subseteq\mathbb F_2^m\) be a complement-invariant binary code of minimum distance at least three and even size \(t\). Put \(C=A\times\mathbb F_2^p\), with \(a=|C|/2=t2^{p-1}\). Initially pair complementary words of \(C\), and use singleton labels elsewhere, requiring \(K_0=2^n-a\).

The induced cube has \(e(C)=pa\) edges, and disjoint radius-one neighborhoods of the distinct code prefixes imply \(|B_1(C)|=2a(m+1)\). Use every distinct forced successor edge as a phase-one fiber and pair all remaining phase-one words antipodally. The forced-pair count is \(2na-pa=a(n+m)\); the total terminal labels equal
\[
K_1=a(n+m)+\frac{2^n-2a(m+1)}{2}
=2^{n-1}+(n-1)a.
\]
These fibers have minimum distance at least \(n-1\). Every paired initial label maps to its forced successor pair; a singleton initial label maps to a terminal fiber containing the updated word. If \(t\le2^m/n\), then \(a\le2^n/(2n)\) and \(K_1\le K_0\), giving \(\Delta_n\ge a\).

For \(n\ge1024\), set \(\ell=\lceil\log_2 n\rceil\) and \(m=\lceil\log_2(n\ell^2)\rceil\). Then \(m\le2\ell-1\) and \(n\ge 2V(m,2)\), where \(V(m,2)=1+m+\binom m2\). A deterministic greedy algorithm that selects complementary pairs at mutual Hamming distance at least three can choose
\[
t=2\left\lfloor\frac{2^m}{2n}\right\rfloor
\ge\frac{2^m}{n}-2
\]
prefix codewords, because each selected pair excludes at most \(2V(m,2)\) candidate complementary pairs among the \(2^{m-1}\) orbits. Since \(2^m\ge n\ell^2\),
\[
\Delta_n\ge a
=\frac{t2^{n-m}}2
\ge\frac{2^n}{2n}-\frac{2^n}{2^m}
\ge\left(1-\frac{2}{\ell^2}\right)\frac{2^n}{2n}.
\]
This proves the constructive bound and the limit.

The prefix search examines fewer than \(2n\ell^2\) words; indexing by canonical complement-pair representatives and free suffix bits yields polynomial-time labeling, transitions and decoding.

## Reproducibility and scope

The accompanying independent V4 program checks all 256 possible antipodal-pair selections for \(n=4\), 345 additional seeded configurations at \(4\le n\le8\), complete finite subcube state machines at \(n=7,8\), and greedy construction parameters at \(n=1024,1025,2048,4096,10000,65536\). The finite checks verify combinatorial identities and representative protocols; the preceding analytic argument supports the general asymptotic claim.

V2 and V3 mathematical results are preserved on their existing branches. V4 publication and journal submission should use a separately frozen and verified full manuscript.
