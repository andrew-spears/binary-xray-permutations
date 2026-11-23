# HIT: every valid word with letters in {−1, 0, 1} is solvable, for every slack (proved: hand proof + two small finite checks)

**Proved.** There is an explicit family G(s) of interface states, depending on the slack s only, with
G(0) = {∅|∅} and G(s + e) ⊆ step_e(G(s)) for e = −1, 0, 1 and every s ≥ 0. Hence G(slack(x)) ⊆ F(x) for every prefix x
with letters in {−1, 0, 1}, and every valid word of the family L1 (card `l1`) has a permutation, for any slack; the
factor + − (two stones on one diagonal) is allowed too. The proof is an invariant / start / step induction; the step is a
case analysis on Maya diagrams (§2). Two finite sub-cases are done by a script on 4 explicit states each (`local.py`).
The proof is an algorithm: `solve.py` builds the permutation backwards.

**G(s) = Central(s) ∖ T(s).** Central(s) = one parity class (the 2-cores of the two diagrams have charges a, b with
a + b = s mod 2). T(s) is tiny: for 4 | s it is {(λ|λ′)} plus the family E⁰ of `../weights/REPORT2.md`; for s = 4m² + 1 it
is 4 states; otherwise empty. |G(s)| = 1, 2, 4, 8, 12, 24, 48, 80, 126, 212, 332, 512, 770, … (the sizes on card `l1`),
and G is the largest slack-only family (computed for slack ≤ 17).

**Tested only (item 1, exact description, slack ≤ 16):** F(x) = {all states whose class a + b lies in Γ(x)} minus the
(λ|λ′) if x ends in +, with 6 exceptional sets; Γ(x) follows a three-line rule; there are only 70 distinct sets F(x).

**Not checked:** the hand proof has not been read by anyone else. Nothing here is about letters ±2 beyond §5 (no such family exists there).

## 1. Coordinates and the family

Notation as in `../weights/REPORT3.md` (Lemma 1). A state after n stones is (λ|μ); put ν = μ′ and
**M = M(λ), B = M(ν)** (M(λ) = {λ_i − i}, "beads"; charge 0). The state is the pair u = (M, B); slack = |λ| + |ν|.

- **Step.** Letter e: M′ = (M − 1) ∪ {k}, B′ = (B + 1) ∖ {k + 1 − e}, for any k ∉ M − 1 with k + 1 − e ∈ B + 1.
  (Stone N = n + 1 in row N + k + 1, column 2N + e − row.)
- **Predecessors.** The e-predecessors of u are t_k = ((M ∖ k) + 1, (B ∪ {k + 1 − e}) − 1), one for each
  **k ∈ M with k + 1 − e ∉ B**. (`check.py`, part 2: this is the machine of `../weights/maya.py`.)
- **Class.** a = c₀(λ), b = c₀(ν) = c₀(μ), where c₀ = #{even beads ≥ 0} − #{even holes < 0} (2-core charge), c = a + b.
  The pair (a, b) is the parity class (D, K) of cards `paritycount` / REPORT3; it does not depend on n.
  **Central(s) = {slack s, c = s mod 2}.**
- **SC** = {M = B} = {(λ|λ′)}: the states with no 1-predecessor (REPORT2 §3). Central SC states exist only for 4 | s.
- **E⁰** = {M and B are unions of pairs {2i, 2i+1}, and M = (B − 2) ⊔ one more pair} (the diagrams 2ν2 of REPORT2,
  Theorem 2; slack ≡ 0 mod 4, class 0): −|22, 22|− ; −|44, 44|− ; −|66, 22|2222, 2222|22, 66|− ; …
- **A(4m² + 1)**, m ≥ 1 = {central u all of whose 1-predecessors are in SC ∪ E⁰}. Lemma 4: these are 4 states
  (Q ⊔ {κ}, Q ⊔ {y}): Q a union of pairs {2i−1, 2i} coming from a 2-core, {κ, y} one more such pair; λ and μ′ differ by one box.
  m = 1: 2|111, 11|3, 3|11, 111|2; m = 2: 422|33111, 3311|522, 522|3311, 33111|422.
