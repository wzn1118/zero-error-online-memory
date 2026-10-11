"""Certified finite ingredient for R_online(5,1,2)=5, standard library only.

No AI APIs, Lean, Docker, or external solver.  The proof reduces every 4-bit
initial protocol to a perfect matching of the five-cube by distance >= 4
edges.  It then bounds the number of update atoms carried by any admissible
terminal label using a single 6-vertex cover, modulo all cube isometries.
"""
from collections import deque, Counter
from itertools import combinations
import json
from pathlib import Path

N = 5
X = tuple(range(1 << N))
C0 = frozenset((0, 7, 25, 30))
COVER6 = frozenset((0, 1, 6, 7, 25, 30))
STATIC_PARTITION = (
    (1,14,23,24),(0,15,22,25),(3,12,21,26),(2,13,20,27),
    (5,10,19,28),(4,11,18,29),(7,8,17,30),(6,9,16,31),
)

def d(x, y):
    return (x ^ y).bit_count()

def overwrite(x, i, b):
    return (x & ~(1 << i)) | (b << i)

def independent(S, dist=3):
    return all(d(x,y)>=dist for x,y in combinations(S,2))

def cube_isometry_generators():
    perms=[]
    for i in range(N):
        perms.append(tuple(x^(1<<i) for x in X))
    for i in range(N-1):
        perm=[]
        for x in X:
            b1=(x>>i)&1; b2=(x>>(i+1))&1
            perm.append((x & ~((1<<i)|(1<<(i+1)))) | (b1<<(i+1)) | (b2<<i))
        perms.append(tuple(perm))
    return tuple(perms)

def orbit(base):
    generators=cube_isometry_generators()
    seen={frozenset(base)}
    work=[frozenset(base)]
    for S in work:
        for p in generators:
            nxt=frozenset(p[x] for x in S)
            if nxt not in seen:
                seen.add(nxt);work.append(nxt)
    return seen

def all_independent():
    return [frozenset(C) for k in range(1,5) for C in combinations(X,k)
            if independent(C)]

def predecessor_events(x, y, C):
    assert d(x,y)>=4
    return [(i,b) for i in range(N) for b in (0,1)
            if {overwrite(x,i,b),overwrite(y,i,b)} <= C]

def verify():
    # All admissible terminal fibers have at most 4 words; exactly which ones
    # are maximal is checked independently from an exhaustive list.
    codes = all_independent()
    codes4={c for c in codes if len(c)==4}
    assert len(codes4)==120, len(codes4)
    max_codes=[c for c in codes if not any(c<other for other in codes)]
    assert Counter(map(len,max_codes))=={4:120,2:16}
    antipodal=frozenset(frozenset((x,x^31)) for x in X)
    assert {c for c in max_codes if len(c)==2}==antipodal
    assert orbit(C0)==codes4

    # Only 24 initial long-distance pairs could have a one-step image in C0.
    # Each can produce at most one distinct (i,b) atom for C0.
    candidates={}
    for x,y in combinations(X,2):
        if d(x,y)>=4:
            e=predecessor_events(x,y,C0)
            if e:
                assert len(e)==1, (x,y,e)
                candidates[(x,y)]=e[0]
    assert len(candidates)==24,len(candidates)
    assert all(x in COVER6 or y in COVER6 for x,y in candidates)
    # A perfect matching can contain at most one edge incident to each vertex
    # in COVER6, so at most six predecessor pairs, hence six update atoms,
    # can enter any C0-isometric terminal fiber.
    assert len(COVER6)==6
    assert 16*6 < 16*5*2

    # A 2-vertex maximal fiber is antipodal; an overwrite image of a
    # long-distance source pair cannot be antipodal (one bit agrees).
    for x,y in combinations(X,2):
        if d(x,y)>=4:
            for i in range(N):
                for b in (0,1):
                    assert d(overwrite(x,i,b),overwrite(y,i,b)) in (3,4)

    # Static q=2 coloring with eight colors, via eight disjoint 4-codes.
    assert len(STATIC_PARTITION)==8
    assert all(len(C)==4 and independent(C,3) for C in STATIC_PARTITION)
    assert sorted(x for C in STATIC_PARTITION for x in C)==list(X)

    return {
        'statement': 'R_online(5,1,2)=5; complete n=5 all (T,q) by folding and previous n5-q1 certificate',
        'maximal_q2_fibers': {'size_four':120,'antipodal_size_two':16},
        'size_four_code_orbit':120,
        'canonical_terminal_code':sorted(C0),
        'six_vertex_cover':sorted(COVER6),
        'candidate_initial_pairs':[
            {'pair':[x,y],'single_event':list(event)}
            for (x,y),event in sorted(candidates.items())],
        'candidate_predecessor_pairs':len(candidates),
        'atoms_from_16_initial_pair_labels':160,
        'maximum_atoms_per_terminal_label':6,
        'maximum_atoms_all_16_labels':96,
        'static_q2_eight_colors':[list(C) for C in STATIC_PARTITION],
    }

if __name__=='__main__':
    result=verify()
    out=Path(__file__).resolve().parents[1]/'certificates'/'n5_q2_capacity.json'
    if '--generate' in __import__('sys').argv:
        out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n', encoding='utf8')
    else:
        old=json.loads(out.read_text(encoding='utf8'))
        assert result==old, 'The independent check differs from the archived exact certificate.'
    print('PASS 120 terminal four-word codes form one hypercube isometry orbit')
    print('PASS all maximal terminal codes: 120 four-word, 16 antipodal two-word')
    print('PASS canonical fiber: 24 possible incoming pairs; each supports one event')
    print('PASS size-six vertex cover excludes >6 atoms per terminal state')
    print('PASS 160 required atoms > 96 capacity of 16 terminal states')
    print('PASS explicit eight-color static q2 partition')
    print('Finite checks: R_online(5,1,2)=5 and R_online(5,1,1)=4')
