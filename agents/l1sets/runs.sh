#!/bin/sh
# Recheck of REPORT.md.  About 1 minute.
python3 check.py 18 12 > out_check_18.txt
python3 local.py 8 > out_local_8.txt
(python3 solve.py all 13; python3 solve.py random 300 400 7) > out_solve.txt
python3 fam.py 10 > out_fam_10.txt
python3 auto.py 16 > out_auto_16.txt
python3 desc.py 16 > out_desc_16.txt
python3 l2.py 9 > out_l2_9.txt
