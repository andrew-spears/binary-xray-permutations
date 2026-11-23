"""Which valid words can be shortened by a rule from a list, and a greedy cover.
Reads the output of ./rules (lines 'u>v tested T fails F ...'); keeps the rules with F == 0 and T >= Tmin.
A rule u -> v applies to a word w on the prefix side if w = x v y and x u y is a legal word, and on the suffix side
if it applies on the prefix side to the mirror word (reversed, negated).
Usage: python3 cover.py rules_output.txt Bw N [Tmin] [P|PS]     (words: slacks <= Bw, length <= N)"""
import sys, re
from collections import defaultdict
def load(fn, tmin):
    rules = {}
    for line in open(fn):
        m = re.match(r'(.*)>(.*) tested (\d+) fails (\d+)', line)
        if m and int(m.group(4)) == 0 and int(m.group(3)) >= tmin:
            rules[(tuple(map(int, m.group(1).split())), tuple(map(int, m.group(2).split())))] = int(m.group(3))
    return rules
def legal(w, B):
    s = 0; last = None
    for e in w:
        if (last is None and e < 0) or (last is not None and e < last - 1): return False
        s += e; last = e
        if s < 0 or s > B: return False
    return s == 0
def words(B, N):
    out = []
    def gen(w, s, last):
        if w and s == 0 and any(w): out.append(tuple(w))
        if len(w) == N: return
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1):
            w.append(e); gen(w, s + e, e); w.pop()
    gen([], 0, None); return out
def apps(w, byv, Lmax, B):
    """rules applicable on the prefix side of w"""
    out = set()
    for i in range(len(w)):
        for L in range(1, Lmax + 1):
            if i + L > len(w): break
            for u in byv.get(w[i:i + L], ()):
                if legal(w[:i] + u + w[i + L:], B): out.add((u, w[i:i + L]))
    return out
if __name__ == "__main__":
    fn, Bw, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    tmin = int(sys.argv[4]) if len(sys.argv) > 4 else 1; sides = sys.argv[5] if len(sys.argv) > 5 else "PS"
    rules = load(fn, tmin); byv = defaultdict(list)
    for u, v in rules: byv[v].append(u)
    Lmax = max(len(v) for u, v in rules)
    ws = words(Bw, N); uses = defaultdict(set); stuck = []
    for wi, w in enumerate(ws):
        a = {("P",) + r for r in apps(w, byv, Lmax, Bw)}
        if "S" in sides: a |= {("S",) + r for r in apps(tuple(-e for e in reversed(w)), byv, Lmax, Bw)}
        if not a: stuck.append(w)
        for r in a: uses[r].add(wi)
    print(f"{len(rules)} rules; valid nonzero words (slack <= {Bw}, length <= {N}): {len(ws)}; stuck: {len(stuck)}", stuck[:6])
    left = set(range(len(ws))) - {wi for wi, w in enumerate(ws) if not any(wi in uses[r] for r in ())} if False else {wi for r in uses for wi in uses[r]}
    chosen = []
    while left:
        r = max(uses, key=lambda r: (len(uses[r] & left), rules[r[1:]])); chosen.append((r, len(uses[r] & left))); left -= uses[r]
    print(f"greedy cover: {len(chosen)} rules")
    for (side, u, v), c in chosen[:60]: print(f"   {side} {u} -> {v}   ({c} words; tested {rules[(u, v)]})")
