# Delegation queue: side investigations for other agents

Hand this whole file to an agent (plus `claude/state.md` if it wants more background). Each task stands alone and can go to a separate sub-agent.

## How to report (read this first)

We do NOT want a pile of material to sift through. For each task, return **one** of these:

- **NOTHING** — one line. Use it whenever you found nothing that meets the bar. That's the expected outcome for most tasks, and it's fine.
- **HIT** — at most half a page:
  - the claim, stated precisely;
  - why it matters for the conjecture;
  - the evidence (proof sketch, citation with exact theorem number, or computation with exact n range);
  - one way we can check it ourselves in under 10 minutes.

**The bar for a HIT** is one of:
- a proof or disproof of the conjecture or of a stated sub-claim;
- a published theorem that directly implies the conjecture or a non-trivial special case;
- a computation that changes what we believe (a counterexample, or a pattern verified well beyond our current range);
- a technique shown to work on a closely analogous problem, together with a concrete reason it transfers.

"This paper seems related" or "this might be worth exploring" is NOT a hit. Do not summarize literature that doesn't meet the bar.

## Background (self-contained)

**The conjecture.** Bebeacua–Mansour–Postnikov–Severini (2005), Conjecture 5. It is still open as far as we know, and has been verified computationally through n = 22.

- Take an n×n permutation matrix with points (i, π(i)). Each point lies on the diagonal d = π(i) − i, which ranges over −(n−1)…(n−1).
- The x-ray is the vector counting points per diagonal. It is binary if no diagonal has two points.
- **Conjecture:** the binary x-rays are exactly the sets D of n diagonals such that s_k = d_k + n − k (with d_1 < … < d_n sorted) is a tournament score sequence, i.e. satisfies Landau's conditions: Σ_{i≤k} s_i ≥ C(k,2), with equality at k = n.
- Necessity is known. The open part is sufficiency: for every such D, find a permutation using each diagonal in D exactly once. We call such a permutation a **witness**, and W(D) is the number of witnesses.

**Known facts.**
- The fractional version is true (Li–Yao): a doubly stochastic matrix with diagonal sums 1 on D and 0 elsewhere always exists. So the question is purely whether an integral solution exists.
- If D has a tight cut (Landau equality at some k < n), it splits into two smaller instances, and their witnesses glue together. So only instances with no tight cut matter.
- Mirror symmetry d → −d (transpose) maps instances to instances.

**Stones picture** (the language we use). Treat D as n stones on marks −(n−1)…(n−1) of a plank.
- Start: stones on every other mark, which is the transitive tournament with exactly one witness.
- **Minimal move:** stones at a < b, where a+1 and b−1 are empty and every mark strictly between them is occupied, move to a+1 and b−1. (Moves with b = a+3 alone reach nothing from the start.)
- Proved: minimal moves from the start reach exactly the valid D. The move graph is graded by level = number of 3-cycles = C(n,3) − Σ C(s_k, 2).
- A stone's score is the number of empty marks to its left.
- Overhead view (board rotated 45°): each stone slides along its own diagonal. A witness is a choice of heights with no two stones on a common 45° line, i.e. stones at horizontal distance h must not be vertical distance h apart.

**Key computations so far** (exhaustive).
- W(after)/W(before) over all minimal moves has minimum exactly 2/3 for every n from 7 to 16. It is always attained by the local pattern ●●○●○●● → ●○●●●○● (one stone between the moving pair, and each moving stone has an outer neighbour).
- Every other move has ratio ≥ ~0.734: 0.75 (n = 11), ≈0.737 (n = 12, 13), ≈0.734 (n = 14–16).
- **Any** positive lower bound c on this ratio for all n would prove the conjecture: the start has a witness and every state is reachable.

## Tasks

### T1. Literature: integer analogues of Hall's theorem — DONE (2026-11-23, our own agent)
Nothing found. The one new lead is Brualdi–Fritscher, "Hankel and Toeplitz X-rays of permutations", LAA 449 (2014). It needs the full text.

