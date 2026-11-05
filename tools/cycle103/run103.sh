#!/bin/bash
cd /workspace/k4c103; K=$(cat k4.txt); N1=$(sed -n 1p nulls.txt); N2=$(sed -n 2p nulls.txt)
./homo $K qg.bin 30 z340.bin > homo_k4.out 2> homo_k4.err &
./homo $N1 qg.bin 30 z340.bin > homo_null1.out 2> homo_null1.err &
./homo $N2 qg.bin 30 z340.bin > homo_null2.out 2> homo_null2.err &
c3=$(awk '$1=="z3"{print $9}' controls.txt); ./homo $c3 qg.bin 30 z340.bin > homo_ctl_z3.out 2> homo_ctl_z3.err &
for i in 0 1 2 3; do timeout 440 ./polyhomo $K 1 3 100000 zc$i > ph_k4_$i.out 2> ph_k4_$i.err & done
wait
for i in 0 1 2 3; do timeout 440 ./polyhomo $N1 1 3 100000 zc$i > ph_null1_$i.out 2> ph_null1_$i.err & done
c1=$(awk '$1=="z1"{print $9}' controls.txt); timeout 300 ./polyhomo $c1 3 3 100000 zc0 > ph_ctl_z1.out 2> ph_ctl_z1.err &
c2=$(awk '$1=="z2"{print $9}' controls.txt); timeout 300 ./polyhomo $c2 3 3 100000 zc3 > ph_ctl_z2.out 2> ph_ctl_z2.err &
wait; echo DONE
