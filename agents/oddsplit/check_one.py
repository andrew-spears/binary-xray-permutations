"""Theorem A and its converse against brute force (output of ./dump n: every word with its odd splits S).
A one-stone set S = {k} is an odd split  <=>  e_i in {0,1,2} for i < k and e_i in {0,-1,-2} for i > k.
Usage: ./dump 8 > /tmp/os_8.txt; python3 check_one.py /tmp/os_8.txt"""
import sys
nw = fam = bad = 0
for line in open(sys.argv[1]):
    a, b = line.split("|"); e = tuple(map(int, a.split())); n = len(e); nw += 1
    odd = {int(t.split(":")[0]) for t in b.split()}; hit = False
    for k in range(n):
        A = all(0 <= x <= 2 for x in e[:k]) and all(-2 <= x <= 0 for x in e[k + 1:]); hit |= A
        if A != ((1 << k) in odd): bad += 1; print("MISMATCH", e, k)
    fam += hit
print(f"{nw} valid words, {fam} in the family of Theorem A; (word, k) where 'S = {{k}} is an odd split' differs from the letter condition: {bad}")
