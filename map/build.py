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

    N("boundedframes", "families", "Bounded frames build everything", "open",
      "There is a constant K such that every valid D has a witness whose substitution tree uses only the frames 12, 21, the solutions of the P_k, and block-free permutations with at most K points.",
      "Every permutation is a frame with blocks filled in: shrink each maximal block to a point and what remains is the frame, a permutation with no blocks of its own (or 12 / 21 when the board splits corner to corner). Repeating this inside the blocks gives a tree of frames. Example: 3 6 2 1 5 4 is the frame 2413 with two of its points widened into 21. A frame may itself repeat a diagonal — the widening shifts the stones around it and can fix that. The claim: a fixed finite list of small frames, together with P_k's own solutions, is enough to build a solution of every arrangement. Then all the difficulty would sit in a finite list plus one explicit family.",
      [board(6, D=[-3, -2, -1, 0, 2, 4], pts=perm([3, 6, 2, 1, 5, 4]), blocks=[[3, 4, 1, 2], [5, 6, 4, 5]], cap="Frame 2413 (P₄'s solution) with two points widened into 21")],
      evidence="For n ≤ 9 a greedy search found 23 frames of size ≤ 8 that, together with 12, 21 and P_k's solutions, build a witness of every valid D (mirrors and tight cuts included; checked recursively at every level). The frames needed per size so far: 1, 3, 8, 6, 4 for sizes 4–8; about half repeat a diagonal (e.g. 3 1 5 2 4, which builds ±{1, 2, 3}). Whether the sizes stay bounded as n grows is unknown. Interactive builder and data: Block-building experiments page.",
      refs="Basket agent 2026-11-23, /home/claude/agents/basket/ (frames.py, recursive.py); https://claude.ai/artifact/E4q4L8E73nqREQg4RzhDZP"),
    N("pkframes", "families", "Rule: only P_k's solutions as frames", "disproved",
      "Every valid D has a witness whose substitution tree uses only the frames 12, 21 and the solutions of the P_k.",
      "The P_k are the only arrangements that can't be split, so their solutions are the natural building blocks. Claim: gluing and P_k's solutions are all the frames ever needed.",
      [stones([-3, -2, -1, 1, 2, 3], -5, 5, cap="±{1, 2, 3}: each of its 6 solutions needs another frame")],
      evidence="False at n = 6 for ±{1, 2, 3}: two of its solutions are block-free themselves, and the others have frames like 3 1 5 2 4 or 2 5 1 6 4 3. Misses 1, 3, 17, 79 arrangements at n = 6–9.",
      refs="Basket agent 2026-11-23, framesets.py"),
    N("symframes", "families", "Rule: symmetric block-free frames", "disproved",
      "Every valid D has a witness whose substitution tree uses only 12, 21 and block-free permutations that are involutions or centrosymmetric (survive a half turn).",
      "Instead of a fixed list of frames, allow a whole describable family: every block-free frame that folds onto itself across the main diagonal or looks the same after a half turn. P_k's solutions are of this kind. Claim: these frames build a solution of every arrangement.",
      [board(6, D=[-4, -2, -1, 1, 2, 4], pts=perm([3, 6, 2, 5, 1, 4]), cap="A half-turn-symmetric block-free solution, usable as a frame")],
      evidence="With only frames that are themselves solutions (no repeated diagonal): builds everything for n ≤ 7, misses 4 arrangements at n = 8 and 26 at n = 9 (no tight cut, mirrors counted). Allowing symmetric frames that repeat a diagonal (e.g. 4 6 3 1 5 2): misses 2 at n = 8 (the Q₈ pair) and 18 at n = 9. The remaining misses need asymmetric frames such as 5 2 6 4 1 3, 3 1 5 2 4, 5 7 4 2 6 1 3; adding frames greedily, 12 more (10 of them repeating a diagonal) fix everything to n = 9.",
      refs="Basket agent 2026-11-23, symfam.py, symall.py, symfix.py; Block-building experiments page"),
    N("qn", "families", "One move past P_n: two P pieces and a slide", "empirical",
      "Let D be valid with no tight cut and one minimal move past P_n (so D has n − 1 three-cycles; Q_n, the central move, is one of them). Then D has a witness of this form: a solution of P_a (or 21, 132/213 for a = 2, 3) in the top a rows, a solution of P_b in the bottom b = n − a rows, columns as in a skew sum except that the bottom piece's rightmost column slides two places right, past the top piece's two leftmost columns.",
      "Start from two solved pieces stacked corner to corner: one in the top rows, one in the bottom rows, the bottom one entirely to the left. That is a skew sum and always has a tight cut. Now slide the bottom piece's rightmost column two places to the right. Only three stones move: the bottom piece's point goes up two diagonals, and the two top points it passes each go down one. That is exactly one inward move on the stones, across the cut. Example: 3142 over 2413 with the slide gives 7 4 8 5 2 6 1 3, a solution of Q₈. Claim: every arrangement one move past P_n is built this way from two P pieces, with the cut where the move is.",
      [pair(board(8, D=[-6, -5, -3, -2, 2, 3, 5, 6], pts=perm([8, 6, 7, 5, 2, 4, 1, 3])), board(8, D=[-6, -5, -3, 0, 1, 2, 5, 6], pts=perm([7, 4, 8, 5, 2, 6, 1, 3]), cand=[[2, 4], [4, 5], [6, 6]]), "slide →",
            cap="3142 over 2413: skew sum (tight cut), then the slide gives Q₈")],
      evidence="Holds for every such D at n = 8, 9, 10 (2, 3, 3 arrangements up to mirror), and for Q_n for n = 7–12 (exactly one such splice each). All have exactly 4 witnesses (P_n has 2).",
      refs="Basket agent 2026-11-23, splice.py, nearP.py"),
    N("ptwo", "families", "Two moves past P_n: a chain of three P pieces", "disproved",
      "Every valid no-tight-cut D two minimal moves past P_n has a witness that is a chain of P pieces (solutions of P_k, or 1, 21, 132, 213), skew-stacked, with one slide of length at most 4 (either direction) at each cut.",
      "The next layer out from P_n. If one move past P_n is two P pieces and one slide, two moves might be three P pieces and two slides. Claim: that always works.",
      [board(8, D=[-6, -4, -3, -2, 2, 3, 4, 6], pts=perm([7, 6, 5, 2, 8, 3, 1, 4]), cap="21, 213, 213 stacked, with slides at both cuts")],
      evidence="Works for every such D at n = 8 and 10 and all but one at n = 9 (all have exactly 8 witnesses). Fails for D = {−7, −5, −4, −3, 0, 3, 4, 5, 7} at n = 9 (chains of up to 6 pieces, slides up to 4); its witnesses use pieces like 321 instead (e.g. 8 7 6 4 9 3 2 1 5).",
      refs="Basket agent 2026-11-23, chain.py"),
    N("movecount", "families", "A minimal move adds exactly one 3-cycle", "proved",
      "If E is obtained from D by one minimal move, then t(E) = t(D) + 1, where t(D) = C(n,3) − Σ C(s_i, 2) is the number of 3-cycles of any tournament with D's scores. So every sequence of minimal moves from D to E has length t(E) − t(D).",
      "A minimal move takes two stones whose scores are s and s + 2 and makes them both s + 1 (everything between them is full, so nothing else changes rank). That lowers the sum of squared scores by exactly 2, which is one more 3-cycle. So 'k moves past P_n' is a property of the arrangement, not of the route: it means k more 3-cycles than P_n.",
      [pair(stones([-4, -3, -1, 1, 3, 4], -5, 5), stones([-4, -3, 0, 1, 2, 4], -5, 5), "move −1, 3 → 0, 2", cap="P_6 (scores 1 1 2 3 4 4, 4 three-cycles) → Q_6 (scores 1 1 3 3 3 4, 5 three-cycles)")],
      evidence="Direct computation."),
    N("grammar", "families", "Short-slide grammar builds a witness for every arrangement", "disproved",
      "Let G be the smallest set of permutations with distinct diagonals that contains every P_k solution, 1, 21, 132, 213 and every anti-diagonal, and is closed under (a) skew-stacking two members with one column slid across the cut by at most 2, and (b) widening each point of a member into a member. Claim: every valid no-tight-cut D has a witness in G.",
      "This is the pattern from the layers past P_n made into a rule: pieces stacked with short slides, and points widened into blocks. It is a strengthening of the conjecture, not a reduction. The slide limit matters: with unlimited slides the rule covers everything for a trivial reason, because a one-row top piece with any slide just means 'add a new top row anywhere', which is peeling the top row.",
      [board(6, D=[-3, -2, -1, 1, 2, 3], pts=perm([2, 4, 6, 1, 3, 5]), cap="Counterexample {±1, ±2, ±3}: a solution, 2 4 6 1 3 5, two interleaved staircases; none of its 6 solutions is in G")],
      evidence="Covers every D at n ≤ 9 up to 12 moves past P_n, including the n = 9 exception to the three-piece chain. Fails for {±1, ±2, ±3} at n = 6 (4 moves past P_6, the most central arrangement), 1 at n = 7, 2 at n = 8, 6 at n = 9, all 13 or more moves past P_n at n = 9.",
      refs="2026-11-23, /home/claude/agents/basket/short.py, minimal.py"),
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
    N("oddcentre", "families", "The odd centre folds into a Skolem pairing", "proved",
      "For n = 2m + 1, D = {−m, …, m} has an involution witness: from a Skolem sequence of order m (m ≡ 0, 1 mod 4; fixed point at position n) or a hooked Skolem sequence of order m (m ≡ 2, 3 mod 4; fixed point at position n − 1).",
      "With an odd number of stones, the most central arrangement fills every mark from −m to m. A solution that folds across the main diagonal pairs up the positions with pair distances 1, 2, …, m and leaves one position as a fixed point. Pairing positions with distances 1…m is exactly a Skolem sequence, and when m ≡ 2, 3 mod 4 a 'hooked' one with a gap next to the end. Claim: these always give a solution.",
      [board(7, D=[-3, -2, -1, 0, 1, 2, 3], pts=perm([2, 1, 5, 7, 3, 6, 4]), cap="m = 3 (hooked): pairs (1,2) (3,5) (4,7), position 6 fixed")],
      evidence="Skolem sequences exist iff m ≡ 0, 1 mod 4; hooked Skolem sequences iff m ≡ 2, 3 mod 4. Checked by search for n ≤ 11.",
      refs="Skolem 1957; O'Keefe 1961 (hooked)"),
    N("centre", "families", "The most central arrangement is solvable", "proved",
      "For every n, the valid D with the most 3-cycles is unique, namely C_n = {−⌊n/2⌋, …, ⌊n/2⌋} with 0 removed when n is even, and C_n has a witness.",
      "Moves only ever squeeze stones together, so they end at one most-crowded arrangement: every mark near the middle filled (the middle mark empty when n is even). In score terms the scores are as equal as possible, which is why it is unique. This is the opposite end from P_n, which has the fewest 3-cycles among arrangements without a tight cut. Both ends have explicit solutions. Claim: the centre is solvable for every n.",
      [board(6, D=[-3, -2, -1, 1, 2, 3], pts=perm([2, 4, 6, 1, 3, 5]), cap="C₆ = ±{1, 2, 3}: two interleaved staircases (F1)"),
       board(7, D=[-3, -2, -1, 0, 1, 2, 3], pts=perm([2, 1, 5, 7, 3, 6, 4]), cap="C₇ = {−3…3}: a folding solution (Skolem)")],
      evidence="Uniqueness: the number of 3-cycles is C(n,3) − Σ C(s_i,2), maximised exactly when the scores differ by at most 1; checked n ≤ 12."),
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

    N("countglobal", "ideas", "Global counting forces every arrangement to be hit", "disproved",
      "For every n, (Σ_D W(D))² / Σ_D W(D)² > A_n − 1, where the sums run over valid D of size n and A_n is the number of valid D.",
      "A counting proof would build many objects (here: all permutations with distinct diagonals), count them, count the repeats, and conclude there are too many for any arrangement to be left out. Cauchy–Schwarz says the number of arrangements that get at least one witness is at least (total)² / (sum of squared counts), so if that exceeded A_n − 1, every arrangement would be hit. Claim: the counts are spread evenly enough for this to work.",
      example="n = 5: 9 arrangements, 23 witnesses, Σ W² = 77:\n23² / 77 ≈ 6.9, not above 8.\nn = 9: 490 arrangements, ΣW = 12657, ratio ≈ 208.",
      evidence="False for every n checked: the ratio is 6.9, 16.4, 34.7, 92, 208 against A_n − 1 = 8, 21, 58, 166, 489 for n = 5–9, so it covers well under half. The counts are very uneven (P_n has 2 witnesses, others hundreds), so any global count with repeats loses. A counting proof has to give a lower bound for each arrangement separately, as the capacity and move-ratio claims do.",
      refs="framesets.py (counts)"),
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
    # ---- interface walks (agents/interface) ----
    N("interface", "ideas", "Solutions are walks on pairs of Young diagrams", "proved",
      "Sort D and put e_k = s_k − (k−1), σ_k = e_1 + … + e_k (the Landau slack of the first k stones). Witnesses of D correspond one-to-one to sequences of pairs of partitions (λ_k, μ_k), k = 0…n, with (λ_0, μ_0) = (λ_n, μ_n) = (∅, ∅), |λ_k| + |μ_k| = σ_k, in which step k adds one bead to each partition at offsets u and v with u + v = e_k. The allowed steps do not depend on k or n. If all σ_k ≤ B, only finitely many pairs can occur, so whether D has a witness is decided by a finite automaton A_B that reads e_1, e_2, … and is the same for every n.",
      "Number the rows from the bottom. Then a stone on the k-th smallest diagonal sits in a cell whose row number plus column number is a fixed target, and the targets increase with k. Place the stones in that order. After k stones, all that matters for the future is which rows and which columns are used. With no drift these would be rows 1…k and columns 1…k. The slack σ_k says exactly how far the used rows and used columns together stick out above that, so the two sets are described by two Young diagrams with σ_k boxes in total. A solution is a walk on such pairs that starts and ends at the empty pair. Nothing in the rules for one step mentions n. Claim: solutions are exactly these walks, and when the slack stays below a fixed bound, one finite machine decides solvability for boards of every size.",
      pics=[board(5, D=[-3, -1, 0, 1, 3], pts=perm([1, 5, 4, 3, 2]), cap="D = {−3,−1,0,1,3}: e = (1,1,0,−1,−1), slacks 1,2,2,1,0")],
      example="The board above, rows numbered from the bottom, stones in order of diagonal:\n(row, column) = (1,2), (2,3), (5,1), (3,4), (4,5); row + column = 3, 5, 6, 7, 9.\nUsed rows / columns after each stone, as (rows diagram, columns diagram):\n{1} / {2}: (∅, 1)   {1,2} / {2,3}: (∅, 1+1)   {1,2,5} / {1,2,3}: (2, ∅)\n{1,2,3,5} / {1,2,3,4}: (1, ∅)   all / all: (∅, ∅).\nBox counts 1, 2, 2, 1, 0 are the slacks.",
      refs="agents/interface/README.md §1; check_walks.py (walk count = number of witnesses, all valid D, n ≤ 8)"),
    N("slackB", "ideas", "Bounded slack: one finite machine per bound", "open",
      "For every B ≥ 1, the automaton A_B accepts every valid no-tight-cut word with all slacks ≤ B. Equivalently: for every B, every valid D of every size whose Landau slacks are all ≤ B has a witness.",
      "The slack measures how far an arrangement is from the start. P_n is the family with slack 1 everywhere, and it needed its own formula. This card slices the whole problem by slack instead of by board size: for a fixed bound there are arrangements of every size, but only finitely many interface states, so the question for that bound is a finite check. Each bound settled is a theorem about all n at once. A proof for every bound needs a description of which interface states are reachable after a given prefix; the red cards below are the simple descriptions that fail. What the machine shows: after a few stones with e_k = 0 every pair of diagrams of the right size is reachable, and what matters is only the part of the word since that last happened. Claim: for every bound, the machine accepts every valid word.",
      example="B = 1: the only words are e = (1, 0, …, 0, −1), which is P_n.\nThe machine has 3 states and accepts all of them: P_n is solvable for every n.",
      evidence="Settled for B ≤ 16 by complete search of A_B (see the card for B = 16). Open for B ≥ 17, where only n ≤ 22 is known. The statement about stones with e_k = 0 was checked for B ≤ 8: from every reachable set of the machine after which a letter 0 is allowed, at most 7 letters 0 lead to the set of all pairs. From a single interface state this is false (at slack 1 the two states just alternate).",
      refs="agents/interface/README.md §2, §4; flat.py"),
    N("slack16", "ideas", "Every arrangement with slack at most 16 is solvable", "empirical",
      "For every n, every valid D whose Landau slacks σ_k are all ≤ 16 has a witness.",
      "The slack of a cut is the total drift of the stones to its left. The largest slack of an arrangement of size n is about n²/8, so small boards have small slack, but so do arrangements of any size that stay close to the start. For slack up to 16 the interface machine has a few thousand states, and a program can run through all of them. Claim: every arrangement of any size whose slacks never exceed 16 has a solution.",
      example="P_n has slack 1 at every cut. A minimal move raises the slack by 1 at the cuts between its two stones,\nso P_n followed by any 15 minimal moves is covered, for every n.\nEvery D with n ≤ 11 has slack ≤ 16.",
      evidence="Not a sample: the automaton A_16 (22,358 reachable states after determinising, 11 s, 0.94 GB) accepts every valid word, and by the interface card this covers every n. It is listed as empirical only because the finite check is done by a program. Three implementations give the same verdict (Python for B ≤ 8, two C++ programs for B ≤ 12), and the step rule was compared with brute force on all 6,742 multisets with repeats for n ≤ 8, including the 39 with no solution. B = 17 was not done: the program packs a state into 64 bits, which stops at B = 16, and the search would also need more than the 7 GB available. Does not depend on the conjecture at any size. Recheck: g++ -O2 -o slack_dfa slack_dfa.cpp && ./slack_dfa 16.",
      refs="agents/interface/slack_dfa.cpp, slack_dfa.py, slack_dfa2.cpp, audit_step.py"),
    N("alivedom", "ideas", "Alive sets are closed under moving boxes down", "disproved",
      "For every valid prefix, the set of alive interface states (λ, μ) is closed under replacing λ or μ by a diagram it dominates (equivalently, moving a box to a lower row), or under the reverse; the same for the combined diagram of rows and columns interleaved.",
      "An induction over the slack bound needs a description of which hole states are still alive after a prefix. The simplest hope is an order-theoretic shape, like Landau's own condition: if a state is alive, so is every 'more spread out' one. Claim: alive sets have that shape.",
      evidence="False in every version. With slack ≤ 6, 100 distinct alive sets occur: all are symmetric under swapping rows and columns, but only 14 are closed downward and 14 upward under dominance, and only 20 are intervals in the interleaved form. Example at slack 5: with no row holes, the column diagrams 41, 32, 311, 221 are alive and 5, 2111, 11111 are dead — the middle of the order survives, both extremes die.",
      refs="2026-11-23, agents/basket/alive.py, shape.py, shape2.py"),
    N("alivebox", "ideas", "Alive sets are boxes", "disproved",
      "For every valid prefix, an interface state (λ, μ) of the current slack is alive exactly when its four dimensions (longest row and number of rows of λ and of μ) are at most the largest values of those dimensions among alive states.",
      "Alive sets are not closed in either direction under moving boxes, because both very deep and very spread-out hole patterns die. The next simplest hope is a two-sided rule: alive means fitting inside a box, not too wide and not too tall. Claim: the alive set is always exactly the states that fit in its bounding box.",
      evidence="Exact for only 20 of the 100 alive sets with slack ≤ 6 and 33 of 363 with slack ≤ 8. Worse, no rule using only these four dimensions (plus the split of the slack between rows and columns) works: at slack 8, with no row holes, column pattern 4 2 2 is alive while 4 3 1 is dead, and the two have the same width, height and size. Adding the number of odd parts separates every case to slack 8, but only because those features then identify every state uniquely, so that says nothing.",
      refs="2026-11-23, agents/basket/twosided.py, parityfeat.py"),
    N("online", "ideas", "Online rule: place each stone before seeing the next diagonal", "disproved",
      "There is a rule that places the stone of the k-th smallest diagonal knowing only n and the k smallest diagonals, and that completes a witness for every valid D.",
      "The simplest proof in diagonal order would be a rule with no lookahead. Claim: such a rule exists.",
      example="n = 8: whatever the rule does, an adversary who reveals the diagonals one at a time can steer to a valid D on which the rule is stuck. No two arrangements suffice for this; the adversary needs a branching strategy.",
      evidence="Exhaustive game search: a rule exists for n ≤ 7 and for no n from 8 to 11. On the automaton: exists for B ≤ 2, not for B = 3…8.",
      refs="agents/interface/online_fixed_n.py, online_check.py (independent recheck, n ≤ 9), online_game.py, online_cex.py"),
    N("summary", "ideas", "Invariant from the slack and the last few diagonals", "disproved",
      "For some L with 1 ≤ L ≤ 4 there is a family I(σ, e_{k−L+1}, …, e_k) of nonempty sets of interface states such that every prefix with that slack and those last L letters reaches every state of I, and each step maps I onto a superset of the next I.",
      "An induction along the word needs an invariant: a set of interface states guaranteed reachable. Claim: the invariant can be read off from the current slack and a bounded window of recent diagonals.",
      example="Window of 2 letters, arrangements with slack ≤ 5: the largest family satisfying the step condition is empty, for instance at slack 1 after the letters (0, 0).",
      evidence="Largest such family computed exactly inside slack ≤ B: a window of L = 1 letter works only for B ≤ 2, L = 2 only for B ≤ 4, L = 3 only for B ≤ 8, L = 4 only for B ≤ 13. So no window of at most 4 letters works for all D, and the window needed grows with the slack bound. Windows of 5 or more letters were not run to failure. Replacing the window by the last letter plus a capped counter (length, largest slack so far, sum of slacks, largest letter, steps since the last rise) fails from B = 4.",
      refs="agents/interface/invariant.cpp, invariant.py, invariant_other.py"),
    N("meet", "ideas", "Counting: the two halves must meet at the middle cut", "disproved",
      "For every valid no-tight-cut D of size n and k = ⌊n/2⌋: |F_k| + |G_k| > N_k, where F_k is the set of interface states reachable by placing the k smallest diagonals, G_k the set reachable backwards by placing the n − k largest, and N_k the number of all interface states at that cut.",
      "D has a solution exactly when some interface state at a cut can be reached both from the left and from the right. If the two reachable sets together had more elements than there are states, they would have to share one. Claim: at the middle cut they always do.",
      example="n = 15, D = {−9, …, 0, 2, 8, 10, 12, 13}, cut after 7 stones: the two sets together have 0.973 times the number of states (they still meet).",
      evidence="True for every D with n ≤ 14 (exhaustive; the smallest ratio falls steadily: 2, 1.75, 1.6, 1.56, 1.47, 1.41, 1.33, 1.23, 1.14, 1.10, 1.03 for n = 4…14). Fails at n = 15 (example).",
      refs="agents/interface/meet.cpp, meet.py"),
    N("twice", "ideas", "Each diagonal used at most twice", "empirical",
      "Let d_1 ≤ … ≤ d_n be integers in which no value occurs more than twice, with Σ_{i≤k} (d_i + n − i) ≥ C(k,2) for all k and equality at k = n. Then some permutation has exactly these diagonals, with these multiplicities.",
      "The conjecture asks for one stone per chosen diagonal. Allow a diagonal to be chosen twice, keeping the same Landau sums. With three stones on one diagonal Landau is no longer enough, and with five even a fractional solution is not enough. With at most two, no failure has turned up. A stronger statement can be easier to prove by induction, because steps may pass through arrangements with a doubled diagonal: for example, swapping two adjacent columns of any solution moves one stone up one diagonal and one stone down one, which often creates a double. Claim: Landau is sufficient whenever no diagonal is used more than twice.",
      example="n = 4, diagonals {−1, −1, 1, 1}: the permutation 2 1 4 3 has them.\nn = 6, diagonals {−2, −2, −2, 2, 2, 2} (Landau holds): no permutation. Rows 1, 2 need diagonal +2 and rows 5, 6 need −2, and both pairs land in columns 3, 4.",
      evidence="Exhaustive for n ≤ 15 (174,292,169 multisets at n = 15, no failure), and for every n when all slacks are ≤ 12 (automaton with repeats, 207,436 states). Among all multisets passing Landau, those with no solution number 1, 6, 32, 145, 634 for n = 6…10 and every one has a diagonal used at least three times. The fractional test stays exact for all multisets up to n = 11 and first fails at n = 12 with a diagonal used five times (the saturation card's example). Does not depend on the conjecture. Recheck: g++ -O2 -o twice twice.cpp && ./twice 13 2.",
      refs="agents/interface/twice.cpp, nonstrict.py, slack_dfa2.cpp, lp_fails.py"),
    N("thrice", "ideas", "Each diagonal used at most three times", "disproved",
      "The same statement with 'no value occurs more than three times'.",
      "Claim: Landau stays sufficient with triples.",
      example="n = 6, diagonals {−2, −2, −2, 2, 2, 2}: Landau holds, no permutation.",
      evidence="Smallest failure is n = 6 (unique there).",
      refs="agents/interface/twice.cpp (./twice 6 3)"),
    N("pairsum", "ideas", "Pairs with prescribed sums, any parity", "disproved",
      "If c_1 < … < c_m are integers with Σ_{i≤j} c_i ≥ j(2j+1) for all j and equality at j = m, then {1, …, 2m} can be split into pairs whose sums are c_1, …, c_m.",
      "A solution is the same as splitting {1, …, 2n} into pairs with the odd sums 2(d_k + n) + 1: an odd sum forces one odd number (a row) and one even number (a column). Dropping 'odd' gives a more symmetric puzzle with no board in it. Claim: the Landau-type condition is sufficient for any prescribed sums.",
      example="m = 4, sums (4, 8, 10, 14): no pairing of {1, …, 8}. Even sums pair odd with odd and even with even; the odd numbers can make {4,12}, {6,10} or {8,8} and the even ones {6,14}, {8,12} or {10,10}.",
      evidence="With all sums odd this is the conjecture (no failure, m ≤ 8). With even sums allowed: 1 of 37 fails at m = 4, 1026 of 50944 at m = 8.",
      refs="agents/interface/pairsum.cpp"),
    N("l1", "ideas", "Every stone within one mark of evenly spaced", "empirical",
      "Let e_1, …, e_n ∈ {−1, 0, +1} have all partial sums ≥ 0 and total 0, in any order. Then some permutation has the diagonals d_k = 2k − n − 1 + e_k (as a multiset; a value occurs twice exactly where a + is followed by a −).",
      "The evenly spaced arrangement −(n−1), −(n−3), …, n−1 is solved by the anti-diagonal. Move each stone at most one mark, keeping Landau: this is the smallest family of arrangements in which the Landau slack is unbounded, so it is not covered by the bounded-slack machine, yet every letter of the word is −1, 0 or +1. It is a test case for any induction along the word: here the set of interface states that every prefix is guaranteed to reach depends on the slack alone. Claim: all these arrangements are solvable.",
      example="n = 5, word + + 0 − −: diagonals {−3, −1, 0, 1, 3}. Witness 2 5 3 1 4.",
      evidence="All 5,798 words at n = 11 and all shorter ones have a witness. Inside slack ≤ 10 there is a family F(σ) of interface states, depending on the slack σ only, with F(σ+e) ⊆ step_e(F(σ)) for each letter e; its sizes are 2, 4, 8, 12, 24, 48, 80 for σ = 1…7, and it needs states with 3 advanced lines from slack 7 on. No description of F was found; the smallest such family (integer program, slack ≤ 7) is forced up to slack 3 and shows no pattern. For letters in {−2, …, 2} the slack plus the last two letters already fails at slack 5. Witnesses must move stones far: the least displacement max |row − k| is ≤ 1 for exactly 2^(n−1) words and reaches 3 at n = 8.",
      refs="agents/interface/letters_notes.md, letters_ansatz.py (n ≤ 11), letters_sigma.py, letters_Fclass.py, letters_min.py, letters.py"),
    N("zigzag", "ideas", "Zigzag chain from every solution", "disproved",
      "Let M be a word as in the parent card, W any witness of M, and add corner stones to get a witness of 0 M 0. Move stone 1 up one row; the stone it displaces is then one short and is moved one column right; continue, alternating rows and columns (or columns first). For every M and W the chain reaches the last stone, giving a witness of + M −.",
      "Every word of the parent card is built from single zeros and blocks + M − with M shorter, so one lemma would finish the induction: a solution of M can be turned into a solution of + M −. The natural repair passes a one-unit shortage from stone to stone. Claim: this chain always ends at the last stone.",
      example="n = 10, M = + 0 − + + 0 − −: from 4 of the 8 witnesses of M the chain returns to its starting position after 28 moves without ever touching the last stone.",
      evidence="True for every witness of every M up to n = 9. At n = 10 it fails for 4 witnesses of one word; the other 4 work. What survives: start only from witnesses that this induction built (direct sums and chain results). That class is non-empty for every word with n ≤ 13 (41,835 words at n = 13; the chain loops in 1,096 of about 200,000 runs, never for all witnesses of a word). No simple choice of witness (least displacement, fewest inversions, lexicographic) always works. The chain never gets stuck at the border: by the leapfrog card its only failure is a closed loop.",
      refs="agents/interface/letters_zigzag.py, letters_zigzag_exc.py, letters_closed.py, letters_static.py, leapfrog.py"),
    N("rounds", "ideas", "The chain runs in rounds", "proved",
      "Let M = U_1 … U_k, each U_i a single 0 or a block + M′ −, and take any witness of each U_i, placed as a direct sum between two corner stones (U_0 and U_{k+1}). Run the zigzag chain of the card 'Zigzag chain from every solution'. Then: (a) the mark only passes between stones of the same U_i or of neighbouring ones; (b) whenever it passes down from U_j to U_{j−1} it goes on down to the bottom stone, undoing every move of the current round outside U_j, so that only U_j has changed; (c) the bottom stone then makes its other move. If U_j in position q sends back a mark that entered by a row move and ends in position q′, then in position q′ it sends back a mark entering by a row move and ends in q; the same for column moves.",
      "The chain looks like one long walk, but it has a simple large-scale shape. The mark climbs through the blocks of M one after another. Each block either lets it through to the next block or sends it back, and a mark that is sent back retraces its steps all the way to the bottom stone, repairing every block below on the way. So a run is a sequence of rounds, started alternately by a row move and a column move; each failed round changes exactly one block. Whether a block lets the mark through depends only on the block's position and on whether the mark enters by a row or a column move.",
      example="M = (+ 0 −)(+ + 0 − −), n = 10. The witness of + 0 − built rows-first always lets the mark through and hands it on by a column move; the one built columns-first hands it on by a row move. A witness of + + 0 − − built rows-first lets a row move through and sends a column move back. So the chain loops exactly when both blocks were built with the same first move.",
      evidence="Proof: let I_i be the rows (= columns) of U_i. By induction on the moves, below the marked block each boundary has exactly one pair of neighbouring lines exchanged (the two rows or the two columns at the boundary), and above it nothing has moved; so a move either stays inside a block, or exchanges the two lines at a boundary going up, or undoes that exchange going down. When the mark comes down into U_{j−1}, no stone of U_{j−1} or below has moved since the mark left, so the stone that receives it is the one that passed it up, back in its earlier place, and its next move is of the kind by which it first received the mark; that move is its own inverse, so it undoes the earlier one, and so on down to the bottom stone. Checked on 1,705,474 chain runs (n ≤ 15): no exception.",
      refs="agents/interface/letters_pass.py (15: 25 seconds), letters_trace.py, letters_notes.md"),
    N("pass", "ideas", "Every block lets each kind of move through", "empirical",
      "Let K be the class of witnesses built by direct sums and the zigzag chain (K(0) = one stone; K(+ M −) = all results of the chain from direct sums of members of K of the blocks of M). For every block B = + M − and for each kind of move m (row or column) there is a witness in K(B) which, placed between two corner stones, lets a mark that enters by m through to the top stone.",
      "By the card 'The chain runs in rounds', the first round reaches the top if every block lets the mark through. A single stone always does. So if every block had, for each kind of entering move, a witness that lets it through, one could choose the witnesses from the bottom up and the first round would never fail. Because of the reflection that exchanges rows and columns, it is enough that some witness of the block lets some move through. Claim: such witnesses always exist.",
      example="B = + + 0 − −: the witness built rows-first lets a row move through and sends a column move back; the one built columns-first does the opposite.",
      evidence="True for all 9,360 blocks of length ≤ 13 (69,907 distinct witnesses in K; 510 of them send both kinds of move back, first at length 10). The claim for B is about a second mark crossing the trail of the first, and is not an induction by itself: for + 0 … 0 − the second mark visits every third stone, so what a block does depends on its length mod 3.",
      refs="agents/interface/letters_pass.py (15: 25 seconds), letters_scatter.py"),
    N("shorten3", "ideas", "Shortening induction: three ways to lengthen a solvable arrangement", "open",
      "For all letter strings x, y: if the word x u y is a valid arrangement with a solution, then x v y has a solution, for each of: PEAK u = (0), v = (1, 0, −1). ZERO u = (0, −1), v = (0, 0, −1). RUN(a, b), a, b ≥ 1, (a, b) ≠ (1, 1): v = (a, a−1, …, −b), u = (a−1, …, −(b−1)) with the letter a−b written twice.",
      "Write an arrangement as its word: for each stone, from the lowest diagonal up, how far it is from its evenly spaced position. A run of letters falling by one each step, such as 2, 1, 0, −1, is a block of neighbouring diagonals. Three operations make a word one or two stones longer. PEAK replaces one stone at its evenly spaced place by three neighbouring diagonals 1, 0, −1. ZERO inserts a 0 between a 0 and a −1. RUN adds one stone to a block of neighbouring diagonals whose letters cross zero. Every arrangement except the evenly spaced one is produced from a shorter valid arrangement by one of the three (proved: look at the first negative letter; it is a −1 after a 0, and before that 0 stands a 0, which gives ZERO, or a 1, which gives PEAK or RUN on the whole block). The evenly spaced arrangement is solved by the anti-diagonal. So the conjecture is equivalent to: each operation keeps an arrangement solvable. The lab shows the chain for any arrangement up to n = 9. Claim: PEAK, ZERO and RUN each turn a solvable arrangement into a solvable one.",
      example="P_4 = (1, 0, 0, −1) comes from (1, 0, −1) by ZERO, which comes from (0) by PEAK.",
      evidence="The reduction (every nonzero valid word is shortened to a valid word) is proved and checked on all 6,561 words of length ≤ 11 with slack ≤ 8. The claim itself follows from the conjecture, so tests of it say nothing new; what is needed is a proof of each operation. The natural stronger form, on whole sets of reachable hole patterns, is false (red child).",
      refs="agents/interface/run_rule.py (docstring: the reduction), SHORTEN_BRIEF.md",
      vis={"file": "labs/shorten.html", "title": "Shorten an arrangement"}),
    N("shorten3set", "ideas", "The three operations never lose a reachable hole pattern", "disproved",
      "F(x) = set of interface states reachable after the prefix x. For every legal prefix x: F(x 0) ⊆ F(x 1 0 −1), F(x −1) ⊆ F(x 0 −1), and F(x u) ⊆ F(x v) for every RUN(a, b).",
      "The interface machine reads a word letter by letter and keeps the set of hole patterns it can reach. If the longer piece v reaches every hole pattern that the shorter piece u reaches, after every beginning x, then the operation keeps arrangements solvable, and this can be tested on the finite machine for each slack bound. It holds for every beginning with slack up to 12, and then breaks. Claim: after every legal beginning, the longer piece reaches every hole pattern the shorter piece reaches.",
      example="RUN(2, 1) fails after x = (4, 3, 2, 1): two hole patterns are reached by x 1 1 0 and not by x 2 1 0 −1 (slack 13 on the way). ZERO fails after x = (2, 3, 3, 2, 2, 1, 1, 0), slack 14.",
      evidence="Slack ≤ 12: 6,061 cases (rule, reachable set, slack, last letter), 0 failures. Slack ≤ 14: ZERO fails in 1 of 904 situations, RUN(2, 1) in 2 of 1,344; PEAK holds in all 1,941. The missing patterns can still be completed, so they are not dead states. With multiplicity (number of placements per pattern) PEAK holds in all 2,812 tests at slack ≤ 6, ZERO and RUN(2, 1) fail. Recheck: python3 zero_fail.py 14 (12 minutes; prints the shortest failing words), run_rule.py 12 (50 seconds), count_rule.py 6 8.",
      refs="agents/interface/run_rule.py, zero_fail.py, count_rule.py, shorten.py (search that found the rules), letters_notes.md"),
    N("l1red", "ideas", "Three shortening rules would settle 'within one mark'", "empirical",
      "For a prefix x with letters in {−1, 0, +1} and partial sums ≥ 0 let F(x) be the set of interface states (pairs of diagrams) reachable after x. (A) F(x 0) ⊆ F(x 0 0). (B) F(x 0) ⊆ F(x + 0 −). (C) F(x) ⊆ F(x + −). All three hold for every such x.",
      "The interface machine reads the word letter by letter and keeps the set of hole patterns that can be reached. If replacing a piece of the word by a longer piece never loses a reachable pattern, then the longer word is solvable whenever the shorter one is. Three such rules are enough for the family where every stone is within one mark of evenly spaced: (A) a zero may be doubled, (B) a zero may be replaced by + 0 −, (C) + − may be inserted anywhere. Any word of the family with a + in it contains + 0 … 0 −, possibly with no zeros. With no zeros, rule (C) backwards removes it. Otherwise rule (A) backwards shortens the zeros to one and rule (B) backwards turns + 0 − into 0. The word left at the end is all zeros, which is the anti-diagonal. For arrangements with distinct diagonals + − never occurs and rules (A), (B) suffice. No rule is true for a single hole pattern, only for the whole reachable set, and (A) is false for general words. Claim: the three rules hold after every prefix of the family.",
      example="P_n is + 0 … 0 −: rule (A) shortens it to + 0 −, rule (B) to 0.",
      evidence="All three hold for every prefix with slack ≤ 23 (233 distinct situations), so every word of the family with slack ≤ 23 is solvable for every n. No proof for all slacks: that needs a description of the reachable sets, or a direct way to turn a solution of the short word into one of the long word with the same hole pattern. Recheck: python3 l1_reduce.py 24 (1 minute).",
      refs="agents/interface/l1_reduce.py, rewrite_l1.py, letters_notes.md"),
    N("paritycount", "ideas", "Odd and even rows: a count every reachable hole pattern obeys", "proved",
      "Reflect the rows, so stone j has row + column = 2j + e_j. After a prefix of k stones with z even letters and p odd letters, every reachable state (R, C) (used rows, used columns) satisfies |#odd(R) − #odd(C)| ≤ p and |#odd(R) + #odd(C) − k| ≤ z.",
      "Colour the board like a chessboard. A stone with an even letter sits on a cell whose row and column have the same parity, a stone with an odd letter on a cell where they differ. Counting the four kinds of stones gives the number of each kind from the hole pattern alone: #(odd row, odd column) = (#odd(R) + #odd(C) − p)/2, and so on. All four must be between 0 and the number of letters of that parity. The number of odd rows in a hole pattern is what the 2-core of its diagram measures, so this is a condition on the two 2-cores. It explains the first missing patterns: the pair (staircase with t rows, staircase with t rows), which has slack t(t+1), cannot be reached before the prefix has t even letters. So the number of zeros needed before every pattern is reachable grows like the square root of the slack, and no bounded window can work. Claim: the two inequalities hold for every reachable state.",
      example="After + + + + + + 0 the pattern ((2,1), (2,1)) is the only one of 65 missing: it would need two stones on (odd, odd) cells and there is one even letter.",
      evidence="Proof: count stones by (row parity, column parity); even letters give equal parities, odd letters unequal. The condition is far from exact: for words with letters −1, 0, +1 and distinct diagonals, slack ≤ 6 and length ≤ 9, of 1,935 unreachable (prefix, pattern) pairs it rules out 45; adding a sum test inside each parity class rules out 1,182. The rest need the same split repeated on rows mod 4, 8, …: e.g. after + + + + the pattern rows {1,2,3,6}, columns {1,2,4,5} fails because no free cell has row + column = 9.",
      refs="agents/interface/parity_test.py (6 9 l1: 1 minute), letters_notes.md"),
    N("neardiag", "ideas", "Plus and minus stones next to the main diagonal", "disproved",
      "Every word with letters −1, 0, +1 (distinct diagonals) has a witness in which each + stone k is at (k, k+1) or (k+1, k) and each − stone at (k−1, k) or (k, k−1), in reflected rows.",
      "In the witnesses of P_n and of + + 0 − − the + and − stones sit right next to the main diagonal and only the 0 stones move far. If that were always possible, the + and − stones would be fixed up to a two-way choice and the problem would become: pair the remaining rows with the remaining columns so that the midpoints are exactly the positions of the zeros. Claim: such a witness always exists.",
      example="+ + 0 0 − − (n = 6) has no such witness; its witnesses move a − stone two rows away.",
      evidence="Fails for 1 of 17 words at n = 6, 106 of 423 at n = 10, 770 of 2,283 at n = 12. With the choice fixed (+ at (k, k+1), − at (k−1, k)) it already fails for + 0 0 −.",
      refs="agents/l1form/form2.py, form.py"),
    N("zeros", "ideas", "Two more zeros never lose a hole pattern", "disproved",
      "For every legal prefix x (any letters) after which a letter 0 is allowed, F(x) ⊆ F(x 0 0).",
      "After a few stones with letter 0 the machine reaches every hole pattern (card 'Bounded slack'). The simplest reason would be that zeros only ever add patterns. One zero can swap patterns around, so the claim is for two. Claim: adding two zeros to a prefix keeps every reachable pattern.",
      example="Fails first at slack 8, after a prefix ending in +1: 131 patterns are reachable and one of them is lost.",
      evidence="True for slack ≤ 7. With slack ≤ 12 it fails in 15 of 1,236 situations (reachable set, slack, last letter), first at slack 8. Among rewrites of at most 2 letters, four lose nothing for slack ≤ 12: (−1) → (0, −1), (−2) → (−2, 0), (−1, −1) → (−2, 0), (−1, −2) → (−2, −1). Inside the family with letters −1, 0, +1 the rule does hold (card 'Two shortening rules').",
      refs="agents/interface/rewrite.py (10 2: 11 seconds), letters_notes.md"),
    N("lookahead", "ideas", "A rule that sees three diagonals ahead", "disproved",
      "For every slack bound B there is a rule that places the k-th stone knowing only the diagonals of stones 1 … k+3.",
      "With no lookahead there is no rule (card 'Online rule'). The next hope is a rule that looks a few stones ahead. Claim: seeing the current diagonal and the next three is enough for every slack bound.",
      example="Seeing three ahead is enough for slack ≤ 8 and fails at slack 9.",
      evidence="Exact game search, knowing L letters (the current one and L − 1 ahead): L = 1, 2 win only for B ≤ 2, L = 3 only for B ≤ 4, L = 4 only for B ≤ 8 (loses at B = 9 and 10). L = 5 wins at B = 9, 11, 13; B = 14 was not run. The thresholds 2, 4, 8 are the same as for an invariant that remembers L − 1 past letters (card 'Invariant from the slack and the last few diagonals'), so the lookahead needed seems to grow with the slack bound; whether some larger fixed lookahead works for all B is not settled.",
      refs="agents/interface/lookahead_game.py (9 4: under a minute)"),
    N("twoends", "ideas", "Repairing from both ends works from every solution", "empirical",
      "Let M be a word as in the card 'Every stone within one mark of evenly spaced', w ANY witness of M, with corner stones added. A bottom round is the zigzag chain from the bottom stone (rows first or columns first) until the mark is on the top stone (success) or back on the bottom stone; a top round is the same from the top stone downwards (the top stone is one too high: swap it with the previous row or column, and so on). A round that comes back leaves another witness of M. From every w, some sequence of rounds that come back, followed by one that succeeds, exists; so a witness of + M − is reached.",
      "The zigzag chain repairs the board from the bottom stone only, and from some solutions it loops. But the board is equally wrong at the top stone, which is one mark too high, and the same repair can be run downwards from there. A failed round of either kind leaves a different solution of the middle word, so the two kinds of rounds can be mixed. The round graph makes this exact: the solutions of the middle word are joined by failed rounds, and a loop of the one-ended chain is a closed walk in that graph. Claim: with rounds from both ends allowed, a successful round is reachable from every solution of every middle word, not only from specially built ones.",
      example="n = 10, M = + 0 − + + 0 − −: from the 4 witnesses where the bottom chain loops, a round from the top succeeds.",
      evidence="True for all 596,013 witnesses (distinct boards) of all middle words up to n = 15. Bottom rounds alone fail for 4, 20, 88, 392, 1,604, 6,940 witnesses at n = 10 … 15. From n = 12 some witnesses have no successful single round of either kind (10, 42, 210, 922 at n = 12 … 15), so a mixed sequence is needed. Moving the two marks in any order (not in whole rounds) also always reaches a witness (n ≤ 13). No rule for the order of the rounds and no proof. It is not known whether this is more than 'a successful round exists somewhere and the round graph is connected'.",
      refs="agents/interface/letters_two_rounds.py (15: 1 minute), letters_two.py (13: 7 seconds), letters_notes.md"),
    N("flip", "ideas", "A loop is cured by flipping one block", "disproved",
      "With M = B_1 … B_k and K as in the card 'Every block lets each kind of move through', call the two results of the chain from the same start (rows first, columns first) siblings. If the chain from a_1 ⊕ … ⊕ a_k (a_i ∈ K(B_i), plus corner stones) closes into a loop, then for some i it reaches the last stone after a_i is replaced by its sibling.",
      "The solutions the induction builds come in pairs: the chain can start with a row move or a column move, and these are the two ends of one leapfrog path. So every block inside M carries a two-way choice, and in small cases a loop is caused by two blocks whose choices clash. Claim: switching one block always removes the loop.",
      example="n = 15, M = (+ 0 −)(+ + 0 − −)(+ + 0 − −) with all three built rows-first. The second block sends the mark back. Switching the first or the second block gets the mark past the second block, but for one of the two ways the inside of the second block can be built the third block then sends it back; switching the third block changes nothing.",
      evidence="True for every loop up to n = 14. Fails at n = 15 (the example); 138 of 42,052 loops up to n = 16 are not cured by one switch. Switching both the first and the third block cures the example.",
      refs="agents/interface/letters_flip.py (16: 1 minute), letters_trace.py, letters_bits.py, letters_chir.py, letters_canon.py, letters_pos.py"),
    N("leapfrog", "ideas", "Solutions are the ends of leapfrog paths", "proved",
      "Let D be valid of size n+1 with distinct diagonals and largest diagonal n−1 (last letter −1), and let b_1, …, b_n be the targets r′ + c of its other stones. Let X be the set of permutation matrices on [n]² with one marked stone whose sums r′ + c, with the marked one raised by 1, are b_1, …, b_n. Let R swap the marked stone's row with the next row and leave the mark in its row; C the same for columns. Then R and C are involutions on X, undefined only when the mark is in the last row (R) or last column (C); the components of X are alternating paths and cycles; and the number of witnesses of D is twice the number of paths.",
      "Take a solution, remove the top stone, and pull the stone in the last row (or column) back by one: the result is a smaller board with all stones right except one that is one short. Such near-solutions can be changed in exactly two ways that keep 'one stone is one short': swap that stone's row with the next row, or its column with the next column; the shortage passes to the other stone. Each change undoes itself, so alternating them traces a path that never branches. A path can only stop when the short stone sits in the last row or column, and those positions are exactly the solutions. Claim: solutions are the ends of these paths, two per path.",
      example="D = {−1, 0, 1}, n = 2, targets 3 and 4. X has three states: stones (1,1), (2,2) with (1,1) marked; stones (1,2), (2,1) with either one marked. R and C join the first to the other two, so X is one path, and D has two witnesses, 1 3 2 and 2 1 3.",
      evidence="Proof: R swaps rows r, r+1 where the marked stone is in row r; the marked stone gains 1 and is now exact, the other loses 1 and is now the marked one, in row r; applying R again swaps back. A witness of D has its top stone at (n, n+1) or (n+1, n), since its sum is 2n+1; the stone in row n+1 (or column n+1) moved back by one gives a state with the mark in the last row (column), and conversely. With distinct diagonals the mark is never at (n, n), so these states are exactly the vertices with one edge. Checked against direct counts for n+1 ≤ 8. X is the union over j of the witnesses of 'D without its top stone, stone j one diagonal lower', so X is non-empty whenever one of those smaller arrangements is solvable.",
      refs="agents/interface/leapfrog_check.py, leapfrog_cycles.py, letters_notes.md"),
    N("nocycle", "ideas", "Leapfrog paths never close up", "disproved",
      "For D as in the parent card, X has no cycle component.",
      "If near-solutions could never run in a closed loop, any near-solution would lead to a solution, and near-solutions exist by induction on the size. Claim: there are no cycles.",
      example="n + 1 = 10, word + + 0 − + + 0 − − −: 8 paths and 2 cycles.",
      evidence="No cycle for n+1 ≤ 9 (2,031 paths at 9). At n+1 = 10: 8 cycles against 12,216 paths, in 4 words. Every word still has a path.",
      refs="agents/interface/leapfrog_cycles.py"),
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
e("boundedframes", "decomp", "implies", "For n > K and D ≠ P_n, such a witness's top frame is smaller than the board, so its blocks give a split with a realizable layout.")
e("pkframes", "boundedframes", "implies", "The case K = 2.")
e("symframes", "conj", "implies", "A witness built this way is a witness.")
e("qn", "symframes", "related", "Q_n, the central case, is where the symmetric family first fails.", "unchecked")
e("grammar", "ptwo", "related", "Generalises the chain: allows widening, which handles the n = 9 exception.", "unchecked")
e("movecount", "qn", "related", "Makes the layer of an arrangement well defined.", "unchecked")
e("ptwo", "qn", "related", "The next layer out; the same construction with one more cut.", "unchecked")
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
e(["f1", "oddcentre"], "centre", "implies", "Even n: C_n = ±{1…n/2} is F1. Odd n: the Skolem / hooked Skolem folding.")
e("centre", "pn", "related", "The two ends of the move order: most and fewest 3-cycles. Both are solved by explicit formulas.", "unchecked")
e("grammar", "centre", "related", "The short-slide grammar first fails exactly at C_6.", "unchecked")
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
e("countglobal", "conj", "implies", "If more than A_n − 1 arrangements must be hit, all A_n are.")
e("greedy", T, "implies", "A rule that never gets stuck produces a witness.")
# interface walks
e(["interface", "slackB"], T, "implies", "A valid D of size n has all slacks ≤ n²/8, so it is covered by the bound B = n²/8; an accepted word is a walk, and a walk is a witness.")
e("slack16", "slackB", "related", "The bounds B ≤ 16.", "unchecked")
e("alivedom", "slackB", "related", "A shape like this would be the natural induction hypothesis for every slack bound.", "unchecked")
e("alivebox", "slackB", "related", "A two-sided version of the same hope.", "unchecked")
e("online", "slackB", "implies", "An online rule traces an accepted walk for every word.")
e("summary", "slackB", "implies", "Induction along the word with invariant 'every state of I is reachable'; nonempty at the end means a witness.")
e("meet", T, "implies", "Two sets with more elements than their universe intersect; a common state joins a left half-walk to a right half-walk.")
e("twice", "conj", "implies", "The case with no repeated diagonal.")
e("thrice", "twice", "implies", "At most twice is a special case.")
e("twice", "sat", "related", "Answers the side question there: no gap with multiplicities ≤ 2 for n ≤ 15.", "unchecked")
e("pairsum", "conj", "implies", "The case where every sum is odd.")
e("twice", "l1", "implies", "These words use each diagonal at most twice and satisfy Landau.")
e("zigzag", "l1", "implies", "Induction on the length: a word is a concatenation of zeros and blocks + M −; direct sums handle concatenation and the chain handles + M −.")
e("flip", "l1", "implies", "Induction on the length shows K is never empty: K of a block contains both siblings of each member, so if one combination of block witnesses loops, a switched combination is available and gives a witness of + M −; direct sums handle concatenation.")
e("zigzag", "flip", "related", "The weaker statement that survives: only witnesses built by the induction, and one switch allowed.", "unchecked")
e(["rounds", "pass"], "l1", "implies", "Induction on the length: K(M) is the direct sums; for + M − choose the witnesses of the blocks of M from the bottom up so that each lets through the move handed on by the one below (a single stone always does); by the rounds card the first round reaches the top stone.")
e("flip", "pass", "related", "What replaced it: choose every block for the move that reaches it, instead of repairing a loop afterwards.", "unchecked")
e("shorten3", "conj", "implies", "Induction on n: every valid word other than the all-zero word is shortened by PEAK, ZERO or RUN to a valid word; the all-zero word is the anti-diagonal.")
e("shorten3set", "shorten3", "implies", "If the longer piece reaches every hole pattern the shorter one reaches, any completion of the shorter word completes the longer one.")
e("shorten3set", "slackB", "related", "A uniform induction step that would not depend on the slack bound; false from slack 13.", "unchecked")
e("shorten3", "l1", "implies", "With letters −1, 0, +1 only PEAK and ZERO are ever used.")
e("l1red", "shorten3set", "related", "The same kind of rule for letters −1, 0, +1 only: (B) is PEAK; these three hold through slack 23.", "unchecked")
e("zeros", "shorten3set", "related", "Another zero rule of the same kind; it fails earlier, at slack 8.", "unchecked")
e("l1red", "l1", "implies", "Induction on the length: a word with a + contains + 0…0 − (possibly no zeros); (C), or (A) and (B), reduce it to a shorter word of the family; the all-zero word is the anti-diagonal.")
e("paritycount", "slackB", "related", "A proved necessary condition on reachable hole patterns; shows the number of zeros needed to reach every pattern grows with the slack.", "unchecked")
e("paritycount", "summary", "related", "Explains why a bounded window fails: staircase pairs need about √slack even letters.", "unchecked")
e("paritycount", "parity", "related", "The counting part of the parity test, for boards with holes in both rows and columns (interface states).", "unchecked")
e("neardiag", "l1", "related", "A special form of witness that would have reduced the family to a pairing problem on the zeros; fails.", "unchecked")
e("zeros", "slackB", "related", "A monotonicity that would explain why zeros fill up the reachable set; false in general.", "unchecked")
e("zeros", "l1red", "related", "The same rule restricted to letters −1, 0, +1 is rule (A).", "unchecked")
e("lookahead", "slackB", "implies", "A rule with lookahead traces an accepted walk for every word.")
e("online", "lookahead", "related", "The case L = 1.", "unchecked")
e("twoends", "l1", "implies", "Induction on the length with no special class of witnesses: any witness of M (by induction) leads to a witness of + M −; direct sums handle concatenation.")
e("zigzag", "twoends", "related", "What survives of 'from every solution': rounds from the top stone are allowed too.", "unchecked")
e("leapfrog", "zigzag", "related", "The chain is the leapfrog walk started from 0 M 0 with the mark on stone 1.", "unchecked")
e(["leapfrog", "nocycle"], "l1", "related", "Would give only the words with no repeated diagonal (no + directly followed by −), by induction on the length: such a word ends in − or splits at a tight cut; lower the last + of the word without its final −, which is again such a word, so X is non-empty; without cycles X has a path, whose ends are witnesses.", "unchecked")

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
