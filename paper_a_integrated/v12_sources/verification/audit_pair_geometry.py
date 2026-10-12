#!/usr/bin/env python3
"""No-solver verification of all pairs, forced successor sets, collision and orbit counts."""
from collections import defaultdict,Counter
from itertools import combinations
n=7;N=1<<n
P=[(x,y) for x in range(N) for y in range(x+1,N) if (x^y).bit_count()>=6]
assert len(P)==512

def update(x,i,b): return (x|(1<<i)) if b else (x&~(1<<i))
F=[];pre=defaultdict(list)
for k,(x,y) in enumerate(P):
    images={tuple(sorted((update(x,i,b),update(y,i,b)))) for i in range(n) for b in (0,1)}
    assert len(images)==14
    F.append(images)
    for image in images:pre[image].append(k)
for imag,ids in pre.items():
    for i,j,k in combinations(ids,3):
        assert len(set(P[i]+P[j]+P[k]))<6
count=Counter(); bad=0
for i in range(len(P)):
 for j in range(i+1,len(P)):
    if len(set(P[i]+P[j]))!=4:continue
    e=sum((x^y).bit_count()==1 for x in P[i] for y in P[j])
    d=len(F[i]&F[j])
    assert 0<=d<=e<=2 and e-d in (0,1)
    if e>d:bad+=1
    if d==2:
      diff=(P[i][0]^P[i][1]).bit_count()
      assert diff==(P[j][0]^P[j][1]).bit_count()
      if diff==7:count['antipodal']+=1
      else:
        missing=next(k for k in range(n) if not ((P[i][0]^P[i][1])>>k)&1)
        delta=next(k for k in range(n) if P[j]==tuple(sorted((P[i][0]^(1<<k),P[i][1]^(1<<k)))))
        count['special' if missing==delta else 'normal']+=1
assert bad==21504 and count=={'normal':1344,'special':224,'antipodal':224}
print('PASS: 512 legal source pairs; 21,504 bad adjacencies; 1,792 strong collisions; no three disjoint preimages')
