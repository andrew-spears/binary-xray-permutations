# DEL0 at cuts of slack 2 — REPORT

DEL0: N(x 0 y) ≥ N(x y) whenever both words are legal (ZERO is the case where y starts with −1).

**HIT (a precise finite statement, tested, that gives DEL0 at slack 2; not a proof).** DEL0 at every cut of slack 2
follows from five linear inequalities S2 between the three numbers that describe a beginning at slack 2 (§1, the
implication is proved). S2 holds for all 33,975 beginnings with slacks ≤ 8 and length ≤ 12. Proved outright: the
implication, the slack-2 formulas, invariance of S2 under the letter 0, and DEL0 for cuts whose excursion above
slack 1 is (1, 0, …, 0, −1). **NOTHING** for an injection of the form "keep x, transpose y" (§3) and for the
hole-count refinements of general DEL0 (§4). What a proof needs at slack s: §5.

## 1. The slack-2 forms and the statement S2
States of slack 2 (row diagram | column diagram), after m stones (`python3 stones2.py` lists them and their stones):
(2|−): row m unused, row m+2 used; (11|−): row m−1 unused, row m+1 used; (1|1): row m and column m unused, row m+1
and column m+1 used; and the mirror images (−|2), (−|11). By transposition a beginning x is described by

    α = L_x(11|−) = L_x(−|11),    β = L_x(2|−) = L_x(−|2),    γ = L_x(1|1),

and the ending y by the same three numbers α', β', γ' of y* (y reversed and negated). The half-turn exchanges the
classes of α and β and fixes (1|1). The stones for a letter 0 are: from (11|−) one stone, to (−|2); from (2|−) two,
to (11|−) and to (1|1); from (1|1) two, to (11|−) and (−|11). Hence (proved by this list; `python3 slack2check.py 9` compares with brute force: 1,193 cuts, 329 followed by a 0,
0 mismatches)

    N(x y)   = 2αβ' + 2βα' + γγ'
    N(x 0 y) = 2αα' + 2ββ' + 2βγ' + 2γβ'
    N(x 0 y) − N(x y) = 2(α−β)(α'−β') + 4ββ' − (γ−2β)(γ'−2β'),

and the letter 0 acts by T₀(α, β, γ) = (β+γ, α, 2β). The difference is a form of signature (+, +, −), so some
inequality between α, β, γ is needed.

**S2.** For every legal beginning x that ends at slack 2 with last letter ≤ 1:

    γ ≤ 4β,    β ≤ 2α,    α ≤ β+γ,    γ ≤ α+β,    β ≤ α+γ.

**S2 ⇒ DEL0 at slack 2 (proved).** With P = α/β − 1, Q = γ/β − 2 the difference is ββ'·(2PP' + 4 − QQ'), and S2 says
that (P, Q) lies in the pentagon with vertices (−1/2, −3/2), (0, −2), (4, 2), (2, 2), (−1/2, −1/2). The form is affine
in each argument, so its minimum over two points of the pentagon is at a pair of vertices; the 15 values are ≥ 0,
with 0 only at (0, −2) twice (that is x = (1,1), y* = (1,1), where x y is not legal). (β = 0 forces α = γ = 0.)

**S2, tested.** `python3 slack2.py 8 12` (2.5 minutes, `out_slack2_8_12.txt`; `slack2.py 6 9` takes 2 seconds):
0 violations of each of the five inequalities on 33,975 beginnings (last letter 1: 9,910; 0: 11,532; −1: 8,420;
−2: 3,577; −3: 536). Each is an equality somewhere: γ = 4β at (2,1,0,0,−1,0); β = 2α at (2,1,0,0,−1); α = β+γ and
β = α+γ at (1,1); γ = α+β at (1,1,0). Two inequalities one might guess are false: α ≥ β fails after a negative last
letter (321 of 1,181 at slack ≤ 6, length ≤ 10, e.g. (2,1,0,0,−1): (α, β, γ) = (2, 4, 2)), and γ ≤ 2α fails at
(2,1,1,0,1,0,0,−1,−1,0,−1): (70, 106, 148).

**The triangle inequalities are an integer decomposition (tested).** u = (β+γ−α)/2, v = (α+γ−β)/2, w = (α+β−γ)/2
are nonnegative integers for every beginning at slack 2, any last letter (same run: 40,548 beginnings). In these coordinates
α = v+w, β = u+w, γ = u+v, T₀(u, v, w) = (w, 2u+w, v), a first arrival by the letter 2 from slack 0 is (1, 0, 0), by
the letter 1 from slack 1 it is (0, 0, 1), and

    N(x 0 y) − N(x y) = vv' + 5uu' + 2(vw' + wv') + 2(uw' + wu') − (uv' + vu')

has a single negative term. In terms of words: with a, b, c the numbers of ways to finish x by two stones on the
diagonals {2m, 2m+4}, {2m+1, 2m+3}, {2m+2, 2m+2} (the last one a repeated diagonal), a = 2α+γ, b = 2α+2β, c = 2β+γ,
and the triangle inequalities read  b ≤ 2a,  b ≤ 2c,  a + c ≤ 2b.

