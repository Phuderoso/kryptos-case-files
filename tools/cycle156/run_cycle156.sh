#!/bin/bash
# Cycle 156 (IDEAS I-050): key on both sides of the Hill step (Vigenere k1 -> Hill n -> Vigenere k2), exact (hill2s.c).
# Bank strict (165,065 entries x both directions x model Q/carved x A-Z/KRYPTOS x every alignment): n=2, the 18 (k1,k2) pairs with
#   k1,k2 >= 2, k1+k2 <= 12 and lcm(k1,2,k2) > 14 (outside case 132's period range).
# Direct (VERB counts + DROP=1 block-drop one-error mode): n=2 k1,k2 2..12; n=3 k1 2..8, k2 2..5; n=4 k1,k2 2..3.
# Texts: K4 + two shuffled-K4 nulls (plant.py, seeds 15601-15602). 8 workers, bank jobs in 4 slices, resumable (files with a C line skipped).
# Launch: setsid timeout 480 bash run_cycle156.sh   (own process group; kill with kill -- -PGID)
W=${W:-/workspace/k4c156}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K4=$(cat /tmp/kcf/data/k4.txt); mkdir -p out
s=$(date +%s)
{
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $13}' data/controls.txt)
  for kk in "2 9" "3 5" "3 7" "3 8" "3 9" "4 5" "4 7" "5 3" "5 4" "5 6" "5 7" "6 5" "7 3" "7 4" "7 5" "8 3" "9 2" "9 3"; do set -- $kk
    for sl in 0 1 2 3; do echo "$l $T 2 $1 $2 B $((sl*41267)) $(((sl+1)*41267)) $sl"; done; done
done
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $13}' data/controls.txt)
  for a in $(seq 2 12); do for b in $(seq 2 12); do echo "$l $T 2 $a $b D 0 1 0"; done; done
  for a in $(seq 2 8); do for b in 2 3 4 5; do echo "$l $T 3 $a $b D 0 1 0"; done; done
  for a in 2 3; do for b in 2 3; do echo "$l $T 4 $a $b D 0 1 0"; done; done
done
} | xargs -P 8 -L 1 sh -c 'f=out/$0_n$2_a$3_b$4_$5_s$8.txt; grep -q "^C " $f 2>/dev/null && exit 0;
   if [ $5 = D ]; then VERB=1 DROP=1 timeout 120 tools/hill2s $1 - D$0 0 1 1 $2 $3 $4 > $f.tmp; else tools/hill2s $1 '$P' $0 $6 $7 1 $2 $3 $4 > $f.tmp; fi && mv $f.tmp $f'
echo "T $(( $(date +%s)-s ))" > time.txt
