# HIT: a new proved family (letters ≤ 1, then a pyramid with letters in [−2, 2], then letters ≥ −1) by a parity transfer through a normal word; plain HYBRID is false (smallest word 2 1 0 −1 −2)

Continues `../l2sets/REPORT.md` (Theorem 0, Theorem 0′, BRIDGE) and `../oddsplit/REPORT.md`, `REPORT2.md` (Lemma R, Theorems E, A, B).
Throughout w = x m y is a valid word, m runs from the first letter ≥ 2 to the last letter ≤ −2, so x has all letters ≤ 1 and y all
letters ≥ −1 (x may contain −2, −3, …; y may contain 2, 3, …); s₁, s₂ are the slacks before and after m.
States are u = (λ|μ) = (M, B) as in `../l1sets/REPORT.md` §1; L_z(u) = the number of placements of a prefix z that end in the state u.

**Proved (by hand, §2–§4; no finite check is part of a proof):**
1. *Plain HYBRID is false.* w = m = 2 1 0 −1 −2 has s₁ = s₂ = 0, G(0) = conj G(0) = {∅|∅}, and the number of m-walks is the
   number of solutions, 6.
2. *Lemma O.* Every state with an odd number of placements of the prefix 1^s lies in G(s). These states are
   O(s) = {(λ|μ) : C(s, |λ|) f^λ f^μ odd}.
3. *Theorem T (transfer).* Let w₀ = 1^{s₁} m (−1)^{s₂} (the **normal word** of w; it is valid). If for some set S of stones **of m**
   and some rows R and columns C the number of solutions of w₀ with the stones of S in R × C is odd, then w is solvable.
   So an odd split of the normal word whose chosen stones lie in the middle solves every word with that middle and those two slacks,
   whatever x and y are. The same holds with 1^{s₁}, 1^{s₂} replaced by any z, z′ whose odd states lie in G ("normal prefixes").
4. *Theorem H.* **Every valid word x a b y with x letters ≤ 1, a ∈ {0, 1, 2}\*, b ∈ {0, −1, −2}\*, y letters ≥ −1 is solvable**,
   at every slack and for every depth of x and height of y. (Theorem A of oddsplit is the case x ∈ {0, 1}\*, y ∈ {0, −1}\*.)
   One stone of m sits on an explicit cell that depends only on (m, s₁, s₂).
5. *Theorem H2.* Every valid word x m y whose middle is m = a b, a ∈ {0, 1, 2}\*, b ∈ {0, −1, …, −4}\*, with
   **s₁ < T := Σ_{letters e ≤ −3 of b} (|e| − 2)** is solvable (two stones of m, Theorem B). Mirror: a ∈ {0, …, 4}\*, b ∈ {0, −1, −2}\*,
   s₂ < Σ_{e ≥ 3} (e − 2).

**Tested only (§5):**
- Plain HYBRID fails for 13,377 of the 13,387 valid words of length ≤ 12 that Theorem 0′ does not cover. The 10 words with an odd
  pair (u, v) all have (s₁, s₂) = (3, 3) and m = 2 1 0 −1 −2 or 2 1 0 0 −1 −2.
- Theorem T with extreme splits (Theorem E) of the normal word, S inside m: covers 13,263 of those 13,387 words (length ≤ 12), and
  34,297 of 34,677 at length 13. Least |S|: 1 exactly for the middles of Theorem H, else 2 for most, up to 7.
  First word not covered: 1 1 1 2 1 0 −1 −2 −3 (s₁ = 3 ≥ T = 1).
- With other normal prefixes z, z′ of length ≤ 5: 85 of the 124 left-over words of length ≤ 12 are covered; 39 words
  (13 pairs (s₁, m)) remain, smallest 1 3 2 1 0 −1 −2 (−1)⁴. (BRIDGE itself has no failure to length 13, l2sets.)
- Fixing one stone of m directly between G(s₁) and conj G(s₂) (no normal word): always possible for the middles of Theorem H
  (length ≤ 11), not in general (first failure 3 2 1 0 −1 −2 −3). Asking the other stones to be row-extreme is too strong
  (first failure 1 2 2 1 0 −1 −2 −2 −1).

