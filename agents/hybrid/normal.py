"""Transfer (Theorem T): w = x m y is solvable if the normal word  w0 = 1^s1 m (-1)^s2  has an odd split (S; R, C) with S inside m.
For every valid word of length <= N not covered by Theorem 0' this looks for an extreme split of w0 (Theorem E of ../oddsplit: RR, CC, RC, CR)
with S a set of stones of m, and prints how many words are covered, by the least size of S.
  python3 normal.py N [v]"""
import sys, itertools
sys.path.insert(0, "../oddsplit")
from ext import crit
N = int(sys.argv[1]); VERB = "v" in sys.argv[2:]
def split(w):
    i = next((j for j, e in enumerate(w) if e >= 2), None); j = max((j for j, e in enumerate(w) if e <= -2), default=None)
    return None if i is None or j is None or i > j else (w[:i], w[i:j + 1], w[j + 1:])
memo = {}
def least(s1, m):
    """(least |S|, S, types) of an extreme split of 1^s1 m (-1)^s2 with S inside m, or None"""
    if (s1, m) not in memo:
        s2 = s1 + sum(m); e = (1,) * s1 + m + (-1,) * s2; r = None
        for size in range(1, len(m) + 1):
            for S in itertools.combinations(range(s1, s1 + len(m)), size):
                if len(S) == len(e): continue
                c = crit(e, sum(1 << k for k in S))
                if c: r = (size, tuple(k - s1 + 1 for k in S), c.strip()); break
            if r: break
        memo[s1, m] = r
    return memo[s1, m]
def unimodal(m):
    t = next((i for i, e in enumerate(m) if e < 0), len(m))
    return all(0 <= e <= 2 for e in m[:t]) and all(-2 <= e <= 0 for e in m[t:])
stat = {}
def rec(w, s):
    n = len(w)
    if n and s == 0 and split(w):
        x, m, y = split(w); r = least(sum(x), m); st = stat.setdefault(n, [0, 0, {}, None, 0]); st[0] += 1; st[4] += unimodal(m)
        if r is None:
            st[1] += 1
            if st[3] is None: st[3] = w
        else: st[2][r[0]] = st[2].get(r[0], 0) + 1
        if VERB: print(" ".join(map(str, w)), "| s1", sum(x), "m", " ".join(map(str, m)), "|", r)
    if n == N: return
    L = N - n - 1
    for e in range(max((w[-1] - 1) if w else -N, -s), 2 * N):
        if s + e + L * e - L * (L + 1) // 2 > 0: break
        rec(w + (e,), s + e)
if __name__ == "__main__":
    rec((), 0)
    for n in sorted(stat):
        c, bad, by, w, uni = stat[n]
        print(f"n {n}: {c} words not covered by Theorem 0'; middle in {{0,1,2}}*{{0,-1,-2}}* (Theorem H): {uni}; normal word has an extreme split inside m: {c - bad}"
              f" (by least |S|: {dict(sorted(by.items()))}); none: {bad}" + (f" (first {' '.join(map(str, w))})" if w else ""), flush=True)