### T2. Generating polynomial, Newton polytope, saturation — DONE
Saturation fails at n = 12. P_D is not log-concave or Lorentzian, and Gurvits' one-variable step fails at n = 5. Details are in state.md.

### T3. Combinatorial Nullstellensatz / Alon–Tarsi — DONE (ruled out; see state.md §5)

### T4. Local repair radius — DONE
The radius is 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5 for n = 4–14. From the best witness, ≤ 4 rows always suffice for n ≤ 12.

### T5. Push the ratio computation further — LOW (only report if something changes)
- The fast C counter enumerates permutations with distinct displacements by backtracking with bitmasks and hashes the displacement mask. It handles n = 15 in about 2.5 minutes on 2 cores; time grows about 8× per n.
- Run n = 16 and n = 17. n = 17 needs 64-bit masks.
- HIT only if:
  - the minimum ratio over minimal moves drops below 2/3; or
  - the minimum is attained by a move not of the pattern ●●○●○●● → ●○●●●○●; or
  - the best ratio among the other moves goes below 2/3.

### T6. Repair-radius definition — RESOLVED
Your numbers are right. Ours used only moves with no stones between the movers.

## Round 2 (2026-11-23): open exploration for Devin

Read `AGENTS.md`, `docs/claims-map-guide.md`, `docs/state.md` (§5 lists what's ruled out) and `map/graph.json` first. Reporting is the same: HIT or NOTHING per task. For exploration we will also accept a short **LEAD**: a precise statement, true on an exhaustive range you name, that is not on the map and that you think could carry a proof. One paragraph, plus a recheck command.

New since round 1:
- A minimal move adds exactly one 3-cycle, so the "layer" of D is t(D) − t(P_n), whatever the route (map: movecount).
- Both ends of the move order have explicit witnesses: P_n (fewest 3-cycles without a tight cut) and the centre C_n (most 3-cycles; F1 for n even, Skolem / hooked Skolem for n odd). Map: pn, centre.
- Near P_n, witnesses are P pieces stacked with short slides. A grammar of "stack with slide ≤ 2, plus widen points into blocks" covers everything up to 12 moves past P_n (n ≤ 9) but fails near the centre, first at C_6 (map: qn, ptwo, grammar). We don't want more operations bolted onto it.

### T7. One construction for both ends — OPEN
Find a single, motivated family of permutations (or a construction with one parameter) that gives P_n's witness at one end and C_n's at the other, and see how far it reaches in between. Lead: both witnesses are two interleaved step-2 staircases (F1 = 2 4 6 … 1 3 5, ascending; P_n descending plus two corner points). Report which no-tight-cut D (n ≤ 12) the family covers, as a function of the layer.

### T8. Free exploration — OPEN
Try anything not in state.md §5. Some directions we have not looked at: interleavings of two witnesses (columns of one piece alternate with another's); witnesses with a large symmetry group beyond involutions and half-turns; LLL / entropy compression; algebraic constructions mod n or mod 2n folded back (state §4.10); the matroid or polytope structure of the set of valid D; the literature on graceful labellings, Langford pairings and "perfect Skolem sets" beyond Nordh. Small exhaustive data first, then a precise claim.

### T9. Describe the alive sets of the interface machine — OPEN
Background: map cards interface, slackB, alivedom, alivebox; code agents/basket/alive.py (builds every distinct alive set for slack ≤ B; pickles alive4/6/8.pkl are in the repo), shape.py, twosided.py.
Known: alive sets are always symmetric under swapping rows and columns. They are not closed up or down under dominance, not intervals in the interleaved diagram, not boxes, and not determined by widths, heights and sizes (slack 8: μ = 422 alive, 431 dead with λ = ∅). Devin's invariant search showed the needed history grows with B.
Wanted: any exact description of the alive set as a function of the prefix that could support an induction over B, e.g. in terms of the last few shifts plus a statistic of (λ, μ) (contents, hook lengths, 2-quotients, Littlewood–Richardson / Schur-function coefficients, since the problem is a coefficient of m_δ²). Report a LEAD with the exact range checked, or NOTHING.
