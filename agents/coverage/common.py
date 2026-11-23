"""Shared helpers: enumeration of valid D, splits, witness search, constructions."""
from itertools import combinations
from functools import lru_cache
from math import gcd


def scores(D, n):
    return [d + n - k for k, d in enumerate(sorted(D), 1)]


def is_valid(D, n):
    D = sorted(D)
    if len(D) != n or (n and (D[0] < -(n - 1) or D[-1] > n - 1)):
        return False
    t = 0
    for k, d in enumerate(D, 1):
        t += d + n - k
        if t < k * (k - 1) // 2:
            return False
    return t == n * (n - 1) // 2


def tight_cuts(D, n):
    D = sorted(D)
    t, out = 0, []
    for k, d in enumerate(D[:-1], 1):
        t += d + n - k
        if t == k * (k - 1) // 2:
            out.append(k)
    return out


def enum_valid(n):
    """All valid D (sorted tuples) of size n."""
    res = []
    lo = -(n - 1)

    def rec(k, prev, t, cur):
        if k == n:
            if t == n * (n - 1) // 2:
                res.append(tuple(cur))
            return
        # choose d_{k+1} > prev
        for d in range(prev + 1, n):
            # remaining picks need room: n-k-1 more values above d, <= n-1
            if d + (n - k - 1) > n - 1:
                break
            t2 = t + d + n - (k + 1)
            if t2 < (k + 1) * k // 2:
                continue
            if t2 > n * (n - 1) // 2:
                break
            cur.append(d)
            rec(k + 1, d, t2, cur)
            cur.pop()

    rec(0, lo - 1, 0, [])
    return res


def canon(D):
    a = tuple(sorted(D))
    b = tuple(sorted(-x for x in D))
    return min(a, b)


def diags(p):
    """p: tuple of images of 1..n (1-based values)."""
    return tuple(sorted(p[i] - (i + 1) for i in range(len(p))))


def find_witness(D, n, involution=False):
    D = sorted(D)
    Dset = set(D)
    if involution:
        if any(-d not in Dset for d in D):
            return None
        pos = [d for d in D if d > 0]
        nfix = 1 if 0 in Dset else 0
        p = [0] * (n + 1)

        def rec(j, used):
            if j == len(pos):
                free = [i for i in range(1, n + 1) if not used >> i & 1]
                if len(free) != nfix:
                    return False
                for i in free:
                    p[i] = i
                return True
            d = pos[j]
            for i in range(1, n - d + 1):
                if not (used >> i & 1) and not (used >> (i + d) & 1):
                    p[i], p[i + d] = i + d, i
                    if rec(j + 1, used | 1 << i | 1 << (i + d)):
                        return True
            return False

        return tuple(p[1:]) if rec(0, 0) else None
    idx = {d: j for j, d in enumerate(D)}
    p = [0] * n

    def rec(i, usedD, usedC):
        if i == n:
            return True
        r = i + 1
        for d in D:
            if usedD >> idx[d] & 1:
                continue
            c = r + d
            if 1 <= c <= n and not usedC >> c & 1:
                p[i] = c
                if rec(i + 1, usedD | 1 << idx[d], usedC | 1 << c):
                    return True
        return False

    return tuple(p) if rec(0, 0, 0) else None


def affine_perms(n, moduli):
    """Rank of the residues (a*i+b mod M), i=1..n, for gcd(a,M)=1. Yields (M,a,b,perm)."""
    for M in moduli:
        if M < n:
            continue
        for a in range(1, M):
            if gcd(a, M) != 1:
                continue
            for b in range(M):
                v = [(a * i + b) % M for i in range(1, n + 1)]
                order = sorted(v)
                rk = {x: j + 1 for j, x in enumerate(order)}
                yield M, a, b, tuple(rk[x] for x in v)


def band_sets(n):
    out = set()
    if n % 2 == 0:
        a = n // 2
        out.add(tuple(sorted(list(range(1, a + 1)) + list(range(-a, 0)))))
    # {-k..k} minus {0,±m}: size 2k+1-3 = n  => k = (n+2)/2
    if n % 2 == 0:
        k = (n + 2) // 2
        for m in range(1, k + 1):
            out.add(tuple(x for x in range(-k, k + 1) if x not in (0, m, -m)))
    return out
