"""Print all witnesses of an L_1 word as row displacements u_k = row(k) - k  (column displacement is e_k - u_k).
Usage: python3 letters_wit.py '++0--' ..."""
import sys
def witnesses(e):
    m = len(e); out = []
    def rec(k, R, C, acc):
        if k > m: out.append(tuple(acc)); return
        for r in range(1, m + 1):
            c = 2 * k + e[k - 1] - r
            if 1 <= c <= m and not (R >> r & 1) and not (C >> c & 1):
                acc.append(r - k); rec(k + 1, R | 1 << r, C | 1 << c, acc); acc.pop()
    rec(1, 0, 0, []); return out
if __name__ == "__main__":
    for w in sys.argv[1:]:
        e = [{"+": 1, "0": 0, "-": -1}[ch] for ch in w]; ws = witnesses(e)
        print(w, len(ws), "witnesses")
        for u in sorted(ws, key=lambda u: sum(x * x for x in u))[:10]:
            print("   u =", " ".join(f"{x:+d}" for x in u), "  v =", " ".join(f"{a - x:+d}" for a, x in zip(e, u)))
