"""Restricted interface machine.  States (lam|mu) with slack |lam| + |mu| <= B, step = succ of ../universal/maya.py.
A family T (a set of states, always containing the empty state) ACCEPTS if for every valid word with slacks <= B
(e_{k+1} >= e_k - 1, partial sums in [0, B], total 0) some walk stays in T.  Checked by the subset construction on
(set of T-states, last letter); a prefix is legal if it extends to a valid word with slacks <= B, i.e.
slack + (e-1) + (e-2) + ... + 1 <= B for the last letter e."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "universal"))
from maya import succ
from functools import lru_cache

@lru_cache(maxsize=None)
def parts(n, m=None):
    if m is None: m = n
    if n == 0: return ((),)
    return tuple((k,) + p for k in range(min(n, m), 0, -1) for p in parts(n - k, k))

class M:
    def __init__(s, B):
        s.B = B
        s.states = [(l, m) for t in range(B + 1) for a in range(t + 1) for l in parts(a) for m in parts(t - a)]
        s.idx = {st: i for i, st in enumerate(s.states)}
        s.slack = [sum(l) + sum(m) for l, m in s.states]
        s.nxt = {}          # (i, e) -> bitmask of successors
        for i, st in enumerate(s.states):
            for e in range(-s.slack[i], B - s.slack[i] + 1):
                m = 0
                for t in succ(st, e): m |= 1 << s.idx[t]
                s.nxt[i, e] = m
        s.full = (1 << len(s.states)) - 1
    def letters(s, sl, last):
        """legal next letters after a prefix at slack sl with last letter last (None at the start)"""
        lo = -sl if last is None else max(-sl, last - 1)
        return [e for e in range(lo, s.B - sl + 1) if sl + e + (e * (e - 1) // 2 if e > 0 else 0) <= s.B]
    def step(s, S, e, T):
        out = 0
        while S:
            b = S & -S; S ^= b; out |= s.nxt[b.bit_length() - 1, e]
        return out & T
    def mask(s, pred): return sum(1 << i for i, (l, m) in enumerate(s.states) if pred(l, m)) | 1
    def accepts(s, T, want_word=False, stats=False):
        """True, or the first (shortest) legal prefix after which no walk in T survives"""
        seen = {(1, None): None}; todo = [(1, None, 0)]; k = 0; big = 0
        while k < len(todo):
            S, last, sl = todo[k]; k += 1
            for e in s.letters(sl, last):
                R = s.step(S, e, T)
                if not R:
                    if not want_word: return False
                    w = [e]; key = (S, last)
                    while seen[key] is not None: w.append(key[1]); key = seen[key]
                    return w[::-1]
                if (R, e) not in seen:
                    seen[R, e] = (S, last); todo.append((R, e, sl + e)); big = max(big, bin(R).count("1"))
        return (True, len(seen), big) if stats else True
    def name(s, i):
        l, m = s.states[i]; f = lambda p: "".join(map(str, p)) if max(p, default=0) < 10 else ".".join(map(str, p))
        return (f(l) or "-") + "|" + (f(m) or "-")

conj = lambda p: tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
if __name__ == "__main__":
    B = int(sys.argv[1]); m = M(B)
    print(B, len(m.states), "states;  full machine:", m.accepts(m.full, stats=True))
