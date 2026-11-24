#!/bin/sh
# recheck of agents/damage/REPORT.md; writes out_runs.txt
{
echo "== cores.py"; python3 cores.py
echo "== small.py 9 10 -3"; python3 small.py 9 10 -3
echo "== small.py 11 11 -3 2"; python3 small.py 11 11 -3 2
echo "== lev.py 6 7 12 2 2 -3"; python3 lev.py 6 7 12 2 2 -3
echo "== CUT=1 lev.py 6 7 12 2 2 -3"; CUT=1 python3 lev.py 6 7 12 2 2 -3
echo "== CUT=1 lev.py 5 8 11 2 2 -3"; CUT=1 python3 lev.py 5 8 11 2 2 -3
echo "== landau.py 4 7 12 -3"; python3 landau.py 4 7 12 -3
} > out_runs.txt 2>&1
python3 sword.py 6 '2 2 2 2 1 0 0'; python3 sword.py 7 '2 2 2 2 2 1 0 0'   # counterexamples to statement S (not in out_runs.txt)
