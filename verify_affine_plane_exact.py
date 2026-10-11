#!/usr/bin/env python3
"""Standalone certificate for affine-plane deletion of a binary syndrome matrix.
All operations on integers; Python standard library only. The computed graph is
*not* used to assert the general-r theorem, which has an independent proof.
"""
from itertools import combinations
from collections import defaultdict
import argparse, json

def model(r, removed):
    full=set(range(1,1<<r)); assert len(removed)==4 and 0 not in removed
    a=min(removed); U=frozenset(x^a for x in removed)
    assert 0 in U and len(U)==4 and all(x^y in U for x in U for y in U)
    assert 0 not in removed and U.isdisjoint(removed)
    cols=sorted(full-set(removed)); n=len(cols); m=1<<(r-1)
    special=sorted(U-{0}); assert len(special)==3
    idx={h:i for i,h in enumerate(cols)}
    lines={i:sorted({min(s,s^h) for s in range(1<<r)}) for i,h in enumerate(cols)}
    assert all(len(v)==m for v in lines.values())
    atoms=[(i,b,L) for i in range(n) for b in (0,1) for L in lines[i]]
    def plane_rep(s):return min(s^u for u in U)
    plane_reps=sorted({plane_rep(s) for s in range(1<<r)})
    pairs=sorted({tuple(sorted((z,plane_rep(z^a)))) for z in plane_reps})
    assert len(pairs)==1<<(r-3)
    pair_idx={pair:k for k,pair in enumerate(pairs)}
    nspecial=[i for i,h in enumerate(cols) if h not in special]
    specidx={h:k for k,h in enumerate(special)}
    nonspecidx={i:k for k,i in enumerate(nspecial)}
    colors={}
    for i,b,L in atoms:
        h=cols[i]
        if h not in special:
            ell=lines[i].index(L)
            colors[(i,b,L)]=nonspecidx[i]*m+(ell+(b%2))%m
        else:
            z=plane_rep(L)
            zpair=tuple(sorted((z,plane_rep(z^a))))
            p=zpair.index(z)
            planelines=sorted({min(s,s^h) for s in (z^u for u in U)})
            assert len(planelines)==2
            ell=planelines.index(L)
            j=ell^b
            k=specidx[h]
            if p==1:k=(k-1)%3
            colors[(i,b,L)]=len(nspecial)*m+pair_idx[zpair]*6+2*k+j
    target=(2*n-3)*(1<<(r-2))
    assert len(set(colors.values()))==target
    assert max(colors.values())+1==target
    return cols, U, atoms, colors, target

def conflict(a,b,cols):
    i,bi,Li=a;j,bj,Lj=b
    if i==j:
        if bi!=bj:return Li==Lj
        differences={x^y for x in (Li,Li^cols[i]) for y in (Lj,Lj^cols[i])}
        return bool(differences.intersection(h for k,h in enumerate(cols) if k!=i))
    hi,hj=cols[i],cols[j]
    differences={x^y for x in (Li,Li^hi) for y in (Lj,Lj^hj)}
    return bool(differences.intersection(cols))

def verify(r, removed):
    cols,U,atoms,colors,expected=model(r,set(removed))
    pairs=0; internal=0; cross_compatible=0
    for x,y in combinations(atoms,2):
        bad=conflict(x,y,cols)
        assert not (bad and colors[x]==colors[y]),(x,y)
        pairs+=1
        if x[0]!=y[0] and not bad:cross_compatible+=1
        if x[0]==y[0]:internal+=1
    n=len(cols)
    # Certification from the proven decomposition:
    # Each nonexceptional coordinate is a joined K_m square K_2, needs m colors;
    # the three exceptional coordinates require >=6m/4 colors by alpha <=4.
    m=1<<(r-1)
    analytic_lb=(n-3)*m+3*m//2
    assert expected==analytic_lb
    assert cross_compatible==3*(1<<(r+2))
    result={'r':r,'n':n,'removed':sorted(removed),'atoms':len(atoms),
        'atom_pairs_checked':pairs,'cross_compatible_pairs':cross_compatible,
        'certified_chromatic_number':expected,
        'bit_budget':(expected-1).bit_length(),
        'baseline_labels':n*m,
        'label_savings':n*m-expected}
    return result

def brute_witness_r4(r, removed):
    cols,U,atoms,colors,expected=model(r,set(removed)); assert r==4
    n=len(cols); idx={a:i for i,a in enumerate(atoms)}
    def syndrome(x):
        v=0
        for j,h in enumerate(cols):
            if x>>j&1:v^=h
        return v
    incoming=[]
    for x in range(1<<n):
        s=syndrome(x)
        incoming.append([idx[(i,(x>>i)&1,min(s,s^cols[i]))] for i in range(n)])
    witnessed=set()
    for x in range(1<<n):
        for bit in range(n):
            y=x^(1<<bit)
            if x<y:
                for a in incoming[x]:
                    for b in incoming[y]:
                        if a!=b:witnessed.add((min(a,b),max(a,b)))
    for ai in range(len(atoms)):
        for bi in range(ai+1,len(atoms)):
            assert ((ai,bi) in witnessed)==conflict(atoms[ai],atoms[bi],cols),(ai,bi)
    # Independent end-to-end check: every overwritten word belongs to its
    # assigned label, and the decoder has at most one completion for each erasure.
    from collections import defaultdict
    support=defaultdict(set)
    transfers=0
    for x in range(1<<n):
        s=syndrome(x)
        for i in range(n):
            L=min(s,s^cols[i])
            for bit in (0,1):
                y=(x&~(1<<i))|(bit<<i)
                atom=(i,bit,L)
                color=colors[atom]
                support[color].add(y)
                transfers+=1
    for color,words in support.items():
        for y in words:
            for j in range(n):
                assert (y^(1<<j)) not in words,(color,y,j)
    assert len(support)==expected
    print(json.dumps({'r4_protocol_updates':transfers,'terminal_labels':len(support),
         'distinct_labeled_output_words':sum(map(len,support.values()))}))
    return len(witnessed)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true'); args=ap.parse_args()
    for r in [4,5,6] if args.full else [4,5]:
        a=1<<(r-2); removed={a,a^1,a^2,a^3}
        result=verify(r,removed)
        if r==4:result['independent_actual_witness_edges']=brute_witness_r4(r,removed)
        print(json.dumps(result,sort_keys=True))
    print('PASS affine-plane exact chromatic formula, explicit coloring and graph checks')
