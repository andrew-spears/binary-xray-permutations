# Common setup (binary x-ray conjecture)
- D = {d_1<…<d_n} ⊂ {−(n−1)…n−1}. A witness is a permutation π of {1..n} whose diagonals π(i)−i are exactly D (each once). W(D) = #witnesses.
- Valid: s_k = d_k + n − k satisfies Landau (Σ_{i≤k} s_i ≥ C(k,2), equality at n). No tight cut: strict for k<n. Conjecture (BMPS Conj 5 = Nordh Conj 10): valid ⇒ witness exists. Verified n ≤ 22. Only no-tight-cut D matter (tight cuts split into a skew sum). Mirror: D ↔ −D (transpose).
- Stones picture: D = stones on marks −(n−1)…n−1. Minimal move: two stones with exactly two empty marks between them each slide one mark inward; from "every other mark" (unique witness) these reach exactly the valid D.
- P_n (unique "prime"): D = {±(n−2)} ∪ {|d| ≤ n−3, d ≡ n−1 mod 2}; exactly 2 witnesses.
- Existing code to reuse/read: /home/claude/agents/paritydata/witenum.c (fast witness enumeration), /home/claude/agents/prime/prime.c, /home/claude/agents/blocks/blocks.c, /home/claude/agents/capacity/caplib.py (permanent, capacity), /home/claude/agents/holes/ (parity LP on boards with holes), /home/claude/agents/cell/, /home/claude/agents/dual/.
- Canonical project state (read-only for you): /home/claude/state.md.
