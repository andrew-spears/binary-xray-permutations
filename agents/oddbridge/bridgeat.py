"""BRIDGE, BRIDGE-ODD and LINE on one middle.  python3 bridgeat.py s1 "m"
BRIDGE: step_m(G(s1)) meets conj G(s2).  BRIDGE-ODD: step_m(Odd(1^s1)) meets Odd'((-1)^s2).  LINE: line state to line state."""
import sys
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
import l1, neg0
s1 = int(sys.argv[1]); m = tuple(map(int, sys.argv[2].split())); s2 = s1 + sum(m)
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
E = ((), ())
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def G(s): return frozenset(u for k in range(s + 1) for lam in parts(k) for nu in parts(s - k) for u in [(lam, nu)] if neg0.in_G(u))
def odd(s, step, e):
    P = {E: 1}
    for _ in range(s):
        Q = {}
        for u, c in P.items():
            for k, v in step(u, e): Q[v] = Q.get(v, 0) ^ c
        P = {u: 1 for u, c in Q.items() if c}
    return frozenset(P)
def line(s): return [E] if s == 0 else [((1,), ()), ((), (1,))] if s == 1 else [((s,), ()), ((), (s,)), ((1,) * s, ()), ((), (1,) * s)]
def push(F):
    for e in m: F = frozenset(v for u in F for k, v in l1.succs(u, e))
    return F
cG = frozenset((l1.conj(u[0]), l1.conj(u[1])) for u in G(s2))
print("s1 =", s1, " m =", *m, " s2 =", s2, " n =", s1 + len(m) + s2)
I = push(G(s1)) & cG
print("  BRIDGE: |step_m(G(s1)) meet conj G(s2)| =", len(I), " e.g.", [l1.name(u) for u in sorted(I)[:4]])
print("  BRIDGE-ODD: joined odd states at the end:", len(push(odd(s1, l1.succs, 1)) & odd(s2, l1.preds, -1)))
print("  LINE: line states reached at the end:", len(push(frozenset(line(s1))) & frozenset(line(s2))))
print("  full padded word 1^s1 m (-1)^s2 solvable:", E in (lambda F: [F := frozenset(v for u in F for k, v in l1.succs(u, e)) for e in (1,) * s1 + m + (-1,) * s2][-1])(frozenset([E])))
