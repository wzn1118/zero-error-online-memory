"""Exact integer bounds and explicit polynomial moment sketches.
Python standard library only. The private update map is CHARGED to memory.
"""
from __future__ import annotations
from itertools import combinations
from math import comb, log2
import random


def ceil_log2_positive(k: int) -> int:
    if k < 1:
        raise ValueError(k)
    return (k - 1).bit_length()


def volume(n: int, radius: int) -> int:
    return sum(comb(n, j) for j in range(min(n, radius) + 1))


def dictionary_count(n: int, t: int) -> int:
    return sum(comb(n, j) * (1 << j) for j in range(min(n, t) + 1))


def bounds(n: int, t: int, q: int):
    assert n >= 1 and t >= 0 and 1 <= q <= n
    s = t + q
    if s >= n:
        return {"lower": n, "upper_greedy": n, "lower_volume": n, "saturation": True}
    r = s // 2
    return {
        "lower": max(1, ceil_log2_positive(volume(n, r))),
        "upper_greedy": min(n, ceil_log2_positive(volume(n, s)) + ceil_log2_positive(dictionary_count(n, t))),
        "lower_volume": ceil_log2_positive(volume(n, r)),
        "saturation": False,
    }


def next_prime(n: int) -> int:
    candidate = n + 1
    while True:
        if all(candidate % d for d in range(2, int(candidate ** .5) + 1)):
            return candidate
        candidate += 1


class MomentMemory:
    """An explicit zero-error online sketch. 1-indexed coordinate updates.

    No external transcript is used. 'overwrites' is a private dictionary
    and its entire maximum cardinality is included in the bit budget.
    Each query supplies the current bits outside the erasure set.
    """
    def __init__(self, bits: tuple[int, ...], horizon: int, q: int):
        assert all(v in (0, 1) for v in bits)
        self.n = len(bits)
        assert 1 <= q <= self.n and horizon >= 0
        self.T = horizon
        self.q = q
        self.s = horizon + q
        if self.s >= self.n:
            self.raw = list(bits)
            self.private_bits = self.n
            self.overwrites = None
            self.prime = None
            return
        self.raw = None
        self.prime = next_prime(self.n)
        self.checks = [sum(pow(i + 1, k, self.prime) * value for i, value in enumerate(bits)) % self.prime for k in range(self.s)]
        self.overwrites: dict[int, int] = {}
        self.private_bits = self.s * ceil_log2_positive(self.prime) + ceil_log2_positive(dictionary_count(self.n, horizon))
        self.updates = 0

    def overwrite(self, index: int, value: int):
        assert 0 <= index < self.n and value in (0, 1)
        if self.raw is not None:
            self.raw[index] = value
            return
        assert self.updates < self.T
        self.overwrites[index] = value
        self.updates += 1

    def recover(self, missing: tuple[int, ...], observed: dict[int, int]):
        missing = set(missing)
        assert len(missing) <= self.q and all(0 <= i < self.n for i in missing)
        assert set(observed) == set(range(self.n)) - missing
        if self.raw is not None:
            return {j: self.raw[j] for j in missing}
        S = set(self.overwrites)
        unknown = sorted(S | missing)
        k = len(unknown)
        assert k <= self.s
        known_orig = {i: observed[i] for i in range(self.n) if i not in unknown}
        if k:
            rhs = []
            matrix = []
            for degree in range(k):
                rhs.append((self.checks[degree] - sum(pow(i + 1, degree, self.prime) * b for i, b in known_orig.items())) % self.prime)
                matrix.append([pow(i + 1, degree, self.prime) for i in unknown])
            solved = solve_mod(matrix, rhs, self.prime)
            assert all(v in (0, 1) for v in solved), "Inconsistent test data"
            recovered = dict(zip(unknown, solved))
        else:
            recovered = {}
        return {j: self.overwrites[j] if j in self.overwrites else recovered[j] for j in missing}


def solve_mod(A: list[list[int]], b: list[int], p: int) -> list[int]:
    n = len(b)
    if not n:
        return []
    rows = [[z % p for z in A[i]] + [b[i] % p] for i in range(n)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        inv = pow(rows[col][col], -1, p)
        rows[col] = [v * inv % p for v in rows[col]]
        for i in range(n):
            if i == col:
                continue
            factor = rows[i][col]
            if factor:
                rows[i] = [(a - factor * z) % p for a, z in zip(rows[i], rows[col])]
    return [rows[i][-1] for i in range(n)]


def simulate(n: int, t: int, q: int, trials: int = 250, seed: int = 526):
    rng = random.Random(seed)
    for trial in range(trials):
        current = [rng.randrange(2) for _ in range(n)]
        mem = MomentMemory(tuple(current), t, q)
        for _ in range(rng.randrange(t + 1)):
            i = rng.randrange(n)
            b = rng.randrange(2)
            current[i] = b
            mem.overwrite(i, b)
        misses = tuple(sorted(rng.sample(range(n), rng.randrange(1, q + 1))))
        observed = {i: v for i, v in enumerate(current) if i not in misses}
        got = mem.recover(misses, observed)
        assert all(got[i] == current[i] for i in misses), (trial, n, t, q, current, got)
    return trials


if __name__ == '__main__':
    for case in [(7, 1, 1), (15, 1, 1), (19, 2, 2), (31, 3, 2), (50, 5, 4), (5, 2, 3)]:
        n, t, q = case
        print(case, bounds(n, t, q), 'moment tests:', simulate(*case))
