"""Sharply smaller families?  Forward run with a fixed rule on x, backward run with a fixed rule on zbar, some cut where
they meet (lam_A(x) = conj lam_B(zbar))."""
import sys
sys.path.insert(0, "../intervals")
from iv import words
from pm import succ
conj = lambda u: tuple(sum(1 for p in u if p > i) for i in range(u[0] if u else 0))
def run(w, pick):
    """states after each prefix (None once stuck)"""
    u = (); out = [u]
    for e in w:
        S = succ(u, e) if u is not None else []
        u = pick(S) if S else None
        out.append(u)
    return out
rules = {"min": lambda S: S[0], "max": lambda S: S[-1]}
for n in range(4, int(sys.argv[1]) + 1):
    W = words(n); res = {}
    for a in rules:
        for b in rules:
            bad = []
            for w in W:
                fw = run(w, rules[a]); bw = run(tuple(-e for e in reversed(w)), rules[b])
                if not any(fw[j] is not None and bw[n - j] is not None and fw[j] == conj(bw[n - j]) for j in range(n + 1)):
                    bad.append(w)
            res[(a, b)] = (len(bad), bad[:1])
    print(n, len(W), res)