**Not proved / not checked:** any rule naming S for a general middle (it would be RR restricted to normal words with S inside m,
and that restricted statement is false for z = 1^s alone); Theorem T for |S| ≥ 3 is used only in the tests; nobody else has read the proofs.
`../l2sets/bridge.py` is unchanged (its output is quoted in l2sets); `hybrid.py` is the same enumeration with the walks counted mod 2.

## 1. The middle as a placement problem; which u, v fit a given (R, C)
Coordinates relative to N = |x|, k = |m|. By the step rule (stone j of m goes to row j + κ + 1 for the new bead κ):
- rows used in u: R_u = {κ + 1 : κ ∈ M_u}; rows used in v after the k stones: R_v = {κ + k + 1 : κ ∈ M_v};
- free columns of u: X_u = {−y : y ∈ B_u}; of v: X_v = {k − y : y ∈ B_v}.

An m-walk u → v is a placement of the stones of m (diagonals 2j + m_j) on R × C, **R = R_v ∖ R_u, C = X_u ∖ X_v**, and it needs
R_u ⊆ R_v, X_v ⊆ X_u. Conversely, for a pair (R, C) with |R| = |C| = k that carries at least one placement:
- v is determined by u: v = (R_u ⊔ R, X_u ∖ C). So u fits iff **R ∩ R_u = ∅ and C ⊆ X_u**, and then slack(v) = s₂ automatically.
- The class of v is determined by the class of u and the parities of the elements of R and C (each stone adds one row and
  removes one free column; in the notation of L1 Lemma 1 a stone with odd letter sends c to 1 − c, one with even letter sends c to
  2 − c or −c according to the parity of its row). So "v central" is one parity condition on (R, C) for each class of u.
- Hence: (u, v) with u ∈ G(s₁), v ∈ conj G(s₂) exist for (R, C) iff some central u ∉ T(s₁) has its rows off R and its free columns
  over C, (R, C) has the parity that makes v central, and v ∉ conj T(s₂). T is thin, so apart from the parity this is a
  containment condition, as the task predicted.

I did not push this further, because the count on R × C for the **whole** middle is almost never odd (§2). With some stones of m
fixed, the rows and columns of the other stones are not named by the method below: Theorem T finds u and v by counting.

## 2. Plain HYBRID fails
For w = m = 2 1 0 −1 −2 the only pair is u = v = ∅|∅ and the number of walks is the number of solutions, 6. So HYBRID fails at
length 5, the first length where Theorem 0′ leaves a word. `hybrid.py 12` (the pairs (u, v) kept as a bit mask over G(s₁), xor
along m):

| n | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|
| words not covered by Theorem 0′ | 1 | 3 | 12 | 51 | 197 | 733 | 2,687 | 9,703 |
| no odd pair (u, v) | 1 | 3 | 12 | 51 | 197 | 733 | 2,686 | 9,694 |

The 10 exceptions have m = 2 1 0 −1 −2 or 2 1 0 0 −1 −2 with s₁ = s₂ = 3 (16 odd pairs each, 4 of them row-extreme, none with
hook states). This matches card `paritylr`: a count over all stones of a self-contained piece of board is almost always even;
parity only says something once a few stones are taken out. So the right statement fixes a few stones of m (HYBRID-RR, second form).

## 3. Lemma O and Theorem T
**Lemma O.** If L_{1^s}(u) is odd then u ∈ G(s).

*Proof.* s = 0 is clear. Let s ≥ 1, L_{1^s}(u) odd; so u ∈ F(1^s).
*Central.* By L1 Lemma 1 the letter 1 sends class c to 1 − c, and ∅|∅ has class 0; so every state of F(1^s) has class s mod 2.
*Not in SC.* A state of SC has no 1-predecessor (L1 §1), so it is not in F(1^s).
*Not in E⁰ (4 | s).* For the prefix 1^s the diagram θ of the parity theorem is s separate boxes, so
L_{1^s}(λ|μ) ≡ ⟨p₁^s, s_λ s_μ⟩ = C(s, |λ|) f^λ f^μ (mod 2) (`../unimodal/REPORT.md`, Corollary 1 and the line after it). For u ∈ E⁰ both Maya diagrams are unions of pairs {2i, 2i + 1}, i.e.
both diagrams are 2 × 2 blow-ups, and one of them, say of α with |α| = a ≥ 1, is nonempty. A box of α with hook h gives four
boxes with hooks 2h + 1, 2h, 2h, 2h − 1, so v₂(∏ hooks) = 2a + 2 v₂(∏_α h) and
v₂(f) = v₂((4a)!) − 2a − 2 v₂(∏_α h) = (3a + v₂(a!)) − 2a − 2(v₂(a!) − v₂(f^α)) = a − v₂(a!) + 2 v₂(f^α) ≥ (number of binary digits 1 of a) ≥ 1.
So L_{1^s}(u) is even.
*Not in A(4m² + 1).* Such a state has exactly one 1-predecessor and it is in E⁰ (L1 Lemma 4), so its count equals an even count. ∎

