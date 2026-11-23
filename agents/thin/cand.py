"""Step 2: closed-form candidate families, each tested by the restricted subset construction.
Prints the smallest slack bound at which the family rejects a legal prefix (and that prefix).  Usage: python3 cand.py [Bmax] [substring of the family name]"""
import sys
from lazy import *
Bmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
rows = len; cols = lambda p: p[0] if p else 0
hook = lambda p: len(p) < 2 or p[1] == 1
rect = lambda p: len(set(p)) <= 1
two = lambda p: len(set(p)) <= 2
sub = lambda p, q: len(p) <= len(q) and all(a <= b for a, b in zip(p, q))
stair = lambda p: all(x <= len(p) - i for i, x in enumerate(p))       # inside the staircase (len, len-1, ..., 1)
def core2(p):
    """number of boxes of the 2-core: d(2d - 1), 2d = #beads on even positions - #beads on odd (even number of beads)"""
    n = len(p) + (len(p) & 1); b = [x + n - 1 - i for i, x in enumerate(p)] + list(range(n - len(p) - 1, -1, -1))
    d = sum(1 if x % 2 == 0 else -1 for x in b) // 2
    return d * (2 * d - 1)
durfee = lambda p: sum(1 for i, x in enumerate(p) if x > i)
C = {}
for k in (1, 2, 3):
    C[f"lambda and mu have <= {k} rows"] = lambda l, m, k=k: rows(l) <= k and rows(m) <= k
    C[f"lambda and mu have <= {k} columns"] = lambda l, m, k=k: cols(l) <= k and cols(m) <= k
    C[f"each of lambda, mu has <= {k} rows or <= {k} columns"] = lambda l, m, k=k: min(rows(l), cols(l)) <= k and min(rows(m), cols(m)) <= k
    C[f"lambda has <= {k} rows (mu free)"] = lambda l, m, k=k: rows(l) <= k
    C[f"lambda has <= {k} columns (mu free)"] = lambda l, m, k=k: cols(l) <= k
    C[f"lambda or mu has <= {k} rows"] = lambda l, m, k=k: rows(l) <= k or rows(m) <= k
    C[f"lambda or mu has <= {k} columns"] = lambda l, m, k=k: cols(l) <= k or cols(m) <= k
    C[f"Durfee squares <= {k}"] = lambda l, m, k=k: durfee(l) <= k and durfee(m) <= k
    C[f"| |lambda| - |mu| | <= {k}"] = lambda l, m, k=k: abs(sum(l) - sum(m)) <= k
C["lambda empty or mu empty"] = lambda l, m: not l or not m
C["both hooks"] = lambda l, m: hook(l) and hook(m)
C["lambda a hook (mu free)"] = lambda l, m: hook(l)
C["lambda or mu a hook"] = lambda l, m: hook(l) or hook(m)
C["both rectangles"] = lambda l, m: rect(l) and rect(m)
C["lambda a rectangle (mu free)"] = lambda l, m: rect(l)
C["lambda or mu a rectangle"] = lambda l, m: rect(l) or rect(m)
C["both with <= 2 part sizes"] = lambda l, m: two(l) and two(m)
C["lambda a rectangle and mu <= 2 part sizes, or swapped"] = lambda l, m: (rect(l) and two(m)) or (rect(m) and two(l))
C["lambda inside mu or mu inside lambda"] = lambda l, m: sub(l, m) or sub(m, l)
C["lambda inside mu' or mu inside lambda'"] = lambda l, m: sub(l, conj(m)) or sub(m, conj(l))
C["lambda = mu'  (|diff| <= 1 box)"] = lambda l, m: (sub(l, conj(m)) or sub(conj(m), l)) and abs(sum(l) - sum(m)) <= 1
C["lambda = mu  (|diff| <= 1 box)"] = lambda l, m: (sub(l, m) or sub(m, l)) and abs(sum(l) - sum(m)) <= 1
C["both inside their staircase (lambda_i <= rows - i + 1)"] = lambda l, m: stair(l) and stair(m)
C["both or their conjugates inside a staircase"] = lambda l, m: (stair(l) or stair(conj(l))) and (stair(m) or stair(conj(m)))
C["2-cores: both empty / one empty, one a box (core2 of weights)"] = lambda l, m: core2(l) + core2(m) == (sum(l) + sum(m)) % 2
C["2-cores have <= 1 box each"] = lambda l, m: core2(l) <= 1 and core2(m) <= 1
C["distinct parts in lambda and mu"] = lambda l, m: len(set(l)) == len(l) and len(set(m)) == len(m)
C["distinct parts or conjugate has distinct parts"] = lambda l, m: (len(set(l)) == len(l) or len(set(conj(l))) == cols(l)) and (len(set(m)) == len(m) or len(set(conj(m))) == cols(m))
if __name__ == "__main__":
    for k, f in C.items():
        if len(sys.argv) > 2 and sys.argv[2] not in k: continue
        r = first_fail(f, Bmax)
        print(f"{k:58s}", (f"rejects at B = {r[0]}: {' '.join(map(str, r[1]))}" if isinstance(r, tuple) else r), flush=True)