- **T(0) = ∅; T(s) = SC ∪ E⁰ if 4 | s, s > 0; T(4m² + 1) = A(4m² + 1); T(s) = ∅ otherwise. G(s) = Central(s) ∖ T(s).**

**Theorem.** For e ∈ {−1, 0, 1} and s, s − e ≥ 0: every u ∈ G(s) has an e-predecessor in G(s − e).

**Corollary 1.** If x ∈ {−1, 0, 1}^n has all partial sums ≥ 0 and sum s, then every state of G(s) is in F(x).
*Proof.* Induction on n. x = x′e, u ∈ G(s): take t ∈ G(s − e) from the Theorem. The slack of t is at most the number
of + in x′, so both diagrams of t have at most n − 1 rows and t is a state with n − 1 stones; t ∈ F(x′), and the step
places stone n in a new row ≥ 1 and a new column ≥ 1 with sum 2n + e. ∎

**Corollary 2 (L1).** Every word in {−1, 0, 1}^n with partial sums ≥ 0 and sum 0 has a permutation σ with
{k + σ(k)} = {2k + x_k} (as multisets): G(0) = {∅|∅} ⊆ F(x), i.e. rows and columns 1..n are used. ∎

**Corollary 3 (universal states, item 2).** For every cut x | y of a valid L1 word at slack s, every state of
G(s) ∩ conj G(s) = Central(s) ∖ (T(s) ∪ conj T(s)) lies in F(x) ∩ A(y) (Central is closed under conj: c₀(λ′) = c₀(λ)).

## 2. Proof of the Theorem

Window counts: in [−2L, 2L), L large, a charge-0 diagram M has L + a even and L − a odd beads.

**Lemma 1 (counts and classes).** Let u have class c.
- e = 0: the predecessors with k even have class 2 − c and there are at least c of them; those with k odd have class −c
  and there are at least 1 − c of them.
- e = ±1: every predecessor has class 1 − c. For e = −1 there are at least 2; for e = 1 there are |M ∖ B|, none iff u ∈ SC.

*Proof.* Even k ∈ M with k + 1 ∈ B: at most L − b (odd beads of B), so at least (L + a) − (L − b) = c have k + 1 ∉ B.
Odd k: k + 1 runs over the even numbers of [−2L + 2, 2L], of which L + b − 1 are in B: at least (L − a) − (L + b − 1).
e = −1: M has 2L beads in the window, B has 2L − 2 in the window shifted by 2. Classes: for a diagram S let
ε(S) = #even − #odd beads in the window (= 2a for charge 0). Then ε(S ± 1) = 1 − ε(S), removing k changes ε by −1
(k even) or +1 (k odd), adding does the opposite. So a_t = 1 − a (k even), −a (k odd); b_t = −b (y = k + 1 − e even),
1 − b (y odd). ∎

So a central state has a central predecessor under every letter (e = 0: c = 0 uses odd k, c = 1 uses even k), unless
e = 1 and u ∈ SC. All that is left is to avoid T. Call a predecessor *bad* if it is in T. "oe-pair" = {2i − 1, 2i},
"eo-pair" = {2i, 2i + 1}. If t_k ∈ E⁰ then (M ∖ k) + 1 and (B ∪ {y}) − 1 are unions of eo-pairs, so
**(∗) Q = M ∖ k and Q′ = B ∪ {k + 1 − e} are unions of oe-pairs**, and Q = (Q′ − 4) ⊔ one oe-pair.

**Lemma 2 (at most one bad predecessor into SC ∪ E⁰).** For any state u:
(a) e = −1: no predecessor is in SC, at most one is in E⁰.
(b) e = 1: at most one predecessor is in SC ∪ E⁰.
(c) e = 0: at most one predecessor with k odd is in SC ∪ E⁰.

