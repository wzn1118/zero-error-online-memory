"""Independent 12,544-case validation of a 5-bit / n=7 online sketch.
Only standard-library Python. Certificate is a list of 28 compatible pairs
of the 56 pieces (i,b, quotient of Hamming syndrome).
"""
from __future__ import annotations
from pathlib import Path
import json

N=7

def syndrome(x):
    result=0
    for i in range(N):
        if (x >> i) & 1: result ^= i+1
    return result


def quotient(s, i):
    return min(s, s ^ (i+1))


def piece(i,b,quot):
    return {y for y in range(1<<N) if ((y>>i)&1)==b and quotient(syndrome(y),i)==quot}


def verify(path=None):
    if path is None:
        path=Path(__file__).parent.parent/'certificates'/'n7_one_update_matching.json'
    raw=json.loads(Path(path).read_text())
    pairs=raw['pairs']
    assert len(pairs)==28
    ids={}
    candidate_by_label={}
    for label,pair in enumerate(pairs):
        assert len(pair)==2
        union=set()
        for key in pair:
            key=tuple(key)
            assert key not in ids
            ids[key]=label
            ys=piece(*key)
            assert len(ys)==16
            union |=ys
        candidate_by_label[label]=union
        for y in union:
            assert all((y^(1<<j)) not in union for j in range(N)),(label,y)
    expected={(i,b,s) for i in range(N) for b in (0,1) for s in range(8) if s < (s^(i+1))}
    assert set(ids)==expected,(len(ids),len(expected))
    obs={}
    count=0
    for x in range(1<<N):
        sx=syndrome(x)
        for i in range(N):
            for b in (0,1):
                y=(x& ~(1<<i))|(b<<i)
                label=ids[(i,b,quotient(sx,i))]
                assert y in candidate_by_label[label]
                for j in range(N):
                    observation=(label,j,y & ~(1<<j))
                    ans=(y>>j)&1
                    if observation in obs:
                        assert obs[observation]==ans
                    obs[observation]=ans
                    count+=1
    assert count == 128*7*2*7
    # Initially the syndrome is recoverable from the un-erased coordinates.
    for x in range(1<<N):
        sx=syndrome(x)
        for j in range(N):
            x_without_j=x&~(1<<j)
            recovered=(syndrome(x_without_j)^sx)//(j+1)
            assert recovered == ((x>>j)&1)
    return {'candidate_pieces':len(ids),'final_states':len(pairs),'full_cases':count,'distinct_observations':len(obs)}

if __name__=='__main__':
    print(verify())
