# HIT (conjecture + range): on old prefixes F(x) ⊇ (1–3 charge classes) ∖ (explicit thin set), a function of the slack and the last two letters, uniform in the largest letter. NOTHING for tails that contain a letter ≥ 2

Follow-up to `REPORT2.md` (card `blocktypes`) and `../l1sets/REPORT.md` (cards `l1`, `upone`). Nothing here is proved
except two negative statements by exhaustive computation (§2). Code: `types.cpp` (new feature `Y` / `y`), `fw.cpp`
(exact F(x) of single words, slack ≤ 30), `jstar.py`, `closed.py`, `old.py`, `stair.py`, `tail.py`, `loc.py`.
Build: `g++ -O2 -std=c++17 -o types types.cpp && g++ -O2 -std=c++17 -o fw fw.cpp`.

**Definition.** A prefix x is **old** if every suffix of j letters has sum ≤ j, for all j; equivalently slack(i) − i takes
its minimum over i ≤ |x| at i = |x|. With y = max(0, max_j (sum of the last j letters − j)), old means y = 0, and y is
updated by y′ = max(0, y + e − 1). Every prefix ending a run of letters ≤ 1 that is long enough is old; a prefix
with a recent large letter is young. Every complete word is old.

**Conjecture OLD (tested, range below).** Notation of `../l1sets`: state u = (λ, ν = μ′), a, b = 2-core charges of λ and ν,
c = a + b (c ≡ s mod 2), D = |a − b|. For every old prefix x of slack s ≥ 11 that ends in a letter 0 or 1,
F(x) ⊇ J*(s, τ), where τ is the last two letters of x, the first replaced by "." if the last letter is a rise:

| τ | class | removed |
|---|---|---|
| 1 1 | c ∈ {0, 1}, D ≤ 4 | SC = {(λ\|λ′)} |
| . 1 | −1 ≤ c ≤ 2, D ≤ 3 | SC, the four states A(s) for s = 4m² + 1 (in range: only s = 17), and k\|k (λ = μ = (k), s = 2k) |
| 1 0 | −1 ≤ c ≤ 2, D ≤ 3 | −\|s, s\|−, −\|nn, nn\|− (s = 2n), E⁰ |
| 0 0 | −2 ≤ c ≤ 3, D ≤ 2 | −\|s, s\|− |
| . 0 | −2 ≤ c ≤ 3, D ≤ 3 | −\|s, s\|− |

SC, E⁰, A(s) are the pieces of T(s) in `../l1sets/l1.py`. So the class is Central(s) for the tail 1 1, Central plus one
neighbouring class for the tails . 1 and 1 0, and three classes for 0 0 and . 0.

**Size of the exception.** At s = 20 the classes have 15296, 22964, 22964, 24708, 24708 states (of 24842); the bound on D
removes 0, 36, 36, 36, 36 of them and the listed families 36, 37, 8, 2, 2. For the tail 0 0 at odd slack D ≤ 2 removes more
(742 of 17410 at s = 19). J* is 68 % of all states at s = 11 and 61 % at s = 20 for the tail 1 1, and 92–99.7 % for the others;
it is never close to empty.

**Range.**
- Exhaustive, all words with slack ≤ 20, any letters: J* is contained in the largest block-closed family J of
  `KLO=0 ./types 20 YA1` (which is inside F(x) for every old x), for all 49 pairs (s, τ) with 11 ≤ s ≤ 20; and J* = J
  except that J also has k|k for τ = . 1 at s = 12, 14, …, 20. `python3 jstar.py 20` (about 8 min the first time; `jstar.py 16`: 30 s).
  The sets do not move with the bound: J of bound 16 and of bound 18 equal J of bound 20 on every type (78 and 88 types,
  including the top slack); bound 14 differs in one state (5|5 at (10, . 1)).
- Direct, exact F(x) from `fw`: 0 states of J* missing in
  4,287 old prefixes of 400 steep words (1^i 2 3 … c^k … 1 0 −1 … then 0/1 letters; letters ≤ 7, slack ≤ 28; `old.py 28 10 400 0 3`, 5 min),
  195 old prefixes of 300 words made of falling runs (letters ≤ 10, slack ≤ 30; `old.py 30 10 300 2 3`, 12 min),
  9,779 old prefixes of 300 random words of 78 letters (letters ≤ 8, slack ≤ 26; `old.py 26 8 300 1 3`, 16 min),
  1,686 old prefixes after one full staircase k, k−1, …, −j with k ≤ 7 (`stair.py 3 7`, 4 min; slack ≥ 9), and
  1,734 after two staircases (`TWO=1 SMAX=24 python3 stair.py 2 6 2 9`).
