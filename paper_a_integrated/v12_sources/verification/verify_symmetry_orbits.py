"""Solver-independent exhaustive verification of all strong-collision orbit representatives."""
from itertools import permutations
from collections import Counter
N=128;n=7
P=[(x,y) for x in range(N) for y in range(x+1,N) if (x^y).bit_count()>=6]
idx={p:i for i,p in enumerate(P)}
def write(x,i,b):return (x | (1<<i)) if b else (x & ~(1<<i))
F=[{tuple(sorted((write(x,i,b),write(y,i,b)))) for i in range(n) for b in range(2)} for x,y in P]
strong=set()
for i in range(len(P)):
 for j in range(i+1,len(P)):
  if len(set(P[i]+P[j]))!=4:continue
  if len(F[i]&F[j])==2:strong.add((i,j))
assert len(strong)==1792
cases={'distance6-normal':((0,63),(1,62)),
       'distance6-special':((0,63),(64,127)),
       'antipodal':((0,127),(1,126))}
found={}
for case,seeds in cases.items():
 orbit=set()
 for perm in permutations(range(n)):
  trans=[]
  for p in seeds:
   rr=[]
   for v in p:
    rr.append(sum(1<<perm[i] for i in range(n) if (v>>i)&1))
   trans.append(rr)
  for offset in range(N):
   i=idx[tuple(sorted(x^offset for x in trans[0]))]
   j=idx[tuple(sorted(x^offset for x in trans[1]))]
   orbit.add((min(i,j),max(i,j)))
 assert orbit<=strong,(case,len(orbit-strong))
 print('PASS',case,'isometry-orbit-size',len(orbit))
 found[case]=orbit
assert all(not (found[a]&found[b]) for a in found for b in found if a<b)
assert set().union(*found.values())==strong
assert tuple(len(found[k]) for k in cases)==(1344,224,224)
print('PASS strong collision pair orbit COVERAGE: 1792 of 1792, no omissions')
