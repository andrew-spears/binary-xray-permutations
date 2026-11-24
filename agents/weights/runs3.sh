#!/bin/sh
# Recheck of REPORT3.md.  About 2 minutes.
mkdir -p out2
python3 maya.py > out2/maya.txt
python3 mix.py 10 40 > out2/mix.txt
python3 mix2.py 8 24 > out2/mix2.txt
python3 hub.py 10 > out2/hub.txt
python3 greedy.py 9 > out2/greedy.txt
(python3 items.py class 10 26; python3 items.py shift 6 1; python3 items.py sets 8 9; python3 items.py ones 4 7; python3 items.py block 9 6) > out2/items.txt
