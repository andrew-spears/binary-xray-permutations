#!/bin/sh
# Fixed rows r = p (mod 3), every phase p, on all words without a tight cut whose prefix sums stay in [1, smax].
# Usage: sh sweep.sh > lowslack_100.txt     (about 6 minutes; the last line, n = 15 with no bound, takes 4 of them)
g++ -O2 -mpclmul -o lowslack lowslack.cpp
for n in $(seq 3 28); do ./lowslack $n 2 100 | tail -1; done
for n in $(seq 3 21); do ./lowslack $n 3 100 | tail -1; done
for n in $(seq 3 18); do ./lowslack $n 4 100 | tail -1; done
for n in $(seq 3 16); do ./lowslack $n 5 100 | tail -1; done
for n in $(seq 3 15); do ./lowslack $n 99 100 | tail -1; done
