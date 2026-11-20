#!/bin/bash
# Cycle 223 (I-318 audit): col21 at p 20,21 over all w 9 + 10 orders for K4, the 8 cycle-219 nulls, 160 new nulls, and 20 plants
# on their true pi[0] slice. Resumable: a job whose output already ends with its C line is skipped. Call under setsid + timeout 480.
set -e
T=$(cd "$(dirname "$0")" && pwd); R=$T/../..; W=${WORK:-/workspace/k4c223/w}; mkdir -p $W/out
gcc -O2 -o $W/col21 $T/col21.c
echo -e "K4\t$(cat $R/data/k4.txt)" > $W/texts.tsv
tail -n +2 $R/data/cycle219/nulls219.tsv | awk -F'\t' '{print "null"$1"\t"$2}' >> $W/texts.tsv
tail -n +2 $R/data/cycle223/nulls223.tsv | awk -F'\t' '{print "null"$1"\t"$2}' >> $W/texts.tsv
: > $W/jobs.txt
while IFS=$'\t' read lab ct; do echo "$lab $ct 9 -1" >> $W/jobs.txt; for f in 0 1 2 3 4 5 6 7 8 9; do echo "$lab $ct 10 $f" >> $W/jobs.txt; done; done < $W/texts.tsv
tail -n +2 $R/data/cycle223/plants223.tsv | awk -F'\t' '{split($10,a,","); print "plant"$1" "$14" "$2" "a[1]}' >> $W/jobs.txt
cat $W/jobs.txt | xargs -P 8 -L 1 bash -c 'o='$W'/out/$0/w$2_f$3.raw; mkdir -p '$W'/out/$0; if [ -s $o ] && tail -1 $o | grep -q "^C "; then exit 0; fi; '$W'/col21 $1 $2 $3 20,21 $0 > $o.tmp && mv $o.tmp $o'
echo DONE
