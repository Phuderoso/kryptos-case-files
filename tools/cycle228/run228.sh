#!/bin/bash
# Cycle 228 reproduction (I-312 chunk 3): col1e4 (tools/cycle220/col1e4.c, verbatim) NAL=4 over the w 11 orders with pi[0] in {4,5}
# (2 x 10! = 7,257,600 orders), split into sub-slices by pi[1] (resumable: a sub-slice is complete iff its .raw ends with a C line),
# for K4 + eight nulls; 20 plants on their true (pi[0], pi[1]) sub-slice; gate T = K4 w11 pi[0]=0 pi[1]=1 rerun (compare to cycle 220).
# Run under setsid + timeout by the caller. Inputs: $W/plants228.tsv, $W/nulls228.tsv.
set -e
T=$(cd "$(dirname "$0")" && pwd); W=${WORK:-/workspace/k4c228/w}; mkdir -p $W/out
gcc -O3 -march=native -o $W/col1e4 $T/../cycle220/col1e4.c
K4=$(cat $T/../../data/k4.txt)
echo -e "K4\t$K4" > $W/texts.tsv
tail -n +2 $W/nulls228.tsv | awk -F'\t' '{print "null"$1"\t"$2}' >> $W/texts.tsv
: > $W/jobs.txt
echo "gateT K4 $K4 11 0 1 4" >> $W/jobs.txt
tail -n +2 $W/plants228.tsv | awk -F'\t' '{split($10,a,","); print "plant"$1" plant"$1" "$14" "$2" "a[1]" "a[2]" 4"}' >> $W/jobs.txt
while IFS=$'\t' read lab ct; do for f in 4 5; do for s in 0 1 2 3 4 5 6 7 8 9 10; do [ $s = $f ] || echo "$lab $lab $ct 11 $f $s 4" >> $W/jobs.txt; done; done; done < $W/texts.tsv
# job fields: outdir label ct w first second nal
cat $W/jobs.txt | xargs -P 8 -L 1 bash -c 'mkdir -p '$W'/out/$0; o='$W'/out/$0/w$3_f$4_s$5.raw; if [ -s $o ] && tail -1 $o | grep -q "^C "; then exit 0; fi; '$W'/col1e4 $2 $3 $4 18 18 $1 $6 $5 > $o.tmp && mv $o.tmp $o'
echo DONE