(`lemmao.py 24`: O(s) ⊆ G(s) for s ≤ 24, |O(s)| = 1, 2, 4, 8, 8, 16, 32, 64, 16, …; for s ≤ 9 the states with an odd path count
of 1^s are exactly O(s); f of a blown-up diagram is even for |α| ≤ 6.)

Call a sequence of letters z (diagonals 2j + z_j distinct) **normal** if every u with L_z(u) odd lies in G(slack z). Lemma O: 1^s is normal.

**Theorem T.** Let w = x m y be valid, x letters ≤ 1, y letters ≥ −1, and let z, z′ be normal with slacks s₁, s₂. Put
w₀ = z m (−reverse z′). If for a set S of stones of m and sets R, C of |S| rows and columns the number of solutions of w₀ with the
stones of S in the rows R and the columns C is odd, then w is solvable: there are u ∈ G(s₁), v ∈ conj G(s₂) and an m-walk
from u to v (with the stones of S on the same cells, counted from the first stone of m).

*Proof.* Cut every such solution of w₀ after z and after m. The number is Σ_{u, v} L_z(u) · W(u, v) · L_{z′}(conj v), where
W(u, v) is the number of m-walks from u to v with the stones of S in R × C, and the last factor is the number of completions of
v by −reverse z′ (mirror). The sum is odd, so some term is odd: L_z(u) odd, L_{z′}(conj v) odd, W(u, v) ≥ 1. By normality
u ∈ G(s₁) and conj v ∈ G(s₂). By Theorem 0 (l2sets, Corollary) G(s₁) ⊆ F(x), and by its mirror conj G(s₂) ⊆ A(y). States and
m-walks do not depend on the number of stones before m (§1), so the walk joins a placement of x to a completion by y. ∎

For z = 1^{s₁}, z′ = 1^{s₂} the word w₀ is valid: its slacks are those of w inside m, and 1 → m₁ ≥ 2, m_k ≤ −2 → −1 keep the
diagonals increasing. An odd split of oddsplit (Theorem E: L_S(R, C) and L_{S^c}(R^c, C^c) both odd) is a special case of the hypothesis.

## 4. Theorems H and H2
**Theorem H.** Every valid word w = x a b y with x letters ≤ 1, a ∈ {0, 1, 2}\*, b ∈ {0, −1, −2}\*, y letters ≥ −1 is solvable.

*Proof.* If w has no letter ≥ 2 before a letter ≤ −2, Theorem 0′ applies. Otherwise a contains a 2 and b a −2 (the letters ≥ 2 of y
come after every letter ≤ −2, and those ≤ −2 of x before every letter ≥ 2). Move the letters of a before its first 2 into x and
the letters of b after its last −2 into y; then m = a b is the middle of w, x still has letters ≤ 1 and y letters ≥ −1. The normal word w₀ = 1^{s₁} a b (−1)^{s₂} is valid and
satisfies the hypothesis of Theorem A (oddsplit) with k = the stone just before the first negative letter, which is a stone of m.
So the number of solutions of w₀ with stone k on the cell (p + q + 1, p + 1) is odd, and Theorem T applies with S = {k}. ∎

*The cell.* Let κ be the last stone of m before its first negative letter, p = #{0 in m before κ} + #{−2 in m after κ},
q = s₁ + s₂ + #{1 in m before κ} + #{−1 in m after κ}. Counted from the first stone of m (row and column |x| + ·) the stone κ is on
**(p + q + 1 − s₁, p + 1 − s₁)**; the column may be ≤ 0, i.e. a hole left by x. u and v are not named: the proof shows that the
number of pairs (u, v) ∈ O(s₁) × conj O(s₂) with an odd number of placements of the other stones is odd.
`thmh.py 11` checks exactly this for the 535 pairs (s₁, m) of the 2,084 words of the family with length ≤ 11: always odd, least value 1.

