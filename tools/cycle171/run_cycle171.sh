#!/bin/bash
# Cycle 171: (1) I-096 Porta one-error behind the 165,782 K3-law decimations/routes; (2) I-091 one-error named running keys
# (bookrk1e, cycle 169) behind the 165,065-perm transposition bank. Checkpointed: a stage output counts as done iff it ends
# with its terminal line (porta171: "EXPECT V2B", bookrk1e: "SUMMARY"); finished outputs are skipped on rerun.
set -e
W=${W:-/workspace/k4c171/run}; T=$(cd "$(dirname "$0")" && pwd); B=/home/box/kryptos_support_backup; mkdir -p $W; cd $W
ln -sf /workspace/k4c168/run/all.bin all.bin; [ -f texts.txt ] || cp /workspace/k4c168/run/texts.txt .
ln -sf $B/alpha.bin alpha.bin; ln -sf $B/perms97.bin bank.bin
gcc -O3 -march=native -fopenmp -o porta171 $T/porta171.c -lm; gcc -O3 -march=native -o bookrk1e $T/../cycle169/bookrk1e.c
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
done_p(){ [ -f $1 ] && tail -1 $1 | grep -q '^EXPECT V2B'; }; done_b(){ grep -qs '^SUMMARY' $1; }
mkdir -p out ctl ctl171b nulls
# A. controls
[ -f ctl/plants.txt ] || python3 $T/ctl171.py all.bin alpha.bin texts.txt 12 17101 > /dev/null
for i in $(seq 0 11); do o=ctl/ctl$i.out; done_p $o || { ./porta171 $(cat ctl/ctl$i.txt) ctl/ctl${i}_slice.bin alpha.bin texts.txt > $o.tmp 2>/dev/null && mv $o.tmp $o; }; done
[ -f ctl171b/planted.txt ] || python3 $T/ctl171b.py bank.bin texts.txt 17102 > /dev/null
for c in ctl171b/*.txt; do b=$(basename $c .txt); [ $b = planted ] && continue; o=ctl171b/$b.out
  done_b $o || echo "./bookrk1e $(cat $c) ctl171b/${b}_slice.bin texts.txt 20 > $o.tmp && mv $o.tmp $o"; done | xargs -P 8 -I{} bash -c "{}"
echo "controls done $(date +%T)"
# C. K4 Porta one-error, full family: periodic all survivors, running keys for d-free survivors (16 chunks)
for i in $(seq 0 15); do o=out/k4p.c$i; done_p $o || { RKFREE=1 ./porta171 $K4 all.bin alpha.bin texts.txt 16 $i > $o.tmp 2>/dev/null && mv $o.tmp $o; }; done
echo "K4 porta full done $(date +%T)"
# D. K4 Porta one-error, running keys for every survivor (d forced too) on the 1/8 slice p%8==0 (2 strided chunks)
for i in 0 8; do o=out/k4pall.s16o$i; done_p $o || { ./porta171 $K4 all.bin alpha.bin texts.txt 16 $i > $o.tmp 2>/dev/null && mv $o.tmp $o; }; done
echo "K4 porta RK-all slice done $(date +%T)"
# E. 40 shuffled-K4 nulls, Porta periodic one-error (NORK) on the same 1/8 slice (p%8==0)
[ -f nulls171.txt ] || python3 -c "
import random
K4='$K4'
for s in range(40):
  l=list(K4); random.Random(171000+s).shuffle(l); print(''.join(l))" > nulls171.txt
i=0; while read n; do o=nulls/pnull$i.out; i=$((i+1)); done_p $o || { NORK=1 ./porta171 $n all.bin alpha.bin texts.txt 8 0 > $o.tmp 2>/dev/null && mv $o.tmp $o; }; done < nulls171.txt
o=out/k4p_nork_s8o0; done_p $o || { NORK=1 ./porta171 $K4 all.bin alpha.bin texts.txt 8 0 > $o.tmp 2>/dev/null && mv $o.tmp $o; }
echo "porta nulls done $(date +%T)"
# F. I-091: bookrk1e K4 behind the bank (16 chunks of ~10,317 perms) + 40 nulls on a 500-perm slice (first 250 + last 250)
NB=165065; CH=$(( (NB+15)/16 ))
for i in $(seq 0 15); do f=bank_chunk_$(printf %02d $i); [ -f $f ] || dd if=bank.bin of=$f bs=194 skip=$((i*CH)) count=$CH status=none; done
[ -f bankslice.bin ] || { head -c $((194*250)) bank.bin > bankslice.bin; tail -c $((194*250)) bank.bin >> bankslice.bin; }
{ for c in bank_chunk_??; do o=out/k4b_$c.out; done_b $o || echo "./bookrk1e $K4 $c texts.txt 11 > $o.tmp && mv $o.tmp $o"; done
  o=out/k4b_slice.out; done_b $o || echo "./bookrk1e $K4 bankslice.bin texts.txt 9 > $o.tmp && mv $o.tmp $o"
  i=0; while read t; do o=nulls/bnull$i.out; i=$((i+1)); done_b $o && continue; echo "./bookrk1e $t bankslice.bin texts.txt 9 > $o.tmp && mv $o.tmp $o"; done < nulls171.txt
} | xargs -P 8 -I{} bash -c "{}"
echo "bank done $(date +%T)"
