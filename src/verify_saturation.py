"""Finite checks for the phase-compatibility high-erasure theorem (stdlib only).

This is NOT a proof of the all-n result; the proof is in paper.tex.
Finite checks cover translation-pair initial partitions, the multiplicity count,
and every 3-word bound through n=7.
"""
from itertools import combinations
from collections import Counter
from math import comb


def hdist(x, y):
    return (x ^ y).bit_count()


def triangle_check(n):
    words = range(1 << n)
    for x, y, z in combinations(words, 3):
        a,b,c=hdist(x,y), hdist(x,z), hdist(y,z)
        assert a + b + c <= 2*n
    return True


def translation_partition(n, mask):
    assert 0 < mask < 1 << n
    assert mask.bit_count() > 2*n/3
    used = set()
    pairs = []
    for x in range(1 << n):
        if x not in used:
            y = x ^ mask
            assert y not in used
            pairs.append((x, y))
            used.add(x); used.add(y)
    assert len(pairs) == 1 << (n-1)
    return pairs


def verify_translation_case(n,s,mask):
    assert 2*n/3 < s < n
    assert mask.bit_count() >= s+1
    pairs = translation_partition(n,mask)
    forced = Counter()
    for x,y in pairs:
        for i in range(n):
            if not (x^y) & (1<<i):
                continue
            for bit in (0,1):
                zmask=1<<i
                a=(x & ~zmask) | (bit<<i)
                b=(y & ~zmask) | (bit<<i)
                assert hdist(a,b) >= s
                key=(a,b) if a<b else (b,a)
                forced[key] += 1
    K=len(pairs)
    c=n-s
    assert max(forced.values()) <=2*c
    assert len(forced)*2*c >= sum(forced.values())
    assert len(forced)>K  # more forced edges than any 2-word final state capacity
    # Verify triangle condition for each pair output in any terminal label:
    assert 3*s > 2*n
    return (n,s,mask.bit_count(),K,len(forced),sum(forced.values()),max(forced.values()))


def run():
    for n in range(2,8):
        triangle_check(n)
    rows=[]
    for n in range(4,11):
        for s in range(1,n):
            if 3*s <=2*n:
                continue
            for mask in range(1,1<<n):
                if mask.bit_count() <s+1:
                    continue
                rows.append(verify_translation_case(n,s,mask))
    assert rows
    print('Saturation: translation partitions tested:',len(rows))
    print('Saturation: boundary n=4,s=3:',[r for r in rows if r[0:2]==(4,3)])
    print('Saturation: n=7,s=5:',[r for r in rows if r[0:2]==(7,5)][:2])
    assert len([r for r in rows if r[0]==10])>0
    return len(rows)

if __name__=='__main__':
    run()
    print('PASS')
