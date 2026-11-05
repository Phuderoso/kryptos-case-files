#!/bin/bash
cd /workspace/k4c101; K=$(cat k4.txt)
for c in d1 d2 d3; do ct=$(awk -v c=$c '$1==c{print $9}' controls.txt); ./polyhomo $ct 1 7 50 > ctl_$c.out 2> ctl_$c.err & done
for c in b1 b2; do ct=$(awk -v c=$c '$1==c{print $9}' controls.txt); f=$(awk -v c=$c '$1==c{print $2}' controls.txt); ./polyhomo $ct 1 3 50 $f > ctl_$c.out 2> ctl_$c.err & done
wait
for f in perms97 dec_perm affine route_perm; do ./polyhomo $K 1 3 200 $f.bin > k4_bank_$f.out 2> k4_bank_$f.err & done
i=0; while read n; do i=$((i+1)); ./polyhomo $n 1 7 20 > null${i}_direct.out 2> null${i}_direct.err & done < nulls.txt
wait
for i in 1 2; do n=$(sed -n ${i}p nulls.txt); for f in perms97 dec_perm affine route_perm; do ./polyhomo $n 1 3 200 $f.bin > null${i}_bank_$f.out 2> null${i}_bank_$f.err & done; done
wait; echo DONE
