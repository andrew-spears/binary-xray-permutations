"""Is F(x), x with letters -1, 0, +1, exactly the set of states that pass the odd/even count (card paritycount)?
A state after k stones: rows R, columns C (absolute, reflected rows).  With z zeros and p = k - z odd letters:
OO = (odd(R) + odd(C) - p) / 2 must be an integer with 0 <= OO <= z, OO <= odd(R), OO <= odd(C).
Usage: python3 par.py B K   (slacks <= B, prefixes of length <= K)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from sets import allstates
from rewrite import machine
from collections import defaultdict
def odd(mask, k, B):
    # bit B+u set <=> line k+1+u used; all lines <= k-B are used: count odd lines among 1..k-B plus set bits
    n = (k - B + 1) // 2 if k - B >= 1 else 0
    for b in range(2 * B + 1):
        if mask >> b & 1:
            line = k + 1 + b - B
            if line >= 1 and line % 2: n += 1
            if line < 1 and not (mask >> b & 1): pass
    return n
def passes(st, k, z, B):
    a, b = odd(st[0], k, B), odd(st[1], k, B); p = k - z; t = a + b - p
    return t % 2 == 0 and 0 <= t // 2 <= z and t // 2 <= min(a, b)
if __name__ == "__main__":
    B, K = int(sys.argv[1]), int(sys.argv[2]); step, start = machine(B); lvl = allstates(B, step, start)
    seen = {}; layer = [(frozenset([start]), 0, None, 0, 0, "")]; stats = defaultdict(lambda: [0, 0, None])
    while layer:
        nxt = []
        for S, s, last, k, z, w in layer:
            if k == K: continue
            for e, ch in ((-1, "-"), (0, "0"), (1, "+")):
                if s + e < 0 or s + e > B - 1 or (last == 1 and e == -1): continue
                S2 = step(S, e); key = (S2, s + e, e, (k + 1) % 2, min(z + (e == 0), B))
                if key in seen: continue
                seen[key] = 1; k2, z2, w2 = k + 1, z + (e == 0), w + ch
                P = {st for st in lvl[s + e] if passes(st, k2, z2, B)}
                assert S2 <= P, (w2, "reachable state fails the parity count")
                st_ = stats[(s + e, min(z2, 3))]; st_[0] += 1
                if S2 != P:
                    st_[1] += 1
                    if st_[2] is None: st_[2] = (w2, len(S2), len(P))
                nxt.append((S2, s + e, e, k2, z2, w2))
        layer = nxt
    for (s, z), (n, bad, ex) in sorted(stats.items()):
        print(f"slack {s}, zeros {z}{'+' if z == 3 else ''}: {n} sets, {bad} differ from the parity-count set", ex or "")
