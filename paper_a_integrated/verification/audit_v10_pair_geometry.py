"""Independent forced-pair incidence experiment (no V10 imports)."""
from itertools import combinations
from collections import defaultdict
def audit(n):
    N=1<<n
    pairs=[(x,y) for x in range(N) for y in range(x+1,N) if (x^y).bit_count()>=n-1]
    images=[]; pre=defaultdict(list)
    for pid,(a,b) in enumerate(pairs):
        f=set()
        for i in range(n):
            bit=1<<i
            for new in (0,1):
                u=(a&~bit)|(bit if new else 0)
                v=(b&~bit)|(bit if new else 0)
                assert u!=v
                f.add(tuple(sorted((u,v))))
        assert len(f)==2*n
        images.append(f)
        for edge in f: pre[edge].append(pid)
    checked=collisions=0
    for i,j in combinations(range(len(pairs)),2):
        p,q=pairs[i],pairs[j]
        if len({*p,*q})!=4:continue
        e=sum((x^y).bit_count()==1 for x in p for y in q)
        d=len(images[i]&images[j])
        assert d<=e,(n,p,q,d,e)
        checked+=1
        if d:collisions+=1
    for edge,ids in pre.items():
        if len(ids)<3:continue
        for i,j,k in combinations(ids,3):
            assert len(set(pairs[i]+pairs[j]+pairs[k]))<6,(n,edge,i,j,k)
    print(f'PASS V10 n={n} pairs={len(pairs)} disjoint-pair-checks={checked} colliding-pairs={collisions}')
for n in (7,8):audit(n)