Examples not covered before (any slack is reached by lengthening): 1 1 1 1 0 −1 −2 2 1 0 −1 −2 −1 (a deep letter in x), and
1 1 2 1 0 −1 −2 3 2 1 0 (−1)⁸ (high letters in y).

**Theorem H2.** Let w = x m y be valid with middle m = a b, a ∈ {0, 1, 2}\*, b ∈ {0, −1, −2, −3, −4}\* containing a letter ≤ −3,
T = Σ_{e ≤ −3 in b} (|e| − 2), s₁ the slack before m. If s₁ < T then w is solvable. (Mirror: a ∈ {0, …, 4}\*, b ∈ {0, −1, −2}\*, s₂ < Σ_{e ≥ 3 in a} (e − 2).)

*Proof.* w₀ = 1^{s₁} a b (−1)^{s₂} is unimodal with rising part in {0, 1, 2}\* and falling part in {0, …, −4}\*, and its T is the T
above (the letters −1 add nothing). Theorem B gives an RR-split S = {k₁, k₂}: k₁ = the first k with P(k) ≥ T, where P(k) is the slack
after k stones, and k₂ = t + 1 or t + 2, t the stone before the first negative letter. P(s₁) = s₁ < T, so k₁ > s₁ is a stone of m (k₁ ≤ t). After its first
negative letter (a −1) b still reaches −3, so t + 1 and t + 2 are stones of m. Theorem T with S. The mirror statement is
the same for the mirrored word, since Theorems 0 and T are mirror-symmetric. ∎

(`thmh2.py 13`: 6,996 pairs (word of length ≤ 13, orientation) with such a middle and s₁ < T; Theorem B's two stones are an
RR-split of w₀ inside m in all of them.) The condition s₁ < T is needed for this choice: for 1 1 1 2 1 0 −1 −2 −3 (s₁ = 3, T = 1)
k₁ = 1 is a stone of the padding, and no extreme split of w₀ lies inside m.

## 5. Tests
**Extreme splits of the normal word inside m** (`normal.py`; Theorem E types RR, CC, RC, CR; all S ⊆ m):

| n | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|
| words not covered by Theorem 0′ | 1 | 3 | 12 | 51 | 197 | 733 | 2,687 | 9,703 | 34,677 |
| middle of Theorem H (least \|S\| = 1) | 1 | 3 | 11 | 41 | 140 | 454 | 1,434 | 4,424 | 13,403 |
| least \|S\| = 2 | 0 | 0 | 1 | 10 | 56 | 274 | 1,227 | 5,114 | 20,282 |
| least \|S\| ≥ 3 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 69 | 612 |
| none | 0 | 0 | 0 | 0 | 1 | 5 | 22 | 96 | 380 |

**The words left** (`normal2.py`, `fails.py`): at length ≤ 12 they are 124 words with 21 pairs (s₁, m); every m has depth or height ≥ 3.
- A prefix in {0, 1}\* with s ones has the same odd states as 1^s (same formula), so zeros in the padding change nothing.
- Other normal prefixes exist: of 728 prefixes with letters ≥ 0 and a letter ≥ 2 (length ≤ 6, slack ≤ 7) 114 are normal
  (`oddz.py 6 7`), e.g. (3), (5), (7), 3 3, 1 5, 2 1 2 1. With z, z′ of length ≤ 5: 8 of the 21 pairs get an extreme split
  (85 words), e.g. (s₁; m) = (3; 2 1 0 −1 −2 −3) with z = (3): the word 3 2 1 0 −1 −2 −3, S = {2, 7}, RR. Length ≤ 7 for z, z′
  adds nothing at n ≤ 11.
- Left: 13 pairs, 39 words: (1; 3 2 1 0 −1 −2), (4; 2 1 0 −1 −2 −3), (0; 2 3 2 1 0 −1 −2), (1; 3 2 1 0 0 −1 −2), (2; 3 2 1 0 −1 −2 −3),
  (4; 2 1 0 −1 −1 −2 −3), (4; 2 1 0 0 −1 −2 −3), (5; 2 1 0 −1 −2 −3 −2), (5; 2 1 0 −1 −2 −2 −3), (4; 2 2 1 0 −1 −2 −3 −3),
  (4; 3 2 1 0 −1 −2 −3 −4), (1; 4 3 2 1 0 −1 −2 −3 −3), (2; 3 3 2 1 0 −1 −2 −3 −4). For the last three no single stone of m on a cell gives
  an odd count between G(s₁) and conj G(s₂) either (`out/fails12.txt`, column P).
