# capcut: universal hole patterns at a cut 1|0 for capped letters

`python3 capcut.py LEN SMAX C` (10 s for `9 8 2`).

NOTHING yet (exploratory). For letters in [-2, 2], prefixes of length <= 9 and slack <= 8:
the set U(s) of patterns reachable by every prefix ending in 1 and completable from every
suffix starting with 0 is nonempty for s = 1..8 (sizes 2, 4, 4, 6, 6, 12, 16, 28).
Range is far too small to trust (set-level claims in this repo have failed at slack 13-17).
