"""Online game with lookahead on the bounded-slack automaton (compare online_game.py = lookahead 1).
The word e_1 e_2 ... (valid, no tight cut inside, all slacks <= B) is revealed L letters at a time:
Placer puts stone k down knowing e_k, ..., e_{k+L-1} (fewer if the word ends earlier) and nothing later.
Position = (sigma_{k-1}, used rows, used columns, known letters).  Computes the greatest set of positions
from which Placer survives, and reports whether every opening is in it.
Usage: python3 lookahead_game.py B L"""
import sys
def solve(B, L):
    def succ(mask):
        out = []
        for u in range(-B, B + 1):
            bit = B + u
            if mask >> bit & 1: continue
            m = mask | (1 << bit)
            if not (m & 1): continue
            out.append((u, m >> 1))
        return out
    cache = {}
    def sm(m):
        if m not in cache: cache[m] = succ(m)
        return cache[m]
    base = (1 << B) - 1
    def legal(eprev, sig):                      # letters that may follow (eprev, slack sig); sig > 0 or the start
        lo = 0 if eprev is None else eprev - 1
        for e in range(max(lo, -sig), B - sig + 1):
            s2 = sig + e
            if s2 == 0 and sig == 0: continue
            if s2 + max(e, 0) * max(e - 1, 0) // 2 > B: continue
            yield e
    def extend(sig, w, eprev):                  # all ways to fill the window up to L letters; sig = slack before w
        s = sig + sum(w); last = w[-1] if w else eprev
        if len(w) == L or (w and s == 0): return [w]
        out = []
        for e in legal(last, s): out += extend(sig, w + (e,), eprev)
        return out
    starts = [(0, base, base, w) for w in extend(0, (), None)]
    pos = set(starts); stack = list(starts); moves = {}
    while stack:
        p = stack.pop(); sig, rm, cm, w = p
        e = w[0]; s1 = sig + e; opts = []          # opts: list of (list of adversary replies) per placement
        ended = sig + sum(w) == 0
        nxt = [w[1:]] if ended else [w[1:] + (x,) for x in legal(w[-1], sig + sum(w))]
        for (u, r2) in sm(rm):
            v = e - u
            if v < -B or v > B or cm >> (B + v) & 1: continue
            c2 = cm | (1 << (B + v))
            if not (c2 & 1): continue
            c2 >>= 1
            if s1 == 0: opts.append([]); continue         # word finished
            qs = [(s1, r2, c2, w2) for w2 in nxt]
            opts.append(qs)
            for q in qs:
                if q not in pos: pos.add(q); stack.append(q)
        moves[p] = opts
    win = set(pos); changed = True
    while changed:
        changed = False
        for p in list(win):
            if not any(all(q in win for q in qs) for qs in moves[p]):
                win.discard(p); changed = True
    return all(s in win for s in starts), len(pos), len(win), win, moves, starts
if __name__ == "__main__":
    B, L = int(sys.argv[1]), int(sys.argv[2])
    ok, npos, nwin, win, moves, starts = solve(B, L)
    print(f"B={B} L={L}: positions {npos}, safe {nwin}, Placer {'WINS' if ok else 'LOSES'}", flush=True)
