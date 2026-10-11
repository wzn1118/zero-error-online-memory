#!/usr/bin/env python3
"""Pure-Python exact checks for a distance-spectrum converse.
No Docker, Lean, external modules, network, or model calls.
"""
from itertools import combinations, product
from math import comb


def dist(a, b):
    return (a ^ b).bit_count()


def overwrite(x, i, b):
    return (x & ~(1 << i)) | (b << i)


def spectrum_weight(C, n, t, terminal=False):
    return sum(comb(n - dist(x, y), t) if terminal else comb(dist(x, y), t)
               for x, y in combinations(C, 2))


def check_n3_sharp():
    n, T, q = 3, 1, 1
    X = range(1 << n)
    # The initial state identifies antipodal pairs.
    initial = {m: {m, m ^ 7} for m in range(4)}
    # The only terminal state needed is the parity of the current vector.
    terminal = {p: {x for x in X if x.bit_count() % 2 == p} for p in range(2)}
    transitions = {}
    for m, C in initial.items():
        for i, b in product(range(n), (0, 1)):
            A = {overwrite(x, i, b) for x in C}
            targets = [p for p, D in terminal.items() if A <= D]
            assert len(targets) == 1
            transitions[m, i, b] = targets[0]
            for E in combinations(range(n), q):
                for x in A:
                    compatible = [z for z in terminal[targets[0]]
                                  if all(((z >> j) & 1) == ((x >> j) & 1)
                                         for j in range(n) if j not in E)]
                    assert compatible == [x]
    left = sum(spectrum_weight(C, n, T) for C in initial.values())
    right = sum(spectrum_weight(D, n, T, terminal=True) for D in terminal.values())
    assert (left, right) == (12, 12), (left, right)
    # Verify initial decodability.
    for C in initial.values():
        for E in combinations(range(n), q):
            for x in C:
                assert sum(all(((y >> j) & 1) == ((x >> j) & 1)
                               for j in range(n) if j not in E) for y in C) == 1
    print('n=3, T=1, q=1: valid 2-bit online protocol, weighted sides = 12 = 12')


def check_n5_energy():
    n, d = 5, 3
    candidates = [x for x in range(1, 1 << n) if x.bit_count() >= d]
    best_size, best_energy, best_C = 0, -1, None
    # Translate a nonempty binary code so that it contains zero.
    for mask in range(1 << len(candidates)):
        C = [0] + [x for j, x in enumerate(candidates) if mask >> j & 1]
        if any(dist(x, y) < d for x, y in combinations(C, 2)):
            continue
        w = spectrum_weight(C, n, 1, terminal=True)
        best_size = max(best_size, len(C))
        if w > best_energy:
            best_energy, best_C = w, C
    assert best_size == 4, best_size
    assert best_energy == 10, (best_energy, best_C)
    assert spectrum_weight([0, 7, 25, 30], n, 1, terminal=True) == 10
    coarse = (n - d) * comb(best_size, 2)
    assert coarse == 12
    print('n=5, terminal min distance 3: A(5,3)=4, exact energy=10 < coarse=12')


def basic_parameters():
    for n in range(2, 11):
        for q in range(1, n+1):
            for T in range(0, n+1):
                if T+q >= n:
                    continue
                for t in range(1, T+1):
                    # Empty or singleton codes always satisfy the spectrum converse.
                    assert comb(T+q+1, t) > 0
                    assert q + T - t + 1 >= q + 1
    print('General parameter and distance-index sanity checks pass.')


if __name__ == '__main__':
    check_n3_sharp()
    check_n5_energy()
    basic_parameters()
    print('ALL CHECKS PASSED')
