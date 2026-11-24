#!/bin/sh
# Recheck of REPORT.md (about 5 minutes, 0.7 GB).  Data files go to $W (default /tmp/weights), outputs to out/.
cd "$(dirname "$0")" || exit 1
W=${W:-/tmp/weights}; mkdir -p $W out
g++ -O2 -o dump dump.cpp || exit 1
./dump 16 $W/w16 1; ./dump 20 $W/w20 0; ./dump 24 $W/w24 0 0 1
python3 mirror.py $W/w16 > out/mirror.txt
python3 weights.py $W/w20 > out/allcuts_20.txt
python3 essential.py $W/w20 > out/essential_20.txt
python3 essential.py $W/w24 19 > out/essential_24.txt
python3 perletter.py $W/w20 "core2 dim^2" -3 4 > out/perletter_core2dim2_20.txt
python3 perletter.py $W/w20 "dim" -3 4 > out/perletter_dim_20.txt
python3 argmin.py $W/w20 "dim" > out/argmin_dim_20.txt
python3 argmin.py $W/w20 "core2 dim^2" > out/argmin_core2dim2_20.txt
python3 paths.py $W/w16 > out/paths_16.txt
python3 ones.py $W/w20 > out/ones_20.txt
python3 ones.py - 44 > out/ones_P_44.txt
python3 ratio.py $W/w16 "dim" > out/ratio_16.txt; python3 ratio.py $W/w16 "core2 dim^2" >> out/ratio_16.txt
python3 transport.py $W/w16 dim 13 0 -1 1 > out/transport.txt; python3 transport.py $W/w16 uniform 13 0 >> out/transport.txt; python3 transport.py $W/w16 "dim^2" 11 0 >> out/transport.txt
python3 pairing.py $W/w16 12 > out/pairing.txt
python3 universal.py $W/w24 > out/universal_24.txt
python3 rowinsert.py $W/w16 10 > out/rowinsert.txt
