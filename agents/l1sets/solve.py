"""The proof as an algorithm.  Input: a word in {-1,0,1} with all partial sums >= 0 and total 0.  Output: a permutation sigma with
{k + sigma(k)} = {2k + x_k} as multisets.  Backwards from the empty state: for stone n, n-1, .., 1 choose any e-predecessor in G(slack).
  python3 solve.py + + 0 - 0 + - -          one word
  python3 solve.py all N                     every valid word of length <= N (with and without the factor + -)
  python3 solve.py random COUNT LEN [seed]   random valid words (uniform +-1/0 steps reflected at 0, forced back to 0)"""
import sys, random, itertools, l1
def in_G(u):
    return u == ((), ()) if l1.slack(u) == 0 else (l1.central(u) and not l1.in_T(u))
def solve(w, rng=None):
    n = len(w); u = ((), ()); stones = []
    for N in range(n, 0, -1):
        e = w[N - 1]; cand = [(k, t) for k, t in l1.preds(u, e) if in_G(t)]
        assert cand, ("step lemma fails", w, N, u)
        k, t = rng.choice(cand) if rng else cand[0]
        r = N + k + 1; stones.append((r, 2 * N + e - r)); u = t
    assert u == ((), ())
    rows = sorted(r for r, c in stones); cols = sorted(c for r, c in stones)
    assert rows == list(range(1, n + 1)) and cols == list(range(1, n + 1)), (w, stones)
    assert sorted(r + c for r, c in stones) == sorted(2 * k + x for k, x in enumerate(w, 1))
    sig = [0] * n
    for r, c in stones: sig[r - 1] = c
    return sig
def valid(w):
    s = 0
    for x in w:
        s += x
        if s < 0: return False
    return s == 0
if __name__ == "__main__":
    if sys.argv[1] == "all":
        for n in range(1, int(sys.argv[2]) + 1):
            cnt = cnt2 = 0
            for w in itertools.product((1, 0, -1), repeat=n):
                if valid(w):
                    solve(w); cnt += 1; cnt2 += not any(a == 1 and b == -1 for a, b in zip(w, w[1:]))
            print(f"n {n}: {cnt} valid words in {{-1,0,1}}^n solved ({cnt2} without the factor + -)", flush=True)
    elif sys.argv[1] == "random":
        cnt, ln = int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1); mx = 0; hist = {}
        for it in range(cnt):
            up = rng.choice((0.4, 0.6, 0.8, 0.95)); w = []; s = 0
            while len(w) + s < ln:
                x = rng.choices((1, 0, -1), (up, (1 - up) / 2, (1 - up) / 2))[0] if rng.random() < 0.9 or s % 4 > 1 else 0
                if s + x < 0: x = 0
                w.append(x); s += x
            top = max(itertools.accumulate(w))
            while s > 0:
                x = rng.choices((-1, 0, 1), (0.7, 0.2, 0.1))[0]
                if len(w) > 3 * ln: x = -1
                w.append(x); s += x
            top = max(itertools.accumulate(w)); solve(tuple(w), rng); mx = max(mx, top); hist[top // 25 * 25] = hist.get(top // 25 * 25, 0) + 1
        print(f"{cnt} random valid words, length about {ln}..: all solved; largest slack {mx}; words by largest slack (bins of 25): {dict(sorted(hist.items()))}")
    else:
        w = tuple({"+": 1, "0": 0, "-": -1}[a] for a in sys.argv[1:]); print(solve(w))
