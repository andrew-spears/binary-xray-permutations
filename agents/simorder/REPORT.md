# NOTHING: no hole pattern is "at least as good" as another

**Question.** Is there an order on interface states (pairs of Young diagrams) such that a better state completes
every continuation a worse one completes, step by step? Such an order would let a reachable set be replaced by its
best elements, and would turn the set inclusions of card shorten3set into comparisons of single states.

**Exact claim tested.** The largest relation `t <=_l t'` (same slack, last letter l) with: t empty ⇒ t' empty, and for
every legal next letter e every e-successor of t is `<=_e` some e-successor of t'.

**Result.** For slack bound 5 and 8 (434 states), and every last letter, the only pairs t ≠ t' with `t <=_l t'` are a
state and its mirror (rows and columns swapped), apart from the top slack level where the bound leaves no letter to
challenge. Truncating at a bound only removes challenges, so the true relation is contained in this one: it is
trivial for every state of slack ≤ 7.

**Meaning.** Every hole pattern has its own set of continuations; none dominates another move by move. Any monotone
statement about reachable sets has to be about whole sets (several states together covering what one state did).

**Recheck.** `python3 agents/simorder/sim.py 8` (3 seconds). Columns: slack : states / comparable ordered pairs /
pairs comparable both ways. The second and third numbers agree and equal the number of states that differ from
their mirror.
