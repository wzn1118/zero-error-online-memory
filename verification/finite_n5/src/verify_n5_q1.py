"""Independent exact finite certificate for R_1^online(5,1) = 4.

No external libraries, Docker, SAT solver, Lean, or AI service needed.
Recomputes all 8,865 antipodal-independent four-word partitions,
classifies their 28 cube-isometry orbits, verifies a 9-clique in the
80-atom compatibility graph of each representative, and checks the
16-state constructive protocol.
"""
from itertools import combinations
from collections import deque
from pathlib import Path
import json
import hashlib
import sys

N_BITS = 5
N = 1 << N_BITS
MASK = N - 1


def hd(x,y):
    return (x^y).bit_count()


def write(x, i, b):
    return (x & ~(1<<i)) | (b<<i)


def make_4codes():
    return sorted(sum(1<<x for x in word) for word in combinations(range(N),4)
                  if all(hd(a,b)>=3 for a,b in combinations(word,2)))


def make_partitions():
    codes = make_4codes()
    bypoint = [[] for _ in range(N)]
    for code in codes:
        for j in range(N):
            if code>>j & 1:
                bypoint[j].append(code)
    out = []
    def rec(free, acc):
        if not free:
            assert len(acc)==8
            out.append(tuple(sorted(acc)))
            return
        j=(free&-free).bit_length()-1
        for code in bypoint[j]:
            if code&free==code:
                rec(free^code,acc+[code])
    rec((1<<N)-1,[])
    return codes, out


def transforms():
    # The generators x -> x XOR e_i, and adjacent coordinate exchanges,
    # generate the full 2^5 * 5! hypercube isometry group.
    perms=[]
    for i in range(N_BITS):
        perms.append(tuple(x^(1<<i) for x in range(N)))
    for i in range(N_BITS-1):
        transformed=[]
        for x in range(N):
            mask=(1<<i)|(1<<(i+1))
            yi=(x>>i)&1
            yj=(x>>(i+1))&1
            transformed.append((x&~mask)|(yi<<(i+1))|(yj<<i))
        perms.append(tuple(transformed))
    return perms


def transform_partition(part, permutation):
    result=[]
    for code in part:
        newcode=0
        for x in range(N):
            if code>>x&1:
                newcode |= 1<<permutation[x]
        result.append(newcode)
    return tuple(sorted(result))


def classify_orbits(partitions):
    lookup={p:i for i,p in enumerate(partitions)}
    assert len(lookup)==len(partitions)
    allperms=transforms()
    unseen=set(range(len(partitions)))
    result=[]
    while unseen:
        seed=min(unseen)
        unseen.remove(seed)
        work=[seed]
        for ix in work:
            for perm in allperms:
                nxt=lookup[transform_partition(partitions[ix],perm)]
                if nxt in unseen:
                    unseen.remove(nxt)
                    work.append(nxt)
        result.append((seed,len(work)))
    return result


def make_graph(partition):
    # Each code block corresponds to a different initial memory label.
    atoms=[]
    for label, code in enumerate(partition):
        src=tuple(x for x in range(N) if code>>x&1)
        assert len(src)==4
        for i in range(N_BITS):
            for b in (0,1):
                dst=tuple(sorted({write(x,i,b) for x in src}))
                assert len(dst)==4
                assert all(hd(x,y)>=2 for x,y in combinations(dst,2))
                atoms.append((label,i,b,dst))
    assert len(atoms)==80
    # Edge iff there exist two distinct output words differing in one bit.
    graph=[0]*len(atoms)
    for a in range(len(atoms)):
        for b in range(a):
            if any(hd(x,y)==1 for x in atoms[a][3] for y in atoms[b][3]):
                graph[a] |= 1<<b
                graph[b] |= 1<<a
    return atoms,graph


def find_clique9(graph):
    # Pure greedy search: success gives a valid certificate, failure is
    # not evidence of nonexistence.
    m=len(graph)
    starts=sorted(range(m),key=lambda v:(graph[v].bit_count(),-v),reverse=True)
    for start in starts:
        clique=[start]
        candidates=graph[start]
        while candidates:
            choices=[j for j in range(m) if candidates>>j&1]
            v=max(choices,key=lambda j:((graph[j]&candidates).bit_count(), graph[j].bit_count(), -j))
            clique.append(v)
            if len(clique)>=9:
                return clique[:9]
            candidates &= graph[v]
    raise AssertionError('Greedy heuristic did not find a certificate: no mathematical conclusion')


def check_16_state_scheme():
    # Initial state pairs every word with its bitwise complement.
    blocks=[(x,x^MASK) for x in range(N) if x<(x^MASK)]
    assert len(blocks)==16
    for index, (a,b) in enumerate(blocks):
        assert hd(a,b)==5
        for i in range(5):
            for value in (0,1):
                results=[write(a,i,value),write(b,i,value)]
                parities=[x.bit_count()%2 for x in results]
                assert parities[0]==parities[1]
                for x in results:
                    for missing in range(5):
                        observed=x & ~(1<<missing)
                        restored_bit = (parities[0] ^ (observed.bit_count()%2))
                        recovered=observed|(restored_bit<<missing)
                        assert recovered==x
    return {'initial_labels':16,'updates_checked':16*5*2*2,'queries_checked':16*5*2*2*5}


def main():
    codes, partitions=make_partitions()
    assert len(codes)==120, len(codes)
    assert len(partitions)==8865,len(partitions)
    orbits=classify_orbits(partitions)
    assert len(orbits)==28,len(orbits)
    assert sum(size for _,size in orbits)==8865
    proof=[]
    for index,size in orbits:
        part=partitions[index]
        atoms,graph=make_graph(part)
        clique=find_clique9(graph)
        assert len(clique)==9 and len(set(clique))==9
        assert all((graph[a]>>b)&1 for a,b in combinations(clique,2))
        proof.append({'index':index,'orbit_size':size,'partition':list(part),
                      'clique_atom_ids':clique,
                      'clique_triples':[[atoms[j][0],atoms[j][1],atoms[j][2]] for j in clique]})
    upper=check_16_state_scheme()
    result={'statement':'R_online(n=5,T=1,q=1)=4 bits',
            'number_4codes':len(codes), 'number_partitions':len(partitions),
            'number_orbits':len(orbits), 'orbit_certificates':proof,
            'constructive_upper':upper}
    here=Path(__file__).resolve().parents[1]
    dest=here/'certificates/n5_orbit_cliques.json'
    if '--generate' in sys.argv:
        dest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    else:
        existing=json.loads(dest.read_text(encoding='utf-8'))
        assert existing==result,'Certificate mismatch!'
    sha=hashlib.sha256(dest.read_bytes()).hexdigest()
    print('A(5,3) <= 4: parity-ball argument in paper')
    print('valid size-four codes:',len(codes))
    print('exact-cover partitions:',len(partitions))
    print('isometry orbits:',len(orbits))
    print('sizes:',[s for _,s in orbits])
    print('9-cliques certified:',len(proof),'* 36 edges')
    print('16-state upper:',upper)
    print('SHA256 certificate:',sha)
    print('PROVED FOR THIS FINITE INSTANCE: R_1^online(5,1)=4 bits')

if __name__=='__main__':
    main()
