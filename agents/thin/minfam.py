"""Exact smallest accepting family for slack bound B (N(B)), by integer programming with lazy constraints.
Variables t_st (state kept) and, for every prefix x in a growing trie, r_{x,st} in [0,1] with
  r_{x,st} <= t_st,   r_{xe,st'} <= sum of r_{x,st} over st with st' in succ(st, e),   sum_st r_{x,st} >= 1,
which say exactly "some walk along x stays in T".  Each round solves the programme, runs the subset construction
restricted to the optimum T, and adds the rejected prefixes.  Every round's optimum is a lower bound for N(B); the
last one is attained.  Any family that accepts all valid words (no slack bound) has >= N(B) states of slack <= B.
Usage: python3 minfam.py B [per-round]"""
import sys, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
from thin import *
B = int(sys.argv[1]); per = int(sys.argv[2]) if len(sys.argv) > 2 else 40
m = M(B); n = len(m.states); t0 = time.time()
bits = lambda S: [i for i in range(n) if S >> i & 1]
trie = {(): (1, None, 0)}                  # prefix -> (full F(x), last letter, slack)
var = {((), 0): n}; nv = n + 1             # (prefix, state) -> column
rows = []                                  # (list of (col, coef), lower, upper)
rows.append(([(n, 1)], 1, 1)); rows.append(([(n, 1), (0, -1)], -np.inf, 0))
def add_prefix(x):
    global nv
    for j in range(1, len(x) + 1):
        y = x[:j]
        if y in trie: continue
        S, last, sl = trie[y[:-1]]; e = y[-1]; R = m.step(S, e, m.full); trie[y] = (R, e, sl + e)
        pre = bits(S); cols = []
        for st in bits(R):
            var[y, st] = nv; nv += 1; cols.append(var[y, st])
            rows.append(([(var[y, st], 1), (st, -1)], -np.inf, 0))
            rows.append(([(var[y, st], 1)] + [(var[y[:-1], p], -1) for p in pre if m.nxt[p, e] >> st & 1], -np.inf, 0))
        rows.append(([(c, 1) for c in cols], 1, np.inf))
def rejected(T, cap):
    """rejected prefixes (shortest first) of the machine restricted to T"""
    out = []; seen = {(1, None)}; todo = [((), 1, None, 0)]; k = 0
    while k < len(todo) and len(out) < cap:
        x, S, last, sl = todo[k]; k += 1
        for e in m.letters(sl, last):
            R = m.step(S, e, T)
            if not R: out.append(x + (e,))
            elif (R, e) not in seen: seen.add((R, e)); todo.append((x + (e,), R, e, sl + e))
    return out
rnd = 0
while True:
    rnd += 1
    I = [i for i, (c, lo, hi) in enumerate(rows) for _ in c]; J = [c for cs, lo, hi in rows for c, v in cs]; V = [v for cs, lo, hi in rows for c, v in cs]
    A = coo_matrix((V, (I, J)), shape=(len(rows), nv)).tocsr()
    cost = np.zeros(nv); cost[:n] = 1; integ = np.zeros(nv); integ[:n] = 1
    res = milp(cost, constraints=LinearConstraint(A, [r[1] for r in rows], [r[2] for r in rows]), integrality=integ, bounds=Bounds(0, 1))
    T = sum(1 << i for i in range(n) if res.x[i] > 0.5) | 1
    bad = rejected(T, per)
    print(f"round {rnd}: {nv} variables, optimum {bin(T).count('1')}, {len(bad)} rejected prefixes, {time.time() - t0:.0f} s", flush=True)
    if not bad: break
    for x in bad: add_prefix(x)
assert m.accepts(T) is True
per_s = [sum(1 for i in bits(T) if m.slack[i] == s) for s in range(B + 1)]
print(f"N({B}) = {bin(T).count('1')} of {n};  per slack {per_s} of {[sum(1 for i in range(n) if m.slack[i] == s) for s in range(B + 1)]}")
print(" ".join(m.name(i) for i in bits(T)))
