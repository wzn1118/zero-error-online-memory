"""Exact 14-state protocol for n=4, T=1, q=2 (stdlib only).

The public round index is available to the decoder.
The update map uses only (current label, coordinate, assigned value).
"""
from itertools import combinations, product

N, Q = 4, 2
WORDS = [''.join(p) for p in product('01', repeat=N)]

def bitflip(x):
    return ''.join('1' if v == '0' else '0' for v in x)

def overwrite(x, i, b):
    return x[:i] + b + x[i + 1:]

def hamming(x, y):
    return sum(a != b for a, b in zip(x, y))

# Phase-zero labels: two antipodal pairs and twelve singleton fibers.
PAIRS0 = [('0000', '1111'), ('0001', '1110')]
SINGLETONS = [(x,) for x in WORDS if all(x not in p for p in PAIRS0)]
FIBERS0 = PAIRS0 + SINGLETONS
assert len(FIBERS0) == 14
ENC = {x: k for k, fiber in enumerate(FIBERS0) for x in fiber}
assert len(ENC) == len(WORDS)

# The 14 forced successor edges of the two initial antipodal pairs.
EDGES = sorted({tuple(sorted((overwrite(x, i, b), overwrite(y, i, b))))
                for x, y in PAIRS0 for i in range(N) for b in '01'})
assert len(EDGES) == 14
assert all(hamming(x, y) >= Q + 1 for x, y in EDGES)
assert {x for edge in EDGES for x in edge} == set(WORDS)

# Every transition is deterministic and uses solely the initial label & event.
TRANSITION = {}
for m, fiber in enumerate(FIBERS0):
    for i in range(N):
        for b in '01':
            image = {overwrite(x, i, b) for x in fiber}
            candidates = [j for j, edge in enumerate(EDGES) if image <= set(edge)]
            assert candidates, (m, i, b, sorted(image))
            TRANSITION[m, i, b] = candidates[0]

# Exact verification of universal zero-error decoder after 0 or 1 updates.
def certify_phase(round_index, histories):
    observations = {}
    for current, label in histories:
        for k in range(Q + 1):
            for E in combinations(range(N), k):
                visible = ''.join(current[i] for i in range(N) if i not in E)
                erased = ''.join(current[i] for i in E)
                observation = (label, E, visible)
                previous = observations.setdefault(observation, erased)
                assert previous == erased, (round_index, observation, previous, erased)
    return len(observations)

PHASE0 = [(x, ENC[x]) for x in WORDS]
PHASE1 = [(overwrite(x, i, b), TRANSITION[ENC[x], i, b])
          for x in WORDS for i in range(N) for b in '01']
a = certify_phase(0, PHASE0)
b = certify_phase(1, PHASE1)

# A(4,3) = A(4,4) = 2, so the paper's refined incidence converse yields
# K >= ((2 - 1 + 3*2) * 16)/((2-1)*2 + 3*2) = 14.
for d in (3,4):
    assert all(not all(hamming(x,y)>=d for x,y in combinations(triple,2))
               for triple in combinations(WORDS,3))

print('PASS: n=4 T=1 q=2, K=14, phase0 histories=',len(PHASE0),
      'phase1 histories=',len(PHASE1))
print('PASS: observations phase0=',a, 'phase1=',b)
print('PASS: exact 14-state optimum from refined incidence lower bound')
print('phase1 pairs:')
for k, edge in enumerate(EDGES): print(f'{k:02}: {edge[0]} {edge[1]}')
