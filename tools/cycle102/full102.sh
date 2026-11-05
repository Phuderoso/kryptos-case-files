#!/bin/bash
cd /workspace/k4c102; K=$(cat k4.txt)
for f in perms97 dec_perm; do timeout 450 ./polyhomo $K 3 3 1000000 $f.bin > full_k4_$f.out 2> full_k4_$f.err & done
for i in 1 2; do n=$(sed -n ${i}p nulls.txt); for f in perms97 dec_perm; do timeout 450 ./polyhomo $n 3 3 1000000 $f.bin > full_null${i}_$f.out 2> full_null${i}_$f.err & done; done
wait
for s in k4 null1 null2; do if [ $s = k4 ]; then ct=$K; else ct=$(sed -n ${s#null}p nulls.txt); fi; cat full_${s}_*.out | ./polyanneal $ct qg.bin 30 > full_$s.ann & done
wait; echo DONE
