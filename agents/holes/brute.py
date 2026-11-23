"""Enumerate boards rows {1..m}, columns = {1..m+h} minus h columns, all D;
record (board, D) passing the two-sided sum test but with no placement.
Usage: python3 brute.py m h  -> writes holes_m{m}_h{h}.txt"""
import sys, itertools

def sumtest(R, C, D):
    m = len(R); Rs = sorted(R); Cs = sorted(C); Ds = sorted(D)
    if sum(Ds) != sum(Cs) - sum(Rs): return False
    a = b = c = 0
    for k in range(1, m):
        # lower: k smallest D >= k smallest C - k largest R
        if sum(Ds[:k]) < sum(Cs[:k]) - sum(Rs[-k:]): return False
        if sum(Ds[-k:]) > sum(Cs[-k:]) - sum(Rs[:k]): return False
    return True

def placement(R, C, D):
    """backtrack: assign each diagonal (fewest options first) to a row."""
    Cset = set(C); Ds = list(D)
    opts = {d: [r for r in R if r + d in Cset] for d in Ds}
    if any(not opts[d] for d in Ds): return None
    Ds.sort(key=lambda d: len(opts[d]))
    usedR = set(); usedC = set(); sol = {}
    def rec(i):
        if i == len(Ds): return True
        d = Ds[i]
        for r in opts[d]:
            if r not in usedR and r + d not in usedC:
                usedR.add(r); usedC.add(r + d); sol[r] = r + d
                if rec(i + 1): return True
                usedR.discard(r); usedC.discard(r + d); del sol[r]
        return False
    return dict(sol) if rec(0) else None

def boards(m, h):
    R = list(range(1, m + 1))
    for dele in itertools.combinations(range(1, m + h + 1), h):
        C = [c for c in range(1, m + h + 1) if c not in dele]
        yield R, C

if __name__ == "__main__":
    m, h = int(sys.argv[1]), int(sys.argv[2])
    out = open(f"/home/claude/agents/holes/holes_m{m}_h{h}.txt", "w")
    npass = nholes = npos = 0
    for R, C in boards(m, h):
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D): continue
            npass += 1
            p = placement(R, C, D)
            if p is None:
                nholes += 1
                out.write(f"{C} {list(D)}\n")
            else:
                npos += 1
    print(m, h, "pass", npass, "realizable", npos, "holes", nholes)
