"""Exact bit-packing of a private overwrite map and a one-step quotient state.
Standard-library Python. Inputs/outputs are integers in charged bit ranges.
"""
from math import comb
from .bounds_and_moments import dictionary_count, ceil_log2_positive


def rank_map(n:int,T:int,mapping:dict[int,int])->int:
    assert all(0<=i<n and b in (0,1) for i,b in mapping.items())
    k=len(mapping)
    assert k<=T
    keys=sorted(mapping)
    subset=sum(comb(i,j) for j,i in enumerate(keys,start=1) if i>=j)
    bit_pattern=sum(mapping[i]<<j for j,i in enumerate(keys))
    rank=sum(comb(n,j)*(1<<j) for j in range(k))+subset*(1<<k)+bit_pattern
    assert 0<=rank<dictionary_count(n,T)
    return rank


def unrank_map(n:int,T:int,rank:int)->dict[int,int]:
    assert 0<=rank<dictionary_count(n,T)
    k=0
    while rank>=comb(n,k)*(1<<k):
        rank-=comb(n,k)*(1<<k)
        k+=1
        assert k<=T
    subset_id=rank>>k
    pattern=rank&((1<<k)-1)
    positions=[0]*k
    hi=n-1
    for j in range(k,0,-1):
        lo=j-1
        # Standard colex combinadic greedy unranking.
        best=lo
        for candidate in range(lo,hi+1):
            if comb(candidate,j)<=subset_id:
                best=candidate
            else:
                break
        positions[j-1]=best
        subset_id-=comb(best,j)
        hi=best-1
    assert subset_id==0
    return {pos:(pattern>>j)&1 for j,pos in enumerate(positions)}


def compress_quotient(a:int,h:int,r:int)->int:
    """The canonical representative has its highest-bit pivot of h equal 0."""
    assert 0<h<(1<<r)
    a=min(a,a^h)
    pivot=h.bit_length()-1
    assert ((a>>pivot)&1)==0
    return (a&((1<<pivot)-1))|((a>>(pivot+1))<<pivot)


def expand_quotient(z:int,h:int,r:int)->int:
    assert 0<=z<(1<<(r-1))
    pivot=h.bit_length()-1
    return (z&((1<<pivot)-1))|((z>>pivot)<<(pivot+1))


def pack_one_step(i:int,a:int,n:int)->int:
    r=ceil_log2_positive(n+1)
    return i*(1<<(r-1))+compress_quotient(a,i+1,r)


def unpack_one_step(memory:int,n:int)->tuple[int,int]:
    r=ceil_log2_positive(n+1)
    K=1<<(r-1)
    assert 0<=memory<n*K
    i,z=divmod(memory,K)
    return (i,expand_quotient(z,i+1,r))


def test_packing():
    from itertools import combinations,product
    dictionaries=0
    for n in range(1,9):
        T=min(n,3)
        values=set()
        for k in range(T+1):
            for selected in combinations(range(n),k):
                for bits in product((0,1),repeat=k):
                    mapping=dict(zip(selected,bits))
                    rank=rank_map(n,T,mapping)
                    assert unrank_map(n,T,rank)==mapping
                    assert rank not in values
                    values.add(rank)
                    dictionaries+=1
        assert values==set(range(dictionary_count(n,T)))
    encoded=0
    for n in range(2,35):
        r=ceil_log2_positive(n+1)
        for i in range(n):
            for a in range(1<<r):
                z=pack_one_step(i,a,n)
                i1,rep=unpack_one_step(z,n)
                assert i==i1 and rep==min(a,a^(i+1))
                encoded+=1
    return {'dictionaries_verified':dictionaries, 'quotient_labels_verified':encoded}

if __name__=='__main__':print(test_packing())
