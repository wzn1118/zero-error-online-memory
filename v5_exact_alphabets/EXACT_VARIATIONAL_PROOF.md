# Exact one-write alphabets: new V5 proof note

Zinan Wang · 2026-10-12

## Operational model

Let X={0,1}^n. An initial encoder f:X→[K] observes x. One blind update receives only its state label and a coordinate/value assignment (i,b), after which a phase-aware decoder receives the label and the current unerased coordinates and must recover every erasure set of size at most q. Denote the minimum common state-alphabet cardinality by κ₁(n,q).

In the extremal regime q=n−2, every nonsingleton phase-zero fiber is an antipodal pair {x,x̄}; every phase-one label supports at most two words, at Hamming distance at least n−1.

## Exact variational theorem

Write N=2^n. For any complement-invariant C⊆X (so x∈C iff x̄∈C), put a=|C|/2, d_C(y)=|{i:y⊕e_i∈C}| and

Ξ(C)=Σ_{y∉C} max(d_C(y)−1,0).

Then, for every n≥4,

κ₁(n,n−2) = min_{C complement-invariant} max{N−a, N/2+(n−1)a+Ξ(C)/2}.

This identity is exact for arbitrary deterministic online protocols.

### Proof

Every valid initial encoder has a antipodal two-word fiber for each paired state and singleton fibers elsewhere. Let C be the union of its doubleton fibers; then at least N−a phase-zero labels are needed.

For each initial pair {x,x̄} and each of the 2n events (i,b), its images form a *forced* terminal pair of distance n−1. Put e(C)=the number of distance-one edges induced by C. Each forced pair identifies its updated coordinate and value; duplicates from two distinct initial pairs occur exactly along adjacent antipodal source pairs. Therefore the number of distinct forced terminal pairs is 2na−e(C), and their union is the closed Hamming neighborhood B₁(C).

Counting incidences of unit-radius balls yields the exact identity:

|B₁(C)| = 2(n+1)a − 2e(C) − Ξ(C).

Indeed, centered points in C contribute 2e(C) repetitions; the exterior point y contributes max(d_C(y)−1,0). Each forced terminal pair needs a distinct label since A(n,n−1)=2. The reachable points outside B₁(C) require at least (N−|B₁(C)|)/2 additional labels. Consequently

K₁ ≥ (2na−e(C))+(N−|B₁(C)|)/2 = N/2+(n−1)a+Ξ(C)/2.

For achievability, use exactly those source antipodal fibers and other singleton fibers at phase zero. Give each distinct forced terminal pair one label and pair every word outside B₁(C) with its antipode. The residual set is complement-invariant, and terminal pairs have distance n−1 or n. Map an initial pair to its forced output label; map an initial singleton to a canonical label containing its updated word. Both maps depend only on the initial label and the public assignment. Every erasure observation of size at most n−2 is uniquely decodable. The phase-specific labels can be reused, so K=max(K₀,K₁) attains the formula. Since complementation pairs the exterior points, Ξ(C) is even.

## Sharp universal converse and exact dyadic optima

Because Ξ(C)≥0, minimizing the maximum of N−a and N/2+(n−1)a yields

2^n−κ₁(n,n−2) ≤ floor(2^(n−1)/n).

If n=2^r with r≥2, let m=r+1, p=n−m and C={0^m,1^m}×{0,1}^p. This C is complement-invariant, a=2^p=2^(n−1)/n, and Ξ(C)=0: an exterior word has at most one C neighbor because the two allowed prefixes have distance m≥3. Hence the above bound is attained *exactly*:

κ₁(n,n−2) = 2^n − 2^(n−1)/n, for every n=2^r≥4.

These extremizers admit polynomial-time state indexing and transition computation from the fixed prefix and unconstrained suffix.

At a dyadic n, equality for any canonical protocol induced by C holds **if and only if** |C|=2^n/n and Ξ(C)=0. Necessity follows from simultaneously forcing both affine lower bounds to their common meeting value.

## Exact length-five optimum

For n=5 and q=3, the converse gives κ₁(5,3)≥32−floor(32/10)=29. Choose C from the three antipodal pairs

- (00000,11111)
- (00001,11110)
- (00010,11101).

Here a=3 and Ξ(C)=2. Thus K=max(32−3,16+4·3+1)=29, proving κ₁(5,3)=29.

## Relationship to the integrated research manuscript

This independent new theorem augments the V3 one-write saturation and V4 sharp all-length asymptotics Δₙ ~ 2^(n−1)/n. The full integrated 46-page V5 LaTeX/PDF and comprehensive reproducibility package are distributed as separate research artifacts. This note captures the exact new mathematical proofs for repository review; it is not a substitute for peer review or a priority certificate.

Foundational comparisons: H. S. Witsenhausen, *IEEE Trans. Inf. Theory* (1976), DOI 10.1109/TIT.1976.1055607; R. W. Hamming (1950), DOI 10.1002/j.1538-7305.1950.tb00463.x; P. Nakkiran, N. Shah, K. V. Rashmi, *IEEE GLOBECOM* (2014), arXiv:1409.1666.
