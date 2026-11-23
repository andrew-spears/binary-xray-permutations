"""Item 2 via lookup: for each n <= 8, does ANY rule in a family work for all Landau D?
Uses good_n{n}.pkl from mine.py.  Families (rule may depend on n arbitrarily):
  F_d    : a = f(d)                         (fixed labelling of the 2n-1 diagonals)
  F_k    : a = f(k)                         (pattern on ranks of sorted D)
  F_kp   : a = f(k, d mod 2)
  F_jp   : a = f(j, d mod 2), j = rank of d within its parity class (ascending)
  F_jpE  : a = f(j, d mod 2, #even d in D)
  F_dk   : a = f(d, k)  (most general 'local' rule; solved by backtracking)
Reports number of functions in the family that work for all D."""
import pickle, itertools, sys

def check_family(n, good, key):
    """key(D, idx) -> hashable feature; count functions feature->bit consistent with some good a for every D.
    Backtracking over D (each D must pick one good a consistent with partial f)."""
    items = []
    for D, gs in good.items():
        feats = [key(D, i) for i in range(n)]
        items.append((feats, gs))
    items.sort(key=lambda t: len(t[1]))
    sols = [0]; example = [None]
    def rec(i, f):
        if sols[0] >= 1000: return
        if i == len(items):
            sols[0] += 1
            if example[0] is None: example[0] = dict(f)
            return
        feats, gs = items[i]
        seen = set()
        for a in gs:
            ok = True; new = []
            for ft, b in zip(feats, a):
                if ft in f:
                    if f[ft] != b: ok = False; break
                elif any(x == ft and y != b for x, y in new): ok = False; break
                else: new.append((ft, b))
            if not ok: continue
            nd = dict(new)
            sig = tuple(sorted(nd.items()))
            if sig in seen: continue
            seen.add(sig)
            f.update(nd); rec(i + 1, f)
            for ft in nd: del f[ft]
    rec(0, {})
    return sols[0], example[0]

def jrank(D, i):
    d = D[i]; return sum(1 for x in D[:i] if x % 2 == d % 2) + 1

FAM = {
    "F_d": lambda D, i: D[i],
    "F_k": lambda D, i: i,
    "F_kp": lambda D, i: (i, D[i] % 2),
    "F_jp": lambda D, i: (jrank(D, i), D[i] % 2),
    "F_jp_desc": lambda D, i: (sum(1 for x in D[i:] if x % 2 == D[i] % 2), D[i] % 2),
    "F_jpE": lambda D, i: (jrank(D, i), D[i] % 2, sum(1 for x in D if x % 2 == 0)),
    "F_dk": lambda D, i: (D[i], i),
}

def run(FAM, N):
  for name, key in FAM.items():
    out = []
    for n in range(1, N + 1):
        good = pickle.load(open(f"/home/claude/agents/start/good_n{n}.pkl", "rb"))
        c, ex = check_family(n, good, key)
        out.append(f"n{n}:{'>=1000' if c >= 1000 else c}")
        if c == 0: break
    print(f"{name:14s}", " ".join(out), flush=True)

if __name__ == "__main__":
    run(FAM, int(sys.argv[1]) if len(sys.argv) > 1 else 8)
