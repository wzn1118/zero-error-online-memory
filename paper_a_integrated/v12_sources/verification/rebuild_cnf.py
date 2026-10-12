#!/usr/bin/env python3
"""Rebuild 5 independent, logically exact DIMACS encodings for n=7, T=1, q=4.

This recreates *new*, semantically equivalent encodings, not the unavailable
V12 original byte-identical CNFs. CNF + a separately checked UNSAT proof are
necessary for formal certification. Nothing here is claimed UNSAT by itself.
"""
from itertools import combinations
from pathlib import Path
import hashlib, json, sys

N = 128
PAIRS = [(i,j) for i in range(N) for j in range(i+1,N) if (i^j).bit_count() >= 6]
assert len(PAIRS)==512

def write(x,i,b): return x | (1<<i) if b else x & ~(1<<i)
def forced(pair):
    x,y=pair
    return frozenset(tuple(sorted((write(x,i,b),write(y,i,b)))) for i in range(7) for b in (0,1))
FORCED=[forced(p) for p in PAIRS]

def bad_pairs():
    bad=[]; collisions=[]
    for i,p in enumerate(PAIRS):
        for j in range(i+1,len(PAIRS)):
            q=PAIRS[j]
            if len(set(p+q))!=4:continue
            e=sum((x^y).bit_count()==1 for x in p for y in q)
            d=len(FORCED[i]&FORCED[j])
            if e>d: bad.append((p,q))
            if d==2: collisions.append((p,q))
    assert len(bad)==21504
    assert len(collisions)==1792
    return bad

