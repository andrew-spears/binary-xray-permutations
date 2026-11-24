#!/bin/sh
# recheck of agents/l2sets/REPORT.md, about 90 seconds.  Run inside agents/l2sets.
set -e
python3 neg0.py check 12          # §1: counts and classes for letters -6..2; G- = Central n step_-1(G); step relations for -k
python3 neg0.py all 13            # Theorem 0 as an algorithm: every valid word with letters <= 1, length <= 13
python3 neg0.py random 150 250    # 150 random words with letters <= 1, length >= 250
python3 neg0.py hooks 300         # (s|-) and (1^s|-) are in G(s)
python3 neg0.py split 12          # Theorem 0': every valid word with no letter >= 2 before a letter <= -2, length <= 12
python3 neg0.py splitrandom 100 120
python3 bridge.py 12              # (BRIDGE) for every valid word of length <= 12 with a letter >= 2 before a letter <= -2
python3 bridge.py random 60 30 9 2
python3 keys.py 2 9               # c = 2: F(x) is not a function of (slack, class set, last letters)
python3 blocks.py 2 10 3 central  # c = 2: no block family inside the central class
