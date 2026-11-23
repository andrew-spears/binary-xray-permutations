"""Online game on the interface machine: the letters arrive one at a time, each stone is placed for good.
A position is (hole pattern, last letter).  Safe = the placer can answer every legal continuation with slacks <= B
(letters in [lo, hi], next letter >= last - 1, slack >= 0).  Prints whether the empty board is safe, and how many
positions are safe at each slack.     python3 game.py B lo hi [look]
look = 1: the placer sees one letter ahead (answers the pair (current, next))."""
import sys
sys.path.insert(0, "../weights")
from maya import Maya
B, lo, hi = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
Mo = Maya(B + 1); St = [Mo.states(s) for s in range(B + 1)]
FIRST = 99
def letters(s, l):
    return [e for e in range(max(lo, -s, (l - 1) if l != FIRST else 0), hi + 1) if s + e <= B]
succ = {}
def sc(s, t, e):
    k = (t, e)
    if k not in succ: succ[k] = set(Mo.succ(t, e))
    return succ[k]
ls = [FIRST] + list(range(hi, max(lo, -B) - 1, -1))
safe = {(s, t, l) for s in range(B + 1) for t in St[s] for l in ls if (l != FIRST or s == 0)}
ch = True
while ch:
    ch = False
    for (s, t, l) in list(safe):
        for e in letters(s, l):
            if not any((s + e, u, e) in safe for u in sc(s, t, e)):
                safe.discard((s, t, l)); ch = True; break
start = (0, St[0][0], FIRST)
print(f"B = {B}, letters in [{lo}, {hi}]: empty board safe: {start in safe}")
for s in range(B + 1):
    print(f"  slack {s}: {len(St[s])} patterns; safe after last letter",
          " ".join(f"{l}: {sum(1 for t in St[s] if (s, t, l) in safe)}" for l in ls[1:6]))
if start not in safe and len(sys.argv) > 4:
    # shortest forced loss: rank[p] = number of further letters the adversary needs
    rank = {}
    def lose(p, d):
        """adversary wins from p within d letters"""
        s, t, l = p
        if d == 0: return None
        for e in letters(s, l):
            subs = [(s + e, u, e) for u in sc(s, t, e)]
            if not subs: return [e]
            if d > 1:
                lines = []
                for q in subs:
                    r = lose(q, d - 1)
                    if r is None: break
                    lines.append(r)
                else: return [e, max(lines, key=len)]
        return None
    for d in range(1, 14):
        r = lose(start, d)
        if r: print("adversary wins in", d, "letters; one line:", r); break
