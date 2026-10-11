#!/usr/bin/env python3
"""Deterministic conditional-expectation completion of a repeated simplex code.

The mathematical existence theorem uses Hoeffding's inequality. This program
implements its conditional-expectation greedy choice (double precision scoring)
and validates the final binary code by exact integer popcounts.
"""
import argparse
import math


def select_dimension(n):
    options=[]
    for k in range(2,max(3,n.bit_length()+1)):
        r=1<<k
        if n>=16*(r**1.5)*math.sqrt(math.log(2*r)):
            options.append(k)
        else:
            break
    if not options:
        raise ValueError('n below the analytic all-length construction threshold')
    return max(options)


def construct(n):
    k=select_dimension(n)
    r=1<<k
    m=2*(n//(2*(r-1)))
    a=n-m*(r-1)
    assert 0<=a<2*(r-1)
    assert m>=4+2*math.sqrt((r-1)*math.log(2*r))
    columns=[v for _ in range(m) for v in range(1,r)]
    if a:
        h=m/2-2
        theta=4*h/a
        attenuation=math.exp(-theta)
        weights=[1.0]*r
        for _ in range(a):
            best_v=None
            best_score=-1.0
            for v in range(1,r):
                score=sum(weights[u] for u in range(1,r) if ((u&v).bit_count()&1))
                if score>best_score:
                    best_score=score
                    best_v=v
            columns.append(best_v)
            for u in range(1,r):
                if (u&best_v).bit_count()&1:
                    weights[u]*=attenuation
    assert len(columns)==n
    min_weight=min(sum((u&v).bit_count()&1 for v in columns) for u in range(1,r))
    q=(n+1)//2
    assert min_weight>=q+2,(n,k,m,a,min_weight,q+2)
    return {'n':n,'k':k,'r':r,'base_repeats':m,'added_columns':a,'minimum_code_distance':min_weight,'required_distance':q+2,'online_bits':n,'static_bits_upper':n-k,'columns':columns}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('lengths',nargs='*',type=int,default=[185,200,300,512,1000,2400,5000,10000])
    p.add_argument('--save-columns',action='store_true')
    args=p.parse_args()
    for n in args.lengths:
        v=construct(n)
        print({k:v[k] for k in v if k!='columns'})
        if args.save_columns:
            from pathlib import Path
            from json import dumps
            Path(f'completed_simplex_n{n}.json').write_text(dumps(v,indent=2))
    print('PASS: independently certified one-write all-length static constructions')

if __name__=='__main__':main()
