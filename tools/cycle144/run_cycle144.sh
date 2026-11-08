#!/bin/bash
# Cycle 144: Hill n x n + additive key of period k (independent of n), exact joint solve; direct + full 165k bank
# (both directions, model Q and carved), A-Z/KRYPTOS, every alignment. n=2 k=1..14, n=3 k=1..10, n=4 k=1..4.
# Texts: K4 and two shuffled-K4 nulls from plant.py. Needs hillvk (gcc -O2 -march=native hillvk.c).
W=${W:-/workspace/k144}; P=/home/box/kryptos_support_backup/perms97.bin; cd "$W"; K4=$(cat /tmp/kcf/data/k4.txt)
while read nm n k src q t; do [[ $nm == ctl* ]] || continue
  if [ $src = - ]; then ./hillvk $t - $nm 0 1 1 $n $k; else ./hillvk $t $P $nm $q $((q+1)) 1 $n $k; fi; done < controls.txt > controls_check.txt
mkdir -p out; s=$(date +%s)
for l in K4 null1 null2; do T=$([ $l = K4 ] && echo $K4 || awk -v l=$l '$1==l{print $6}' controls.txt)
  for nk in $(for k in $(seq 1 14); do echo 2:$k; done; for k in $(seq 1 10); do echo 3:$k; done; for k in 1 2 3 4; do echo 4:$k; done); do
    echo "$l $T ${nk%:*} ${nk#*:}"; done; done | xargs -P 8 -L 1 sh -c './hillvk $1 - D$0 0 1 1 $2 $3 > out/direct_$0_$2_$3.txt; ./hillvk $1 '$P' $0 0 165065 1 $2 $3 > out/bank_$0_$2_$3.txt'
echo "T $(( $(date +%s)-s ))" > time.txt
