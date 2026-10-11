#!/usr/bin/env python3
"""Exact minimization over all complement-invariant source sets for n=4,5."""
from itertools import combinations

def score(n,mask):
    N=1<<n
    pairs=[(x,N-1-x) for x in range(N) if x<N-1-x]
    C=set()
    a=0
    for i,(x,y) in enumerate(pairs):
        if mask>>i&1:C.update((x,y));a+=1
    xi=sum(max(sum((y^(1<<i)) in C for i in range(n))-1,0)
           for y in range(N) if y not in C)
    assert xi%2==0
    return max(N-a,N//2+(n-1)*a+xi//2),a,xi

for n,expected in [(4,14),(5,29)]:
    p=1<<(n-1);best=1<<n;optimal=0
    for c in range(1<<p):
        K,a,xi=score(n,c)
        if K<best:best,optimal=K,1
        elif K==best:optimal+=1
    assert best==expected,(n,best)
    print('PASS',n,'exact optimum',best,'optimal configurations',optimal)

for r in range(2,13):
    n=1<<r;N=1<<n;m=r+1;p=n-m
    a=1<<p
    assert a==N//(2*n)
    assert N-a==N//2+(n-1)*a
    print('PASS dyadic algebra n=',n,'saving=',a)
print('All finite variational certificates passed.')
