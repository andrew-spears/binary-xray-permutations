#!/bin/sh
# Recheck everything quoted in REPORT.md (bounded.py 21 is the heavy step).
cd "$(dirname "$0")"
python3 maxslack.py 16 11
python3 bounded.py 10
python3 bounded.py 12
python3 bounded.py 21
python3 online.py 4 8
python3 sorted.py 12 0
python3 inversions.py 9 0
python3 classA.py 8 max | tail -3
python3 classA.py 8 A | tail -2
python3 hd.py 6 | tail -3
python3 twophase.py 8 | tail -2
python3 multi.py 4 5
