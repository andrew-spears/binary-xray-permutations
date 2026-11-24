"""Which prefixes z (letters >= 0, next >= last - 1) have all their odd states (odd number of placements) inside G(slack)?
  python3 oddz.py LEN SMAX      prints the words z with a letter >= 2 that qualify, and counts"""
import sys
LEN, SMAX = int(sys.argv[1]), int(sys.argv[2])
sys.argv = [sys.argv[0], str(LEN + SMAX)]
import hybrid as h
good = []; tot = 0; emp = 0
def rec(z, s, odd):
    global tot, emp
    if z and max(z) >= 2:
        tot += 1
        if not odd: emp += 1
        elif all(h.in_G(u) for u in odd): good.append((z, len(odd)))
    if len(z) == LEN: return
    for e in range(max(0, (z[-1] - 1) if z else 0), SMAX - s + 1):
        nxt = {}
        for u in odd:
            for k, v in h.l1.succs(u, e): nxt[v] = nxt.get(v, 0) ^ 1
        rec(z + (e,), s + e, {v for v, b in nxt.items() if b})
rec((), 0, {((), ())})
print(f"prefixes with a letter >= 2, length <= {LEN}, slack <= {SMAX}: {tot}; no odd state: {emp}; all odd states in G: {len(good)}")
for z, c in good[:60]: print("  ", " ".join(map(str, z)), " odd states:", c)