**Proved cases.** S2 is preserved by T₀: the image (β+γ, α, 2β) satisfies the five inequalities because the original
satisfies β ≤ 2α, α ≤ β+γ, γ ≤ α+β, β ≤ α+γ. The first arrival (1,1) gives (α, β, γ) = (1, 1, 0), which satisfies
S2. With the slack-1 lemma of COUNT_REPORT.md this proves DEL0 at a cut of slack 2 whenever the word stays at slack
2 between the last cut of slack ≤ 1 before the 0 and the first one after it, i.e. N(x 1 0^{k+1} −1 y) ≥ N(x 1 0^k −1 y).

## 2. What parametrises the cone at slack 2
By the slack-1 lemma the direction of (α, β, γ) depends only on the part of x after its last cut of slack ≤ 1.
That part is not a one-parameter family: it may climb to any slack and come back, and the cone keeps getting new
extreme rays (COUNT_REPORT §4). What is true is that it stays inside the pentagon S2, and all five sides are
touched. So the statement at slack 2 is: every return to slack 2 from above maps the pentagon into itself. A return
is a 3×3 nonnegative integer matrix M_e, one for each excursion e above slack 2; S2 for all x is the statement
that every M_e (and the arrivals from slack 0 and 1 over the top) preserves the pentagon.

## 3. "Keep x, transpose y" at slack 2: not defined at any state
The rule needs the 0-stone to lead from the state t after x back to t (then y is shifted) or to its mirror image
(then y is shifted and transposed). At slack 2 neither happens for any of the five states (list in §1): the
letter 0 always changes the class, α-states to β-states, β-states to α-states and (1|1), (1|1) to α-states. So
there is nothing to test to n = 10; the comparison at slack 2 is between different classes,

    2αβ' + 2βα' + γγ'  ≤  2αα' + 2ββ' + 2γβ' + 2βγ'.

Its first part is the rearrangement inequality (true when α−β and α'−β' have the same sign, which holds after a last
letter 0 or 1 but not after a negative one), its second part, γγ' ≤ 2γβ' + 2βγ', follows from γ ≤ 4β on both sides. An injection therefore has
to turn solutions ending in a β-state into solutions ending in an α-state of the same beginning, or the reverse,
depending on the last letter: it cannot be a fixed local rule on the y-part. "One stone inserted" was already
refuted (COUNT_REPORT §4).

## 4. Hole counts for DEL0 at general slack (tested, mostly NOTHING)
`python3 del0holes.py 10` (`out_del0holes_10.txt`), all DEL0 placements in words of length ≤ 10, classes by the
state after x; h_r, h_c = numbers of unused rows and columns among the first m.
- ZERO placements (1,447): h_r + h_c works (0 violations); h_r, h_c, (h_r, h_c), h_r − h_c all fail (18–20).
- other placements (4,721): nothing works: h_r and h_c fail in 2 ((1,1,0,0,0,1,0,0,−1,−2), the 0 at index 4,
  slack 2: 14 > 12), h_r + h_c in 23.
- The 0-stone either sits at (m+1, m+1), or fills a row hole (row ≤ m, column ≥ m+2), or a column hole; h_r + h_c
  changes by −1, 0 or +1 (−1 for the filled hole, +1 for each of row m+1, column m+1 that is still unused). No
  pattern "h ↦ h ± 1" survives, because the class sums at slack 2 are explicit:
  one hole: 2(α−β)(α'−β') + 2βγ';  two holes, i.e. the state (1|1): γ(2β' − γ').
- **Mechanism of the one true refinement.** For ZERO, y* ends with the letter 1, and then (α', β', γ') is
  proportional to (1, 1, 0) (proved: that 1 arrives from slack 1, and from each state of slack 1 it has one stone
  to an α-state and one to a β-state). The two class sums become 0 and 2γβ'. So at slack 2
  N(x 0 −1 y) − N(x −1 y) = 2γβ' = the number of solutions of x 0 −1 y whose state after x is (1|1): on the one-hole
  states "0 then −1" and "−1" give the same number, and (1|1) is the state where no stone for −1 exists. ZERO
  gains exactly where the −1 is blocked.

## 5. What a proof needs at slack s
1. The forms: N(x y) and N(x 0 y) as bilinear forms on the symmetric vectors of slack s (dimension 1, 3, 5, 11, 18).
2. A polyhedral cone K_s containing every L_x with last letter ≤ 1, on which the difference is ≥ 0 at all pairs of
   extreme rays (a finite check; done for s = 2 with the pentagon).
3. Invariance: every letter maps K_s into K_{s+e}. This couples all slacks; at slack 2 it is "every return from
   above preserves the pentagon". A proof needs the cones for all s at once, so a description uniform in s.
The integer coordinates u, v, w are the hint for such a description: they suggest that the placements at slack 2
split into three kinds of groups (3 placements in the states (2|−), (1|1), (−|2); 3 in (11|−), (1|1), (−|11); 4 in the
four one-hole states), and the letter 0 and both first arrivals are nonnegative in them. I did not find the rule
that forms the groups; finding it, or the analogue of a + c ≤ 2b ≤ 4·min(a, c) for three stones at slack 3, is the
next step.
