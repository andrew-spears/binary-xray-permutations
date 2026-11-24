"""Lazy restricted machine: only states satisfying pred are ever built, so a thin family can be tested at a high bound.
accepts(pred, B) -> (True, #determinised states, largest set)  or  (False, shortest rejected legal prefix)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "universal"))
from maya import succ

def letters(B, sl, last):
    lo = -sl if last is None else max(-sl, last - 1)
    return [e for e in range(lo, B - sl + 1) if sl + e + (e * (e - 1) // 2 if e > 0 else 0) <= B]

def accepts(pred, B, limit=None):
    memo = {}
    def nxt(st, e):
        r = memo.get((st, e))
        if r is None: r = memo[st, e] = frozenset(t for t in succ(st, e) if pred(*t))
        return r
    S0 = frozenset([((), ())]); seen = {(S0, None): None}; todo = [(S0, None, 0)]; k = 0; big = 1
    while k < len(todo):
        S, last, sl = todo[k]; k += 1
        for e in letters(B, sl, last):
            R = frozenset().union(*[nxt(st, e) for st in S])
            if not R:
                w = [e]; key = (S, last)
                while seen[key] is not None: w.append(key[1]); key = seen[key]
                return False, w[::-1]
            if (R, e) not in seen:
                seen[R, e] = (S, last); todo.append((R, e, sl + e)); big = max(big, len(R))
                if limit and len(seen) > limit: return None, len(seen)
    return True, len(seen), big

conj = lambda p: tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
def first_fail(pred, Bmax=14, limit=400000):
    """smallest bound B <= Bmax at which pred rejects, with the rejected prefix"""
    for B in range(1, Bmax + 1):
        r = accepts(pred, B, limit)
        if r[0] is False: return B, r[1]
        if r[0] is None: return f"gave up at B = {B} ({r[1]} determinised states)"
    return f"accepts up to B = {Bmax}: {r[1]} determinised states, largest set {r[2]}"
