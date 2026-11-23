from lib import *
x = (2,3,3,2,2,1,1,0); k = len(x); S = sums_of(x)
print("S", S)
X = F(S + (2*k+1,)); Y = F(S + (2*k+2, 2*k+3))
miss = [t for t in X if Sh(t) not in Y]
print(len(X), len(Y), len(miss))
def placements(sums, A, B):
    """all placements of sums (list) on rows mask A, cols mask B"""
    out = []
    def rec(i, A, B, acc):
        if i == len(sums): out.append(tuple(acc)); return
        s = sums[i]
        for a in bits(A):
            b = s - a
            if b >= 1 and B >> (b-1) & 1:
                acc.append((a, b)); rec(i+1, A & ~(1 << (a-1)), B & ~(1 << (b-1)), acc); acc.pop()
    rec(0, A, B, [])
    return out
for A, B in miss:
    print("rows", bits(A), "cols", bits(B))
    for p in placements(S + (2*k+1,), A, B): print("   ", p)
    print("  target rows", bits(Sh((A,B))[0]), "cols", bits(Sh((A,B))[1]), "sums", S + (2*k+2, 2*k+3))
print("=== why the target is unsolvable: all ways to seat 18 and 19, and the board left for S")
A, B = miss[0]; TA, TB = Sh((A, B)); FS = F(S)
print("|F(x)| =", len(FS))
def landau(sums, A, B):
    """sum test: j smallest sums >= j smallest rows + j smallest cols, j largest sums <= j largest rows + cols"""
    a, b, s = sorted(bits(A)), sorted(bits(B)), sorted(sums)
    for j in range(1, len(s) + 1):
        if sum(s[:j]) < sum(a[:j]) + sum(b[:j]): return "low%d" % j
        if sum(s[-j:]) > sum(a[-j:]) + sum(b[-j:]): return "high%d" % j
    return "ok"
for a2 in bits(TA):
    b2 = 19 - a2
    if b2 < 1 or not TB >> (b2-1) & 1: continue
    for a1 in bits(TA):
        b1 = 18 - a1
        if a1 == a2 or b1 == b2 or b1 < 1 or not TB >> (b1-1) & 1: continue
        A2 = TA & ~(1 << (a1-1)) & ~(1 << (a2-1)); B2 = TB & ~(1 << (b1-1)) & ~(1 << (b2-1))
        print(f"  18 at {(a1,b1)}, 19 at {(a2,b2)}: rows {bits(A2)} cols {bits(B2)} in F(x): {(A2,B2) in FS}; sum test: {landau(S, A2, B2)}")
