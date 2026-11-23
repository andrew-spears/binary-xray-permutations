"""Sizes of the restricted reachable sets along one word, for T(1,2), T(1,3), T(2,2) and the full machine; then the
alive states (those from which the rest of the word can be finished inside the family) at each step for T(2,2)/T(1,3).
Usage: python3 trace.py word..."""
import sys
from lazy import *
cn = lambda p: len(set(p))
w = tuple(map(int, sys.argv[1:])) or (4, 3, 5, 4, 3, 2, 1, 0, 0, -1, -2, -3, -4, -5, -3, -4)
def inT(t, a, b): return (cn(t[0]) <= a and cn(t[1]) <= b) or (cn(t[0]) <= b and cn(t[1]) <= a)
def sets(a, b):
    S = [{((), ())}]
    for e in w: S.append({t for st in S[-1] for t in succ(st, e) if inT(t, a, b)})
    return S
def alive(S, a, b):
    A = [None] * len(S); A[-1] = S[-1] & {((), ())}
    for k in range(len(w) - 1, -1, -1): A[k] = {st for st in S[k] if any(t in A[k + 1] for t in succ(st, w[k]))}
    return A
fams = [(1, 2), (1, 3), (2, 2), (99, 99)]
S = {f: sets(*f) for f in fams}; A = {f: alive(S[f], *f) for f in fams}
print("letter  " + "  ".join(f"T{f} reach/alive".ljust(22) for f in fams))
for k, e in enumerate(w): print(f"{e:4d}    " + "  ".join(f"{len(S[f][k + 1])}/{len(A[f][k + 1])}".ljust(22) for f in fams))
for f in [(1, 3), (2, 2)]:
    print(f"alive states of T{f} needing more than T(1,2):")
    for k in range(len(w)):
        x = sorted(st for st in A[f][k + 1] if not inT(st, 1, 2))
        if x: print("  after", " ".join(map(str, w[:k + 1])), ":", len(x), "of", len(A[f][k + 1]), "e.g.", x[:3])