*Proof.* *Two in E⁰ (all e).* If t_k, t_j ∈ E⁰, k ≠ j, then by (∗) j lies in a pair of M ∖ k, whose other element is in
M ∖ j while j is not: M ∖ j is not a union of pairs. For e = 0 one can also say: (∗) gives k + 1 ∉ M for odd k.
*SC.* t_k ∈ SC iff M ∖ k = (B ∪ {y}) − 2, y = k + 1 − e. e = −1: the right side contains k: impossible.
e = 1: iff M = (B − 2) ⊔ {k − 2, k}; e = 0: iff M = (B − 2) ⊔ {k − 1, k}. In both cases M ∖ (B − 2) determines k.
*One SC (k), one E⁰ (j), e = 1.* M = Q ⊔ {j} with Q a union of oe-pairs, so j is the only element of M whose partner is
missing ("loner"). Also M = ((Q′ − 2) ∖ {j − 2}) ⊔ {k − 2, k} with Q′ = B ∪ {j}. If j ≠ k + 2: the partner of j − 2
and k are two loners (the partner of k cannot be in Q′ − 2, else k would be). If j = k + 2:
M = (Q′ − 2) ⊔ {k − 2} and the only loner is k − 2 ≠ j. Contradiction.
*One SC (k), one E⁰ (j), e = 0, k, j odd.* M = Q ⊔ {j}; M = ((Q′ − 2) ∖ {j − 1}) ⊔ {k − 1, k}, Q′ = B ∪ {j + 1}. The
partner j − 2 of j − 1 is a loner different from j unless j − 1 is put back, i.e. k = j. ∎

**Lemma 3 (unique bad central predecessor, e = 0, class 0).** Let u be central of class 0 with exactly one predecessor t_k, k odd.
(a) If t_k ∈ SC then u ∈ E⁰. (b) If t_k ∈ E⁰ then u ∈ SC. Conversely every u ∈ E⁰ has exactly one such predecessor, and it is in SC.

*Proof.* (a) M = (B − 2) ⊔ {k − 1, k}, k + 1, k + 2 ∉ B, and every odd j ∈ M, j ≠ k has j + 1 ∈ B. Such j is in B − 2,
so j − 1 ∈ M. An odd b ∈ B has b − 2 ∈ M odd, ≠ k, so b − 1 ∈ B. So in M and in B every odd bead has the even bead
below it. The number of even beads without the odd one above is 2a in M and 2b in B, both ≥ 0, and a + b = 0: none.
So M, B are unions of eo-pairs. (b) By (∗) k + 1 ∉ M, k ∈ B. Uniqueness: odd j ∈ Q has j + 1 ∈ B ⊆ Q′, so Q ⊆ Q′;
the charges are −1 and +1, so Q′ = Q ⊔ {k, k + 1} and B = Q′ ∖ {k + 1} = Q ⊔ {k} = M. Converse: for u ∈ E⁰ with new
pair {p, p + 1}: an odd k ∈ M other than p + 1 is in B − 2, so k + 1 ∈ B; and t_{p+1} ∈ SC. ∎

**Lemma 4 (the family A).** Let u be central of odd slack s + 1 ≥ 5 with all 1-predecessors in SC ∪ E⁰. Then u has exactly
one predecessor t_k, t_k ∈ E⁰, and M = Q ⊔ {k}, B = Q ⊔ {y}, where {k, y} is an oe-pair and Q = oe-pairs(Q°) for a
2-core diagram Q° (closed under −2), the pair {k, y} sitting two places above a top of Q°. The slack is 4m² + 1, where
Q° and Q° ⊔ {pair} are the staircases δ_{m−1}, δ_m in some order. So |A(4m² + 1)| ≤ 4 and no such u exists at other slacks.

*Proof.* u ∉ SC (class 1 is odd), so by Lemma 2(b) M ∖ B = {k}. If t_k ∈ SC: (B − 2) ⊔ {k − 2} ⊆ B, so B and
M = (B ∖ y) ∪ k are closed under −2: λ, ν are 2-cores with neighbouring charges and a + b = 1, i.e. ∅ and (1): slack 1.
So t_k ∈ E⁰. By (∗) Q = M ∖ k and Q′ = B ∪ k are unions of oe-pairs; M ∖ B = {k} gives Q ⊆ Q′, and Q′ ∖ Q = {k, y} is one
pair. In pair indices Q° = ((Q° ⊔ {i₀}) − 2) ⊔ {p}: Q° − 2 ⊂ Q° and i₀ − 2 is a top. The predecessor is
(2κ2 | …) for the two neighbouring 2-cores κ = δ_j, δ_{j±1}, of slack 4(T_j + T_{j±1}) = 4 max² . ∎

