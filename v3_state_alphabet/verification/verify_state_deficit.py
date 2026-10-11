"""Enumerate one-write updates and erasure observations for the new theorems."""
from itertools import combinations

def write(x,i,b): return (x | (1<<i)) if b else (x & ~(1<<i))
def d(x,y): return (x^y).bit_count()
def columns(n):
    special={0:(),1:(1,2,4,8,15),2:(1,2,3,4,8,12),3:(1,2,3)}[n%4]
    Q=1<<(n+23).bit_length()
    result=list(special)
    for b in range(4,Q,4):
        block=range(b,b+4)
        if len(result)+4<=n and all(x not in special for x in block):
            result.extend(block)
    assert len(result)==n and len(set(result))==n and min(result)>0
    sx=0
    for x in result: sx^=x
    assert sx==0
    return result,Q
def build(n,pairs):
    N=1<<n
    paired={x for edge in pairs for x in edge}
    assert len(paired)==2*len(pairs)
    f0=list(pairs)+[(x,) for x in range(N) if x not in paired]
    encoded={x:i for i,f in enumerate(f0) for x in f}
    edges=sorted({tuple(sorted((write(x,i,b),write(y,i,b))))
                 for x,y in pairs for i in range(n) for b in (0,1)})
    occupied={v for e in edges for v in e}
    f1=list(edges)+[(x,) for x in range(N) if x not in occupied]
    lookup={x:[] for x in range(N)}
    for label,f in enumerate(f1):
        for x in f:lookup[x].append(label)
    tr={}
    for a,f in enumerate(f0):
        for i in range(n):
            for b in (0,1):
                target={write(x,i,b) for x in f}
                cand=[j for j in lookup[min(target)] if target<=set(f1[j])]
                assert cand
                tr[a,i,b]=cand[0]
    assert all(len(f)==1 or d(*f)==n-1 for f in f1)
    return f0,f1,encoded,tr,edges,occupied

def audit(n,pairs,q):
    N=1<<n
    f0,f1,enc,tr,edges,occupied=build(n,pairs)
    patterns=[m for m in range(N) if m.bit_count()<=q]
    checked=0
    for phase in (0,1):
        seen={}
        for x in range(N):
            cases=[(x,enc[x])] if phase==0 else [
                (write(x,i,b),tr[enc[x],i,b])
                for i in range(n) for b in (0,1)]
            for y,label in cases:
                for erased in patterns:
                    key=(label,erased,y&~erased)
                    assert seen.setdefault(key,y&erased)==(y&erased)
                    checked+=1
    return len(f0),len(f1),len(edges),len(occupied),checked

for n in range(4,8):
    N=1<<n
    f0,f1,e,v,queries=audit(n,[(0,N-1),(1,N-2)],n-2)
    assert f0==f1==N-2
    assert e==4*n-2 and v==4*n
    cols,Q=columns(n)
    C=[x for x in range(N) if __import__('functools').reduce(
        lambda s,i:s^cols[i] if x>>i&1 else s,range(n),0)==0]
    assert all(d(x,y)>=3 for x,y in combinations(C,2))
    pairs=sorted((x,(N-1)^x) for x in C if x<((N-1)^x))
    K0,K1,E,V,checks=audit(n,pairs,n-2)
    a=len(pairs)
    assert K0==N-a and K1==N-2*a
    assert E==2*n*a and V==2*(n+1)*a
    lower=(n*N+n)//(n+1)
    print('PASS',n,'two-pair',f0,'packed',K0,'lower',lower,
          'packed-pairs',a,'queries',queries+checks)
print('ALL V3 STATE-DEFICIT CERTIFICATES PASS')
