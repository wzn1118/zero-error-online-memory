#!/usr/bin/env python3
"""Independent unit-propagation check for compact integer cardinality circuits."""
import sys,itertools
sys.path.insert(0,__file__.rsplit('/',1)[0])
from rebuild_compact import C

def propagate(n,clauses,assumptions):
    val={}
    for lit in assumptions:
        v=abs(lit); value=(lit>0)
        if v in val and val[v]!=value:return False,val
        val[v]=value
    for _ in range(n+2):
        changed=False
        for clause in clauses:
            if any((val.get(abs(x)) is not None and val[abs(x)]==(x>0)) for x in clause):continue
            unknown=[x for x in clause if abs(x) not in val]
            if not unknown:return False,val
            if len(unknown)==1:
                l=unknown[0];v=abs(l); b=l>0
                if v in val and val[v]!=b:return False,val
                if v not in val:val[v]=b;changed=True
        if not changed:return True,val
    raise AssertionError('failed to reach fixed point')

trials=0
for n in range(1,8):
    for k in range(n+2):
        c=C();inp=[c.var() for i in range(n)]
        out=c.geq(inp,k)
        for bits in itertools.product((False,True),repeat=n):
            given=[i+1 if b else -(i+1) for i,b in enumerate(bits)]
            sat,assignment=propagate(c.n,c.cs,given)
            assert sat,(n,k,bits,'circuit contradicts inputs')
            expected=sum(bits)>=k
            if isinstance(out,bool):assert out==expected
            else:
                assert out in assignment and assignment[out]==expected,(n,k,bits,expected,assignment.get(out))
                wrong=given+([-out] if expected else [out])
                sat2,_=propagate(c.n,c.cs,wrong)
                assert not sat2,(n,k,bits,'opposite threshold accepted')
            trials+=1
print('PASS EXACT CARDINALITY: UP/equivalence truth-table cases:',trials)
