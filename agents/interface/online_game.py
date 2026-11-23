"""Online (no-lookahead) game on the bounded-slack automaton.
Adversary reveals e_1, e_2, ... one at a time (any valid word with max slack <= B that can still
be completed inside the bound); Placer must put stone k down before seeing e_{k+1}.
Position = (e_prev, sigma, rowmask, colmask).  Computes the greatest set of positions from which
Placer survives forever (safety game) and reports whether the start position is in it.
Usage: python3 online_game.py B [--tight]"""
import sys
def solve(B, allow_tight=False):
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
    def legal(eprev, sig):
        lo = 0 if eprev is None else eprev - 1
        for e in range(max(lo, -sig), B - sig + 1):
            s2 = sig + e
            if s2 == 0 and sig == 0: continue
            if s2 == 0 and not allow_tight and False: continue
            if s2 + max(e, 0) * max(e - 1, 0) // 2 > B: continue
            yield e
    # forward reachability of positions
    start = (None, 0, base, base)
    pos = {start}; stack = [start]; moves = {}
    while stack:
        p = stack.pop(); eprev, sig, rm, cm = p
        mv = {}
        for e in legal(eprev, sig):
            opts = []
            for (u, r2) in sm(rm):
                v = e - u
                if v < -B or v > B: continue
                if cm >> (B + v) & 1: continue
                c2 = cm | (1 << (B + v))
                if not (c2 & 1): continue
                q = (e, sig + e, r2, c2 >> 1)
                if sig + e == 0:
                    q = ("END",) if not allow_tight else (None, 0, base, base)
                opts.append(q)
                if q != ("END",) and q not in pos: pos.add(q); stack.append(q)
            mv[e] = opts
        moves[p] = mv
    win = set(pos); win.add(("END",))
    changed = True
    while changed:
        changed = False
        for p in list(win):
            if p == ("END",): continue
            if any(not any(q in win for q in opts) for opts in moves[p].values()):
                win.discard(p); changed = True
    return start in win, len(pos), len(win) - 1, win, moves
if __name__ == "__main__":
    B = int(sys.argv[1]); tight = "--tight" in sys.argv
    ok, npos, nwin, win, moves = solve(B, tight)
    print(f"B={B}: positions {npos}, safe {nwin}, Placer {'WINS' if ok else 'LOSES'} the online game")
