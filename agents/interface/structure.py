"""Structure of the reachable sets in the bounded-slack automaton.
For each (sigma, e_prev): how many distinct reachable sets, is there a unique minimal one
(= the intersection is itself reachable), are they a chain?  Usage: python3 structure.py B"""
import sys
from slack_dfa import run
B = int(sys.argv[1])
bad, seen, nstates, maxset = run(B)
def part(mask):
    # bits 0..2B-1 <-> positions k-B+1..k+B ; partition = (x_(i) - i) nonzero parts, sorted desc
    xs = [j - B + 1 for j in range(2 * B) if mask >> j & 1]   # relative to k (k -> 0)
    # ranks: the j-th largest of the k elements should be at 0,-1,-2,...
    xs.sort(reverse=True)
    return tuple(x + i for i, x in enumerate(xs) if x + i > 0)
groups = {}
for (eprev, S, sig) in seen:
    groups.setdefault((sig, eprev), []).append(S)
tot = 0; uniq = 0; chain = 0
for key in sorted(groups, key=lambda t: (t[0], -99 if t[1] is None else t[1])):
    Ss = groups[key]
    inter = frozenset.intersection(*Ss)
    is_min = inter in Ss
    is_chain = all(a <= b or b <= a for a in Ss for b in Ss)
    tot += 1; uniq += is_min; chain += is_chain
    if "-v" in sys.argv:
        print(key, "#sets", len(Ss), "sizes", sorted(len(s) for s in Ss), "min reachable" if is_min else "NO UNIQUE MIN", "inter", len(inter), "chain" if is_chain else "")
        if "-vv" in sys.argv:
            print("    min set:", sorted((part(r), part(c)) for r, c in inter))
print(f"B={B}: {tot} (sigma,e) classes; unique minimal set in {uniq}; chain in {chain}")
