"""Which simple rule for S always gives an odd split?  Reads the output of ./dump n.   Usage: python3 rules.py file"""
import sys
rows = []
for line in open(sys.argv[1]):
    a, b = line.split("|"); e = list(map(int, a.split())); ok = {int(t.split(":")[0]) for t in b.split()}
    rows.append((e, ok))
n = len(rows[0][0])
def mask(pred, e):
    sig = 0; m = 0
    for k in range(n):
        if pred(e, k, sig): m |= 1 << k
        sig += e[k]
    return m
def admissible(e, S):
    # S-word and complement word nonnegative
    d = [2 * (k + 1) + e[k] for k in range(n)]
    A = [d[k] for k in range(n) if S >> k & 1]; Bc = [2 * n + 2 - d[k] for k in range(n - 1, -1, -1) if not S >> k & 1]
    return all(x >= 2 * (j + 1) for j, x in enumerate(A)) and all(x >= 2 * (j + 1) for j, x in enumerate(Bc))
rules = {
 "e > 0": lambda e, k, s: e[k] > 0,
 "e >= 0": lambda e, k, s: e[k] >= 0,
 "e > 0, or e = 0 at slack 0": lambda e, k, s: e[k] > 0 or (e[k] == 0 and s == 0),
 "e > 0, or e = 0 at slack > 0": lambda e, k, s: e[k] > 0 or (e[k] == 0 and s > 0),
 "e > 0, or e = 0 after a positive letter": lambda e, k, s: e[k] > 0 or (e[k] == 0 and k > 0 and e[k - 1] > 0),
 "e > 0, or e = 0 before a positive letter": lambda e, k, s: e[k] > 0 or (e[k] == 0 and k < n - 1 and e[k + 1] > 0),
}
for name, pr in rules.items():
    bad = [e for e, ok in rows if mask(pr, e) not in ok and any(e)]
    print(f"{name:45}: fails for {len(bad)} of {len(rows) - 1}", bad[:3])
tot = adm = 0; frac = []
for e, ok in rows:
    if not any(e): continue
    A = [S for S in range(1, (1 << n) - 1) if admissible(e, S)]
    assert ok <= set(A), (e, sorted(ok - set(A))[:3])
    frac.append(len(ok) / len(A))
if not frac: sys.exit("no word other than 0 ... 0 at this n")
print(f"odd splits are always admissible (both part-words nonnegative); share of admissible S that are odd: min {min(frac):.3f}, mean {sum(frac)/len(frac):.3f}")
worst = min((len(ok), e) for e, ok in rows if any(e)); print("fewest odd S:", worst)
