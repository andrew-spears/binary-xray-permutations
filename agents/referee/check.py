"""Referee checks, written independently of agents/l1sets/l1.py: everything is computed from the forward machine
../universal/maya.py on all pairs of partitions (lambda | mu) with slack <= S + 1, and from bead sets in a window.
Each line printed is one statement of agents/l1sets/REPORT.md or agents/l2sets/REPORT.md; a failed statement prints FAIL
with the smallest counterexample found.          python3 check.py [S]      (S = 17: about 3 minutes; S = 13: 20 seconds)"""
import sys, itertools
sys.path.insert(0, "../universal")
from maya import succ
S = int(sys.argv[1]) if len(sys.argv) > 1 else 17
TOP = S + 1; W = 2 * TOP + 12                                   # window [-W, W) for bead sets, W even
def parts(n, m=None):
    if n == 0: yield (); return
    for k in range(min(n, m or n), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
P = [list(parts(n)) for n in range(TOP + 1)]
St = [[(l, m) for i in range(s + 1) for l in P[i] for m in P[s - i]] for s in range(TOP + 1)]
conj = lambda p: tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
beads = lambda p: frozenset((p[i - 1] if i <= len(p) else 0) - i for i in range(1, W + 1))
def c0(p):
    b = beads(p); return sum(1 for k in range(0, W, 2) if k in b) - sum(1 for k in range(-W, 0, 2) if k not in b)
MB = lambda u: (beads(u[0]), beads(conj(u[1])))                  # (M, B) = (M(lambda), M(mu'))
cls = lambda u: c0(u[0]) + c0(conj(u[1]))
slack = lambda u: sum(u[0]) + sum(u[1])
central = lambda u: cls(u) == slack(u) % 2
SC = lambda u: u[0] == conj(u[1])
def E0(u):
    M, B = MB(u)
    if any((k ^ 1) not in X for X in (M, B) for k in X): return False
    B2 = {b - 2 for b in B if b - 2 >= -W} | {-W, -W + 1}
    return B2 <= M and len(M - B2) == 2 and (min(M - B2) ^ 1) == max(M - B2)
LET = range(-5, 3)
pred = {e: {} for e in LET}                                      # pred[e][u] = list of (k, t)
for s in range(TOP + 1):
    for t in St[s]:
        Mt = beads(t[0])
        for e in LET:
            if 0 <= s + e <= TOP:
                for u in succ(t, e):
                    k = min(beads(u[0]) - {b - 1 for b in Mt})   # M_u = (M_t - 1) u {k}
                    pred[e].setdefault(u, []).append((k, t))
P_ = lambda u, e: pred[e].get(u, [])
A = {s: {u for u in St[s] if central(u) and all(SC(t) or E0(t) for k, t in P_(u, 1))} for s in range(1, TOP + 1, 2)}
isA = lambda u: slack(u) >= 5 and slack(u) % 2 == 1 and u in A[slack(u)]
def T(u):
    s = slack(u)
    return s > 0 and ((s % 4 == 0 and (SC(u) or E0(u))) or isA(u))
G = lambda u: central(u) and not T(u)
U = lambda u: slack(u) > 0 and slack(u) + 1 <= TOP and all(isA(t) for k, t in P_(u, -1))
Gm = lambda u: central(u) and not U(u)
nm = lambda u: "|".join("".join(map(str, p)) or "-" for p in u)
def report(label, bad):
    print(("ok    " if not bad else "FAIL  ") + label + ("" if not bad else "   first: " + str(bad[0]) + "  kinds: " + str(sorted({b[0] for b in bad}))), flush=True)
allst = [u for s in range(S + 1) for u in St[s]]

# ---- l1sets section 1 and Lemma 1 / l2sets Lemma G (i), (ii), (iv): predecessor formula, counts, classes
bad = []
for u in allst:
    M, B = MB(u); a, b = c0(u[0]), c0(conj(u[1])); c = a + b; s = slack(u)
    for e in LET:
        if not 0 <= s - e <= TOP: continue
        pr = P_(u, e); ks = sorted(k for k, t in pr)
        if ks != sorted(k for k in M if k > -W + 8 and k + 1 - e not in B): bad.append(("formula", nm(u), e))
        ev = [t for k, t in pr if k % 2 == 0]; od = [t for k, t in pr if k % 2]
        if e % 2 == 0:
            f = e // 2
            if len(ev) < c - f or len(od) < 1 - c - f or any(cls(t) != 2 - c for t in ev) or any(cls(t) != -c for t in od): bad.append(("G(i)", nm(u), e))
        else:
            f = (e - 1) // 2
            if len(ev) < a - b - f or len(od) < b - a - f or any(cls(t) != 1 - c for k, t in pr): bad.append(("G(ii)", nm(u), e))
        if e == -1 and len(pr) < 2: bad.append(("L1 e=-1", nm(u)))
        if e == 1 and (len(pr) == 0) != SC(u): bad.append(("L1 e=1", nm(u)))
        if sum(1 for k, t in pr if E0(t)) > 1: bad.append(("G(iii)", nm(u), e))
        if (not pr) != all(k + 1 - e in B for k in M if k > -W + 8): bad.append(("G(iv)", nm(u), e))
report(f"predecessor formula, Lemma 1, Lemma G (i)-(iv): all {len(allst)} states of slack <= {S}, letters -5..2", bad)

# ---- Lemma 2, Lemma 3
bad = []
for u in allst:
    s = slack(u)
    if s + 1 <= TOP and any(SC(t) for k, t in P_(u, -1)): bad.append(("2a", nm(u)))
    if s >= 1 and sum(1 for k, t in P_(u, 1) if SC(t) or E0(t)) > 1: bad.append(("2b", nm(u)))
    if sum(1 for k, t in P_(u, 0) if k % 2 and (SC(t) or E0(t))) > 1: bad.append(("2c", nm(u)))
    od = [t for k, t in P_(u, 0) if k % 2]
    if central(u) and cls(u) == 0 and len(od) == 1:
        if SC(od[0]) and not E0(u): bad.append(("3a", nm(u)))
        if E0(od[0]) and not SC(u) and s > 0: bad.append(("3b", nm(u)))
    if E0(u) and not (len(od) == 1 and SC(od[0])): bad.append(("3 converse", nm(u)))
report(f"Lemma 2 (a), (b), (c), Lemma 3 (a), (b), converse: slack <= {S}", bad)
print("      note: -|- is in SC and satisfies the definition of E0:", SC(((), ())) and E0(((), ())),
      "; other states in both, slack <=", S, ":", [nm(u) for u in allst if slack(u) and SC(u) and E0(u)])

# ---- Lemma 4: the definitional A
print("      central states of odd slack with all 1-predecessors in SC u E0 (definition of A), by slack:",
      {s: sorted(nm(u) for u in A[s]) for s in A if A[s]})
bad = [("4", nm(u)) for s in A if s >= 5 for u in A[s] if not (len(P_(u, 1)) == 1 and E0(P_(u, 1)[0][1]) and round(((s - 1) / 4) ** .5) ** 2 * 4 + 1 == s)]
bad += [("4 count", s) for s in A if s >= 5 and len(A[s]) not in (0, 4)]
report(f"Lemma 4: at odd slack 3..{TOP} such states exist only for slack 4m^2 + 1, 4 of them, one predecessor, in E0", bad)

# ---- Lemma 5 (needs successors: slack of a + 1 <= TOP)
bad = []
for s in A:
    if s < 5 or s + 1 > TOP: continue
    m = round(((s - 1) / 4) ** .5)
    for a in A[s]:
        sm = succ(a, -1)
        if len(sm) != 1 or not all(E0(v) for v in sm) or not all(isA(t) for v in sm for k, t in P_(v, -1)): bad.append(("5a", nm(a)))
        for v in succ(a, 1):
            if len(P_(v, 1)) < 2 * m - 2: bad.append(("5b", nm(a)))
            if all(isA(t) for k, t in P_(v, 1)): bad.append(("finite case e=1", nm(v)))
        for v in succ(a, 0):
            if not central(v): continue
            cp = [t for k, t in P_(v, 0) if central(t)]
            if len(cp) < m - 1: bad.append(("5c", nm(a)))
            if not isA(v) and all(isA(t) for t in cp): bad.append(("finite case e=0", nm(v)))
report(f"Lemma 5 (a), (b), (c) and the two finite sub-cases, for A(s), s + 1 <= {TOP}", bad)

# ---- the L1 Theorem, Theorem 0 (a), (b), (c), Lemma H
bad = []
for u in allst:
    s = slack(u)
    if G(u):
        for e in (-1, 0, 1):
            if s - e >= 0 and not any(G(t) for k, t in P_(u, e)): bad.append(("L1 theorem", nm(u), e))
    if central(u) and s + 1 <= S:
        if Gm(u) != any(G(t) for k, t in P_(u, -1)): bad.append(("0(b)", nm(u)))
        for k in range(2, 6):
            if s + k <= S and not any(Gm(t) for j, t in P_(u, -k)): bad.append(("0(c)", nm(u), -k))
    if G(u) and not Gm(u): bad.append(("G inside G-", nm(u)))
report(f"L1 Theorem (e = -1, 0, 1), Theorem 0 (b) with equality, (c) for k = 2..5, G inside G-: slack <= {S}", bad)
print("      slacks where G-(s) != G(s):", [(s, sum(1 for u in St[s] if Gm(u) and not G(u))) for s in range(S + 1) if any(Gm(u) and not G(u) for u in St[s])],
      " (slack, number of states in G- minus G)")
Us = {s: [u for u in St[s] if central(u) and U(u)] for s in range(1, S + 1)}
report("U(s) is empty except U(4m^2) = two states, both in E0: " + str({s: sorted(map(nm, v)) for s, v in Us.items() if v}),
       [("U", s) for s, v in Us.items() if (len(v) != (2 if round((s / 4) ** .5) ** 2 * 4 == s else 0)) or not all(E0(u) for u in v)])
fails = sorted({(slack(u) + k, k) for u in allst if G(u) for k in range(2, 6) if slack(u) + k <= S and not any(G(t) for j, t in P_(u, -k))})
print("      remark of l2sets section 2 (tested only): (source slack s, k) with G(s - k) not inside step_-k(G(s)):", fails)
bad = [("H", s) for s in range(1, S + 1) if not (G(((s,), ())) and G(((1,) * s, ())))]
report(f"Lemma H: (s|-) and (1^s|-) are in G(s), 1 <= s <= {S}", bad)

# ---- A(y) = conj F(-reverse(y)), abstract machine, all cuts of all valid words of length <= N
N = 8; bad = []; cuts = 0; cj = lambda u: (conj(u[0]), conj(u[1]))
def words(n, pre=(), s=0):
    if len(pre) == n:
        if s == 0: yield pre
        return
    for e in range((pre[-1] - 1) if pre else 0, n):
        if s + e >= 0: yield from words(n, pre + (e,), s + e)
def fwd(x):
    F = {((), ())}
    for e in x: F = {v for t in F for v in succ(t, e)}
    return F
import functools
fwd = functools.lru_cache(maxsize=None)(fwd)
@functools.lru_cache(maxsize=None)
def acc(y):                                                      # states from which y leads to -|-
    if not y: return frozenset([((), ())])
    nxt = acc(y[1:]); s = -sum(y)
    return frozenset(u for u in ALL(s) if any(v in nxt for v in succ(u, y[0])))
@functools.lru_cache(maxsize=None)
def ALL(s): return tuple((l, m) for i in range(s + 1) for l in parts(i) for m in parts(s - i))
for n in range(1, N + 1):
    for w in words(n):
        for i in range(n + 1):
            x, y = w[:i], w[i:]; cuts += 1
            if acc(y) != frozenset(cj(u) for u in fwd(tuple(-e for e in reversed(y)))): bad.append(("A(y)", w, i))
report(f"A(y) = conj F(-reverse(y)) with conj = conjugate both partitions: all {cuts} cuts of all valid words of length <= {N}", bad)
print("      conj(1^5|-) =", nm(cj(((1,) * 5, ()))))
