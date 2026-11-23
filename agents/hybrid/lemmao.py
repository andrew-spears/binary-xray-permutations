"""Lemma O: the states with an odd number of placements of the prefix 1^s lie in G(s).
  python3 lemmao.py S [D]    for s <= S: O(s) = {(lam|mu): C(s, |lam|) f^lam f^mu odd} is inside G(s)  (sizes printed);
                             for s <= D (default 9) the set O(s) against the parities of the path counts of 1^s; and f of a doubled diagram is even (|alpha| <= S // 4)."""
import sys
from math import comb, factorial
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
S = int(sys.argv[1]); D = int(sys.argv[2]) if len(sys.argv) > 2 else 9
sys.argv = [sys.argv[0], "0"]
import l1
from neg0 import in_G
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def f(lam):
    n = sum(lam); c = l1.conj(lam) if lam else (); h = 1
    for i, a in enumerate(lam):
        for j in range(a): h *= a - j + c[j] - i - 1
    return factorial(n) // h
odd = {n: [p for p in parts(n) if f(p) % 2] for n in range(S + 1)}
cur = {((), ()): 1}
for s in range(S + 1):
    O = [(lam, nu) for k in range(s + 1) if comb(s, k) % 2 for lam in odd[k] for nu in odd[s - k]]
    bad = [u for u in O if not in_G(u)]; msg = ""
    if s <= D:
        cnt = sum(1 for u, c in cur.items() if c % 2); ok = {u for u, c in cur.items() if c % 2} == set(O)
        msg = f"; path counts of 1^{s}: {len(cur)} states, {cnt} odd, the odd ones are O(s): {ok}"
        nxt = {}
        for u, c in cur.items():
            for k, v in l1.succs(u, 1): nxt[v] = nxt.get(v, 0) + c
        cur = nxt
    print(f"s {s}: |O(s)| = {len(O)}, not in G(s): {len(bad)}{msg}", flush=True)
dbl = lambda l: tuple(2 * a for a in l for _ in range(2))
print("f(doubled alpha) odd for", sum(f(dbl(al)) % 2 for a in range(1, S // 4 + 1) for al in parts(a)), "of the diagrams alpha with 1 <= |alpha| <=", S // 4)