- Block step: J*(s′, τ′) ⊆ step_w(J*(s, τ)) for every block w of at most 7 letters with letters ≤ 5 and slack ≤ 21 inside, from
  source slacks 11–16 and both ends at slack ≥ 11: 1,209 (source, block) pairs, 0 failures (`closed.py 11 16 7 5 21`, 1 min).
- Recheck (1 min): `python3 jstar.py 16 && python3 closed.py 11 14 5 3 20 && python3 stair.py 5 6`.

**How far to trust it.** The table was fitted, and corrected three times by tests beyond bound 20:
- without the bounds on D: fails at slack 16–18 on near-staircases (321|4321, 21|54321, 321|6321, …) and with 290 states at
  slack 24 after `1 1 2^10 1 0^10 1^7`;
- with D ≤ 2 for every tail: nothing found, but it is smaller than J on the range; the table has the largest D that survived;
- k|k: missing after the staircase k, k−1, …, 1, 0, −1, …, −(k−2), 1 (found for k = 5, 6, 7; slack 2k). The staircase reaches
  slack k(k + 1)/2, so the exhaustive bound 20 sees only k = 5. Slack 30 allows staircases with k ≤ 7 only, so an exception
  that needs a staircase with k ≥ 8 cannot have been seen.
Below slack 11 there are sporadic extra exceptions (2–11 states per (s, τ), e.g. 1|4211 at (9, . 1), 111|33 and 11|52 at
(9, 1 0)); there the sets are a finite table (`jstar.py 20 0` lists the differences).

**What it gives.** If J(s, τ) (the table for s ≤ 10, J* above) is closed under blocks, every valid word has a permutation:
w complete ⇒ w 0 is old, ends in 0, has slack 0, and J(0, ·) = {∅|∅}. A block is the word between two consecutive old
prefixes ending in 0 or 1: one letter 0 or 1, or negative letters and then 0 or 1, or an **excursion** that starts with a letter
≥ 2 and ends when y is back at 0. The step for the one-letter blocks is of the kind proved in `../l1sets`. The step for
excursions is not: an excursion is an arbitrary young word, and I have no description of what happens inside one (§1).

## 1. Tails with letters ≥ 2: Central ∖ J is not thin, and not local (item 1)

`python3 tail.py c B` (letters ≤ c, all words with slack ≤ B, τ = final non-increasing run, at most 4 letters): for each (s, τ),
C = exact core = ∩ F(x) over the prefixes with that slack and tail; Loc = states with a chain of predecessors along the
letters of τ starting from any state; G = Central ∖ T. Entries: |C| / |C ∖ Central| / |G ∖ Loc| / |(G ∩ Loc) ∖ C|.
|G(s)| = 48, 80, 126, 212, 332, 512, 770, 1176 for s = 6, …, 13.

| c | τ | s = 6 | 8 | 10 | 12 | 13 |
|---|---|---|---|---|---|---|
| 2 | 2 | 12/4/4/12 | 50/18/15/83 | 158/54/26/202 | 590/206/40/358 | |
| 2 | 2 1 | 30/6/4/20 | 90/26/8/54 | 312/90/6/104 | 823/242/5/186 | |
| 2 | 2 2 | 34/10/18/6 | 86/26/28/42 | 210/72/40/154 | 630/218/54/316 | |
| 3 | 2 | 12/4/4/12 | 22/8/15/99 | 104/36/26/238 | 248/86/40/570 | 358/124/50/892 |
| 3 | 3 | 8/0/16/24 | 4/0/30/92 | 2/0/48/282 | 12/0/80/680 | 8/0/100/1068 |
| 3 | 3 2 1 | 27/9/30/0 | 75/22/41/32 | 166/54/50/170 | 363/100/54/453 | 608/182/70/680 |

- **Not thin.** For τ = 2 at c = 2, s = 12 the core has 384 of the 770 states of G; for τ = 3 2 1 at s = 13 it has 426 of 1176; for
  τ = 3 it has 8. The block-closed sets J of `A2K` / `A3K` are smaller still (`python3 exc.py 2 14 A2K`: for τ = 2 1 at s = 14,
  |G ∖ J| = 1074 of 1744).
