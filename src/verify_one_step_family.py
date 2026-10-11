"""Formula-based online code for T=q=1, distinct nonzero syndrome columns.
No matching solver, third-party dependencies, or neural networks.
"""
from __future__ import annotations
from .bounds_and_moments import ceil_log2_positive


def syndrome(x: int,n:int)->int:
    s=0
    for i in range(n):
        if x & (1<<i): s^=i+1
    return s


def canonical(s: int,h: int)->int:
    return min(s,s^h)


def choose_v(h:int,r:int)->int:
    return next(a for a in range(1,1<<r) if a!=h)


def online_label(initial_syndrome:int,i:int,b:int,n:int):
    r=ceil_log2_positive(n+1)
    h=i+1
    v=choose_v(h,r)
    return (i,canonical(initial_syndrome^(v if b else 0),h))


def recover(label: tuple[int,int],j:int,visible:int,n:int)->int:
    i,beta=label
    r=ceil_log2_positive(n+1)
    h=i+1
    v=choose_v(h,r)
    if j==i:
        # Quotient of current word is independent of the erased coordinate i.
        alpha=canonical(syndrome(visible,n),h)
        if beta==alpha:
            return 0
        assert beta==canonical(alpha^v,h)
        return 1
    b=(visible>>i)&1
    alpha=canonical(beta^(v if b else 0),h)
    base=canonical(syndrome(visible,n),h)
    if base==alpha:
        return 0
    assert canonical(base^(j+1),h)==alpha
    return 1


def check_one_step(n:int):
    assert n>=2
    r=ceil_log2_positive(n+1)
    terminal_labels=set()
    checks=0
    for x in range(1<<n):
        sx=syndrome(x,n)
        for j in range(n):
            sx_without=syndrome(x&~(1<<j),n)
            assert sx^sx_without in (0,j+1)
            assert ((sx^sx_without)!=0)==bool((x>>j)&1)
        for i in range(n):
            for b in (0,1):
                y=(x&~(1<<i))|(b<<i)
                label=online_label(sx,i,b,n)
                terminal_labels.add(label)
                for j in range(n):
                    visible=y&~(1<<j)
                    assert recover(label,j,visible,n)==((y>>j)&1),(n,x,i,b,j,label)
                    checks+=1
    limit=n*(1<<(r-1))
    assert len(terminal_labels)==limit,(n,len(terminal_labels),limit)
    budget=max(ceil_log2_positive(1<<r),ceil_log2_positive(limit))
    assert budget==max(r,(r-1)+ceil_log2_positive(n))
    return {'n':n,'r':r,'states':len(terminal_labels),'bits':budget,'checked':checks}

if __name__=='__main__':
    for n in range(2,9):print(check_one_step(n))