- Only extreme splits were tried; the exact parity of the normal word with |S| ≥ 2 stones on arbitrary rows and columns was not computed.

**One stone directly** (`hybrid1.py`; u ∈ G(s₁), v ∈ conj G(s₂), one stone of m on a cell, the others an odd number of ways):
no such choice for 1, 8, 42, 199, 895 words at n = 7, …, 11 (first 3 2 1 0 −1 −2 −3); for middles of Theorem H it always exists
(n ≤ 11). With the other stones row-extreme (first case of Lemma R): 1, 8, 43, 206, 931, and within Theorem H's middles 1, 7, 34 at
n = 9, 10, 11 (first 1 2 2 1 0 −1 −2 −2 −1). For m = 2 1 0 −1 −2 the number of odd (stone, cell, u, v) is 6, 40, 140 at s₁ = 0, 1, 2,
of which 6, 10, 10 are row-extreme: many candidates, and the extreme ones do not grow with the slack.

## 6. Answers to the three items
1. HYBRID as stated fails (§2). The version that works fixes stones of m: the rule is "take an odd split of the normal word
   1^{s₁} m (−1)^{s₂} with S inside m"; it names S and its cells from (m, s₁, s₂) alone, and x, y enter only through Theorem 0.
   Extreme shapes of the whole of (R, C) are not the point; extreme shapes for the two parts of the normal word are (Theorem E).
   Which u, v fit a given (R, C): §1.
2. Theorem H (the pyramid-like middle, one stone, board with holes) and Theorem H2 (Theorem B's two stones when s₁ < T) are proved.
3. Smallest failure of plain HYBRID: 2 1 0 −1 −2. Replacement: Theorem T. Its own first failure with z = 1^s and extreme splits is
   1 1 1 2 1 0 −1 −2 −3; other normal prefixes repair part of it. Cutting m further at letters 0, ±1 was not tried.

## 7. What a proof of the rest would need
- Theorem T reduces "every x, y" to one word per (m, s₁, s₂), but the split must avoid the padding. In Theorem B terms the first
  stone k₁ must come after the s₁ padding stones: the padding 1^{s₁} already carries the running sum past the target T.
  A padding that rises more slowly per stone is not available (the letters of x are ≤ 1 but the padding must be normal), so the
  open case is "large s₁ against a small T": deep middles entered at high slack.
- Normal prefixes other than 1^s: which z have all odd states in G? (s) for s = 3, 5, 7 are; a description of all of them, or of
  the set of odd states of a general prefix with letters ≤ 1, would say how much freedom the padding has.
- The 39 words above are the test set.

## 8. Recheck
```
cd agents/hybrid && sh runs.sh     # 40 seconds; outputs in out/
```
Longer runs kept in `out/`: `normal.py 13` (3 min), `normal2.py 12 5` and `fails.py 12` (1 min each).

| file | what |
|---|---|
| `hybrid.py N [v]` | plain HYBRID: odd pairs (u, v) for the whole middle |
| `lemmao.py S` | Lemma O |
| `thmh.py N`, `thmh2.py N` | Theorems H, H2 through their proofs |
| `normal.py N [v]` | extreme splits of the normal word with S inside m |
| `normal2.py N LZ`, `oddz.py LEN SMAX` | other normal prefixes |
| `hybrid1.py N [v] [uni]`, `fails.py N` | one stone of m on a cell, directly between G and conj G |
| `NOTES.md` | working notes |

## 9. Suggested cards
- green, child of `bridge`: Theorem H ("letters ≤ 1, then a rise in {0, 1, 2} and a fall in {0, −1, −2}, then letters ≥ −1: solvable").
- green, child of `bridge`: Theorem T with Lemma O ("an odd split of the normal word inside the middle solves every word with that middle").
- green: Theorem H2.
- red child of `bridge`: plain HYBRID (2 1 0 −1 −2, six walks between the only pair of states).
- red child of the Theorem T card: "the normal word 1^{s₁} m (−1)^{s₂} always has an extreme split inside m" (1 1 1 2 1 0 −1 −2 −3).
