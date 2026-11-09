#!/bin/bash
# Cycle 160: periodic Quagmire IV with two vocabulary alphabets behind the 165k bank (p 1-16, both
# directions, both index orders, Vig/Beau), K4 + 4 shuffled nulls; direct p 1-26 strict and one-error
# (leave-one-crib-out) for K4, 4 shuffled and 20 profile-matched nulls.  Resumable: finished slices are skipped.
W=${W:-/workspace/k4c160}; B=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; mkdir -p run
K=$(cat k4.txt); NP=165065; S=8; STEP=$(( (NP+S-1)/S ))
texts() { echo "K4 $K"; grep '^null' controls.txt; }
# direct
{ texts; cut -d' ' -f1,2 mnulls.txt | grep '^mnull'; } | while read lab ct; do
  [ -s run/direct_$lab.txt ] && continue
  { ./q4v $ct vocab.txt x $lab 0 1 1 26 1 | grep -v '^M'
    for d in $(seq 0 23); do ./q4v $ct vocab.txt x $lab 0 1 1 26 1 $d | grep -v '^M' | sed "s/^/D$d /"; done; } 2>/dev/null > run/direct_$lab.tmp && mv run/direct_$lab.tmp run/direct_$lab.txt
done
# bank
texts | while read lab ct; do for ((i=0;i<S;i++)); do lo=$((i*STEP)); hi=$((lo+STEP));
  [ -s run/bank_${lab}_$i.txt ] || echo "$ct $lab $lo $hi $i"; done; done |
 xargs -P 8 -L 1 sh -c './q4v "$0" vocab.txt '"$B"' "$1" "$2" "$3" 1 16 2>/dev/null > run/bank_"$1"_"$4".tmp && mv run/bank_"$1"_"$4".tmp run/bank_"$1"_"$4".txt'
date > run/done.txt
