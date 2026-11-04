#!/bin/bash
# Cycle 28: run the Quagmire IV checker on K4, 3 planted controls and 3 shuffled nulls (PMAX 16).
cd "$(dirname "$0")"; mkdir -p out
while read n c; do ./q4_perm q4_alpha.bin perms97.bin "$c" 16 > out/q4_$n.txt; echo "$n $(tail -1 out/q4_$n.txt)"; done < q4_cases.txt
