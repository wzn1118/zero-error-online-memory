"""Exact integer certificates for logarithmic-separation families.

No floats or external libraries are used in the actual certificate inequalities.
Finite numerical audits are not used as proofs of the infinite families.
"""
from math import comb
import csv
from pathlib import Path

def certificate(n,T,q,k):
    s=T+q
    assert 1<=T and 1<=q and s<n and q*2>n
    d_phase=q+1
    plotkin_bound=(2*d_phase)//(2*d_phase-n)
    b=comb(plotkin_bound,2)
    num=comb(s+1,T)
    den=comb(n-s-1+T,T)
    # Prove stronger than Plotkin-over-count saturation with exact integers.
    assert num > b*den, (n,T,q,k)
    assert plotkin_bound < (1<<(k+2))
    return dict(n=n,T=T,q=q,s=s,k=k,plotkin_A_upper=plotkin_bound,
       pair_capacity_bound=b,ratio_exceeds_capacity=True,
       ratio_log2_lower_cert='verified by exact integer cross-multiplication',
       static_bit_upper=n-k,online_exact=n,gap_lower=k)

def subsequence(k):
    r=1<<k; T=r*(k+1); m=4*T
    n=m*(r-1); d=m*r//2; q=d-T-1
    assert d==n//2+2*T
    return certificate(n,T,q,k)

def all_n(n):
    # n >= 1536. Largest integer k with n >= 32 * 4**k * (k+1).
    k=2
    assert n>=32*(4**k)*(k+1)
    while n>=32*(4**(k+1))*(k+2):k+=1
    r=1<<k; T=4*r*(k+1)
    m,a=divmod(n,r-1)
    assert m>=7*T and a<T
    d=m*r//2
    assert d*2-n == m-a
    q=d-T-1
    return certificate(n,T,q,k)

def run(out=None):
    rows=[]
    for k in range(2,7):
        rows.append({'family':'subsequence',**subsequence(k)})
    for n in [1536,1537,1600,1900,2200,3000,4000,5000,6000,7500,
              10000,12000,20000,30000,50000,100000,123456,1000000]:
        rows.append({'family':'all-n',**all_n(n)})
    if out:
        with open(out,'w',newline='',encoding='utf8') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys())
            w.writeheader();w.writerows(rows)
    print('Exact binomial certificates:',len(rows))
    return rows

if __name__=='__main__':
    print(run()[:7])
