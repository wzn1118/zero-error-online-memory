#!/usr/bin/env python3
"""Independent finite-geometry enumeration for the exceptional seven-cube."""
from itertools import combinations
from collections import defaultdict
from time import perf_counter

N=64
NEI=[tuple(v^b for b in (1,2,4,8,16,32,63)) for v in range(N)]
assert all(len(set(x))==7 for x in NEI)

def closure(a,exceptional,forbidden):
    while True:
        new=a
        for v in range(N):
            if (a>>v)&1 or (exceptional>>v)&1: continue
            t=0
            for u in NEI[v]:
                if (a>>u)&1:
                    t+=1
                    if t==2:
                        new|=1<<v
                        break
        if new&forbidden or new.bit_count()>9:return None
        if new==a:return a
        a=new

def xi_half(a):
    return sum(max(sum((a>>u)&1 for u in NEI[v])-1,0)
               for v in range(N) if not (a>>v)&1)

def search(seeds, exceptions=(), forbidden=()):
    E=sum(1<<v for v in exceptions)
    B=E|sum(1<<v for v in forbidden)
    if set(seeds)&(set(exceptions)|set(forbidden)):return 0,0
    seen=set()
    extensions=0
    def walk(a):
        nonlocal extensions
        a=closure(a,E,B)
        if a is None or a in seen:return
        seen.add(a)
        if a.bit_count()==9:
            if xi_half(a)<=2:
                raise AssertionError('Nine-point low-overlap counterexample')
            return
        for v in range(N):
            if not ((a|B)>>v)&1:
                extensions+=1
                walk(a|(1<<v))
    walk(sum(1<<v for v in seeds))
    return len(seen),extensions

def main():
    out=defaultdict(lambda:[0,0,0])
    def audit(kind,seed,E=(),forbidden=()):
        a,b=search(seed,E,forbidden)
        out[kind][0]+=1;out[kind][1]+=a;out[kind][2]+=b
    start=perf_counter()
    audit('Xi0',(0,))
    n0=NEI[0]
    audit('Xi1',n0[:2],(0,),n0[2:])
    for c in combinations(n0,3):
        audit('Xi2-triplet',c,(0,),set(n0)-set(c))
    for v in (1,3,7):
        for a in combinations(n0,2):
            for b in combinations(NEI[v],2):
                forbidden=(set(n0)-set(a))|(set(NEI[v])-set(b))
                audit('Xi2-double',set(a)|set(b),(0,v),forbidden)
    assert out['Xi0'][:2]==[1,7549]
    assert out['Xi1'][:2]==[1,26]
    assert sum(out[k][0] for k in ('Xi2-triplet','Xi2-double'))==1358
    assert sum(out[k][1] for k in ('Xi2-triplet','Xi2-double'))==1721
    for name,row in out.items():
        print('PASS',name,'cases',row[0],'states',row[1],'extensions',row[2])
    print('PASS independent folded-cube exception; elapsed_seconds',round(perf_counter()-start,2))

if __name__=='__main__':main()
