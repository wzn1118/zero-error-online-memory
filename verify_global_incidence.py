#!/usr/bin/env python3
"""Independent finite checks for the global one-overwrite incidence converse.

Uses standard library only. It does not assert to verify the universal theorem by enumeration.
"""
import argparse
import itertools
import math
from fractions import Fraction


def code_plotkin_bound(n,d):
    return (2*d)//(2*d-n) if 2*d>n else None


def nonzero_simplex(k,m):
    r=1<<k
    cols=[v for _ in range(m) for v in range(1,r)]
    code=[sum(((a & v).bit_count()&1)<<j for j,v in enumerate(cols)) for a in range(r)]
    return cols,code


def verify_onewrite_simplex(k):
    r=1<<k
    n=4*(r-1)
    d=2*r
    q=n//2
    cols,code=nonzero_simplex(k,4)
    assert len(cols)==n
    assert len(set(code))==r
    weights=[(v.bit_count()) for v in code[1:]]
    assert set(weights)=={d}
    assert code_plotkin_bound(n,d)==r
    s=q+1
    assert d==s+1
    phase_cap=code_plotkin_bound(n,s)
    assert phase_cap==s
    assert phase_cap<=s+1
    k_states=1<<n
    assert Fraction((s+1)*k_states,phase_cap+s) > k_states//2
    print(f'k={k}, n={n}, T=1, q={q}, d={d}, A(n,d)={r}, bound A(n,s)<={phase_cap}; exact gap={k} bits')


def verify_local_support(n,s):
    # Check the universal *geometric* heart: for two initial words at
    # distance >=s+1, the forced alternative outputs have distance 2.
    count=0
    for x in range(1<<n):
        for y in range(x+1,1<<n):
            ds=(x^y).bit_count()
            if ds<s+1: continue
            differing=[i for i in range(n) if ((x^y)>>i)&1]
            outputs=[(y&~(1<<i)) | (x & (1<<i)) for i in differing]
            assert len(set(outputs))==ds
            assert all((u^v).bit_count()==2 for u,v in itertools.combinations(outputs,2))
            assert all((x^u).bit_count()==ds-1 for u in outputs)
            count+=1
    print(f'n={n}, s={s}, all {count} admissible initial pairs pass the distinct-update-label geometric check')


def verify_plotkin_threshold(max_n):
    for n in range(4,max_n+1):
        s=(n+1)//2+1  # ceil(n/2)+1
        assert s<n or n<=4
        if s<n:
            A=code_plotkin_bound(n,s)
            assert A<=s+1, (n,s,A)
    print(f'Plotkin numerical implication verified for all 4 <= n <= {max_n}')


def verify_extension_moments():
    # Existence bound and admissible even m, arbitrary n over finite range.
    total=0
    for n in range(185,3001):
        choices=[k for k in range(2,13) if n>=16*(2**k)**1.5*math.sqrt(math.log(2*(2**k)))]
        if not choices: continue
        k=max(choices); r=1<<k
        m=2*(n//(2*(r-1)))
        a=n-m*(r-1)
        assert 0<=a<2*(r-1)
        assert m>=4+2*math.sqrt((r-1)*math.log(2*r)), (n,k,m,a)
        total+=1
    print(f'Randomized-extension analytic parameter inequalities verified at {total} consecutive integer lengths')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-k',type=int,default=5)
    args=parser.parse_args()
    for k in range(1,args.max_k+1):
        verify_onewrite_simplex(k)
    for n in range(4,9):
        s=(n+1)//2+1
        if s<n: verify_local_support(n,s)
    verify_plotkin_threshold(300)
    verify_extension_moments()
    print('PASS: global-incidence and one-write simplex certificates')

if __name__=='__main__': main()
