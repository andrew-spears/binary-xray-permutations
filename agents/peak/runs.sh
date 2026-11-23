#!/bin/sh
# the runs quoted in REPORT.md (logs in logs/); needs g++
g++ -O2 -o peak_check peak_check.cpp && g++ -O2 -o cut_check cut_check.cpp || exit 1
mkdir -p logs
run() { f=logs/$1_$(echo $2 | tr ' ' '_').log; /usr/bin/time -f "%es %MKB" ./$1_check $2 > $f 2> $f.err; tail -1 $f.err >> $f; rm $f.err; }
for a in "17 -1000 1000 3" "31 -1 1" "24 -1 2" "21 -1000 3" "20"; do run peak "$a"; done
for a in "18" "22" "24 1 0 0 0" "26 1 0 0 0 0" "27 1 0 0 0 0"; do run cut "$a"; done    # the last two need 4 and 7 GB
./cut_check 16 0 0 2 0 0 | grep common > logs/common_16.log
python3 verify_nonneg.py > logs/verify_nonneg.log
