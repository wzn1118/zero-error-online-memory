#!/usr/bin/env python3
"""Independent, standard-library exact certificate of 120-state upper bound at n=7,T=1,q=4."""
from itertools import combinations
n=7;N=128;q=4;full=N-1
W=[0,7,25,30,42,45,51,52]
P=[(x,x^full) for x in W]
assert len({v for edge in P for v in edge})==16
assert all((x^y).bit_count()>=3 for x,y in combinations({v for edge in P for v in edge},2))
def write(x,i,b):return ((x | (1<<i)) if b else (x & ~(1<<i)))
def forced(P):return tuple(sorted({tuple(sorted((write(x,i,b),write(y,i,b)))) for x,y in P for i in range(n) for b in (0,1)}))
T=forced(P)
assert len(T)==112, len(T)
assert all((x^y).bit_count()==6 for x,y in T)
assert set(v for e in T for v in e)==set(range(N))
initial=P+[(x,) for x in range(N) if x not in {v for edge in P for v in edge}]
assert len(initial)==120
enc={x:k for k,S in enumerate(initial) for x in S}
terminal={e:i for i,e in enumerate(T)}
byword={v:i for i,e in enumerate(T) for v in e}
assert len(byword)==N
transition={}
for i,S in enumerate(initial):
 for j in range(n):
  for b in (0,1):
   dest=tuple(sorted({write(x,j,b) for x in S}))
   if len(dest)==2:
    assert dest in terminal
    transition[i,j,b]=terminal[dest]
   else:
    transition[i,j,b]=byword[dest[0]]
erasures=[sum(1<<j for j in E) for k in range(q+1) for E in combinations(range(n),k)]
assert len(erasures)==99
for phase in (0,1):
 table={};n_hist=0
 for x in range(N):
  cases=[(x,enc[x])] if phase==0 else [(write(x,i,b),transition[enc[x],i,b]) for i in range(n) for b in (0,1)]
  n_hist+=len(cases)
  for w,lab in cases:
   for E in erasures:
    obs=(lab,E,w&(full^E));ans=w&E
    assert table.setdefault(obs,ans)==ans,(phase,x,obs)
 print('PASS phase',phase,'histories',n_hist,'distinct erasure observations',len(table))
print('PASS exact 120-state protocol (8 initial antipodal pairs; 112 forced terminal edges)')
