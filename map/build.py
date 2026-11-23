"""Generates graph.json (the claims map). Rules: docs/claims-map-guide.md.
Every node's `statement` is one precise claim; `intuition` is exposition that ends with that claim in plain words."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

areas = [
    {"id": "families", "label": "Decomposition & families"},
    {"id": "moves", "label": "Moves"},
    {"id": "peeling", "label": "Peeling & parity"},
    {"id": "algebra", "label": "Fractional & algebraic"},
    {"id": "ideas", "label": "Other routes"},
]

def N(id, area, title, status, statement, intuition="", pics=None, example="", evidence="", refs="", active="", vis=None):
    d = {"id": id, "area": area, "title": title, "status": status}
    if intuition: d["intuition"] = intuition
    if pics: d["pics"] = pics
    d["statement"] = statement
    for k, v in (("example", example), ("evidence", evidence), ("refs", refs), ("active", active), ("vis", vis)):
        if v: d[k] = v
    return d

def board(n=None, rows=None, cols=None, D=(), pts=(), cap="", **kw):
    b = {"t": "board", "rows": list(rows or range(1, n + 1)), "cols": list(cols or range(1, n + 1)), "D": list(D)}
    if pts: b["pts"] = [list(p) for p in pts]
    if cap: b["cap"] = cap
    b.update(kw); return b
def perm(p, rows=None):
    rows = rows or range(1, len(p) + 1)
    return [[r, c] for r, c in zip(rows, p)]
def stones(D, lo, hi, hl=(), cap=""):
    s = {"t": "stones", "lo": lo, "hi": hi, "D": list(D)}
    if hl: s["hl"] = list(hl)
    if cap: s["cap"] = cap
    return s
def pair(a, b, mid="→", cap=""):
    p = {"t": "pair", "a": a, "b": b, "mid": mid}
    if cap: p["cap"] = cap
    return p

D2413 = [-2, -1, 1, 2]
half_cells = [(1,6),(1,7),(2,7),(2,8),(3,1),(3,5),(4,1),(4,2),(5,2),(5,5),(6,6),(6,8)]
PEELB = dict(rows=[1, 2, 3, 4, 5], cols=[1, 3, 4, 5, 6], D=[-2, -1, 0, 3, 4], holes=[2])

nodes = [
    # ================= goal =================
    N("conj", "goal", "The conjecture: Landau ⇒ binary x-ray", "open",
      "Let D = {d₁<…<dₙ} be n distinct diagonals (d = column − row) of the n×n board, and s_k = d_k + n − k. If s satisfies Landau (Σ_{i≤k} s_i ≥ C(k,2) for all k, with equality at k = n), then some permutation uses each diagonal of D exactly once (a witness). Necessity is proved: the points on the k lowest diagonals sit in k different rows and columns, so their diagonals sum to at least (k leftmost columns) − (k bottom rows). BMPS 2005 Conj. 5 = Nordh 2008 Conj. 10.",
      "Put n stones on a plank with marks −(n−1) … n−1, at most one per mark; the start has a stone on every other mark. A stone's score is the number of empty marks to its left. Landau's condition says that, for every k, the k leftmost stones have at least as many empty marks to their left in total as at the start, with equality for all n stones: no group of left stones has drifted left, and the whole is balanced. A witness is a board with one point in each row and column whose points sit on exactly the stones' diagonals. The four-views tab shows the same question as stones, grid, matching and Skolem arcs. Claim: every arrangement satisfying Landau's condition has a witness.",
      [stones([-3, -1, 1, 3], -3, 3, cap="Start: 4 stones on every other mark"),
       board(4, D=D2413, pts=perm([2, 4, 1, 3]), cap="The arrangement {−2, −1, +1, +2} and a witness, 2 4 1 3")],
      evidence="Exhaustively verified for n ≤ 22 (Devin round 1). Open as of 2026.",
      refs="Bebeacua–Mansour–Postnikov–Severini 2005; Nordh, Perfect Skolem sets, Discrete Math 308 (2008); Brualdi–Fritscher, Hankel and Toeplitz X-rays of permutations, LAA 449 (2014) (not yet read)",
      vis={"file": "labs/views.html", "title": "Four equivalent views"}),
    N("notight", "goal", "The conjecture for arrangements with no tight cut", "open",
      "Every valid D whose Landau inequalities are strict for every k < n has a witness.",
      "A tight cut is a place on the plank where the stones to its left have exactly as many empty marks to their left as at the start: that group hasn't drifted right at all. Arrangements with no such place are the core case. Claim: every valid arrangement with no tight cut has a witness.",
      [pair(stones([-5, -3, -1, 1, 3, 5], -5, 5, cap="start"), stones([-4, -3, -2, 2, 3, 4], -5, 5, cap="tight cut in the middle"), "→"),
       stones([-4, -3, 0, 1, 2, 4], -5, 5, cap="No tight cut: {−4, −3, 0, +1, +2, +4}")]),
    N("tightcut", "goal", "Tight cuts split", "proved",
      "If Σ_{i≤k} s_i = C(k,2) for some k < n, then D_low = {d₁…d_k} + (n−k) and D_high = {d_{k+1}…d_n} − k are valid at sizes k and n − k, and if both have witnesses, so does D (their skew sum).",
      "If the left k stones haven't drifted at all, their points are squeezed into the bottom-left k×k corner of the board, and the other points into the top-right corner. Each corner is a smaller board of the same kind. Claim: a tight cut splits the arrangement into two smaller valid ones, and solutions of those two drop into the corners to solve the whole.",
      [board(6, D=[-4, -3, -2, 2, 3, 4], pts=perm([4, 6, 5, 1, 3, 2]), blocks=[[4, 6, 1, 3], [1, 3, 4, 6]],
             cap="{−4,−3,−2,+2,+3,+4}: tight cut after three stones; two 3×3 corners")]),

    # ================= decomposition =================
    N("inflation", "families", "Block layouts glue solutions", "proved",
      "Let D split into groups G₁…G_k of sizes n_i with integer means c_i. If each G_i − c_i has a witness, and there are an order of the groups by rows and an order by columns (a permutation σ) with c_i = (total size of the groups before i in the column order) − (total size of the groups before i in the row order), then D has a witness (the inflation σ[π₁,…,π_k]).",
      "Cut the board into a grid of blocks. A small permutation σ picks one block in each block-row and block-column, and each picked block holds a smaller solved board. Every point in a block is shifted by the same amount, the block's offset: the column it starts in minus the row it starts in. On the plank, a block is a group of stones that is a shifted copy of a smaller arrangement, centred at the block's offset. In the picture, σ = 2413 holds blocks of sizes 1, 1, 3, 1, and the 3×3 block carries the solution 321 of {−2, 0, +2}, shifted by −2. Claim: if the stones split into groups, each group (recentred) has a solution, and the group sizes and centres fit some block layout, then the whole arrangement has a solution.",
      [board(6, D=[-4, -2, -1, 0, 3, 4], pts=perm([4, 6, 3, 2, 1, 5]), blocks=[[1, 1, 4, 4], [2, 2, 6, 6], [3, 5, 1, 3], [6, 6, 5, 5]],
             cap="π = 4 6 3 2 1 5: σ = 2413 with blocks of sizes 1, 1, 3, 1"),
       stones([-4, -2, -1, 0, 3, 4], -5, 5, hl=[-4, -2, 0], cap="Groups: {−4, −2, 0} around −2 (the 3×3 block), and {−1}, {+3}, {+4} alone")]),
    N("directsum", "families", "Direct sums glue (Nordh Thm 27)", "proved",
      "If π₁ witnesses D₁ (size n₁), π₂ witnesses D₂ (size n₂), and D₁ ∩ D₂ = ∅, then π₁ ⊕ π₂ witnesses D₁ ∪ D₂.",
      "Two solved boards placed corner to corner along the main diagonal make a bigger board whose points keep their diagonals. Unlike a tight cut, the two sets of stones can interleave on the plank, so the result can have no tight cut. Claim: two solved boards with disjoint diagonal sets combine this way into a solution of the union.",
      [board(5, D=[-2, -1, 0, 1, 2], pts=perm([2, 1, 5, 4, 3]), blocks=[[1, 2, 1, 2], [3, 5, 3, 5]], cap="21543 = 21 ⊕ 321: {±1} and {−2, 0, +2} interleave")],
      refs="Nordh 2008, Thm 27"),
    N("fixedpoint", "families", "Fixed-point reduction", "proved",
      "If 0 ∈ D and D ∖ {0} has a witness at size n − 1, then D has a witness with π(1) = 1.",
      "A stone on the middle mark can go in the top-left corner: that uses row 1 and column 1 and changes no other cell's diagonal. Claim: if the other stones form a solvable arrangement one size smaller, the whole arrangement is solvable with that corner point.",
      [board(5, D=[-2, -1, 0, 1, 2], pts=perm([1, 3, 5, 2, 4]), blocks=[[2, 5, 2, 5]], cap="Corner point on diagonal 0; the 4×4 board below uses {±1, ±2}")]),
    N("decomp", "families", "Every arrangement but P_n splits into blocks", "empirical",
      "For n ≥ 4, every valid no-tight-cut D other than P_n splits into k < n groups satisfying the hypotheses of the block-layout lemma: integer means c_i, each G_i − c_i valid at its size, and the layout of sizes and centres realizable by some σ.",
      "To split an arrangement, partition its stones into groups that each balance around a whole-number centre, such that each group moved back to the middle is a valid smaller arrangement, and the group sizes and centres can be laid out as blocks. In the example, {−3, −2, −1, 0, +2, +4} splits as {−3, −1} around −2, {−2, 0} around −1, and {+2}, {+4} alone; the layout 2413 with block sizes 1, 1, 2, 2 puts every block at its centre. Both choices — the grouping and the layout — are searches, and the layout is itself a placement puzzle with wide blocks of the same total size. So this claim is not a reduction to smaller cases: the blocks are smaller, but the layout is not, and the claim is at least as strong as the conjecture. Claim: every valid arrangement with no tight cut except P_n splits this way.",
      [stones([-3, -2, -1, 0, 2, 4], -5, 5, cap="Grouped: {−3,−1} around −2, {−2,0} around −1, {+2}, {+4}"),
       board(6, D=[-3, -2, -1, 0, 2, 4], pts=perm([3, 6, 2, 1, 5, 4]), blocks=[[1, 1, 3, 3], [2, 2, 6, 6], [3, 4, 1, 2], [5, 6, 4, 5]], cap="The layout: pattern 2413, block sizes 1, 1, 2, 2")],
      evidence="Exhaustive for 4 ≤ n ≤ 12: exactly one no-tight-cut D per n fails, P_n (up to mirror, out of 1, 3, 5, 15, 36, 107, 306, 969, 3055). Checked through witnesses (D splits iff some witness is not a simple permutation), so it relies on the conjecture at those sizes, which is verified. The layout can need up to n − 1 blocks.",
      refs="Prime agent 2026-11-22, /home/claude/agents/prime/"),
    N("pn", "families", "The prime arrangement P_n is solvable", "proved",
      "P_n (scores 1, 1, 2, 3, …, n−3, n−2, n−2; D = {±(n−2)} ∪ {|d| ≤ n−3, d ≡ n−1 mod 2}) has a witness for every n ≥ 4: π(2) = n; π(i) = n−1−i for odd i ≤ n−2; π(i) = n+3−i for even i ≥ 4; and π(n−1) = 1 (n even) or π(n) = 2 (n odd).",
      "P_n is the no-tight-cut arrangement closest to the start: stones on every other mark, except that each end pair is squeezed together. It is the one arrangement that can't be split into blocks, so it needs its own solution. The solution is two interleaved staircases plus two corner points. Claim: the formula gives a solution for every n.",
      [stones([-4, -3, -1, 1, 3, 4], -5, 5, cap="P₆"), board(6, D=[-4, -3, -1, 1, 3, 4], pts=perm([4, 6, 2, 5, 1, 3]), cap="The formula at n = 6: 4 6 2 5 1 3")],
      refs="Verify agent 2026-11-23, /home/claude/agents/verify/pn.py (formula checked n ≤ 30; exactly two witnesses for n ≤ 14)"),
    N("twoblock", "families", "Every arrangement but P_n has a 2×2 block", "empirical",
      "Every valid no-tight-cut D other than P_n has stones x, x + 2 such that some witness contains a 2×2 block (points (r, c+1) and (r+1, c)) on those two diagonals. Equivalently, the layout with one 2-wide stone at offset x + 1 and all other stones 1-wide is solvable.",
      "A 2×2 block is two points in neighbouring rows and neighbouring columns, the upper one a step to the right. On the plank it is two stones two marks apart; in a block layout it becomes one fat stone at their midpoint, with every other stone alone. Example: in 2 6 5 4 1 3 (stones −4, −3, 0, +1, +2, +4), rows 3–4 and columns 4–5 hold a block on diagonals 0 and +2. Shrinking the block to one point usually leaves a permutation that repeats a diagonal, so this does not reduce to a smaller instance of the same problem. Laying out one fat stone and n − 2 thin ones is still a full-size placement puzzle, so this claim is stronger than the conjecture: it says every arrangement has a solution of a special shape. Its value is that it narrows what kind of solution to look for. Claim: every valid arrangement with no tight cut except P_n has a solution with a 2×2 block.",
      [board(6, D=[-4, -3, 0, 1, 2, 4], pts=perm([2, 6, 5, 4, 1, 3]), blocks=[[3, 4, 4, 5]], cap="Rows 3–4, columns 4–5: a 2×2 block on diagonals 0 and +2")],
      evidence="Exhaustive for no-tight-cut D up to mirror, n = 4–14 (33,284 D at n = 14); the only exception at each n is P_n. Also exact there: shrinking a 2×2 block never leaves an arrangement with a tight cut. A block (any size) whose shrunken permutation has distinct diagonals does not always exist: 1, 2, 3, 5, 11 arrangements at n = 5–9 have none (first beyond P_n: ±{1, 2, 3}).",
      refs="Blocks agent 2026-11-22, /home/claude/agents/blocks/"),
    N("closestpair", "families", "Rule: the pair nearest the middle", "disproved",
      "For every valid no-tight-cut D ≠ P_n, the pair {x, x + 2} ⊂ D whose centre x + 1 is closest to 0 forms a 2×2 block in some witness.",
      "A natural way to pick the block: among stones two marks apart, take the pair centred nearest the middle. Claim: that pair always works.",
      [stones([-3, -2, -1, 1, 2, 3], -5, 5, hl=[-1, 1], cap="It picks {−1, +1}, but only {−3, −1} and {+1, +3} form blocks")],
      evidence="First failure n = 6, D = ±{1, 2, 3} (picture). Right for 99.3% of D up to n = 14, but failures grow (424 at n = 14). Also failed: the leftmost pair, any pair with an empty mark between, pairs whose outer neighbours are empty.",
      refs="Blocks agent 2026-11-22"),
    N("mergepair", "families", "Rule: merge the pair into one stone", "disproved",
      "For every valid no-tight-cut D ≠ P_n, some pair {x, x + 2} ⊂ D has D ∖ {x, x+2} ∪ {x+1} valid at size n − 1.",
      "The simplest reduction: replace two stones two marks apart by one stone between them and solve the smaller arrangement. Claim: some pair can always be merged into a valid smaller arrangement.",
      [stones([-4, -3, 0, 1, 2, 4], -5, 5, cap="No pair is centred at 0, so every merge leaves the stones unbalanced")],
      evidence="A valid arrangement's stones sum to 0, but the merged set sums to −(x + 1), so only a pair centred at 0 can work. D = {−4, −3, 0, 1, 2, 4} has no such pair (picture); overall only 7.7% of pairs pass.",
      refs="Blocks agent 2026-11-22"),
    N("weighted", "families", "An exact test for fat-stone layouts", "disproved",
      "A layout of stones of width 1 or 2 with target offsets t (total width W; row and column orders free) is solvable iff for every set S of stones with total width V, Σ_S width·t ≥ −V(W − V).",
      "Replace a pair of stones by one 2-wide fat stone at their midpoint. A Landau-style count over all groups of stones is clearly necessary for such a layout to be solvable. Claim: the count is also sufficient.",
      [stones([-4, -2, 0, 1, 2, 3], -5, 5, hl=[-2, 0], cap="Fat stone at −1 from {−2, 0}: passes the count, but no solution has that block")],
      evidence="False: D = {−4, −2, 0, 1, 2, 3} with {−2, 0} fattened passes the count, yet no witness has that block (the pairs {−4, −2}, {0, 2}, {+1, +3} do). Failures are common (117 of 260 in one class at total width 8), and parity gives no fix.",
      refs="Weighted agent 2026-11-22, /home/claude/agents/weighted/"),

    # ================= symmetric / non-symmetric split =================
    N("sym", "families", "Symmetric arrangements are solvable", "open",
      "Let 𝒩 be the valid arrangements with no tight cut and 𝒮 ⊂ 𝒩 the symmetric ones (D = −D). Every D ∈ 𝒮 has a witness.",
      "Symmetric means the plank looks the same in a mirror held at the middle mark: every stone at +d has a partner at −d, so the x-ray reads the same forwards and backwards. Claim: every symmetric arrangement with no tight cut has a solution.",
      [stones([-5, -3, -2, 0, 2, 3, 5], -6, 6, cap="Symmetric: 0, ±2, ±3, ±5"),
       board(7, D=[-5, -3, -2, 0, 2, 3, 5], pts=perm([3, 7, 6, 1, 5, 4, 2]), cap="One of its solutions, 3 7 6 1 5 4 2")]),
    N("nonsym", "families", "Non-symmetric arrangements are solvable", "open",
      "Every D ∈ 𝒩 ∖ 𝒮 (no tight cut, D ≠ −D) has a witness.",
      "A non-symmetric arrangement has a different mirror image. Flipping a solution across the main diagonal turns it into a solution of the mirror image, so each mirror pair stands or falls together. Claim: every non-symmetric arrangement with no tight cut has a solution.",
      [pair(stones([-4, -2, 0, 1, 2, 3], -5, 5), stones([-3, -2, -1, 0, 2, 4], -5, 5), "mirror ↔", cap="An arrangement and its mirror image"),
       board(6, D=[-4, -2, 0, 1, 2, 3], pts=perm([1, 4, 6, 5, 3, 2]), cap="A solution of the first, 1 4 6 5 3 2")]),
    N("symodd", "families", "Odd symmetric arrangements fold", "empirical",
      "If D ∈ 𝒮 has n = 2m + 1 and L = D ∩ (0, ∞), then for some position f the positions {1, …, n} ∖ {f} split into pairs with distances exactly L; equivalently, D has an involution witness with fixed point (f, f). (In terms of L, Landau says: the K largest elements of L sum to at most K(n − K), for every K.)",
      "With an odd number of symmetric stones, one sits on the middle mark. A solution that folds onto itself across the main diagonal puts that stone's point on the diagonal and pairs every other point with its mirror image. So a folding solution is a pairing puzzle: leave one position free and pair up the rest so that the pair distances are exactly the stones' distances from the middle. Claim: for every odd symmetric arrangement with no tight cut, the puzzle has a solution for a suitable free position.",
      [board(5, D=[-3, -1, 0, 1, 3], pts=perm([4, 3, 2, 1, 5]), cap="{0, ±1, ±3}: positions paired (1,4) and (2,3), position 5 free")],
      evidence="Holds for every symmetric valid D with n odd ≤ 15 (1971 at n = 15). No fixed choice of the free position works (end, centre and start all fail by n = 7), and 'parity + density for the remaining positions ⇒ pairing' is false (n = 5, L = {1, 3}, centre free). No theorem in the Skolem literature covers arbitrary L.",
      refs="Sympair agent 2026-11-23, /home/claude/agents/sympair/"),
    N("symeven", "families", "Even symmetric arrangements are solvable", "open",
      "Every D ∈ 𝒮 with n even has a witness.",
      "With an even number of symmetric stones the middle mark is empty, and every stone at +d has a partner at −d. Claim: every such arrangement with no tight cut has a solution.",
      [stones([-6, -5, -2, -1, 1, 2, 5, 6], -7, 7, cap="±{1, 2, 5, 6}: eight stones, middle mark empty")]),
    N("nordh8", "families", "Even pairings exist (Nordh's Conjecture 8)", "open",
      "Let D ∈ 𝒮 with n = 2m and L = D ∩ (0, ∞), and suppose L has an even number of even elements. Then positions 1…2m split into pairs with distances exactly L; equivalently, D has an involution witness. (The no-tight-cut case of Nordh's Conjecture 8: parity + density ⇒ perfect Skolem set.)",
      "A solution that folds onto itself across the main diagonal pairs each point with its mirror image, so it is a pairing of positions 1…2m whose pair distances are exactly the stones' distances from the middle. A pair at an even distance joins two positions of the same parity; since there are equally many odd and even positions, the even distances must come in an even number. Example: L = {1, 2, 5, 6} has two even distances and pairs as (3,4), (5,7), (1,6), (2,8). Claim: for every even symmetric arrangement with no tight cut and an even number of even distances, such a pairing exists.",
      [board(8, D=[-6, -5, -2, -1, 1, 2, 5, 6], pts=perm([6, 8, 4, 3, 7, 1, 5, 2]), cap="L = {1, 2, 5, 6}: pairs (1,6) (2,8) (3,4) (5,7)")],
      evidence="For even n ≤ 14, a symmetric valid D has an involution witness exactly when L has an even number of even elements. Nordh checked his conjecture for up to 20 distances. Proved special cases: Skolem ({1…m}), Langford/Simpson (intervals), Shalaby (an interval minus one element).",
      refs="Nordh 2008, Conj. 8; sympair agent 2026-11-23"),
    N("centro", "families", "Half-turn solutions when folding is impossible", "empirical",
      "Let D ∈ 𝒮 with n = 2m and L = D ∩ (0, ∞), and suppose L has an odd number of even elements. Then D has a centrosymmetric witness: π(n+1−i) = n+1−π(i).",
      "When L has an odd number of even distances, no solution can fold across the main diagonal. The next symmetry to try is a half turn of the board. A half-turn solution is determined by its top half, which gives a half-size puzzle: pick a permutation σ of 1…m, and for each row i use either the distance |σ(i) − i| (the point and its twin stay on their own sides) or the crossing distance 2m + 1 − i − σ(i) (they cross to the mirrored half); the chosen distances must be exactly L. Claim: every even symmetric arrangement with no tight cut and an odd number of even distances has a half-turn-symmetric solution.",
      [board(8, D=[-6, -4, -3, -2, 2, 3, 4, 6], pts=perm([4, 8, 7, 6, 3, 2, 1, 5]), cap="L = {2, 3, 4, 6} (three even distances): no solution folds, but 4 8 7 6 3 2 1 5 survives a half turn")],
      evidence="Holds for every such D with n even ≤ 14. Narrower versions fail at n = 6 for L = {1, 2, 3}: σ an involution, or a pairing plus one 4-cycle.",
      refs="Sympair agent 2026-11-23"),
    N("f1", "families", "F1: everything but the middle", "proved",
      "For every a ≥ 1, D = {±1, …, ±a} (n = 2a) has the witness π(i) = 2i for i ≤ a, π(i) = 2i − (2a+1) for i > a.",
      "Stones on every mark within distance a of the middle, with the middle mark empty. From above the solution is two parallel lines of slope 2, the top half on even columns and the bottom half on odd ones. Claim: this gives a solution for every a.",
      [board(6, D=[-3, -2, -1, 1, 2, 3], pts=perm([2, 4, 6, 1, 3, 5]), cap="a = 3: π = 2 4 6 1 3 5")],
      refs="Nordh 2008, Thm 28 (arXiv v1 numbering); explicit witness ours"),
    N("f3", "families", "F3: folding solutions are Skolem pairings", "proved",
      "D = ±L (n = 2m) has an involution witness ⇔ positions 1…2m split into pairs with distances exactly L; with one unpaired position, the same holds for D = {0} ∪ ±L. Known solvable L: {1…m} iff m ≡ 0, 1 mod 4 (Skolem 1957); intervals {d…d+m−1} under Simpson's 1983 conditions; {1…k} ∖ {j} on positions 1…2k−2 when k ≡ 0, 1 mod 4 and j odd, or k ≡ 2, 3 mod 4 and j even (Shalaby; Nordh Cor 26).",
      "A solution that folds onto itself across the main diagonal pairs each point (i, j) with its twin (j, i), on diagonals +(j − i) and −(j − i). So folding solutions of ±L are exactly ways to pair up positions with pair distances L, a classical Skolem/Langford puzzle; known solutions of that puzzle give infinite families of solved arrangements. Claim: folding solutions and such pairings correspond one to one.",
      [board(6, D=[-4, -3, -2, 2, 3, 4], pts=perm([5, 4, 6, 2, 1, 3]), cap="Positions paired (1,5) (2,4) (3,6): distances 4, 2, 3")],
      refs="Nordh 2008, Thm 23 and Cor 26; Skolem 1957; Simpson 1983; Shalaby"),

    # ================= moves =================
    N("mm", "moves", "Minimal moves reach every arrangement", "proved",
      "Call a move minimal if it takes stones at a < b, where a + 1 and b − 1 are empty and every mark strictly between them is occupied, to a + 1 and b − 1. Every valid D is reached from the start (stones on every other mark) by minimal moves, and each move raises the number of 3-cycles by exactly 1.",
      "A minimal move slides two stones one mark toward each other when the marks just inside them are empty and everything between those is filled. The picture walks from the start to {−2, −1, +1, +2} in two moves. Claim: these moves, starting from 'every other mark', reach every valid arrangement.",
      [pair(stones([-3, -1, 1, 3], -3, 3, hl=[-3, 1]), stones([-2, -1, 0, 3], -3, 3, hl=[-2, 0]), "→", cap="Move 1: −3 and +1 slide in to −2 and 0"),
       pair(stones([-2, -1, 0, 3], -3, 3, hl=[0, 3]), stones([-2, -1, 1, 2], -3, 3, hl=[1, 2]), "→", cap="Move 2: 0 and +3 slide in to +1 and +2")]),
    N("move", "moves", "Minimal moves keep the board solvable", "open",
      "If D has a witness and D → D′ is a minimal move, then D′ has a witness.",
      "This is the step of an induction whose invariant is simply 'has a solution': the start has exactly one solution, so if every minimal move kept a solution, every arrangement would have one. All of the difficulty sits in this step. Claim: whenever an arrangement has a solution, so does the result of any minimal move.",
      [pair(board(5, D=[-4, -2, 0, 2, 4], pts=perm([5, 4, 3, 2, 1])), board(5, D=[-3, -2, -1, 2, 4], pts=perm([5, 4, 2, 1, 3])), "−4, 0 → −3, −1",
            cap="The start for n = 5 and a solution after one move")]),
    N("ratio", "moves", "A move never loses more than a fixed fraction", "empirical",
      "There is c > 0 with W(D′) ≥ c·W(D) for every minimal move D → D′ and every n.",
      "Count the solutions before and after a move. If a move could never lose more than a fixed fraction of them, solvability would pass along every move. In every test the worst loss comes from the same local picture of seven marks. Claim: some fixed fraction c of the solutions always survives.",
      [pair(stones([0, 1, 3, 5, 6], 0, 6, hl=[1, 5]), stones([0, 2, 3, 4, 6], 0, 6, hl=[2, 4]), "→", cap="The worst move: solutions drop to exactly 2/3")],
      evidence="Minimum ratio = 2/3 for n ≤ 16, attained only by this pattern; next-smallest ≈ 0.734 (n = 14–16)."),
    N("goodwitness", "moves", "Some solution needs only a small fix", "empirical",
      "For every minimal move D → D′ of a solvable D, some witness of D becomes a witness of D′ by changing at most 4 rows (the two moving stones' rows plus at most two more).",
      "After a move, some old solution can usually be fixed by swapping the columns of the two moving points: when the lower point sits the right number of rows below the upper one, the swap moves each onto the next diagonal inward and nothing else changes. When no solution is in that position, changing one or two more rows has always been enough. Claim: some old solution always becomes a new one after changing at most four rows.",
      [pair(board(5, D=[-4, -1, 0, 1, 4], pts=perm([5, 3, 2, 4, 1]), cand=[[3, 2], [5, 1]]), board(5, D=[-3, -2, 0, 1, 4], pts=perm([5, 3, 1, 4, 2]), cand=[[3, 1], [5, 2]]), "swap columns →",
            cap="Move −4, −1 → −3, −2: rows 3 and 5 swap columns 1 and 2")],
      evidence="Best old solution, all minimal moves of all valid D, n ≤ 12: a plain column swap works for 93% of moves (41,726 of 44,972 at n = 12), including every move with nothing between the movers; the rest need 3 or 4 rows, never more. From an arbitrary old solution the fix grows (up to 7 rows at n = 12).",
      refs="Connect agent 2026-11-23, /home/claude/agents/connect/"),
    N("repair", "moves", "Bounded repair from any solution", "disproved",
      "There is R such that for every minimal move D → D′ and every witness π of D, some witness of D′ agrees with π on all but at most R of the non-moving stones' points.",
      "Instead of choosing a good old solution, fix whichever one you have. Claim: the fix never needs more than a fixed number of other points to move.",
      example="n = 7: D = {−5,−2,−1,0,1,2,5}, move −5,−2 → −4,−3,\nπ = 3 7 1 4 6 5 2: every witness after the move\nmoves ≥ 3 of the other 5 points.",
      evidence="The worst case grows: 1, 2, 2, 3, 3, 3 for n = 4–9, and 5 at n = 14 (Devin)."),
    N("fibre", "moves", "Fibrewise 2/3 bound", "disproved",
      "For every minimal move and every placement of the non-moving stones' points that extends to a witness of D, it extends to at least 2/3 as many witnesses of D′.",
      "Freeze every point except the two moving ones, and compare how many ways the moving pair can be placed before and after. Claim: the count never drops below 2/3.",
      evidence="Every fibre has size 0 or 1, so a fibre with one witness before and none after is a counterexample; these occur from small n."),
    N("exchange", "moves", "All solutions connected by small rotations", "disproved",
      "There is k such that for every D, any two witnesses are connected by a chain of witnesses, each obtained from the previous by rearranging at most k points.",
      "If all solutions of an arrangement were linked by small steps, we could walk from any solution to one where a move is easy to fix. Claim: some fixed step size links them all.",
      [pair(board(4, D=D2413, pts=perm([2, 4, 1, 3])), board(4, D=D2413, pts=perm([3, 1, 4, 2])), "?", cap="P₄'s two solutions differ in every row: no small step links them")],
      evidence="False for every fixed k: P_n's two solutions differ in all n rows (n = 5–11). With rotations of up to 4 points, 302 of 306 arrangements are disconnected at n = 10.",
      refs="Connect agent 2026-11-22"),

    # ================= peeling =================
    N("start", "peeling", "Starting lemma: Landau ⇒ parity test", "empirical",
      "If D satisfies Landau, the square n×n board with diagonals D passes the parity test: there is a choice a(d) ∈ {odd, even} for each d ∈ D such that the parity counts match and the fractional placement using only cells (r, c) with r ≡ a(c − r) exists.",
      "The parity test asks: decide for each stone whether its point goes in an odd or an even row, so that the numbers match, and then check that a fractional solution exists using only the allowed cells. Any real solution supplies such a choice, so the test is weaker than having a solution. It can be checked by linear programming once the choice is made, which is what makes it a usable invariant. Claim: every valid square board passes.",
      [board(5, D=[-2, -1, 0, 1, 2], pts=perm([1, 4, 2, 5, 3]), par=True, cap="1 4 2 5 3 gives a choice: 0, −1, −2 in odd rows; +2, +1 in even rows")],
      evidence="Holds for n ≤ 12, tight cuts included, but checked via real solutions, so no evidence beyond the conjecture. Only the all-same-parity D has a unique working choice."),
    N("parityrule", "peeling", "Rule: parity from a stone's position", "disproved",
      "There is a function f such that for every valid D, the choice a(d) = f(d, rank of d in D) passes the parity test.",
      "The simplest kind of parity choice reads a stone's parity off its own mark and its rank. Claim: one such rule works for every arrangement.",
      example="D = {−1, 0, 1} forces a(0) = odd, but D = {−2, 0, 2} forces a(0) = even,\nand 0 has rank 2 in both.",
      evidence="Fails at n = 3 (example). Also fail: rules from parity-class rank (n = 6), local Landau slack (n = 7), alternating within parity classes (n = 6), every function of 4 binary local features (n ≤ 6)."),
    N("paritymove", "peeling", "Minimal moves keep the parity test passing", "empirical",
      "If D passes the parity test and D → D′ is a minimal move, then D′ passes the parity test.",
      "The parity test can be carried along minimal moves like 'has a solution', but it is a weaker property, so the step might be easier. Claim: a minimal move never breaks the parity test.",
      [pair(board(5, D=[-4, -2, 0, 2, 4], pts=perm([5, 4, 3, 2, 1]), par=True), board(5, D=[-3, -2, -1, 2, 4], pts=perm([5, 4, 2, 1, 3]), par=True), "→",
            cap="Before and after a move, each with a passing choice")],
      evidence="True for n ≤ 12, since every valid D passes there (starting lemma); no direct argument yet."),
    N("carry", "peeling", "Carry a parity choice across a move", "open",
      "For every minimal move a, b → a+1, b−1 from a D that passes the parity test, some working choice for D with equal values on a and b becomes a working choice for D′ after giving a+1 and b−1 that value and keeping all other values.",
      "Instead of finding a new parity choice after a move, keep the old one: the two moving stones share a parity and pass it on to their new marks. Claim: some working choice always carries over like this.",
      evidence="Holds for the moves with nothing between the movers, n ≤ 11 (from solutions) and n ≤ 10 (from the LP). Not yet checked for general minimal moves. 'Every working choice carries over' fails at n = 6 (D = (−4,−3,0,1,2,4), x = −3).",
      refs="Parity-data agent 2026-11-22"),
    N("peel", "peeling", "Peeling lemma: some top-row cell keeps the test", "empirical",
      "Every board with rows 1…m and any m columns that passes the parity test has a top-row cell whose peel (delete its row, its column and its diagonal) leaves a board that still passes.",
      "Peeling places one point in the top row and deletes everything it uses, leaving a smaller board with a hole where the column was. The invariant is the parity test, which is weaker than 'has a solution' and checkable, so this is a genuine step rather than the conjecture in disguise. In the example, the top row can use diagonal +1 or +2; +1 runs dry two rows later, while +2 leaves a board that fills. Claim: every board passing the parity test has some top-row cell that keeps it passing.",
      [pair(board(rows=[1, 2, 3, 4, 5], cols=[1, 2, 3, 4, 6], D=[-4, -2, 1, 2, 4], cand=[[1, 2]], pts=[[1, 3]], holes=[5]),
            board(rows=[2, 3, 4, 5], cols=[1, 2, 4, 6], D=[-4, -2, 1, 4], pts=[[2, 6], [3, 4], [4, 2], [5, 1]], holes=[3, 5]), "peel →",
            cap="Top row on +2 (not +1); the peeled board still fills")],
      evidence="Some top-row cell always peels: rows 1…m with h ≤ 3 holes, m ≤ 7, and h = 2, m = 8. The peel can always keep the same parity choice (m ≤ 7, h ≤ 3), but not every passing choice works."),
    N("parity", "peeling", "Parity test is exact on boards with holes", "empirical",
      "A board with rows 1…m and any m columns has a placement ⇔ it passes the parity test.",
      "With holes, two new things go wrong for the plain fractional test. A row can have no usable cell at all (left picture: every column is odd, so row 1 only sees even diagonals). And a fractional solution can put half of each stone in an odd row and half in an even row (right picture). Claim: choosing parities first removes every such cheat, so passing the parity test is the same as having a placement.",
      [board(rows=[1, 2, 3], cols=[1, 3, 5], D=[-1, 1, 3], holes=[2, 4], par=True, cap="Two holes: row 1 has no cell on a diagonal of D"),
       board(rows=[1, 2, 3, 4, 5, 6], cols=[1, 2, 5, 6, 7, 8], D=[-3, -2, 0, 2, 5, 6], holes=[3, 4], par=True,
             w=[[r, c, "½"] for r, c in half_cells], cap="Fractional but not real: every diagonal split ½ odd, ½ even")],
      evidence="Exact on all tested boards: 2 holes up to m = 10, 3 up to m = 9, 4 up to m = 7. General row sets only up to m = 5."),
    N("toprules", "peeling", "Rule: a fixed top-row choice", "disproved",
      "At least one of these always keeps the parity test passing: (a) the top-row cell with the largest diagonal, (b) the smallest, (c) the largest weight in the fractional solution.",
      "The obvious ways to choose the top row's point. Claim: one of them always works.",
      [board(rows=[1, 2, 3, 4], cols=[1, 3, 4, 5], D=[-2, 0, 2, 3], cand=[[1, 1], [1, 4]], pts=[[1, 3]], holes=[2], cap="Largest (+3) and smallest (0) both fail; only +2 works")],
      evidence="(a), (b) fail at m = 4 (picture); (c) fails at m = 6, h = 3, where the restricted fractional solution is all ½."),
    N("ir", "peeling", "Rule: a weight-1 corner for a fixed parity choice", "disproved",
      "For every passing parity choice, the restricted fractional polytope has a vertex with some cell of weight exactly 1.",
      "A cell with weight 1 in a fractional solution uses up its row, column and diagonal, so peeling it keeps the rest of that solution. Claim: every passing choice has such a cell at some vertex.",
      evidence="False: m = 6, h = 3, columns {1,3,4,7,8,9}, D = {−3,−1,2,3,4,6} has a unique all-½ solution for one passing choice. For some choice a weight-1 vertex always existed in tests, but that version is equivalent to the peeling lemma."),
    N("forcing", "peeling", "Bad peels are forced contradictions", "empirical",
      "Peel a top-row cell e of a board passing the parity test, leaving board P. Then P fails the parity test ⇔ for every parity choice a of P, either the parity counts don't match, or forced-move propagation on the a-restricted P empties some row, column or diagonal. (Propagation: while some row, column or diagonal has exactly one usable cell, place a point there and delete its lines.)",
      "Forced moves: if some row, column or diagonal has only one usable cell, the point must go there, which deletes more cells and may force the next point. In the example, taking diagonal 0 in the top row forces +3 into cell (3, 6), and then row 2 has no usable cell left. Claim: a peel is bad exactly when, for every parity choice, the counts are off or forced moves run into an empty line.",
      [pair(board(cand=[[1, 1]], **PEELB), board(rows=[2, 3, 4, 5], cols=[3, 4, 5, 6], D=[-2, -1, 3, 4], pts=[[3, 6]], holes=[1, 2]), "take 0 →",
            cap="Forced: +3 at (3, 6). Then row 2 has no usable cell")],
      evidence="Exact on all tested boards: m ≤ 7 with up to 4 holes, m = 8 with up to 3. Propagation alone (no parity) explains 96–99% of bad cells; parity first matters at m = 7. A real placement survives forced moves, so the rule never wrongly calls a cell bad. The raw LP certificates are a zoo (dozens of sign patterns, weights up to 6).",
      refs="Farkas agent 2026-11-23, /home/claude/agents/farkas/"),
    N("chainpeel", "peeling", "Some top-row cell never sets off a dead end", "open",
      "Every board with rows 1…m passing the parity test has a top-row cell e and a parity choice a for the peeled board such that the parity counts match and forced-move propagation on the a-restricted peeled board never empties a row, column or diagonal.",
      "This is the peeling lemma with the LP taken out: instead of a fractional solution, we only need one top-row cell whose forced consequences never run dry. On the same board as the 'bad peels' example, taking +3 in the top row forces every remaining point one after another, and nothing runs dry. Claim: every board passing the parity test has such a cell.",
      [pair(board(cand=[[1, 1]], pts=[[1, 4]], **PEELB), board(rows=[2, 3, 4, 5], cols=[1, 3, 5, 6], D=[-2, -1, 0, 4], pts=[[2, 6], [3, 1], [4, 3], [5, 5]], holes=[2, 4]), "take +3 →",
            cap="Every remaining point is forced, and no line runs dry")]),
    N("g1", "peeling", "G1: the sum test is exact with one missing column", "empirical",
      "Rows 1…m, columns {1…m+1} ∖ {c}, t_k = d_k + m − k: a placement exists ⇔ Σ_{i≤k} t_i ≥ C(k,2) + max(0, k+1−c) for all k, with equality at k = m.",
      "Place the largest stone in the top row first. Deleting that row and its column leaves a smaller board with a hole where the column was. On such one-hole boards, Landau's test still makes sense if 'the k leftmost columns' skips over the hole. Claim: on boards with one missing column, this adjusted test is exact.",
      [pair(board(4, D=D2413, pts=[[1, 3]]), board(rows=[2, 3, 4], cols=[1, 2, 4], D=[-2, -1, 1], pts=[[2, 1], [3, 4], [4, 2]], holes=[3]), "peel row 1 →",
            cap="+2 goes in row 1, column 3; column 3 becomes a hole and the rest fills")],
      evidence="Sufficiency verified by computer for m ≤ 15 (Devin)."),
    N("sum2", "peeling", "The sum test is exact with two or more holes", "disproved",
      "On boards with rows 1…m and two or more missing columns, the Landau-type sum test implies a placement.",
      "Peeling rows one at a time creates more holes, so G1 would follow if the sum test kept working. Claim: it works with any number of holes.",
      [board(rows=[1, 2, 3], cols=[1, 3, 5], D=[-1, 1, 3], holes=[2, 4], cap="Passes the sum test, but row 1 sees only even diagonals")],
      evidence="Fails from m = 3: rows 1–3, columns {1,3,5}, D = {−1,1,3} (picture)."),
    N("edgepeel", "peeling", "Edge peeling stays inside one-hole boards", "disproved",
      "Some class of boards with at most one hole is closed under peeling a suitable edge row or column, and the sum test is exact on it.",
      "Another route to G1: always peel an edge line chosen so that the board keeps at most one hole. Claim: some such class is closed under peeling and has an exact sum test.",
      example="Stuck board: rows 1–4, columns {1,2,4,5}, D = {−2,−1,2,3}:\nevery peel leaves the class.",
      evidence="About 19% of boards get stuck at m = 8; enlargements of the class fail too."),
    N("plainlp", "peeling", "Plain fractional test is exact with holes", "disproved",
      "On boards with missing columns, a fractional placement implies a real one.",
      "Without choosing parities first. Claim: the plain fractional test is already exact with holes.",
      evidence="First failure at m = 6: columns {1,2,5,6,7,8}, D = {−3,−2,0,2,5,6} has a unique all-½ fractional solution (the parity claim's second picture)."),

    # ================= fractional & algebraic =================
    N("ly", "algebra", "Li–Yao: the fractional version is true", "proved",
      "If s satisfies Landau, there is a doubly stochastic matrix supported on the diagonals of D in which each diagonal of D sums to 1.",
      "Allow points to be split into fractions spread over several cells. Claim: Landau's condition is always enough for such a fractional solution.",
      [board(3, D=[-1, 0, 1], w=[[1, 1, "½"], [3, 3, "½"], [1, 2, "½"], [2, 3, "½"], [2, 1, "½"], [3, 2, "½"]],
             cap="{−1, 0, +1}: every row, column and diagonal sums to 1 using halves")],
      refs="Li–Yao; Li–Liu–Yao, arXiv:2608.01442"),
    N("cap", "algebra", "Capacity bound", "empirical",
      "W(D) ≥ (n!/nⁿ)·cap(P_D), where P_D(x) = per(M) with M_ij = x_{j−i} if j − i ∈ D (else 0), and cap(P_D) = inf_{x>0} P_D(x)/∏_d x_d.",
      "Give each allowed diagonal d a weight x_d and fill the board in every possible way using allowed diagonals, letting stones pile up on the same mark. Each filling contributes the product of the weights it uses; the total is the polynomial P. Fillings that use every weight once are the solutions, so the number of solutions W is the coefficient of the product of all weights. Divide P by that product and push the weights to make the result small: the solutions always contribute exactly W, while piled-up fillings can be pushed down. The smallest value reached is the capacity; it is positive exactly when a fractional solution exists. Claim: the number of solutions is never below n!/nⁿ times the capacity.",
      [board(3, D=[-1, 0, 1], cap="{−1, 0, +1}: each cell carries the weight of its diagonal")],
      example="Weights on {−1, 0, +1}:\n  x₀  x₁  ·\n  x₋₁ x₀  x₁\n  ·   x₋₁ x₀\nFillings: 123 → x₀³ (three stones on mark 0)\n          132 → x₀x₁x₋₁ (a solution)\n          213 → x₁x₋₁x₀ (a solution)\nP = x₀³ + 2·x₋₁x₀x₁, so W = 2.\nP/(x₋₁x₀x₁) = x₀²/(x₋₁x₁) + 2 → smallest value 2: cap = 2.\nBound: W ≥ (6/27)·2 ≈ 0.44. True: W = 2.",
      evidence="Holds for every no-tight-cut D with n ≤ 11 (n ≤ 8 Devin; n = 9–11 exhaustive). The slack W·nⁿ/(n!·cap) is at least 13.8, 17.2, 18.0 at n = 9, 10, 11 and grows with n; the worst cases are near-regular arrangements with many solutions, not P_n. Along P_n (W = 2) the slack grows like e^{0.21n} through n = 20.",
      refs="Capacity agent 2026-11-22, /home/claude/agents/capacity/"),
    N("stable", "algebra", "P_D is real stable or log-concave", "disproved",
      "P_D is real stable, or at least log-concave on the positive orthant (or Lorentzian), so the Gurvits / Anari–Oveis Gharan–Vinzant coefficient bounds apply.",
      "Known proofs that a coefficient is at least a fixed fraction of the capacity need the polynomial to be real stable, or at least log-concave on positive inputs. Claim: ours is.",
      example="D = {−1, 0, 1}: P = x₀³ + 2·x₋₁x₀x₁.\nAt (x₋₁, x₀, x₁) = (½, 1, ½), along (1, 0, 1),\nthe second derivative of log P is 8/9 > 0: not log-concave.",
      evidence="Fails at n = 3 (example) and for every no-tight-cut D with n ≤ 7: not log-concave, not Lorentzian, support not M-convex.",
      refs="Capacity agent 2026-11-22"),
    N("gstep", "algebra", "Gurvits' one-variable step", "disproved",
      "In some order, removing one variable at a time (q = ∂P/∂x_d at x_d = 0) lowers the capacity by at most a factor ((k−1)/k)^{k−1} (k = deg_{x_d}), or by at most a fixed constant c > 0, at every step.",
      "Gurvits' proof removes one variable at a time and shows the capacity never drops by more than a fixed factor per step; chaining the steps gives the bound. Claim: the same per-step bound holds for our polynomials in some order.",
      example="P₅ = {−3, −2, 0, 2, 3}: removing x₀ first gives\nq = a²d² + 2abcd + 2b²c²  (a, b, c, d = x₋₃, x₋₂, x₂, x₃),\ncap(q) = 2 + 2√2; removing any next variable leaves 2·(the rest),\nlosing a factor √2 − 1 where Gurvits allows ½.",
      evidence="Gurvits' factor fails at n = 5 for P₅ in every order. The best constant per step shrinks: 0.5, 0.39, 0.33, 0.33, 0.26, 0.22 for n = 4–9, always worst at P_n.",
      refs="Capstep agent 2026-11-23, /home/claude/agents/capstep/"),
    N("sat", "algebra", "Saturation with repeats allowed", "disproved",
      "Every lattice point of the polytope of all permutation x-rays (repeated diagonals allowed) is the x-ray of some permutation.",
      "If every whole-number point of the fractional region were realised, Li–Yao would immediately give a solution. Claim: it is, even when marks may hold several stones.",
      example="n = 12: e = {−8, −7, −3⁵, 1, 7³, 8} is the average of two x-rays,\nbut no permutation has x-ray e.",
      evidence="Holds for n ≤ 11, fails at n = 12 (example)."),
    N("round", "algebra", "Round any fractional solution", "disproved",
      "Every doubly stochastic matrix with a binary x-ray can be rounded to a permutation matrix with the same x-ray.",
      "Start from a fractional solution and clean it up. Claim: any fractional solution can be rounded to a real one with the same diagonals.",
      evidence="Li–Liu–Yao Sec. 5: a 5×5 doubly stochastic matrix with entries ½ and x-ray (0,0,1,1,1,1,0,0) can't be rounded keeping its x-ray (a permutation with that x-ray exists anyway).",
      refs="Li–Liu–Yao, arXiv:2608.01442, Sec. 5"),
    N("tct", "algebra", "General three-way-table version", "disproved",
      "Integer version of Li–Liu–Yao's Conj. 5.3: every triangular contingency table problem with binary marginals that has a fractional solution has an integer one.",
      "A broader version of the problem, with three families of lines in place of rows, columns and diagonals. Claim: integrality holds there too.",
      evidence="False at n = 112 (Prop 5.4): binary marginals whose table is unique and has a ½ entry. So a proof must use the geometry of the square board.",
      refs="Li–Liu–Yao, arXiv:2608.01442, Prop 5.4"),
    N("at", "algebra", "Signed solution counts are nonzero", "disproved",
      "For every valid no-tight-cut D, Σ_{witnesses π of D} sign(π) ≠ 0.",
      "Polynomial-method proofs (Alon–Tarsi) show existence by showing a coefficient is nonzero; here the natural coefficient is the signed count of solutions. Claim: it never vanishes.",
      evidence="Vanishes for some valid no-tight-cut D at n = 4–6."),

    # ================= other routes =================
    N("delta", "ideas", "Every score sequence has a tournament δ accepts", "open",
      "For every valid score sequence s there is a tournament with scores s on which Davis–Schroeder's reverse map δ is defined (then δ of it is a witness).",
      "Davis–Schroeder turn each solution into a tournament with the same scores, and give a condition on a tournament under which the process can be reversed to produce a solution. Tournaments with given valid scores are easy to build (Landau's theorem), so it would be enough to find, for each score sequence, one tournament satisfying their condition. The accepted tournaments turn out to be exactly those that come from solutions, so this is close to a restatement; the hope is a natural canonical tournament. Claim: every valid score sequence has an accepted tournament.",
      evidence="The accepted tournaments are exactly the images of solutions (checked n ≤ 6), so the claim is equivalent to the conjecture in that range. Accepted fraction drops to 2% at n = 8.",
      refs="Davis–Schroeder, arXiv:2606.21532; tourn agent 2026-11-23, /home/claude/agents/tourn/"),
    N("maxupset", "ideas", "Rule: the most-upsets tournament", "disproved",
      "For every valid score sequence s, some tournament with scores s and the maximum possible number of upsets is accepted by δ.",
      "A canonical choice: among tournaments with the right scores, take one with as many upsets as possible. Claim: one of those is always accepted.",
      evidence="Holds for n ≤ 8; fails at n = 9 for s = (1,2,3,3,4,5,5,6,7) (accepted reach 10 upsets, the maximum is 11). Staircase, rotational and Havel–Hakimi tournaments fail earlier.",
      refs="Tourn agent 2026-11-23"),
    N("greedy", "ideas", "Tested greedy placement rules", "disproved",
      "One of the 92 tested greedy rules (Havel–Hakimi style, fixed diagonal orders, least-damage, row-by-row urgency, most-constrained-first) finds a witness without backtracking for every valid no-tight-cut D.",
      "Landau's theorem for tournaments has step-by-step constructions. Claim: one of these step-by-step placements never gets stuck.",
      example="n = 5, D = {−3, −2, 0, 2, 3}: a few placements can leave rows {2,3,4},\ncolumns {1,3,5}, diagonals {−2,0,2}, all usable only in row 3.",
      evidence="All 92 fail by n ≤ 10; the best fails 0.5–0.9% at n = 11–13."),
]

E = []
def e(a, b, kind, why, status="proved"):
    E.append({"from": a, "to": b, "kind": kind, "status": status, "why": why})

T = "notight"
e(["tightcut", "notight"], "conj", "implies", "Strong induction on n: split at a tight cut into two smaller valid arrangements, solve each, glue.")
# decomposition route
e(["decomp", "pn", "inflation"], T, "implies", "Strong induction on n: every D ≠ P_n splits into smaller valid groups whose layout exists; the groups have witnesses by induction, and the block-layout lemma glues them. P_n has its formula.")
e("inflation", "directsum", "implies", "The direct sum is the layout σ = 12.")
e("directsum", "fixedpoint", "implies", "The fixed point is the direct sum with the 1×1 block {0}.")
e("twoblock", "decomp", "implies", "A 2×2 block plus single stones is such a split.")
e("closestpair", "twoblock", "implies", "Names a pair that works.")
e("mergepair", "twoblock", "related", "Merging would be the simplest way to produce the block; it fails already on the stone sum.", "unchecked")
e("weighted", "twoblock", "related", "An exact test would reduce the claim to showing that some pair passes it.", "unchecked")
# symmetric split
e(["sym", "nonsym"], T, "implies", "𝒩 = 𝒮 ∪ (𝒩 ∖ 𝒮).")
e(["symodd", "symeven"], "sym", "implies", "𝒮 splits by the parity of n.")
e(["nordh8", "centro"], "symeven", "implies", "Even n splits by whether L has an even or odd number of even elements.")
e("f3", "symodd", "related", "F3 turns a folding solution into this pairing puzzle.", "unchecked")
e("f3", "nordh8", "related", "F3 turns a folding solution into this pairing puzzle; its known pairings are special cases.", "unchecked")
e("f1", "symeven", "related", "Settles the arrangements ±{1…a} directly.", "unchecked")
# moves route
e(["mm", "move"], T, "implies", "Induction along minimal moves with invariant 'has a witness': the start has one, every D is reachable, every move keeps it.")
e("ratio", "move", "implies", "W(D′) ≥ c·W(D) > 0.")
e("goodwitness", "move", "implies", "The fixed old solution is a new one.")
e("repair", "move", "implies", "Fix any old solution.")
e("fibre", "ratio", "implies", "Summing over fibres gives c = 2/3.")
e("exchange", "goodwitness", "related", "Would let us walk from any solution to one that is easy to fix.", "unchecked")
# peeling route
e(["start", "peel"], T, "implies", "Induction on rows with invariant 'passes the parity test': the square board passes, each peel keeps it, and a 1-row board that passes is filled.")
e("peel", "parity", "equiv", "⇒: peel, solve the smaller board, add the point back. ⇐: a placement's own top-row point peels.")
e(["forcing", "chainpeel"], "peel", "implies", "By the forcing rule, a cell with such a parity choice is not bad.")
e("toprules", "peel", "implies", "Names a cell that works.")
e("ir", "peel", "implies", "A weight-1 cell can be peeled: the rest of the fractional solution solves the smaller board.")
e(["mm", "paritymove"], "start", "implies", "Induction along minimal moves: the start passes, each move keeps passing.")
e("carry", "paritymove", "implies", "The carried choice works for D′.")
e("parityrule", "start", "implies", "Names a passing choice.")
e("plainlp", "parity", "implies", "The plain test is weaker; if it were exact, so would the parity test be.")
e("g1", T, "implies", "Put d_n in row 1, column 1 + d_n; the rest is a one-hole board with the same scores, and Landau gives G1's inequalities (for k > d_n the slack is Σ_{j=k+1}^{n−1} (j − d_n) ≥ 0).")
e("sum2", "g1", "implies", "Peeling rows one at a time would stay exact.")
e("edgepeel", "g1", "implies", "Induction inside the class.")
# algebra
e(["ly", "cap"], T, "implies", "Li–Yao gives cap(P_D) > 0, so W(D) ≥ (n!/nⁿ)·cap > 0.")
e("stable", "cap", "implies", "Gurvits (real stable) and Anari–Oveis Gharan–Vinzant (log-concave) bound coefficients below by the capacity.")
e("gstep", "cap", "implies", "Chain the per-step bounds over all n variables.")
e(["ly", "sat"], T, "implies", "Li–Yao puts D's point in the polytope; saturation makes it a real x-ray.")
e(["ly", "round"], T, "implies", "Round Li–Yao's fractional solution.")
e("tct", T, "implies", "The conjecture is a special case.")
e("at", T, "implies", "A nonzero signed count means some witness exists.")
# other routes
e("delta", T, "implies", "δ of the accepted tournament is a witness.")
e("maxupset", "delta", "implies", "Names an accepted tournament.")
e("greedy", T, "implies", "A rule that never gets stuck produces a witness.")

PROOFS = json.load(open(os.path.join(HERE, "proofs.json")))
for n in nodes:
    if n["id"] in PROOFS:
        n["proof"] = PROOFS[n["id"]]; n.pop("evidence", None)
ACTIVE = {}
for n in nodes:
    if n["id"] in ACTIVE: n["active"] = ACTIVE[n["id"]]
ids = [n["id"] for n in nodes]
assert len(ids) == len(set(ids))
for x in E: assert all(f in ids for f in (x["from"] if isinstance(x["from"], list) else [x["from"]])) and x["to"] in ids, x
for n in nodes: assert n["status"] in ("proved", "empirical", "open", "disproved", "idea"), n["id"]
json.dump({"updated": "2026-11-23", "areas": areas, "nodes": nodes, "edges": E},
          open(os.path.join(HERE, "graph.json"), "w"), ensure_ascii=False, indent=1)
print(len(nodes), "nodes", len(E), "edges")
