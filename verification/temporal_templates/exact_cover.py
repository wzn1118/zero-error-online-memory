"""Independent exact one-round cover solver for n <= 3 (standard library only).

This enumerates every admissible initial partition and every maximal terminal
independent code via bit masks, then uses exact set cover over update atoms.
It does not solve the full symbolic (n,T,q) closed-form problem.
"""
from functools import lru_cache
from itertools import combinations


def overwrite(x, i, b):
    return (x & ~(1 << i)) | (b << i)


def is_code(mask, n, distance):
    words = [x for x in range(1 << n) if mask >> x & 1]
    return all((a ^ b).bit_count() >= distance for a, b in combinations(words, 2))


def code_masks(n, distance):
    words = 1 << n
    if words > 16:
        raise ValueError('Restricted exhaustive implementation: n<=4')
    return [mask for mask in range(1, 1 << words) if is_code(mask,n,distance)]


def maximal_codes(n, distance):
    valid=set(code_masks(n,distance))
    result=[]
    for m in valid:
        if not any((m | (1 << x)) in valid for x in range(1<<n) if not (m>>x&1)):
            result.append(m)
    return sorted(result)


def partitions(n, distance, K):
    universe=(1 << (1<<n))-1
    cand=code_masks(n,distance)
    containing=[[c for c in cand if c>>x&1] for x in range(1<<n)]
    def recur(left, out):
        if not left:
            yield tuple(out)
            return
        if len(out)>=K:return
        low=left & -left
        x=low.bit_length()-1
        for c in containing[x]:
            if c & left == c:
                yield from recur(left^c, out+[c])
    yield from recur(universe,[])


def image(code,n,i,b):
    out=0
    while code:
        low=code & -code
        x=low.bit_length()-1
        out |=1 << overwrite(x,i,b)
        code ^=low
    return out


def minimal_set_cover(atom_images, terminal_codes, cutoff):
    # each terminal code covers all atoms with image contained in code
    unique=tuple(sorted(set(atom_images)))
    m=len(unique)
    cover=[]
    for target in terminal_codes:
        cov=sum(1<<j for j,a in enumerate(unique) if a & target == a)
        if cov:cover.append(cov)
    if not cover or (0 if not unique else (0 | __import__('functools').reduce(lambda a,b:a|b,cover,0))) != (1<<m)-1:
        return None
    cover=list(set(cover))
    # Inclusion dominance: only maximal atom-coverage sets needed
    cover=[a for a in cover if not any(a!=b and (a & b)==a for b in cover)]
    @lru_cache(None)
    def rec(uncovered,lim):
        if not uncovered:return ()
        if not lim:return None
        # choose uncovered atom with fewest available covering masks
        best=None
        for j in range(m):
            if uncovered>>j&1:
                poss=[c for c in cover if c>>j&1]
                if best is None or len(poss)<len(best):best=poss
                if len(best)==1:break
        for c in sorted(best,key=lambda c:(c&uncovered).bit_count(),reverse=True):
            ans=rec(uncovered & ~c,lim-1)
            if ans is not None:return (c,)+ans
        return None
    for k in range(1,cutoff+1):
        ans=rec((1<<m)-1,k)
        if ans is not None:return k
    return None


def exact_one_round(n,q, max_states=None, trace=False):
    if n>3:raise ValueError('Exhaustive search bounded to n<=3 for speed')
    if max_states is None:max_states=1<<n
    terminal=maximal_codes(n,q+1)
    tested=0
    for K in range(1,max_states+1):
        for p in partitions(n,q+2,K):
            tested+=1
            atoms=[image(c,n,i,b) for c in p for i in range(n) for b in (0,1)]
            cost=minimal_set_cover(atoms,terminal,K)
            if cost is not None:
                if trace:print('n,q,K,init_cells,terminal_cells,tested=',n,q,K,len(p),cost,tested)
                return K,p,terminal
    return None


def exact_static(n,q):
    for K in range(1,1<<n+1):
        for p in partitions(n,q+1,K):return K
    raise AssertionError

if __name__=='__main__':
    assert exact_static(2,1)==2
    assert exact_static(3,1)==2
    assert exact_static(3,2)==4
    for n,q,want in [(2,1,4),(3,1,4),(3,2,8)]:
        K,p,_=exact_one_round(n,q,trace=True)
        assert K==want,(n,q,K,want)
    print('PASS: exact cover enumerations and input partitions (n<=3)')


