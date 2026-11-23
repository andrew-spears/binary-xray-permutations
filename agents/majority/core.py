"""Universal states at a cut.  For slack s and last letter l: U(s, l) = states that lie in F(x) for EVERY legal prefix
x with slack s and last letter l, and in A(y) for EVERY suffix y at slack s whose first letter is >= l - 1
(all slacks <= B).  Prints U as pairs of partitions (row holes | column holes).
Usage: python3 core.py B"""
import sys
from maj import families
def diagram(mask, B):
    """bit i of mask <-> position i - B relative to the frontier (positions <= 0 filled in the empty state)."""
    bits = [mask >> i & 1 for i in range(2 * B + 1)]
    lam = []; holes = 0
    for b in bits:
        if b: lam.append(holes)
        else: holes += 1
    return tuple(x for x in reversed(lam) if x)
def name(t, B):
    f = lambda p: "".join(str(x) if x < 10 else f"({x})" for x in p) or "-"
    return f(diagram(t[0], B)) + "|" + f(diagram(t[1], B))
if __name__ == "__main__":
    B = int(sys.argv[1]); lev, Fs, As = families(B)
    for s in range(1, B + 1):
        for l in sorted({l for F, l in Fs[s]}):
            FF = [F for F, l2 in Fs[s] if l2 == l]; AA = [A for A, f in As[s] if f >= l - 1]
            if not AA: continue
            U = set(lev[s])
            for F in FF: U &= F
            UF = len(U)
            for A in AA: U &= A
            print(f"slack {s:2d} last {l:2d}: {len(FF):4d} F, {len(AA):4d} A, in all F {UF:4d}, universal {len(U):3d}: ", " ".join(sorted(name(t, B) for t in U))[:150])
