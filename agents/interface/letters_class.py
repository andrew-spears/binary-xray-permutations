"""Which simple classes of interface states carry an inductive family for |e| <= c with summary (sigma, last letter)?
Usage: python3 letters_class.py c B [L]"""
import sys
from invariant import analyse
c = int(sys.argv[1]); B = int(sys.argv[2]); L = int(sys.argv[3]) if len(sys.argv) > 3 else 1
def part(mask):
    xs = sorted((j - B + 1 for j in range(2 * B) if mask >> j & 1), reverse=True)
    return tuple(x + i for i, x in enumerate(xs) if x + i > 0)
durfee = lambda p: sum(1 for i, x in enumerate(p) if x >= i + 1)
hook = lambda p: durfee(p) <= 1
rect = lambda p: len(set(p)) <= 1
rowcol = lambda p: len(p) <= 1 or p[0] == 1
classes = {
 "hook x hook": lambda l, m: hook(l) and hook(m),
 "rowcol x rowcol": lambda l, m: rowcol(l) and rowcol(m),
 "rect x rect": lambda l, m: rect(l) and rect(m),
 "durfee<=2 each": lambda l, m: durfee(l) <= 2 and durfee(m) <= 2,
 "one empty": lambda l, m: not l or not m,
 "one empty, other hook": lambda l, m: (not l and hook(m)) or (not m and hook(l)),
 "hook x rowcol (either way)": lambda l, m: (hook(l) and rowcol(m)) or (hook(m) and rowcol(l)),
 "durfee total <= 2": lambda l, m: durfee(l) + durfee(m) <= 2,
 "durfee total <= 3": lambda l, m: durfee(l) + durfee(m) <= 3,
}
for name, f in classes.items():
    nodes, I, fails, allst = analyse(B, L, cap=c, keep=lambda r, cm: f(part(r), part(cm)))
    print(f"c={c} B={B} L={L} class [{name}]:", "SUFFICES" if not fails else f"FAILS ({len(fails)}) e.g. {sorted(fails, key=str)[:2]}", flush=True)
