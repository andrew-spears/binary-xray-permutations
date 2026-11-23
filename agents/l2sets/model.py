"""Compare J(type) of blocks.py with P(run)(s) = step_run(All(s - sum(run))) (the run applied to the set of all states) and with the same from Sat of the central class.
  python3 model.py 2 S WIN MASK"""
import sys, runpy
from fx2 import *
g = runpy.run_path("blocks.py", run_name="__main__")
types, mask = g["types"], g["mask"]
def push(A, s, run):
    for e in run:
        if not 0 <= s + e <= S: return None, None
        A = step(A, s, e); s += e
    return A, s
runs = sorted({r for s, r in types if r}, key=lambda r: (r[-1:], len(r), r))
print("rows: run; columns: slack; entries |J| / |P| (P = run applied to ALL states);  * = J not inside P")
for r in runs:
    out = []
    for s in range(S - 1):
        if (s, r) not in types or s - sum(r) < 0: out.append("      ."); continue
        P, _ = push(full[s - sum(r)], s - sum(r), r); J = types[s, r]
        out.append(f"{cnt(J):3d}/{cnt(P):3d}" + ("*" if J & ~P else ""))
    print(f"{' '.join(map(str, r)):>8} " + " ".join(out))
