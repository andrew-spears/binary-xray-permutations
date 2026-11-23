"""H4/H6 brute-force rule search: a(d) = f(4 binary features of (n, D, d)), all 2^16 f, for every
4-subset of the feature list.  Survivors must satisfy a_f in A(D) for all valid D, n <= NMAX (src lp/wit).
Prints, per subset, the n at which the last f died (or survivors)."""
import sys, itertools
import numpy as np
from pdata import *

NMAX = int(sys.argv[1]); src = sys.argv[2]


def feats(n, D):
    S = set(D); out = []
    for k, d in enumerate(D):
        sl = sum(1 for e in D if e < d and (e - d) % 2 == 0)
        sr = sum(1 for e in D if e > d and (e - d) % 2 == 0)
        ol = sum(1 for e in D if e < d and (e - d) % 2)
        s = d + n - 1 - k
        out.append([d & 1, n & 1, sl & 1, sr & 1, ol & 1, int(d - 1 in S), int(d + 1 in S),
                    k & 1, s & 1, int(s > k), int(s < k), int(d > 0), int(d == 0)])
    return np.array(out, dtype=np.int64)


NAMES = ['d', 'n', 'sameL', 'sameR', 'otherL', 'has(d-1)', 'has(d+1)', 'rank', 's', 's>rank', 's<rank', 'd>0', 'd=0']
data = []
for n in range(1, NMAX + 1):
    W = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)
    for D, A in W.items():
        lut = np.zeros(1 << n, dtype=bool); lut[list(A)] = True
        data.append((n, feats(n, D), lut))
F = ((np.arange(1 << 16)[:, None] >> np.arange(16)[None, :]) & 1).astype(np.int64)  # f table
best = []
for sub in itertools.combinations(range(len(NAMES)), 4):
    alive = np.arange(1 << 16); died = None
    for n, X, lut in data:
        idx = X[:, sub] @ np.array([1, 2, 4, 8])
        masks = (F[alive][:, idx] << np.arange(n)[None, :]).sum(axis=1)
        alive = alive[lut[masks]]
        if len(alive) == 0: died = n; break
    best.append((died if died else 99, [NAMES[i] for i in sub], len(alive), alive[:3].tolist()))
best.sort(key=lambda t: -t[0])
for b in best[:15]: print(b)
