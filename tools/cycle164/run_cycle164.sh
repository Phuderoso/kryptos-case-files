#!/bin/bash
# Cycle 164: Quagmire I/II/IV autokey, two different keyed alphabets (q4ak.c).
# direct: themed(98) x vocabulary(9,395) both ways, L 1-26, K4 + 2 shuffled + 20 profile-matched nulls.
# bank: themed x themed (9,506 ordered pairs, X != Y), 165,065 perms both directions, both index orders, L 1-16;
#       K4 in full, nulls on every NSTEP-th entry.  Resumable.
W=${W:-/workspace/k4c164}; B=/home/box/kryptos_support_backup/perms97.bin; T=$W/repo/tools/cycle164/q4ak; cd "$W"; mkdir -p run
K=$(cat /tmp/kcf/data/k4.txt); NP=165065; S=8; STEP=$(( (NP+S-1)/S )); NSTEP=${NSTEP:-20}
texts() { echo "K4 $K"; grep '^null' controls.txt | cut -d' ' -f1,2; }
if [ "$1" = direct ]; then
 { texts; cut -d' ' -f1,2 mnulls.txt | grep '^mnull'; } | while read lab ct; do for c in vchunk_*; do
   [ -s run/direct_${lab}_$c.txt ] || echo "$ct $lab $c"; done; done |
 xargs -P 8 -L 1 sh -c '{ '"$T"' "$0" themed.txt "$2" x "$1" 0 1 1 26; '"$T"' "$0" "$2" themed.txt x "$1"_rev 0 1 1 26; } > run/direct_"$1"_"$2".txt'
fi
if [ "$1" = bank ]; then
 for ((i=0;i<S;i++)); do lo=$((i*STEP)); hi=$((lo+STEP)); [ -s run/bank_K4_$i.txt ] || echo "$K K4 $lo $hi 1 $i"; done |
  xargs -P 8 -L 1 sh -c ''"$T"' "$0" themed.txt themed.txt '"$B"' "$1" "$2" "$3" "$4" 16 > run/bank_"$1"_"$5".tmp && mv run/bank_"$1"_"$5".tmp run/bank_"$1"_"$5".txt'
 date > run/done_K4.txt
 texts | grep -v '^K4' | while read lab ct; do for ((i=0;i<S;i++)); do lo=$((i*NSTEP)); [ -s run/bank_${lab}_$i.txt ] || echo "$ct $lab $lo $NP $((S*NSTEP)) $i"; done; done |
  xargs -P 8 -L 1 sh -c ''"$T"' "$0" themed.txt themed.txt '"$B"' "$1" "$2" "$3" "$4" 16 > run/bank_"$1"_"$5".tmp && mv run/bank_"$1"_"$5".tmp run/bank_"$1"_"$5".txt'
 date > run/done.txt
fi
# What cycle 164 actually reported for the bank (the full K4 pass above was stopped unfinished at the budget):
# every 40th bank entry (offsets 0,40,...,280 per worker, stride 320), both directions, K4 + null1 + null2.
if [ "$1" = sample ]; then
 { echo "K4 $K"; grep '^null' controls.txt | cut -d' ' -f1,2; } | while read lab ct; do for i in 0 1 2 3 4 5 6 7; do echo "$ct $lab $((i*40)) $i"; done; done |
  xargs -P 8 -L 1 sh -c ''"$T"' "$0" themed.txt themed.txt '"$B"' "$1" "$2" 165065 320 16 > run/samp_"$1"_"$3".txt'
fi