- **Not inside Central.** A quarter to a third of each core lies in the neighbouring classes (second entry), as in the table of OLD.
- **The local part is explicit but small.** u has an e-predecessor iff some bead k of M has k + 1 − e ∉ B (`l1.preds`); so a last
  letter 2 excludes exactly the states with M − 1 ⊆ B: hooks and rows such as −|11, 1|2, 2|2, 1|21, −|1111. For τ = 2 1 the chain
  excludes −|111, −|3, 11|11, 11|2, −|4, …; for 3 2 1 the one-sided states −|6, −|51, −|42, −|411, −|33, … (`tail.py c B show S`).
  The same with central predecessors only is a parity rule (`loc.py`: every bead k of M with k ≡ s mod 2 has k − 1 ∈ B).
- **The residual is not local.** The fourth entry (in G, has predecessors along τ, not in the core) is the bulk of the omission
  and grows with s: 358 of 770 for τ = 2 at s = 12. First cases: −|31, 11|11, 31|− at (4, τ = 2). These states are missing
  because of what stands before the tail, so Exc(s, τ) is not "what the last stones make impossible, plus T(s)".

Reading: after a letter ≥ 2 the prefix is young, and F(x) of a young prefix depends on the whole excursion. The thin description
comes back exactly when the prefix is old again.

## 2. No blocks (item 2)

`./types B F` without `K`: a set on every prefix. "Works" = no empty set and no bad pair. `An` = final non-increasing run, at most
n + 1 letters. `y` = the young excess as part of the type.

| letters | type besides slack | first bound where it fails |
|---|---|---|
| ≤ 2 | A1 / A2 / A3 / A5 / A9 | 5 / 8 / 11 / 12 / 12 |
| ≤ 2 | y A1 | none through 24 (1,373 types at B = 24) |
| ≤ 3 | A1 / A2, A3, A5, A9 | 5 / 7 |
| ≤ 3 | y A1 / y A2 / y A3 | 10 / 15 / 19 |
| any | y A1 / y A2, y A3 | 10 / 10 (empty set at the type of 1 4 5; bad pairs from 14 for y A2) |

- **Letters ≤ 3: impossible, by exhaustion.** The 13 different sets F(x) of the prefixes x of slack 7 whose last letter is a
  rise to 3 have empty intersection (minimal ones: F(1 1 2 3), F(1 2 1 3), F(1 1 1 1 3), F(2 1 1 3), F(2 2 3), F(1 1 1 1 0 3); 110 states).
  So no assignment of sets by (slack, final non-increasing run) exists, whatever the rule. `CORE=2 DUMPMAX=7 LET=-99,3 ./types 7 A3`.
- **Letters ≤ 2: the cores are nonempty but not step-closed.** Through bound 12 every core is nonempty, yet for 32 transitions at
  bound 8 the core after the letter has states with no predecessor in the core before it. After a letter 2:
  (6; 2) → (8; 2 2): −|53, 53|−, 3|311, 31|211, 311|3, 211|31, 2|3111, 21|2111, 3111|2, 2111|21;
  (5; 1 1 1) → (7; 2): 1|42, 42|1;   (6; 2 1) → (8; 2): −|44, 44|−, 31|211, 32|111, 211|31, 111|32.
  Each prefix reaches these states, but through predecessors that depend on the prefix. `CORE=4 DUMPMAX=8 LET=-99,2 ./types 8 A2`.
  With y in the type this goes away for letters ≤ 2 (tested to 24), at the price of a number of types that grows with the slack
  (y takes up to about s values) instead of a bounded number per slack; for letters ≤ 3 the tail has to grow again.
- **Other closing rule.** `K` closes a block at the next letter ≤ 1; `Y` closes it at the next old prefix (y = 0), so blocks are
  longer and fewer prefixes carry a set. Sets carried at B = 14, any letters: `A4K` 576, `YA1` 71 (5 per slack), `Y` 30 (2 per
  slack: last letter 0 or 1). `Y` works through 20 for letters ≤ 3 and through 16 for any letters; `YA1` through 20 for any letters;
  none of the `Y` systems failed anywhere. With `K` the tail has to be as long as the largest letter (`A2K`, `A3K`, `A4K`
  for letters ≤ 2, 3, 4); with `Y` it does not grow in the tested range, and the sets become class-minus-thin. `KLO=0 ./types 16 Y`.

## 3. Not checked / open

- The sets for s ≤ 10 are a table (stable from bound 16 to 20), not a formula.
- OLD beyond slack 20 is sampled only, and by the k|k episode a new exception can appear with each longer staircase.
- Closure of J* under excursions is tested for short blocks only; no proof idea for it. A proof would need the image
  step_w(J*) for a general young word w, i.e. the description that §1 says is not local.
- The bounds D ≤ 4, 3, 3, 2, 3 are the largest that survived, not derived.