class CNF:
    def __init__(self):
        self.nvars=0;self.clauses=[];self.varlabels={}; self.value={}
    def new(self, label=None, value=None):
        self.nvars+=1
        if label is not None:self.varlabels[label]=self.nvars
        if value is not None:self.value[self.nvars]=bool(value)
        return self.nvars
    def clause(self, *args):
        out=[]
        for l in args:
            if l is True:return
            if l is False:continue
            assert type(l)==int and l!=0
            if -l in out:return
            if l not in out:out.append(l)
        self.clauses.append(out)
    def _eval(self, l):
        if type(l)==bool:return l
        x=self.value.get(abs(l))
        if x is None:return None
        return x if l>0 else not x
    def not_(self,x):
        return not x if type(x)==bool else -x
    def gate_or(self,a,b):
        if type(a)==bool:return True if a else b
        if type(b)==bool:return True if b else a
        z=self.new(value=(self._eval(a) or self._eval(b)) if self._eval(a)is not None and self._eval(b)is not None else None)
        self.clause(-a,z);self.clause(-b,z);self.clause(-z,a,b)
        return z
    def gate_and(self,a,b):
        if type(a)==bool:return b if a else False
        if type(b)==bool:return a if b else False
        z=self.new(value=(self._eval(a) and self._eval(b)) if self._eval(a)is not None and self._eval(b)is not None else None)
        self.clause(-z,a);self.clause(-z,b);self.clause(z,-a,-b)
        return z
    def gate_or_many(self,seq):
        seq=list(seq)
        if not seq:return False
        a=seq[0]
        for b in seq[1:]: a=self.gate_or(a,b)
        return a
    def gate_geq(self, seq, k):
        """Full equivalence to count of True literals >= k (small or large k)."""
        t=[True]+[False]*k
        for x in seq:
            t=[True]+[self.gate_or(t[j],self.gate_and(x,t[j-1])) for j in range(1,k+1)]
        return t[k]
    def enforce_at_most(self, seq, k):
        self.clause(self.not_(self.gate_geq(seq,k+1)))
    def exactly(self, seq, k):
        seq=list(seq)
        self.clause(self.gate_geq(seq,k))
        self.enforce_at_most(seq,k)
    def write(self,path,comment):
        with open(path,'w') as f:
            for line in comment.split('\n'):f.write('c '+line+'\n')
            f.write(f'p cnf {self.nvars} {len(self.clauses)}\n')
            for clause in self.clauses:f.write(' '.join(map(str,clause))+' 0\n')
        return {'variables':self.nvars,'clauses':len(self.clauses),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    def check_assignment(self):
        missing=set(abs(l) for clause in self.clauses for l in clause)-set(self.value)
        if missing:raise AssertionError(f'missing assigned variables {len(missing)}')
        return all(any(self.value[abs(l)]==(l>0) for l in clause) for clause in self.clauses)

CASES={
 'B.antipodal':('B',[(0,127)],True),
 'B.mixed':('B',[(0,63)],False),
 'A.normal':('A',[(0,63),(1,62)],False),
 'A.special':('A',[(0,63),(64,127)],False),
 'A.antipodal':('A',[(0,127),(1,126)],False),
}

def build(case, k=9, chosen=None, fixed_override=None):
    kind,fixed,antipodal=CASES[case]
    if fixed_override is not None:fixed=fixed_override
    candidates=[p for p in PAIRS if not antipodal or (p[0]^p[1]).bit_count()==7]
    x=CNF()
    pvar={pair:x.new(label=f'p.{pair}',value=(pair in chosen) if chosen is not None else None) for pair in candidates}
    # Exactly k source doubleton fibers.
    x.exactly(pvar.values(),k)
    neighbors={z:[pair for pair in candidates if z in pair] for z in range(N)}
    # Each source word occurs in at most one source pair.
    for z in range(N):x.enforce_at_most((pvar[e] for e in neighbors[z]),1)
    u={}
    for z in range(N):
        u[z]=x.gate_or_many(pvar[e] for e in neighbors[z])
    # If z is not selected, it contributes (number of selected cube neighbors - 1)_+ to Xi.
    if kind=='B':
        for z in range(N):
            for a,b in combinations((z^(1<<i) for i in range(7)),2):
                x.clause(u[z],x.not_(u[a]),x.not_(u[b]))
    else:
        threshold=[]
        for z in range(N):
            neigh=[u[z^(1<<i)] for i in range(7)]
            t=[True]+[False]*4
            for a in neigh:t=[True]+[x.gate_or(t[j],x.gate_and(a,t[j-1])) for j in range(1,5)]
            for j in (2,3,4):threshold.append(x.gate_and(x.not_(u[z]),t[j]))
        # Xi<=2 iff the truncated 2/3/4 thresholds total <=2.
        x.enforce_at_most(threshold,2)
        # e-D = 0 from V11 exact pairwise nonnegative losses.
        for a,b in bad_pairs():
            if a in pvar and b in pvar:x.clause(-pvar[a],-pvar[b])
    for pair in fixed:x.clause(pvar[pair])
    return x

if __name__=='__main__':
    dst=Path(sys.argv[1]) if len(sys.argv)>1 else Path('cnf')
    dst.mkdir(exist_ok=True,parents=True)
    specs={}
    for case in CASES:
        x=build(case)
        path=dst/(case+'.cnf')
        specs[case]=x.write(path,f'independently regenerated case={case}\n9 disjoint source pairs with specified symmetry seeds; V11 conditions')
        print(case,specs[case],flush=True)
    (dst/'MANIFEST.json').write_text(json.dumps(specs,indent=2,ensure_ascii=False))
    # Known positive control: eight antipodal source pairs (120-state protocol).
    W=[0,7,25,30,42,45,51,52]
    witness={(v,v^127) for v in W}
    test=build('B.antipodal',k=8,chosen=witness,fixed_override=[(0,127)])
    assert test.check_assignment(), 'positive SAT witness rejected by encoding'
    # Wrong k=9 for same selected witness must violate constraints.
    wrong=build('B.antipodal',k=9,chosen=witness,fixed_override=[(0,127)])
    assert not wrong.check_assignment(), 'exact cardinality constraint omitted'
    print('PASS positive witness and cardinality negative control')
