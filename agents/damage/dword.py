"""Theorem D against the exact reachable set along single words: after every letter, |states|, |F|, |A| (A = non-violators of Theorem D), |A - F| and the states of A - F (up to 12).
python3 dword.py "1 1 1 1 1 3 2 1 0 0" ["another word" ...]"""
import sys
from oh import *
from landau_lib import viol, excess
for word in sys.argv[1:]:
    w = tuple(map(int, word.split())); setup(sum(max(e, 0) for e in w) + 2); F = frozenset([((), ())]); s = 0
    print("word", word)
    for i, e in enumerate(w, 1):
        F = step(F, e); s += e
        if s < 6: continue
        A = [u for u in states(s) if not viol(u, w[:i])]; d = sorted(nm(u) for u in A if u not in F); assert all(u in set(A) for u in F)
        print(f"  after letter {i} = {e}: slack {s}, y = {excess(w[:i])}, states {len(states(s))}, F {len(F)}, A {len(A)}, A - F {len(d)}", " ".join(d[:12]) if e <= 0 else "")
