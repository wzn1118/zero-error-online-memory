"""Exhaustively check the independent 3-bit n=4 one-overwrite construction."""

def verify_n4():
    n=4
    query_table={}
    count=0
    for x in range(1<<n):
        m0=min(x,x^15)
        for j in range(n):
            ob=(0,m0,j,x&~(1<<j))
            ans=(x>>j)&1
            assert ob not in query_table or query_table[ob]==ans
            query_table[ob]=ans
        for i in range(n):
            for b in (0,1):
                y=(x&~(1<<i))|(b<<i)
                z=((x^15)&~(1<<i))|(b<<i)
                assert (y^z).bit_count()==3
                e=y if y.bit_count()%2==0 else z
                assert e.bit_count()%2==0
                m1=e&7  # even parity determines coordinate 3, so this is 3-bit storage
                decoded_e=m1|((m1.bit_count()%2)<<3)
                assert decoded_e==e
                for j in range(n):
                    ob=(1,m1,j,y&~(1<<j))
                    ans=(y>>j)&1
                    assert ob not in query_table or query_table[ob]==ans,(x,i,b,j,ob)
                    query_table[ob]=ans
                    count+=1
    return {'n':4,'private_bits':3,'triples':count,'observations':len(query_table)}

if __name__=='__main__':print(verify_n4())
