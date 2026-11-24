# NONNEG (empirical lead, slack <= 15 only; NOT yet tested on steep prefixes)

**Claim NONNEG.** For every legal prefix x ending at slack s with last letter l >= 0 there is a prefix x' whose
letters are all >= 0, with the same end slack and the same last letter, and F(x') inside F(x).

Then x'y is legal whenever xy is, and x'y solvable implies xy solvable: prefixes without negative letters are the
hardest. At s = 0 the only choice is x' = 0...0, so NONNEG contains the conjecture.

**Proved reduction.** NONNEG follows from its single-dip case: x = p n e with p nonnegative ending in 0, n a run of
negative letters (starting with -1), e >= 0. (Induction on the word: nonnegative letters pass through by
monotonicity of the step map.)

**With the mirror.** Applying NONNEG to the prefix up to the last maximum of the slack and to the reversed suffix,
the conjecture reduces to unimodal words (letters >= 0, then letters <= 0) plus NONNEG.

**Tested.** `python3 agents/nonneg/nonneg.py B`: 0 failures for B = 8, 10, 12, 14, 15 (B = 14: 8,280 sets from
nonnegative prefixes, 494 other sets; about 3 minutes). `lowpeak.py B` is the weaker form (x' never rises above its
end slack). `minimal.py B` lists the inclusion-minimal sets.

**Warning.** The set inclusions PEAK, ZERO, RUN all held to slack 12-16 and fail at 13-17 on steep prefixes (few
stones, large letters). NONNEG has to be tested there before it is believed.
