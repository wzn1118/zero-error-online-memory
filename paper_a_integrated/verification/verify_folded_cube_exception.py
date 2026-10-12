#!/usr/bin/env python3
"""Independent finite-geometry enumeration supporting Lemma 7D of Paper A.

No SAT solver and no imported V12 modules. Uses the folded 7-cube with
64 antipodal vertex classes. Certifies every nine-element set S has
sum_{v outside S} (|N(v) intersect S|-1)_+ >= 3 by symmetry and closure.
"""
from itertools import combinations
from collections import defaultdict
from time import perf_counter

N = 64
NEI = [tuple(v ^ b for b in (1, 2, 4, 8, 16, 32, 63)) for v in range(N)]
assert all(len(set(x)) == 7 for x in NEI)

# Add vertices with >=2 already selected neighbors, except explicitly
# nominated exterior vertices E. Monotonicity implies that every target
# S with overlap concentrated inside E must contain the closure.
def closure(a, exceptional, forbidden):
    while True:
        new = a
        for v in range(N):
            if ((a >> v) & 1) or ((exceptional >> v) & 1):
                continue
            t=0
            for x in NEI[v]:
                if (a >> x) & 1:
                    t += 1
                    if t == 2:
                        new |= 1 << v
                        break
        if new & forbidden or new.bit_count() > 9:
            return None
        if new == a:
            return a
        a=new

def direct_xi_half(mask):
    return sum(max(sum((mask>>u)&1 for u in NEI[v])-1, 0) for v in range(N) if not (mask >> v)&1)

def case_search(seeds, exceptions, forbidden, tag):
    E=sum(1<<v for v in exceptions)
    B=sum(1<<v for v in forbidden) | E
    if set(seeds) & set(exceptions) or set(seeds)&set(forbidden):
        return 0,0
    seen=set(); nodes=0; attempts=0
    def dfs(a):
        nonlocal nodes,attempts
        a=closure(a,E,B)
        if a is None or a in seen:return
        seen.add(a);nodes+=1
        if a.bit_count()==9:
            score=direct_xi_half(a)
            if score<=2:
                raise AssertionError(f'COUNTEREXAMPLE {tag}: {a:#018x}, score={score}')
            return
        for v in range(N):
            if not (a>>v)&1 and not (B>>v)&1:
                attempts+=1
                dfs(a | (1<<v))
    mask=sum(1<<v for v in seeds)
    dfs(mask)
    return nodes,attempts

def solve():
    start=perf_counter(); totals=defaultdict(lambda:[0,0,0])
    def check(k,seeds,exceptions=(),forbidden=()):
        a,b=case_search(seeds,exceptions,forbidden,k)
        t=totals[k];t[0]+=1;t[1]+=a;t[2]+=b
    # Xi/2 =0: every nonempty S may be translated to contain zero.
    check('Xi0',(0,))
    # Xi/2 =1: unique exterior vertex with exactly two selected neighbors.
    N0=NEI[0];check('Xi1',(N0[0],N0[1]),(0,),N0[2:])
    # Xi/2 =2, with one exterior vertex contributing two.
    for subset in combinations(N0,3):
        check('Xi2-triplet',subset,(0,),set(N0)-set(subset))
    # Xi/2 =2, with two exterior vertices, each contributing one.
    # Up to cube symmetries their separation is 1,2,3 in F.
    for v in (1,3,7):
        for a in combinations(N0,2):
            for b in combinations(NEI[v],2):
                forb=(set(N0)-set(a)) | (set(NEI[v])-set(b))
                check('Xi2-double',set(a)|set(b),(0,v),forb)
    for name,v in totals.items():print(f'PASS {name}: cases={v[0]}, closed_states={v[1]}, extensions={v[2]}')
    print('PASS: no nine-element folded-cube set with exterior excess <=2')
    print('elapsed_seconds',round(perf_counter()-start,2))

if __name__=='__main__':solve()
