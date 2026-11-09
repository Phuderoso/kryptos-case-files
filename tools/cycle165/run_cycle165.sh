#!/bin/bash
# Cycle 165 (IDEAS I-074): finish / audit I-015 behind the bank with q4akb (blocked q4ak), checkpointed slices.
# Every job writes run/<name>.tmp and renames to run/<name>.txt only on success -> rerunning skips finished slices.
W=${W:-/workspace/k4c165}; B=/home/box/kryptos_support_backup/perms97.bin; T=$W/q4akb; cd "$W"; mkdir -p run
K=$(cat /tmp/kcf/data/k4.txt); NP=165065
job() { [ -s run/$1.txt ] && return; shift0=$1; shift; "$T" "$@" > run/$shift0.tmp && mv run/$shift0.tmp run/$shift0.txt; }
export -f job; export T B
case "$1" in
controls)  # bank plants inside a 80-entry window (plant not at block start); direct plant with the c6 list
  grep '^ctl[1-5]' controls.txt | while read lab ct x y z f fe pr L ix perm dir; do
    echo "ctl_$lab $ct themed.txt themed.txt $B $lab $((perm-40)) $((perm+40)) 1 16"; done | xargs -P 5 -L 1 bash -c 'job "$@"' _
  grep '^ctl6' controls.txt | while read lab ct rest; do job ctl_ctl6 $ct themed.txt c6list.txt x ctl6 0 1 1 20; done ;;
sample)    # exact reproduction of the cycle-164 1/40 sample (K4, null1, null2)
  { echo "K4 $K"; grep '^null' controls.txt | cut -d' ' -f1,2; } | while read lab ct; do for i in 0 1 2 3 4 5 6 7; do
    echo "samp_${lab}_$i $ct themed.txt themed.txt $B $lab $((i*40)) $NP 320 16"; done; done | xargs -P 8 -L 1 bash -c 'job "$@"' _ ;;
k4part)    # independent re-run of 1/8 of the K4 bank (entries = 3 mod 8), 32 slices
  for i in $(seq 0 31); do echo "k4p_$i $K themed.txt themed.txt $B K4 $((3+i*8)) $NP 256 16"; done | xargs -P 8 -L 1 bash -c 'job "$@"' _ ;;
nulls)     # themed x themed nulls: null1, null2 on 1/8 (entries = 5 mod 8); mnull01-04 on 1/32
  { grep '^null' controls.txt | cut -d' ' -f1,2 | while read lab ct; do for i in $(seq 0 15); do
      echo "tn_${lab}_$i $ct themed.txt themed.txt $B $lab $((5+i*8)) $NP 128 16"; done; done
    grep '^mnull0[1-4] ' mnulls.txt | cut -d' ' -f1,2 | while read lab ct; do for i in 0 1 2 3; do
      echo "tn_${lab}_$i $ct themed.txt themed.txt $B $lab $((7+i*32)) $NP 128 16"; done; done; } | xargs -P 8 -L 1 bash -c 'job "$@"' _ ;;
vocab)     # themed x vocabulary behind the bank, every 1000th entry, vocabulary in 22 half-chunks (memory-safe)
  { echo "K4 $K"; grep '^null' controls.txt | cut -d' ' -f1,2; } | while read lab ct; do for c in vh_*; do
    echo "tv_${lab}_$c $ct themed.txt $c $B $lab 11 $NP 1000 16"; done; done | xargs -P 8 -L 1 bash -c 'job "$@"' _ ;;
esac
