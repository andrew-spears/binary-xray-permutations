#!/bin/sh
# recheck of agents/onehigh/REPORT.md, about 40 seconds.  Run inside agents/onehigh.
set -e
python3 oh.py                    > out_runs.txt   # predecessor formula = maya.succ
python3 tight.py 12             >> out_runs.txt   # Lemmas A, B, C, D on all states of slack <= 12
python3 exit.py ones 14         >> out_runs.txt   # what is missing after 2 1^j and after 2 1^j 0
python3 exit.py all 8 7 13      >> out_runs.txt   # (X): everything is back one letter after the first zero
python3 exit.py true 12         >> out_runs.txt   # the missing part depends on x
python3 fam.py 13               >> out_runs.txt   # the two routes as slack-only families
python3 exit.py thin 24         >> out_runs.txt   # (X) on all thin-shaped targets of slack 23, 24
python3 exit.py random 300 40   >> out_runs.txt   # (X) on random targets, slack 34..46
python3 exit.py random 100 90   >> out_runs.txt
python3 exit.py block 13        >> out_runs.txt   # higher blocks need more zeros
