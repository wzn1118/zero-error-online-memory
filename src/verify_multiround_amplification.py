"""Exact small-instance audit of the many-round forced-pair counting lemma.

Standard library only. Counts unordered output pairs arising from EVERY input
pair of min distance s+1 after assigning t DISTINCT originally differing
coordinates (in increasing index order). Uses no optimization black box.
"""
from collections import Counter
from itertools import combinations, product
from math import comb

def audit_case(n, T, q, t):
    s=T+q
    assert 1<=t<=T and s<n
    counts=Counter(); count_sources=0; occurrences=0
    for x in range(1<<n):
        for y in range(x+1,1<<n):
            differing=[i for i in range(n) if (x^y)>>i&1]
            d=len(differing)
            if d<s+1: continue
            count_sources+=1
            before=occurrences
            for W in combinations(differing,t):
                mask=sum(1<<i for i in W)
                for bits in product((0,1), repeat=t):
                    assign=sum(v<<i for i,v in zip(W,bits))
                    a=(x&~mask)|assign
                    b=(y&~mask)|assign
                    assert (a^b).bit_count()==d-t
                    counts[(min(a,b),max(a,b))]+=1
                    occurrences+=1
            assert occurrences-before==comb(d,t)*(1<<t)
    cap=comb(n-s-1+t,t)*(1<<t)
    assert max(counts.values())<=cap
    assert occurrences >= count_sources*comb(s+1,t)*(1<<t)
    assert occurrences <= len(counts)*cap
    return dict(n=n,T=T,q=q,t=t,source_pairs=count_sources,
                occurrences=occurrences,distinct=len(counts),
                observed_max=max(counts.values()),multiplicity_cap=cap)

def run():
    rows=[]
    for n in range(4,8):
        for T in range(1,min(3,n-2)+1):
            for q in range(1,n-T):
                for t in range(1,T+1):
                    rows.append(audit_case(n,T,q,t))
    print('All-pairs t-step combinatorial checks:',len(rows))
    return rows

if __name__=='__main__':
    print(run()[-5:])
