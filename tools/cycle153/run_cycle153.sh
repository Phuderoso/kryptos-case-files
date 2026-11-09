#!/bin/bash
# Cycle 153: one-error audit of Hill + additive key (cycles 143-144) and Hill 5x5 (cycle 141) with hillk1e.c.
# Hill+key: n=2 k=1..14, n=3 k=1..10, n=4 k=1..4; direct + full 165,065-entry bank (both directions, model Q + carved),
# A-Z/KRYPTOS, every alignment. Hill 5 (k=0): direct exhaustive (COMBOCAP 2,000,000); bank stride 20 COUNT ONLY
# (COMBOCAP=0: consistency counters, no decoding -> LOW-POWER statement, not an exclusion).
# Texts: K4 + two shuffled-K4 nulls (plant.py). Resumable: an output with its "C" line is skipped.
# Launch: setsid timeout 900 bash run_cycle153.sh  (own process group; kill with kill -- -PGID)
W=${W:-/workspace/k153}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K4=$(cat /tmp/kcf/data/k4.txt); mkdir -p out
s=$(date +%s)
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $12}' controls.txt)
  for nk in $(for k in 1 2 3 4; do echo 4:$k; done; for k in $(seq 1 10); do echo 3:$k; done; for k in $(seq 1 14); do echo 2:$k; done); do
    n=${nk%:*}; k=${nk#*:}; echo "$l $T $n $k D 0 1 1 4096"; echo "$l $T $n $k B 0 165065 1 4096"; done
  echo "$l $T 5 0 D 0 1 1 2000000"; echo "$l $T 5 0 B 0 165065 20 0"; done |
 xargs -P 8 -L 1 sh -c 'f=out/$0_n$2_k$3_$4.txt; grep -q "^C " $f 2>/dev/null && exit 0;
   if [ $4 = D ]; then COMBOCAP=$8 ./hillk1e $1 - D$0 0 1 1 $2 $3 > $f.tmp; else COMBOCAP=$8 ./hillk1e $1 '$P' $0 $5 $6 $7 $2 $3 > $f.tmp; fi && mv $f.tmp $f'
echo "T $(( $(date +%s)-s ))" > time.txt