**Lemma 5 (out of A).** Let a = (Q ⊔ {κ}, Q ⊔ {y}) ∈ A(4m² + 1), Q° ≅ δ_i (i = m − 1 or m).
(a) a has exactly one (−1)-successor, ((Q ⊔ {κ, y}) − 1, Q + 1), and it is in E⁰.
(b) Every 1-successor of a has at least 2i ≥ 2m − 2 predecessors under 1.
(c) Every central 0-successor of a has at least i ≥ m − 1 central predecessors under 0.

*Proof.* (a) k ∉ M_a − 1 and k + 2 ∈ B_a + 1 iff k + 1 ∈ B_a ∖ M_a = {y}. (b) The successor through k has
M_u ∖ B_u = {k} ∪ ((M_a − 1) ∖ (B_a + 1)) ⊇ {k} ∪ ((Q − 1) ∖ ((Q + 1) ∪ {y + 1})), and |Q ∖ (Q + 2)| = 2i (the i top
beads of the staircase have a hole below). (c) Central predecessors of u are the even j ∈ M_u with j + 1 ∉ B_u (Lemma 1,
c = 1); k is one, and so is every even j ∈ (Q − 1) ∖ (Q ∪ {y}): these are the lower elements 2q − 2 of the pairs of
Q − 1 with q − 1 ∉ Q°, i of them, minus at most one. ∎

**Proof of the Theorem.** Let u ∈ G(s′), letter e, source slack s = s′ − e. By Lemma 1 the central predecessors
exist (for e = 1: u ∉ SC because central SC states have 4 | s′ and are in T). If T(s) = ∅ we are done. Otherwise:
- **s = 0.** T(0) = ∅ by definition; ∅|∅ → ∅|∅ (letter 0), ∅|∅ → 1|−, −|1 (letter 1), and back (letter −1).
- **4 | s, e = −1.** Lemma 2(a): ≥ 2 predecessors, at most one bad.
- **4 | s, e = 1.** Lemma 2(b): at most one bad. If u has only one predecessor and it is bad then u ∈ A(s + 1) = T(s + 1) (Lemma 4).
- **4 | s, e = 0.** Class 0, predecessors with k odd, at most one bad (Lemma 2(c)). If there is only one and it is
  bad, then u ∈ E⁰ or u ∈ SC (Lemma 3): u ∈ T(s).
- **s = 4m² + 1, e = −1.** If all predecessors of u are in A then u is the successor of Lemma 5(a): u ∈ E⁰ ⊆ T(s − 1).
- **s = 4m² + 1, e = 1.** If all 1-predecessors of u are in A, then 2m − 2 ≤ |A| ≤ 4 (Lemma 5(b), Lemma 4): m ≤ 3.
  For m ≤ 3 `local.py` checks all 12, 20, 28 successors.
- **s = 4m² + 1, e = 0.** If all central predecessors of u ∉ A are in A, then m − 1 ≤ 4: m ≤ 5; `local.py` checks m ≤ 8. ∎

The exceptional chain is SC →(0) E⁰ →(+) A →(−) E⁰, and it closes up; this is why T stays small.

## 3. Checks (all in `runs.sh`, about 1 minute)

| script | what | result |
|---|---|---|
| `check.py 18 12` | Central(s) ∖ T(s) = largest slack-only family inside slack ≤ 18 (greatest fixed point), s ≤ 17 | equal for every s; sizes as above |
| | Lemma 1, Lemma 2 on all 3,131 states of slack 1..12; Lemma 3(a), (b) on the 933 central ones with 4 \| s | no exception |
| | step and predecessor formulas of §1 against `../weights/maya.py`, slack ≤ 9 | equal |
| `local.py 8` | A(4m² + 1) for m ≤ 8 (slack ≤ 257): 4 states, one predecessor, in E⁰; Lemma 5; the two finite cases of the proof | ok; least counts 2m and m |
| `solve.py all 13` | the algorithm on every valid word of length ≤ 13 (41,835 at n = 13; 5,373 without + −) | all solved, permutation verified |
| `solve.py random 300 400 7` | 300 random words, length ≥ 400, largest slack 193, random choice among good predecessors | all solved |

