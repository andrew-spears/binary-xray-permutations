# signed: counting witnesses with signs — NOTHING as a route for the whole board; two identities (proved)

Setting. D = {d_1 < … < d_n} valid; a witness puts stone k on (r_k, c_k), c_k − r_k = d_k. With rows reflected,
r′ = n − 1 − r, stone k has r′_k + c_k = t_k := d_k + n − 1, so witnesses are pairs (ρ, κ) of rearrangements of
δ = (n − 1, …, 1, 0) with ρ + κ = t. Hence #witnesses = [z^t] m_δ(z)², m_δ = Σ_w z^{w(δ)}.

**Identity A (proved).** A(D) := Σ_witnesses sgn(ρ) = ± K⁻¹_{δ, μ}, μ_i = d_{n+1−i} + i − 1 (i.e. μ = t sorted
decreasingly minus δ), the inverse Kostka number: m_δ = Σ_μ K⁻¹_{δ, μ} s_μ.
*Proof.* Σ_ρ sgn(ρ) z^ρ = ± a_δ(z) (Vandermonde), so A = ± [z^t] a_δ m_δ. a_δ · f = Σ_μ ⟨f, s_μ⟩ a_{μ+δ} for symmetric
f, and for t with distinct entries [z^t] a_{μ+δ} = ± [μ + δ = sort(t)]. ∎
Since δ is its own complement in the n × (n − 1) rectangle, K⁻¹_{δ, μ} = K⁻¹_{δ, μ*}; so the count with sgn(κ) is ± A.
(Eğecioğlu–Remmel: K⁻¹_{δ, μ} is a signed count of special rim hook tabloids of shape μ with hook lengths
n − 1, …, 1. Not used here.)

**Identity P (proved).** P(D) := Σ_witnesses sgn(ρ) sgn(κ) = ± [z^t] ∏_{i<j} (z_i − z_j)², and sgn(ρ) sgn(κ) is, up to
a global sign, the sign of the permutation matrix. *Proof.* a_δ(z)² = Σ_{ρ, κ} sgn(ρ) sgn(κ) z^{ρ + κ}. ∎

**Partial placements (proved, same computation, not tested).** For stones S (m of them) on rows R = λ + δ_m and columns
C = γ + δ_m: Σ sgn sgn = [z^{t_S}] a_δ(z)² s_λ(z) s_γ(z) = ⟨ D⊥ (h_{t_1} ⋯ h_{t_m}), s_λ s_γ ⟩ with D = the discriminant
as a symmetric function of m variables. Modulo 2 this is the parity theorem (card paritylr). A nonzero value for S
and for its complement on the complementary rows and columns gives a witness; this asks less than an odd split.

**Test (signed.py).** A = 0 or P = 0 does happen, and both together from n = 9:

| n | valid D | A = 0 | P = 0 | both |
|--:|--:|--:|--:|--:|
| 6 | 22 | 4 | 4 | 0 |
| 7 | 59 | 10 | 10 | 0 |
| 8 | 167 | 25 | 25 | 0 |
| 9 | 490 | 82 | 73 | 7 |
| 10 | 1,486 | 216 | 228 | 28 |

First D with A = P = 0: {−7, −6, −4, −3, 1, 3, 4, 5, 7} (8 witnesses).

Recheck: `python3 signed.py 9` (20 s), `python3 signed.py 10` (3 min).
