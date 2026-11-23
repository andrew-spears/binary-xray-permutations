# twoadic: NOTHING (no formula) — the power of 2 dividing the number of solutions

Question: is there an exact formula N(D) = 2^k(D) · odd with k(D) read off D? That would prove N(D) ≠ 0.

Tested (`val2.py n`, all valid D, n ≤ 9). Let p = number of odd diagonals of D (p is even; in every solution exactly p/2 of
the odd-diagonal stones sit on (odd row, even column) cells and p/2 on (even row, odd column) cells).
- v_2(N) = p/2 for most D: 19 of 22 (n = 6), 46 of 59, 117 of 167, 315 of 490 (n = 9).
- Not a bound in either direction: v_2(N) − p/2 takes the values 0…4 and −2 at n = 9
  (1 1 1 1 0 −1 −1 −1 −1 has p = 8 and N = 28; 1 2 2 1 0 −1 −2 −2 −1 has p = 4 and N = 64).
- N is odd only for the evenly spaced D (transposing a solution gives another one unless every stone is on the diagonal).

No formula found. Recheck: `python3 val2.py 8` (seconds), `python3 val2.py 9` (about a minute); `python3 val.py 7 v` lists every D.
