#!/usr/bin/env python3
"""Integer-only checker for parity-sensitive saturation certificates."""
from math import comb
from itertools import combinations

def choose(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def plotkin_upper(n,d):
    assert 2*d>n
    return (2*d)//(2*d-n)

def parity_energy_bound(n,d,t,A):
    assert d%2==1
    n_cross=(A*A)//4
    n_same=choose(A,2)-n_cross
    return n_cross*choose(n-d,t) + n_same*choose(n-d-1,t)

def certificate(n,T,q):
    s=T+q
    assert 1<=q<=n and 1<=T and s<n
    winning=[]
    for t in range(1,T+1):
        d=s-t+1
        if d%2==0 or 2*d<=n: continue
        A=plotkin_upper(n,d)
        L=choose(s+1,t)
        B=parity_energy_bound(n,d,t,A)
        coarse=choose(A,2)*choose(n-d,t)
        if L>B:
            winning.append((t,d,A,L,B,coarse))
    # A(n,s+1) <= 3 certifies static bit bound >= n-1;
    # antipodal pairing gives <=n-1.
    d0=s+1
    assert 2*d0>n
    assert plotkin_upper(n,d0)<=3
    assert winning
    return winning

def selftest_parity_bound():
    # Exhaustively verify parity capacity on every small code of 4 words in F2^5.
    n,d,t,M=5,3,1,4
    upper=parity_energy_bound(n,d,t,M)
    best=-1; arg=None; admissible=0
    for C in combinations(range(1<<n),M):
        ds=[(x^y).bit_count() for x,y in combinations(C,2)]
        if min(ds)<d:continue
        admissible+=1
        E=sum(choose(n-v,t) for v in ds)
        if E>best:best=E;arg=C
        assert E<=upper
    assert best==upper==10
    print('EXHAUSTIVE n=5,M=4,d=3,t=1:',admissible,'codes; max energy',best, 'witness',arg)

def run():
    selftest_parity_bound()
    for args in [(53,5,30),(61,4,36)]:
        result=certificate(*args)
        print('CERTIFICATE n,T,q=',args,'new witnesses=',result)
        # At least one new proof where the old Plotkin/cardinality test fails at every t.
        n,T,q=args;s=T+q
        for t in range(1,T+1):
            d=s-t+1
            if 2*d>n:
                A=plotkin_upper(n,d)
                assert choose(s+1,t) <= choose(A,2)*choose(n-d,t)
    print('PASS all exact integer and exhaustive certificates')

if __name__=='__main__':run()