def maximal_safe_predecessors(n, d, future):
    """Inclusion-maximal d-codes which each update maps into a future template."""
    cands=[]
    for code in code_masks(n,d):
        if all(any(image(code,n,i,b) & target == image(code,n,i,b)
                       for target in future)
               for i in range(n) for b in (0,1)):
            cands.append(code)
    valid=set(cands)
    return tuple(sorted(c for c in valid if not any(
        (c | (1<<x)) in valid for x in range(1<<n) if not (c>>x&1))))


def backward_witness(n,T,q,K):
    """Return (F_0,...,F_T) if feasible; exhaustive n<=3 only."""
    if n>3:raise ValueError('Certificate search intentionally limited to n<=3')
    from itertools import combinations
    terminal=maximal_codes(n,q+1)
    whole=(1 << (1<<n))-1
    @lru_cache(None)
    def visit(t, future):
        cand=tuple(terminal) if t==T else maximal_safe_predecessors(n,q+T-t+1,future)
        if not cand:return None
        if t==0:
            # find smallest family (any subset of maxima) covering the cube
            for size in range(1,min(K,len(cand))+1):
                for family in combinations(cand,size):
                    cover=0
                    for c in family:cover|=c
                    if cover==whole:return (family,)
            return None
        for size in range(1,min(K,len(cand))+1):
            for family in combinations(cand,size):
                earlier=visit(t-1,family)
                if earlier is not None:return earlier+(family,)
        return None
    return visit(T,())


def verify_templates(n,T,q,families):
    assert len(families)==T+1
    assert max(len(x) for x in families)>0
    initial=0
    for S in families[0]:initial|=S
    assert initial==(1<<(1<<n))-1
    for t,F in enumerate(families):
        for S in F:
            assert is_code(S,n,q+T-t+1)
            if t<T:
                for i in range(n):
                    for b in (0,1):
                        A=image(S,n,i,b)
                        assert any(A & D==A for D in families[t+1])
    return True

if __name__=='__main__':
    for n,T,q,want in [(2,1,1,4),(3,0,1,2),(3,0,2,4),(3,1,1,4),(3,1,2,8)]:
        for K in range(1,want):
            assert backward_witness(n,T,q,K) is None,(n,T,q,K)
        witness=backward_witness(n,T,q,want)
        assert witness is not None
        assert verify_templates(n,T,q,witness)
        print('backward PASS',n,T,q,'K',want,'family sizes',tuple(map(len,witness)))


def exhaustive_protocol_test(n,T,q,families):
    """Materialize transition tables and test every history and erasure."""
    from itertools import combinations,product
    verify_templates(n,T,q,families)
    initial=[]
    for x in range(1<<n):
        initial.append(next(j for j,c in enumerate(families[0]) if c>>x&1))
    transitions=[]
    for t in range(T):
        table={}
        for j,c in enumerate(families[t]):
            for i in range(n):
                for b in (0,1):
                    atom=image(c,n,i,b)
                    table[j,i,b]=next(k for k,d in enumerate(families[t+1]) if atom&d==atom)
        transitions.append(table)
    cases=0
    for x0 in range(1<<n):
        for hist in product([(i,b) for i in range(n) for b in (0,1)],repeat=T):
            m=initial[x0]
            x=x0
            for t in range(T+1):
                for r in range(q+1):
                    for E in combinations(range(n),r):
                        observed={i:(x>>i)&1 for i in range(n) if i not in E}
                        consistent=[y for y in range(1<<n) if families[t][m]>>y&1
                                    and all(((y>>i)&1)==b for i,b in observed.items())]
                        assert consistent==[x],(n,T,q,t,x,m,E,consistent)
                        cases+=1
                if t<T:
                    i,b=hist[t]
                    m=transitions[t][m,i,b]
                    x=overwrite(x,i,b)
    return cases

if __name__=='__main__':
    for n,T,q,K in [(2,1,1,4),(3,1,1,4),(3,1,2,8)]:
        w=backward_witness(n,T,q,K)
        tests=exhaustive_protocol_test(n,T,q,w)
        print('operational simulation PASS',n,T,q, 'query events:',tests)
