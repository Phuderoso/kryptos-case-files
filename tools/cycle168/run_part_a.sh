#!/bin/bash
# Cycle 168 part A: named running keys behind K3-law decimations (159,712, cycle 59) + spiral/diagonal routes (6,070,
# cycle 61), exact, tools/bookrk.c unchanged. Checkpointed: one output per (text, chunk); a finished output ends in
# a SUMMARY line and is skipped on rerun. usage: run_part_a.sh NAME CARVED97 [chunks-glob]
W=${W:-/workspace/k4c168/run}; cd $W
name=$1; ct=$2; glob=${3:-chunk_??}
mkdir -p out
for c in $glob; do o=out/${name}_${c}.out
  if [ -f $o ] && grep -q '^SUMMARY' $o; then continue; fi
  echo "./bookrk $ct $c texts.txt 9 > $o.tmp && mv $o.tmp $o"
done | xargs -P 8 -I{} bash -c "{}"
