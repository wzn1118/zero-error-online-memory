"""Independent V10 forced-pair incidence proof experiment; no V10/V12 imports."""
from itertools import combinations
from collections import defaultdict
from time import perf_counter

def test(n):
    start=perf_counter()
    N=1<<n
    pairs=[(x,y) for x in range(N) for y in range(x+1,N) if (x^y).bit_count() >= n-1]
    images=[]; pre=defaultdict(list)
    for pid,(a,b) in enumerate(pairs):
        edges=set()
        for i in range(n):
            bit=1<<i
            for v in (0,1):
                u=(a&~bit)|(bit if v else 0)
                w=(b&~bit)|(bit if v else 0)
                assert u!=w
                edges.add(tuple(sorted((u,w))))
        assert len(edges)==2*n
        images.append(edges)
        for e in edges:pre[e].append(pid)
    checks=bad=nonzero=overlap=0
    for i,j in combinations(range(len(pairs)),2):
        p,q=pairs[i],pairs[j]
        if len({*p,*q})!=4:continue
        cross=sum((x^y).bit_count()==1 for x in p for y in q)
        shared=len(images[i].intersection(images[j]))
        checks+=1
        if shared:overlap+=1
        if shared>cross:bad+=1
        if shared:nonzero+=shared
    # Independently verify that no three source pairs with disjoint endpoints
    # induce one common forced terminal pair.
    triple=0
    for edge,ids in pre.items():
        if len(ids)<3:continue
        for i,j,k in combinations(ids,3):
            if len(set(pairs[i]+pairs[j]+pairs[k]))==6:
                triple+=1
    assert bad==0 and triple==0
    return {'n':n,'pair_count':len(pairs),'disjoint_pair_checks':checks,'shared_forced_edge_pair_cases':overlap,'max_output_multiplicity':max(map(len,pre.values())),'triple_disjoint_violations':triple,'D_le_e_violations':bad,'elapsed_s':round(perf_counter()-start,3)}

if __name__=='__main__':
    for n in (7,8):print('PASS',test(n),flush=True)
