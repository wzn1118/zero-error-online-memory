#!/usr/bin/env python3
"""Independent compact encoding of V11 five Boolean necessary-condition cases.
All gates are bidirectionally equivalent. Fixed source pairs and exact-nine cardinality are retained.
"""
import sys, hashlib, json
from pathlib import Path
from rebuild_cnf import PAIRS, CASES, N, bad_pairs

class C:
 def __init__(self):self.n=0;self.cs=[]
 def var(self):self.n+=1;return self.n
 def neg(self,l):return not l if type(l)==bool else -l
 def add(self,*ls):
  arr=[]
  for l in ls:
   if l is True:return
   if l is False:continue
   assert type(l)==int and l!=0
   if -l in arr:return
   if l not in arr:arr.append(l)
  self.cs.append(arr)
 def and2(self,a,b):
  if a is True:return b
  if b is True:return a
  if a is False or b is False:return False
  if a==b:return a
  if a==-b:return False
  z=self.var();self.add(-z,a);self.add(-z,b);self.add(z,-a,-b);return z
 def or2(self,a,b):
  if a is False:return b
  if b is False:return a
  if a is True or b is True:return True
  if a==b:return a
  if a==-b:return True
  z=self.var();self.add(-a,z);self.add(-b,z);self.add(-z,a,b);return z
 def ormany(self,seq):
  s=list(seq)
  if not s:return False
  if len(s)==1:return s[0]
  z=self.var()
  for p in s:self.add(-p,z)
  self.add(-z,*s)
  return z
 def geq(self,seq,k):
  # Full equivalence via 4-clause DP gate per threshold cell.
  if k==0:return True
  row=[True]+[False]*k
  for x in seq:
   new=[True]
   for j in range(1,k+1):
    a=row[j];b=row[j-1]
    if a is True:z=True
    elif a is False:z=self.and2(x,b)
    elif x is False or b is False:z=a
    elif b is True:z=self.or2(a,x)
    elif x is True:z=self.or2(a,b)
    else:
     z=self.var()
     self.add(-a,z);self.add(-x,-b,z);self.add(-z,a,x);self.add(-z,a,b)
    new.append(z)
   row=new
  return row[k]
 def exactly(self,seq,k):
  s=list(seq);self.add(self.geq(s,k));self.add(self.neg(self.geq(s,k+1)))
 def atmost(self,seq,k):self.add(self.neg(self.geq(seq,k+1)))
 def write(self,path,label):
  with open(path,'w') as f:
   f.write('c '+label+'\n')
   f.write(f'p cnf {self.n} {len(self.cs)}\n')
   for c in self.cs:f.write(' '.join(map(str,c))+' 0\n')
  return {'variables':self.n,'clauses':len(self.cs),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def build(case):
 kind,fixed,antipodal=CASES[case]
 candidates=[p for p in PAIRS if not antipodal or (p[0]^p[1]).bit_count()==7]
 c=C(); pv={p:c.var() for p in candidates}
 c.exactly(pv.values(),9)
 for z in range(N):
  near=[pv[p] for p in candidates if z in p]
  for i in range(len(near)):
   for j in range(i+1,len(near)):c.add(-near[i],-near[j])
 u={z:c.ormany(pv[p] for p in candidates if z in p) for z in range(N)}
 if kind=='B':
  from itertools import combinations
  for z in range(N):
   for a,b in combinations((z^(1<<i) for i in range(7)),2):c.add(u[z],-u[a],-u[b])
 else:
  thresholds=[]
  for z in range(N):
   ne=[u[z^(1<<i)] for i in range(7)]
   for j in (2,3,4):thresholds.append(c.and2(c.neg(u[z]),c.geq(ne,j)))
  c.atmost(thresholds,2)
  for p,q in bad_pairs():
   if p in pv and q in pv:c.add(-pv[p],-pv[q])
 for p in fixed:c.add(pv[p])
 return c
if __name__=='__main__':
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
 results={}
 for case in CASES:
  c=build(case);results[case]=c.write(out/(case+'.cnf'),'compact exact encoding '+case);print(case,results[case],flush=True)
 (out/'manifest.json').write_text(json.dumps(results,indent=2))
