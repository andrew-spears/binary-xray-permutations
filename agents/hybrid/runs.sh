#!/bin/sh
# recheck of REPORT.md; about 40 seconds in total.  Run inside agents/hybrid.
set -e
python3 hybrid.py 12 | tee out/hybrid12.txt        # plain HYBRID: odd pairs (u, v) for the whole middle; 12 s
python3 lemmao.py 24 | tee out/lemmao24.txt        # Lemma O: O(s) inside G(s), s <= 24; path parities of 1^s, s <= 9; 1 s
python3 thmh.py 11 | tee out/thmh11.txt            # Theorem H through its proof (the named cell, pairs in O x conj O); 5 s
python3 thmh2.py 13 | tee out/thmh2_13.txt         # Theorem H2: the two stones of Theorem B inside m; 1 s
python3 normal.py 12 | tee out/normal12.txt        # extreme splits of the normal word with S inside m; 8 s
python3 normal2.py 11 5 | tee out/normal2_11.txt   # other normal prefixes z, z' for the words normal.py leaves; 5 s
python3 hybrid1.py 10 | tee out/hybrid1_10.txt     # one stone of m on a cell, u in G, v in conj G directly; 5 s
python3 fails.py 11 | tee out/fails11.txt          # the pairs (s1, m) left by normal.py: direct one-stone counts; 3 s
# longer: python3 normal.py 13 (3 min, out/normal13.txt), normal2.py 12 5 (1 min, out/normal2_12.txt), fails.py 12 (1 min, out/fails12.txt), hybrid1.py 11 (1.5 min)
