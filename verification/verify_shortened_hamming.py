#!/usr/bin/env python3
"""Independent exhaustive six-bit verification of the shortened-Hamming atom law.
Only the Python standard library is needed.
"""
from itertools import combinations, product

def synd(x, columns):
    out = 0
    for j, h in enumerate(columns):
        if (x >> j) & 1: out ^= h
    return out

def atoms(columns, r):
    n = len(columns)
    rec = {}
    for i, hi in enumerate(columns):
        # unique unordered affine line as pair of syndrome values
        lines = sorted({tuple(sorted((s,s^hi))) for s in range(1<<r)})
        for b in (0,1):
            for line in lines:
                rec[(i,b,line)] = frozenset(x for x in range(1<<n)
                     if ((x>>i)&1)==b and synd(x,columns) in line)
    return rec

def predicted_conflict(a, b, columns):
    (i, v, L), (j, w, P) = a, b
    if i == j:
        if v != w: return L==P
        return any(h in {x^y for x in L for y in P} for k,h in enumerate(columns) if k!=i)
    S=set(columns)|{0}
    return bool({x^y for x in L for y in P} & S)

def canonical_full_conflict(a,b):
    (i,v,L),(j,w,P)=a,b
    return i!=j or (v==w) or (L==P)

def exhaustive(columns, r):
    n=len(columns)
    A=atoms(columns,r)
    edges=0; comparisons=0
    for a,b in combinations(A,2):
        brute = any(((x^y).bit_count()==1) for x in A[a] for y in A[b])
        formula=predicted_conflict(a,b,columns)
        simplified=canonical_full_conflict(a,b)
        assert brute==formula==simplified, ('mismatch',a,b,brute,formula,simplified)
        edges+=brute; comparisons+=1
    m=1<<(r-1)
    assert len(A)==2*n*m
    expected_edges=n*m*m+(n*(n-1)//2)*(2*m)**2
    assert edges==expected_edges, (edges,expected_edges)
    # verify explicit color assignment via cyclic derangement
    lmap={}
    for i in range(n):
        lines=sorted({tuple(sorted((s,s^columns[i]))) for s in range(1<<r)})
        for k,L in enumerate(lines):
            lmap[(i,0,L)]=i*m+k
            lmap[(i,1,L)]=i*m+(k+1)%m
    for a,b in combinations(A,2):
        if lmap[a]==lmap[b]:
            assert not predicted_conflict(a,b,columns)
    # Full encoder -> update -> decoder exhaustive check: the 0/1 completions
    # of each single erased coordinate must be unique for every current word.
    states={}
    for key,atom in A.items():
        states.setdefault(lmap[key], set()).update(atom)
    checks=0
    for x in range(1<<n):
        sx=synd(x, columns)
        for i,h in enumerate(columns):
            line=tuple(sorted((sx,sx^h)))
            for b in (0,1):
                k=lmap[(i,b,line)]
                y=(x & ~(1<<i)) | (b<<i)
                assert y in states[k]
                for er in range(n):
                    other=y ^ (1<<er)
                    assert other not in states[k]
                    checks+=1
    return {'n':n,'r':r,'atoms':len(A),'pairs_checked':comparisons,'edges':edges,'colors':len(set(lmap.values())),'queries':checks}

if __name__=='__main__':
    r=3
    for missing in range(1,1<<r):
        columns=[h for h in range(1,1<<r) if h!=missing]
        ans=exhaustive(columns,r)
        print('removed', missing, ans)
    print('PASS: all 7 shortened Hamming check matrices; no solver, no external data')
