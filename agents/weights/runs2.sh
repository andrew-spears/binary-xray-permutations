#!/bin/sh
# Recheck of REPORT2.md.  About 3 minutes.
cd "$(dirname "$0")" || exit 1
g++ -O2 -o fx fx.cpp || exit 1
g++ -O2 -o tail tail.cpp || exit 1
mkdir -p out2
python3 ones0.py 24 > out2/ones0_24.txt
python3 zeros.py 20 4 > out2/zeros_20.txt
python3 zo.py 10 > out2/zo_10.txt
python3 stair.py 5 6 > out2/stair_5.txt
python3 stair.py 6 1 6 > out2/stair_6.txt
python3 stair6.py 9 > out2/stair6.txt
./tail 60 > out2/tail_60.txt
for k in 3 4 5 6 7 8; do w=""; for i in $(seq $k -1 1); do w="$w $i"; done; echo "x =$w 0"; ./fx $w 0 | tail -2; done > out2/staircase.txt
# near-staircases of section 2: see out2/near.txt (./fx e1 e2 ... prints the weights after every letter)
