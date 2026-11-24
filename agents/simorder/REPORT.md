# NOTHING: no hole pattern is "at least as good" as another

**Question.** Is there an order on interface states (pairs of Young diagrams) such that a better state completes
every continuation a worse one completes, step by step? Such an order would let a reachable set be replaced by its
best elements, and would turn the set inclusions of card shorten3set into comparisons of single states.

**Exact claim tested.** The largest relation `t <=_l t'` (same slack, last letter l) with: t empty ⇒ t' empty, and for
every legal next letter e every e-successor of t is `<=_e` some e-successor of t'.

**Result.** At slack bound 10 (1,215 states): for every slack ≤ 9 and every last letter ≤ 2, the only pairs t ≠ t'
with `t <=_l t'` are a state and its mirror (rows and columns swapped). Truncating at a bound only removes
challenges, so the true relation is contained in the computed one, and is trivial on that range. Cells with last
letter ≥ 3 near the bound are not decided there (the next letters are forced up to the bound and nothing is left to
challenge); each such cell becomes trivial when the bound is raised (slack 6, last letter 3: 4,098 pairs at bound 8,
0 at bound 10).

**Meaning.** Every hole pattern has its own set of continuations; none dominates another move by move. Any monotone
statement about reachable sets has to be about whole sets (several states together covering what one state did).

**Recheck.** From the repository root: `python3 agents/simorder/sim.py 10` (40 seconds) or `... 8` (3 seconds).
The table gives, for each last letter and slack, the number of comparable pairs that are not mirror images.
