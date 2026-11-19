#!/bin/bash
# Cycle 219 reproduction: col1e over all w 9 + 10 orders for K4, cycle 124's null1 (gate R) and eight nulls (seeds 209234-209241),
# plus the 20 plants on their true pi[0] slice. Run under setsid + timeout by the caller. ~4 min on 8 cores.
set -e
T=$(cd "$(dirname "$0")" && pwd); W=${WORK:-/workspace/k4c219/w}; mkdir -p $W/out
gcc -O2 -o $W/col1e $T/col1e.c
K4=$(cat $T/../../data/k4.txt)
python3 $T/../cycle124/plant.py | grep '^null1 ' | awk '{print "null1_124\t"$2}' > $W/texts.tsv
echo -e "K4\t$K4" >> $W/texts.tsv
tail -n +2 $W/nulls219.tsv | awk -F'\t' '{print "null"$1"\t"$2}' >> $W/texts.tsv
: > $W/jobs.txt
while IFS=$'\t' read lab ct; do echo "$lab $ct 9 -1" >> $W/jobs.txt; for f in 0 1 2 3 4 5 6 7 8 9; do echo "$lab $ct 10 $f" >> $W/jobs.txt; done; done < $W/texts.tsv
tail -n +2 $W/plants219.tsv | awk -F'\t' '{split($10,a,","); print "plant"$1" "$14" "$2" "a[1]}' >> $W/jobs.txt
cat $W/jobs.txt | xargs -P 8 -L 1 bash -c 'mkdir -p '$W'/out/$0; '$W'/col1e $1 $2 $3 22 18 $0 > '$W'/out/$0/w$2_f$3.raw'
echo DONE
