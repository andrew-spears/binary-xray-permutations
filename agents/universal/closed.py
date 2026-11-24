"""Is the explicit family J* of jstar.py closed under blocks?  (REPORT3.md, "Range" and "What it gives".)  A block leads from an old prefix ending in 0 or 1
to the next one: a letter 0 or 1, or negative letters and then 0 or 1, or an excursion that starts with a letter >= 2 and ends when the
young excess y is back at 0 on a letter 0 or 1.  For every source slack s in [S0, S1], source tail, and block of at most L letters
(letters <= C, slack <= SMAX inside the block):  J*(target) inside step_block(J*(source)) ?   Only slacks >= 11 on both ends.
Usage: python3 closed.py S0 S1 L C SMAX"""
import sys, functools
import exc, l1, jstar
S0, S1, L, C, SMAX = map(int, sys.argv[1:6])
TAILS = [("1", "1"), (".", "1"), ("1", "0"), ("0", "0"), (".", "0")]
@functools.lru_cache(None)
def J(s, tail): return frozenset(u for u in exc.states(s) if jstar.jstar(u, tail))
def blocks(l):                       # blocks after an old prefix with last letter l
    out = []
    def rec(w, y, s):
        e0 = (w[-1] if w else l) - 1
        for e in range(e0, C + 1):
            y2 = max(0, y + e - 1); w2 = w + [e]
            if y2 == 0 and e in (0, 1): out.append(tuple(w2))
            elif len(w2) < L and s + e <= SMAX - S1: rec(w2, y2, s + e)
    rec([], 0, 0); return out
def tail_after(tail, w):
    x = [tail[0], int(tail[1])] + list(w); return ("." if x[-2] == "." or x[-1] > x[-2] else str(x[-2]), str(x[-1]))
bad = 0; n = 0; succ = functools.lru_cache(None)(lambda u, e: tuple(v for _, v in l1.succs(u, e)))
for s in range(S0, S1 + 1):
    for tail in TAILS:
        for w in blocks(int(tail[1])):
            t2 = tail_after(tail, w); s2 = s + sum(w)
            if s2 < 11 or min(s + sum(w[:i]) for i in range(len(w) + 1)) < 0: continue
            S = J(s, tail)
            for e in w: S = set(v for u in S for v in succ(u, e))
            d = J(s2, t2) - S; n += 1
            if d: bad += 1; print(f"NOT closed: ({s}, {' '.join(tail)}) --[{' '.join(map(str, w))}]--> ({s2}, {' '.join(t2)}): {len(d)} states of J* not reached, e.g.", " ".join(sorted(l1.name(u) for u in d)[:6]))
print(f"{n} (source, block) pairs, {bad} not closed")
