"""Loader for wit_n.txt / lp_n.txt.  a encoded as int mask, bit k = a(d_k), d sorted ascending."""
import os
DIR = '/home/claude/agents/paritydata'


def _bits(hexwords, n):
    W = ((1 << n) + 63) // 64
    S = 0
    for w in range(W):
        S |= int(hexwords[16 * w:16 * w + 16], 16) << (64 * w)
    return S


def masks(S):
    out = []
    m = 0
    while S:
        if S & 1: out.append(m)
        S >>= 1; m += 1
    return out


def load_wit(n):
    """dict D -> (nwit, firstA, set of masks)"""
    out = {}
    with open(f'{DIR}/wit_{n}.txt') as f:
        for line in f:
            p = line.split('|')
            D = tuple(sorted(map(int, p[0].split())))
            out[D] = (int(p[1]), int(p[2]), set(masks(_bits(p[3].strip(), n))))
    return out


def load_lp(n):
    fn = f'{DIR}/lp_{n}.txt'
    if not os.path.exists(fn): return None
    out = {}
    with open(fn) as f:
        for line in f:
            p = line.split('|')
            D = tuple(sorted(map(int, p[0].split())))
            out[D] = set(masks(_bits(p[1].strip(), n)))
    return out


def tight(n, D):
    t = 0
    for k in range(1, n):
        t += D[k - 1] + n - k
        if t == k * (k - 1) // 2: return k
    return 0


def tomask(D, a):  # a: dict d->bit
    return sum(a[d] << k for k, d in enumerate(D))


def todict(D, m):
    return {d: (m >> k) & 1 for k, d in enumerate(D)}
