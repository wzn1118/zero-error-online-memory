#!/usr/bin/env python3
"""Exact finite checks for affine-coset deletion, Python stdlib only.
The underlying all-r theorem uses separate algebraic proof; this program checks
full atom pair compatibility, explicit coloring and minimum-class capacity.
"""
import argparse
from collections import Counter,defaultdict
from itertools import combinations

def build(r,d,check_pairs=True):
    assert 2 <= d <= r-2
    U=list(range(1<<d)); a=1<<d
    deleted={a^u for u in U}
    cols=[h for h in range(1,1<<r) if h not in deleted]
    n=len(cols); m=1<<(r-1); J=(1<<d)-1
    assert n==(1<<r)-1-(1<<d)
    assert n-J==(1<<r)-(1<<(d+1))
    # canonical representatives of U-cosets
    cosets={v & ~((1<<d)-1) for v in range(1<<r)}
    mate_pairs=[(q,q^a) for q in sorted(cosets) if q<q^a]
    assert len(mate_pairs)==(1<<(r-d-1))
    # every line represented by its smaller endpoint
    lines={}
    for i,h in enumerate(cols):
        reps=sorted(min(v,v^h) for v in range(1<<r))
        lines[i]=sorted(set(reps))
        assert len(lines[i])==m
    # atom data (colindex,b,minpoint) -> ID
    atoms=[]; aid={}
    for i in range(n):
        for b in (0,1):
            for L in lines[i]:
                aid[i,b,L]=len(atoms); atoms.append((i,b,L))
    assert len(atoms)==2*n*m
    colors={}; next_color=0
    exc=sorted([i for i,h in enumerate(cols) if h in U]); ordinary=[i for i in range(n) if i not in exc]
    assert len(exc)==J
    # ordinary colors: k associates line k at b=0 with line k+1 at b=1
    for i in ordinary:
        ls=lines[i]
        for k in range(m):
            colors[aid[i,0,ls[k]]]=next_color+k
            colors[aid[i,1,ls[(k+1)%m]]]=next_color+k
        next_color+=m
    # exceptional colors: fixed mate pair & index k gives four atoms
    for Q,P in mate_pairs:
        for j,i in enumerate(exc):
            h=cols[i]
            ip=exc[(j+1)%J]
            hs=cols[ip]
            lq=sorted(set(min(v,v^h) for v in range(Q,Q+(1<<d))))
            lp=sorted(set(min(v,v^hs) for v in range(P,P+(1<<d))))
            ell=(1<<(d-1)); assert len(lq)==len(lp)==ell
            for k in range(ell):
                for atom in [(i,0,lq[k]),(i,1,lq[(k+1)%ell]),
                             (ip,0,lp[k]),(ip,1,lp[(k+1)%ell])]:
                    idx=aid[atom]
                    if idx in colors: raise AssertionError(('duplicate color',atom))
                    colors[idx]=next_color
                next_color+=1
    expected=(2*n-J)*m//2
    assert next_color == expected and len(colors)==len(atoms)
    # All color classes are of size 2 or 4, exact cardinality proof in manuscript.
    class_items=defaultdict(list)
    for idx,c in colors.items(): class_items[c].append(idx)
    assert Counter(map(len,class_items.values())) == Counter({2:len(ordinary)*m,4:J*m//2})
    check_column={h for h in cols}
    def is_conflict(A,B):
        i,b,l=A;j,c,p=B
        h=cols[i];h2=cols[j]
        sums=(l^p,l^p^h,l^p^h2,l^p^h^h2)
        if i!=j: return any(v in check_column for v in sums)
        if b==c: return any(v in check_column and v!=h for v in (l^p,l^p^h))
        return l==p
    # Verify every color class clique of compatibility
    for pairids in class_items.values():
        for ii,jj in combinations(pairids,2):
            assert not is_conflict(atoms[ii],atoms[jj]), ('bad class',atoms[ii],atoms[jj])
    # Independently compute maximum compatible class <=4 using quotient geometry:
    # all cross-coordinate compatibilities imply syndrome lines in mate U-cosets,
    # and within one coordinate & one U-coset at most two mutually compatible atoms.
    # exhaustive pair comparisons validates the characterization also.
    num_compatible_cross=0
    num_same_new=0
    pair_count=0
    if check_pairs:
        for ii in range(len(atoms)):
            i,b,l=atoms[ii]
            qi=l & ~((1<<d)-1)
            for jj in range(ii+1,len(atoms)):
                j,c,p=atoms[jj]
                pair_count += 1
                if i!=j:
                    # independently deduced formula: only exceptional directions
                    # with opposite/mate syndrome cosets may be compatible
                    expected_compatible=(i in exc and j in exc and (qi^(p & ~((1<<d)-1)))==a)
                    actual=not is_conflict(atoms[ii],atoms[jj])
                    assert actual==expected_compatible,(r,d,atoms[ii],atoms[jj])
                    num_compatible_cross+=int(actual)
                elif b==c and l!=p:
                    expected_compatible=(i in exc and (qi^(p & ~((1<<d)-1)))==a)
                    assert (not is_conflict(atoms[ii],atoms[jj]))==expected_compatible
                    num_same_new += int(expected_compatible)
                else:
                    assert b!=c
                    assert (not is_conflict(atoms[ii],atoms[jj])) == (l!=p)
        assert pair_count == len(atoms)*(len(atoms)-1)//2
        assert num_compatible_cross == J*(J-1)//2*(1<<(r+d))
        assert num_same_new == J*(1<<(r+d-2))
    return dict(r=r,d=d,n=n,J=J,atoms=len(atoms),expected_colors=expected,
                actual_colors=next_color,ordinary_classes=len(ordinary)*m,
                exceptional_classes=J*m//2, cross_compatible=num_compatible_cross, same_value_new=num_same_new,
                verified_pairs=pair_count, saved_colors=J*m//2, bit_cost=(next_color-1).bit_length())

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--max-d',type=int,default=3);p.add_argument('--quick',action='store_true');args=p.parse_args()
    for d in range(2,args.max_d+1):
        r=d+2
        result=build(r,d,check_pairs=not args.quick)
        print('PASS',result)
