#!/bin/bash
cd /workspace/k4c102; K=$(cat k4.txt); R=30
# planted controls: true config + every crib-consistent false config found in cycle 101
while read id f n inv t kp m key ct; do
  if [ "$f" = None ]; then f=identity; fi
  L=${#key}
  { echo "CONS $f n=$n inv=$inv t=$t kp=$kp m=$m L=$L key=$key"; cat /workspace/k4c101/ctl_$id.out; } | ./polyanneal $ct qg.bin $R > ctl_$id.ann &
done < controls.txt
cat /workspace/k4c101/k4_bank_*.out | ./polyanneal $K qg.bin $R > k4.ann &
for i in 1 2; do n=$(sed -n ${i}p nulls.txt); cat /workspace/k4c101/null${i}_bank_*.out | ./polyanneal $n qg.bin $R > null$i.ann & done
wait; echo DONE
