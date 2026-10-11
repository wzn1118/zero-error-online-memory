"""Exact certificate for the Hamming-syndrome one-overwrite protocol.
No packages beyond Python standard library. r=3 exhaustive, r=4 algebraic checks.
"""
from itertools import combinations

def syn(x,n):
    s=0
    for i in range(n):
        if x>>i&1:s^=i+1
    return s

def overwrite(x,i,b):return (x&~(1<<i))|(b<<i)

def lines(r,i):
    v=i+1;seen=set();ans=[]
    for s in range(1<<r):
        if s in seen:continue
        L=frozenset((s,s^v));ans.append(L);seen.update(L)
    return ans

def verify_r3():
    r=3;n=7; N=1<<n; W=list(range(N))
    all_L={i:lines(r,i) for i in range(n)}
    A={}
    for i in range(n):
        for b in (0,1):
            for idx,L in enumerate(all_L[i]):
                A[i,b,idx]=frozenset(y for y in W if y>>i&1==b and syn(y,n) in L)
                assert len(A[i,b,idx])==16
    def incompatible(U,V):
        return any((y^(1<<j)) in V for y in U for j in range(n))
    count=0
    edges=0
    for left,right in combinations(A,2):
        i,b,a=left; j,c,d=right
        expected=(i!=j) or (b==c) or (a==d) # same index only when i=j
        observed=incompatible(A[left], A[right])
        assert expected==observed,(left,right,expected,observed)
        count+=1
        edges+=bool(observed)
    m=1<<(r-1)
    terminal={}
    for i in range(n):
        for k in range(m):
            terminal[i*m+k]=A[i,0,k]|A[i,1,(k-1)%m]
            assert len(terminal[i*m+k])==32
            assert all(((x^y).bit_count()>=2) for x,y in combinations(terminal[i*m+k],2))
    checks=0
    for x in W:
        s=syn(x,n)
        for i in range(n):
            L=frozenset([s,s^(i+1)])
            idx=all_L[i].index(L)
            for b in (0,1):
                y=overwrite(x,i,b)
                k=idx if b==0 else (idx+1)%m
                label=i*m+k
                assert y in terminal[label]
                for erased in range(n):
                    obs=y&~(1<<erased)
                    candidates=[v for v in terminal[label] if v&~(1<<erased)==obs]
                    assert candidates==[y],(x,i,b,erased)
                    checks+=1
    print(f'PASS r=3: {len(A)} atoms; {count} comparisons ({edges} conflicting); {len(terminal)} terminal states; {checks} protocol queries')

def verify_all_ranks():
    for r in range(3,8):
        n=(1<<r)-1
        # Any n-3 distinct nonzero r-bit columns span r because a proper subspace has <= 2^(r-1)-1 nonzero members.
        assert n-3>(1<<(r-1))-1
        # For any two directions hi,hj, affine 2-plane differences contain a third nonzero direction.
        for i,j in combinations(range(n),2):
            for d in range(1<<r):
                diff={d,d^(i+1),d^(j+1),d^(i+1)^(j+1)}
                assert any(v not in (0,i+1,j+1) for v in diff)
        print(f'PASS r={r}: direction checks {n*(n-1)//2*(1<<r)}, K={n*(1<<(r-1))}')

def update_label(r,s,i,b):
    m=1<<(r-1); L=frozenset((s,s^(i+1)))
    idx=lines(r,i).index(L)
    k=idx if b==0 else (idx+1)%m
    return i*m+k

def recover(r,label,known,erased):
    n=(1<<r)-1;m=1<<(r-1)
    i,k=divmod(label,m)
    candidates=[]
    for bit in (0,1):
        y=known | (bit<<erased)
        which=k if (y>>i&1)==0 else (k-1)%m
        if syn(y,n) in lines(r,i)[which]: candidates.append(y)
    assert len(candidates)==1,(r,label,known,erased,candidates)
    return candidates[0]

def seeded_checks():
    import random
    rng=random.Random(20261010)
    for r,iterations in ((4,3000),(5,2000)):
        n=(1<<r)-1
        for _ in range(iterations):
            x=rng.randrange(1<<n);i=rng.randrange(n);b=rng.randrange(2)
            er=rng.randrange(n)
            label=update_label(r,syn(x,n),i,b)
            y=overwrite(x,i,b)
            assert recover(r,label,y&~(1<<er),er)==y
        print(f'PASS r={r}: {iterations} seeded full-protocol queries')

if __name__=='__main__':
    verify_r3();verify_all_ranks();seeded_checks()
