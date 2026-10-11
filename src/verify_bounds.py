"""Finite numerical checks of the all-parameter analytic inequalities.
These checks do not replace the proofs in the manuscript.
"""
from __future__ import annotations
from math import log2
from .bounds_and_moments import bounds, volume, dictionary_count, ceil_log2_positive


def run(limit=128):
    cases=0
    maximum_upper_ratio=(0,None)
    for n in range(2,limit+1):
        for s in range(2,n+1):
            lower=ceil_log2_positive(volume(n,s//2))
            f=s*log2(1+n/s)
            assert lower+1e-10 >= f/3
            # Largest T allowed at fixed s maximizes the bound's dictionary term.
            t=s-1
            upper=bounds(n,t,1)['upper_greedy']
            assert upper <= 5*f +1e-9,(n,s,upper,f)
            assert lower<=upper,(n,s,lower,upper)
            ratio=upper/f
            if ratio>maximum_upper_ratio[0]: maximum_upper_ratio=(ratio,(n,s,t))
            cases+=1
    return {'pairs_checked':cases,'largest_upper_ratio':maximum_upper_ratio}

if __name__=='__main__':print(run())
