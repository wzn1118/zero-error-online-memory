#!/usr/bin/env python3
"""Independent exact witness enumeration for the general column-set criterion.
Example: r=4, all nonzero columns except a 4-point affine plane.
The removed plane creates genuinely compatible atoms across distinct coordinates.
"""
from itertools import combinations

def syndrome(x, cols):
    s=0
    for j,h in enumerate(cols):
        if x>>j&1: s^=h
    return s

def key(i,b,s,cols):
    return (i,b,min(s,s^cols[i]))

def compatible_locus(keys,cols):
    (i,b,s),(j,c,z)=keys
    L=(s,s^cols[i]); P=(z,z^cols[j]); diffs={x^y for x in L for y in P}
    if i!=j: return bool(diffs.intersection(cols))
    if b==c: return bool(diffs.intersection(h for k,h in enumerate(cols) if k!=i))
    return s==z

def main():
    r=4
    removed={4,5,6,7}
    cols=[h for h in range(1,1<<r) if h not in removed]
    n=len(cols)
    assert n==11
    # Deletion of any two columns leaves n-2=9 nonzero columns,
    # more than the 7 nonzero elements of a proper subspace.
    assert n-2> (1<<(r-1))-1
    lines={i:sorted({min(s,s^h) for s in range(1<<r)}) for i,h in enumerate(cols)}
    keys=[(i,b,s) for i in range(n) for b in (0,1) for s in lines[i]]
    # Direct Hamming-edge witness enumeration, independent of the column criterion.
    incident=[]
    for x in range(1<<n):
        s=syndrome(x,cols)
        incident.append(tuple(key(i,(x>>i)&1,s,cols) for i in range(n)))
    edges=set()
    for x in range(1<<n):
        for k in range(n):
            y=x^(1<<k)
            if x<y:
                for a in incident[x]:
                    for b in incident[y]:
                        if a!=b: edges.add(frozenset((a,b)))
    compatible_cross=0
    total=0
    for a,b in combinations(keys,2):
        actual=frozenset((a,b)) in edges
        expected=compatible_locus((a,b),cols)
        assert actual==expected,(a,b,actual,expected)
        if a[0]!=b[0] and not actual:compatible_cross+=1
        total+=1
    assert compatible_cross>0, 'test should exercise non-Hamming cross-coordinate compatibility'
    print({'r':r, 'n':n, 'atoms':len(keys),'compared_atom_pairs':total,
      'conflict_edges':len(edges), 'compatible_cross_coordinate_pairs':compatible_cross,
      'witness_count':sum(1 for x in range(1<<n) for k in range(n) if x<(x^(1<<k)))})
    print('PASS: full Hamming-edge witness graph agrees with column-set theorem')

if __name__=='__main__':main()
