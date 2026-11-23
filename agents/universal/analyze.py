"""Tables for REPORT.md from the output of ./cores B.   Usage: python3 analyze.py cores_22.txt"""
import sys
from collections import Counter
from load import load, conj, cc, tr, nm
from maya import succ
D = load(sys.argv[1]); B = max(s for s, l in D)
U = {k: v[0] & v[1] for k, v in D.items()}

def E(p):                                 # even charge: even offsets lambda_i - i >= 0 minus free even offsets < 0
    N = len(p) + 2
    return sum(1 for i in range(1, N + 1) if ((p[i - 1] if i <= len(p) else 0) - i) % 2 == 0) - N // 2
def tri(s):
    a = 0
    while a * (a + 1) // 2 < s: a += 1
    return a
def below(st):                            # states with one box less
    out = set()
    for k in (0, 1):
        p = st[k]
        for i in range(len(p)):
            if i == len(p) - 1 or p[i] > p[i + 1]:
                q = tuple(x for x in p[:i] + (p[i] - 1,) + p[i + 1:] if x)
                out.add((q, st[1]) if k == 0 else (st[0], q))
    return out

print("1. sizes and duality   (LE(s, l) = states in F(x) for every prefix ending at slack s with last letter <= l)")
print("    s | CF0   LE0   CA0   U0 | CF1   LE1   CA1   U1 | CA(s,0) = conj LE(s,1), CA(s,1) = conj LE(s,0) | LE0 = CF0, LE1 = CF0 & CF1")
for s in range(1, B + 1):
    (F0, A0, L0), (F1, A1, L1) = D[(s, 0)], D[(s, 1)]
    print(f"   {s:2d} | {len(F0):5d} {len(L0):5d} {len(A0):5d} {len(U[(s,0)]):4d} | {len(F1):5d} {len(L1):5d} {len(A1):5d} {len(U[(s,1)]):4d} |",
          A0 == {cc(x) for x in L1}, A1 == {cc(x) for x in L0}, "|", L0 == F0, L1 == F0 & F1)

print("\n2. necessary conditions on universal states: box, total even charge = s mod 2, each charge in {-1, 0, 1}, lambda != mu")
for s in range(1, B + 1):
    a = tri(s); row = []
    for l in (0, 1):
        X = U[(s, l)]
        box = all(len(p) <= a + 1 - l and (not p or p[0] <= a + l) for x in X for p in x)
        row += [box, all(E(x[0]) + E(x[1]) == s % 2 for x in X), all(abs(E(p)) <= 1 for x in X for p in x), all(x[0] != x[1] for x in X)]
    viol = sum(1 for x in D[(s, 1)][0] if any(abs(E(p)) > 1 for p in x))
    print(f"   {s:2d} a={a} | l=0:", *row[:4], "| l=1:", *row[4:], f"| states of CF(s,1) with a charge outside -1..1: {viol}")

print("\n3. relations.  conj U0 inside U1 | U1 = conj U0 | U0 with a 0-predecessor in U1(s) | U1 with a 1-predecessor in U0(s-1) | U0 with a box-predecessor in U0(s-1)")
for s in range(1, B + 1):
    U0, U1, P = U[(s, 0)], U[(s, 1)], U.get((s - 1, 0), {((), ())} if s == 1 else set())      # slack 0: the empty state
    c = {cc(x) for x in U0}
    p0 = sum(1 for x in U0 if any(x in succ(b, 0) for b in U1))
    p1 = sum(1 for x in U1 if any(x in succ(b, 1) for b in P))
    ch = sum(1 for x in U0 if below(x) & P)
    print(f"   {s:2d} | {c <= U1} {c == U1} | {p0}/{len(U0)} | {p1}/{len(U1)} | {ch}/{len(U0)}")

col = lambda p: all(x == 1 for x in p)
rect = lambda p: len(set(p)) <= 1
hook = lambda p: all(x == 1 for x in p[1:])
stair = lambda p: bool(p) and p[-1] == 1 and all(p[i] - p[i + 1] == 1 for i in range(len(p) - 1))
classes = [("lambda empty", lambda x: not x[0]), ("|lambda| <= 1", lambda x: sum(x[0]) <= 1),
           ("lambda = 1^j, j >= 1 (one row hole)", lambda x: bool(x[0]) and col(x[0])), ("lambda = (j), j >= 1", lambda x: len(x[0]) == 1),
           ("lambda a rectangle", lambda x: rect(x[0])), ("lambda a hook", lambda x: hook(x[0])), ("mu a rectangle", lambda x: rect(x[1])),
           ("both rectangles", lambda x: rect(x[0]) and rect(x[1])), ("both hooks", lambda x: hook(x[0]) and hook(x[1])),
           ("mu a staircase", lambda x: stair(x[1])), ("mu with <= 2 part sizes", lambda x: len(set(x[1])) <= 2),
           ("lambda = 1^j and mu with <= 2 part sizes", lambda x: col(x[0]) and len(set(x[1])) <= 2),
           ("lambda = mu", lambda x: x[0] == x[1]), ("mu = conj lambda", lambda x: x[1] == conj(x[0])),
           ("lambda, mu both self-conjugate", lambda x: cc(x) == x)]
print("\n4. shape classes (up to transpose): slacks s <= %d with NO universal state of the class" % B)
for name, f in classes:
    for l in (0, 1):
        print(f"   {name:42s} l={l}: ", [s for s in range(1, B + 1) if not any(f(x) or f(tr(x)) for x in U[(s, l)])])

print("\n5. universal states at (s, 0) with no row hole, and with one row hole (lambda = 1^j: values of j)")
for s in range(1, B + 1):
    X = U[(s, 0)]
    print(f"   {s:2d} | {' '.join(sorted(nm(x) for x in X if not x[0])) or 'none'} | j in",
          sorted({len(x[0]) for x in X if x[0] and col(x[0])}), "| fewest part sizes (lambda + mu):", min(len(set(x[0])) + len(set(x[1])) for x in X))
