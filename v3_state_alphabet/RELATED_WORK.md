# Prior-work positioning and journal comparisons

## Direct predecessors

- Witsenhausen, H. S. (1976), "The zero-error side information problem and chromatic numbers," IEEE Transactions on Information Theory. DOI: 10.1109/TIT.1976.1055607. The classical task is a static graph-coloring description; the present model also constrains transitions between descriptions after blind coordinate assignments.
- Hamming, R. W. (1950), "Error Detecting and Error Correcting Codes," Bell System Technical Journal. DOI: 10.1002/j.1538-7305.1950.tb00463.x. Perfect single-error-correcting codes supply radius-one packings used by the new source-state / successor-state construction.
- Nakkiran, P., Shah, N. B., Rashmi, K. V. (2014), "Fundamental Limits on Communication for Oblivious Updates in Storage Networks." DOI: 10.1109/GLOCOM.2014.7037161. The resource is update communication to a stale node, distinct from an alphabet of persistent labels.
- Mazumdar, A., Chandar, V., Wornell, G. W. (2014), "Update-Efficiency and Local Repairability Limits for Capacity-Approaching Codes." DOI: 10.1109/JSAC.2014.140517. The work measures changes to codeword symbols and locality; the present model minimizes persistent states under a blind overwrite interface.

## Published reference points

- SCIENCE CHINA Information Sciences, *Constructions of optimal binary locally repairable codes via intersection subspaces* (DOI: 10.1007/s11432-023-3863-y): optimal code families under their own repairability constraints. The current V3 proves a matching asymptotic *order* for a different online memory alphabet quantity; the leading constant remains open.
- Frontiers of Computer Science, *MDS array codes with low disk I/O and small repair bandwidth* (DOI: 10.1007/s11704-024-3581-7): a cut-set-optimal bandwidth construction in selected regimes. The present results concern exact adversarial zero-error recovery and the number of persistent labels.
- Journal of Computer Science and Technology, *Learnability in Online Kernel Selection with Memory Constraint via Data-Dependent Regret Analysis* (DOI: 10.1007/s11390-024-2896-z): regret bounds and algorithms with fixed online memory. This research studies an adversarial overwrite model and zero-error reconstruction, so regret and alphabet cardinality are different performance metrics.

## Verification scope

The V3 general theorems are supported by analytic proofs, and the executable verifier enumerates all legal write events and erasure observations for lengths 4 through 7. The literature comparison distinguishes resource objectives and does not by itself establish publication priority.