`fam.py S`: the largest family also equals the intersection of F(x) over all L1 prefixes, and over all words in {0, 1}*
(slack ≤ 10). So for L1 "the states every prefix reaches" is exactly G(s).

## 4. Item 1: the exact shape of F(x) (tested, slack ≤ 16; `desc.py 16`, `auto.py 16`)

Proved part: F(x) ⊆ Sat(s, Γ(x)) := {slack s, class c ∈ Γ(x)} by Lemma 1, where
Γ(∅) = {0}; Γ(x+) = 1 − Γ; Γ(x−) = (1 − Γ) ∩ feas(s − 1); Γ(x0) = (−Γ ∪ (2 − Γ)) ∩ feas(s);
feas(s) = {c ≡ s mod 2 : m(m − 1) ≤ s, m = max(c, 1 − c)} (the least slack of a pair of 2-cores with a + b = c is
m(m − 1) or m(m − 1) + 1). In γ = (−1)^n (c − ½): odd letters fix γ, a zero moves it by ±1, the slack bounds |γ|.
Γ(x) always contains the central class. And F(x+) contains no (λ|λ′).

Tested: inside slack ≤ 16 there are only **70 distinct sets F(x)** over all L1 prefixes (`out_auto_16.txt` lists them
with their transitions), and
**F(x) = Sat(s, Γ(x)) ∖ SC if x ends in +, and F(x) = Sat(s, Γ(x)) otherwise**, except for 6 sets:
F(1^s 0) for s = 4, 8, 12, 16 (minus E⁰, REPORT2 Theorem 2) and two sets at slack 5 (after ++++0+ and ++++0+0).
The Γ rule is exact on all 202 transitions. So the answer to "is F(x) the D-class and K-class condition minus an explicit
family" is yes in this range, with the class a + b (K is not restricted at all inside a class), and "containment" plays no role.
I did not prove the lower bound for the non-central classes.

## 5. Item 3: letters in {−2, …, 2} (`l2.py 9`)

- No slack-only family and no family depending on (slack, last letter) exists inside slack ≤ 9 (both greatest fixed points
  are empty; card `l1` says the same for slack + last two letters). There are 376 distinct (F, slack, last letter) inside slack ≤ 9; L1 has 37 distinct (F, slack) inside slack ≤ 10.
- What breaks in the proof is Lemma 1. A letter ±2 acts on classes like a zero (c → −c or 2 − c), but the counts are only
  ≥ c − 1 and ≥ −c for the letter 2: a central state need not have any predecessor. F(2) = {2|−, 1|1, −|2} already
  misses the central states 11|−, −|11. The states with no 2-predecessor are M ⊂ B + 1 (μ′ = λ plus a rim hook):
  2, 4, 5, 6, 10, 12, 15, 20 states for slack 2..9, in several classes; for the letter 1 it is SC: 1, 2, 3, 5 states at even slack.
- The intersections of F(x) by (slack, last letter) stay non-empty (≥ 3 states, slack ≤ 9), as known from `agents/majority`.

## Recheck
    cd agents/l1sets && sh runs.sh        # about 1 minute; outputs out_*.txt
    python3 solve.py + + 0 - 0 + - -      # one word -> permutation [5, 1, 2, 3, 8, 4, 6, 7]

Files of this report: `l1.py` (machine on (λ, μ′), SC, E⁰, A, T), `check.py`, `local.py`, `solve.py`, `fam.py`, `fsets.py`,
`cores.py`, `auto.py`, `desc.py`, `l2.py`; `PROOFNOTES.md` = working notes in order of discovery. The files already in this
folder (`NOTES.md`, `sets.py`, `classes.py`, `full.py`, `par.py`) are untouched; `NOTES.md` items 1, 2, 4 (few sets, the mod 4
effect, predecessors by pigeonhole, p(m) states without a + predecessor) are the observations that §1–§4 explain.
Suggested card change (not made; `map/build.py` untouched): `l1` proved, with the family G(s) as invariant, ∅|∅ as start,
the Theorem as step.
