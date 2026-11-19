#!/bin/bash
# Cycle 220 reproduction (I-312 chunk 1): col1e4 NAL=4 over the w 11 orders with pi[0] in {0,1} (2 x 10! = 7,257,600 orders),
# split into sub-slices by pi[1] (resumable: a sub-slice is complete iff its .raw ends with a C line), for K4 + eight nulls;
# 20 plants on their true (pi[0], pi[1]) sub-slice; gate S (sub-slice sums == full slice, w10 pi[0]=3, NAL=2, K4).
# Run under setsid + timeout by the caller. Inputs: $W/plants220.tsv, $W/nulls220.tsv, $W/k123_eng.txt (cycle 219 copy).
set -e
T=$(cd "$(dirname "$0")" && pwd); W=${WORK:-/workspace/k4c220/w}; mkdir -p $W/out
gcc -O3 -march=native -o $W/col1e4 $T/col1e4.c
K4=$(cat $T/../../data/k4.txt)
echo -e "K4\t$K4" > $W/texts.tsv
tail -n +2 $W/nulls220.tsv | awk -F'\t' '{print "null"$1"\t"$2}' >> $W/texts.tsv
: > $W/jobs.txt
for s in 0 1 2 4 5 6 7 8 9; do echo "gateS $K4 10 3 $s 2" >> $W/jobs.txt; done
tail -n +2 $W/plants220.tsv | awk -F'\t' '{split($10,a,","); print "plant"$1" "$14" "$2" "a[1]" "a[2]" 4"}' >> $W/jobs.txt
while IFS=$'\t' read lab ct; do for f in 0 1; do for s in 0 1 2 3 4 5 6 7 8 9 10; do [ $s = $f ] || echo "$lab $ct 11 $f $s 4" >> $W/jobs.txt; done; done; done < $W/texts.tsv
cat $W/jobs.txt | xargs -P 8 -L 1 bash -c 'mkdir -p '$W'/out/$0; o='$W'/out/$0/w$2_f$3_s$4.raw; if [ -s $o ] && tail -1 $o | grep -q "^C "; then exit 0; fi; P=18; [ $0 = gateS ] && P=22; '$W'/col1e4 $1 $2 $3 $P 18 $0 $5 $4 > $o.tmp && mv $o.tmp $o'
echo DONE
