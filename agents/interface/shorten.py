"""Shortening rules for ALL words with slack <= B (not only letters -1, 0, +1).
A rule u -> v (|u| < |v| <= Lmax, same letter sum) is VALID at bound B if F(xu) is a subset of F(xv) for every legal
prefix x (slacks <= B) after which both u and v can be read legally with slacks <= B.  Then, for a word x v y with slacks
<= B such that x u y is again a legal word, 'x u y solvable' implies 'x v y solvable'.
The script (1) finds all valid rules, (2) checks which valid words of length <= N with slacks <= B can be shortened by
some rule (to a legal word), (3) prints a small set of rules that does all of them (greedy cover).
If every nonzero word can be shortened, slack <= B is proved for length <= N by induction on the length (the all-zero
word is the anti-diagonal), from the valid rules alone.
Usage: python3 shorten.py B Lmax N"""
import sys
from collections import defaultdict
from rewrite import machine
def main(B, Lmax, N):
    step, start = machine(B)
    s0 = (frozenset([start]), 0, None); seen = {s0}; todo = [s0]
    while todo:
        S, s, last = todo.pop()
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1):
            x = (step(S, e), s + e, e)
            if x not in seen: seen.add(x); todo.append(x)
    tested = defaultdict(int); failed = set()
    for S, s, last in seen:
        ext = {}                                   # string -> F
        def rec(w, S2, s2, l2):
            ext[w] = S2
            if len(w) == Lmax: return
            for e in range(0 if l2 is None else max(-s2, l2 - 1), B - s2 + 1): rec(w + (e,), step(S2, e), s2 + e, e)
        rec((), S, s, last)
        bysum = defaultdict(list)
        for w in ext: bysum[sum(w)].append(w)
        for ws in bysum.values():
            for u in ws:
                for v in ws:
                    if len(u) < len(v):
                        tested[(u, v)] += 1
                        if not ext[u] <= ext[v]: failed.add((u, v))
    rules = {r for r in tested if r not in failed}
    print(f"B = {B}: {len(seen)} situations; {len(rules)} valid rules of {len(tested)} candidates (|v| <= {Lmax})", flush=True)
    byv = defaultdict(list)
    for u, v in rules: byv[v].append(u)
    def legal(w):
        s = 0; last = None
        for e in w:
            if (last is None and e < 0) or (last is not None and e < last - 1): return False
            s += e; last = e
            if s < 0 or s > B: return False
        return s == 0
    words = []
    def gen(w, s, last):
        if w and s == 0: words.append(tuple(w))
        if len(w) == N: return
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1):
            w.append(e); gen(w, s + e, e); w.pop()
    gen([], 0, None)
    words = [w for w in words if any(w)]
    uses = defaultdict(set); stuck = []
    for wi, w in enumerate(words):
        ok = False
        for i in range(len(w)):
            for L in range(1, Lmax + 1):
                v = w[i:i + L]
                if len(v) < L: break
                for u in byv.get(v, ()):
                    if legal(w[:i] + u + w[i + L:]): uses[(u, v)].add(wi); ok = True
        if not ok: stuck.append(w)
    print(f"valid nonzero words of length <= {N}: {len(words)}; cannot be shortened: {len(stuck)}", stuck[:8])
    stuckset = set(stuck)
    left = {wi for wi, w in enumerate(words) if w not in stuckset}
    chosen = []
    while left:
        r = max(uses, key=lambda r: len(uses[r] & left)); chosen.append((r, len(uses[r] & left))); left -= uses[r]
    print(f"greedy cover: {len(chosen)} rules")
    for (u, v), c in chosen[:40]: print(f"   {u} -> {v}   ({c} words, tested in {tested[(u, v)]} situations)")
if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
