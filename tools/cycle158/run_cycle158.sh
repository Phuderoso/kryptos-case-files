#!/bin/bash
# Cycle 158 (IDEAS I-056): key on both sides of Hill, both keys vocabulary words (hillw.c). Resumable: output files with a C line are skipped.
# Direct strict: all 10,056 x 10,056 vocabulary words, n 2-4, texts K4, null1, null2 (shuffles), mnull01, mnull02 (cycle-157 profile-matched).
# Direct one error (DROP=1): themed-97 f x all e, and all f x themed-97 e, n 2-3, same texts.
# Bank strict (165,065 x both directions x model Q/carved x A-Z/KRYPTOS x every alignment): core-32 x core-32 words, n 2-4:
#   K4 full; null1 and mnull01 every 4th entry. Power: EXP=1 sample (every 1000th entry) per n for K4.
# Launch: setsid timeout 420 bash tools/run_cycle158.sh   (own process group)
W=/workspace/k4c158; P=/home/box/kryptos_support_backup/perms97.bin; cd $W; mkdir -p out
tx(){ awk -v l=$1 '$1==l{print $NF}' texts.txt; }
s=$(date +%s)
{
for l in K4 null1 null2 mnull01 mnull02; do T=$(tx $l)
  for n in 2 3 4; do for c in 0 1 2 3; do echo "$l $T $n D chunk_0$c all.txt 0 1 1 0 c$c"; done; done
  for n in 2 3; do echo "$l $T $n D themed.txt all.txt 0 1 1 1 te"; echo "$l $T $n D all.txt themed.txt 0 1 1 1 et"; done
done
for n in 2 3 4; do for sl in 0 1 2 3 4 5 6 7; do echo "K4 $(tx K4) $n B core.txt core.txt $((sl*20634)) $(((sl+1)*20634)) 1 0 s$sl"; done; done
for l in null1 mnull01; do for n in 2 3 4; do for sl in 0 1; do echo "$l $(tx $l) $n B core.txt core.txt $((sl*82533)) $(((sl+1)*82533)) 4 0 s$sl"; done; done; done
for n in 2 3 4; do echo "K4 $(tx K4) $n E core.txt core.txt 0 165065 1000 0 exp"; done
} | xargs -P 8 -L 1 sh -c 'f=out/$0_n$2_$3_${10}.txt; grep -q "^C " $f 2>/dev/null && exit 0;
  if [ $3 = B ]; then EXP=0 tools/hillw $1 '$P' $0 $6 $7 $8 $2 $4 $5 > $f.tmp; elif [ $3 = E ]; then EXP=1 tools/hillw $1 '$P' $0 $6 $7 $8 $2 $4 $5 > $f.tmp;
  else DROP=$9 EXP=1 tools/hillw $1 - $0 0 1 1 $2 $4 $5 > $f.tmp; fi && mv $f.tmp $f'
echo "T $(( $(date +%s)-s ))" >> out/time.txt
