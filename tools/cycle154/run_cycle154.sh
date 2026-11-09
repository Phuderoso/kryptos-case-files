#!/bin/bash
# Cycle 154 (IDEAS I-012): Hill first, then a period-k Vigenere on the Hill output (key on the ciphertext side).
# Direct (VERB counts + DROP=1 one-block-drop tolerance): n=2 k=1..24, n=3 k=1..15, n=4 k=1..8.
# Bank strict, full 165,065 entries x both directions x model Q/carved x A-Z/KRYPTOS x every alignment:
#   n=2 k=1..14, n=3 k=1..9, n=4 k=1..3;  sampled: n=3 k=10 (stride 20), n=4 k=5,6 (stride 10).
# Texts: K4 + two shuffled-K4 nulls (plant.py). 8 workers, bank jobs in 4 slices, resumable (files with a C line skipped).
# Launch: setsid timeout 900 bash run_cycle154.sh   (own process group; kill with kill -- -PGID)
W=${W:-/workspace/k154}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K4=$(cat /tmp/kcf/data/k4.txt); mkdir -p out
s=$(date +%s)
{
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $12}' controls.txt)
  for j in "4 5 10" "4 6 10" "3 10 20"; do set -- $j; for sl in 0 1 2 3; do echo "$l $T $1 $2 B $((sl*41267)) $(((sl+1)*41267)) $3 $sl"; done; done
  for k in 9 8 7 6 5 4 3 2 1; do for sl in 0 1 2 3; do echo "$l $T 3 $k B $((sl*41267)) $(((sl+1)*41267)) 1 $sl"; done; done
  for k in 14 13 12 11 10 9 8 7 6 5 4 3 2 1; do for sl in 0 1 2 3; do echo "$l $T 2 $k B $((sl*41267)) $(((sl+1)*41267)) 1 $sl"; done; done
  for k in 3 2 1; do for sl in 0 1 2 3; do echo "$l $T 4 $k B $((sl*41267)) $(((sl+1)*41267)) 1 $sl"; done; done
done
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $12}' controls.txt)
  for k in $(seq 1 24); do echo "$l $T 2 $k D 0 1 1 0"; done; for k in $(seq 1 15); do echo "$l $T 3 $k D 0 1 1 0"; done
  for k in $(seq 1 8); do echo "$l $T 4 $k D 0 1 1 0"; done; done
} | xargs -P 8 -L 1 sh -c 'f=out/$0_n$2_k$3_$4_s$8.txt; grep -q "^C " $f 2>/dev/null && exit 0;
   if [ $4 = D ]; then VERB=1 DROP=1 timeout 120 ./hillcs $1 - D$0 0 1 1 $2 $3 > $f.tmp; else ./hillcs $1 '$P' $0 $5 $6 $7 $2 $3 > $f.tmp; fi && mv $f.tmp $f'
echo "T $(( $(date +%s)-s ))" > time.txt
