#!/bin/bash
# run_chunks.sh TAG CT [NCHUNK] : 16 strided chunks of all.bin, checkpointed (a chunk is done iff its file ends in PERIODIC V2B)
T=$(cd "$(dirname "$0")" && pwd); TAG=$1; CT=$2; NC=${3:-16}; mkdir -p out
for i in $(seq 0 $((NC-1))); do o=out/$TAG.c$i
  if [ -f $o ] && tail -1 $o | grep -q '^PERIODIC V2B'; then continue; fi
  ./porta170 $CT all.bin alpha.bin texts.txt $NC $i > $o.tmp 2>>out/$TAG.log && mv $o.tmp $o
done
