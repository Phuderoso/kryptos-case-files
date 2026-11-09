#!/bin/bash
# I-133: gm177 err 1, ix 0, L 6, base 10, full all.bin, for K4 (rerun), 40 fresh shuffles and 20 matched shuffles. Resumable.
W=${W:-/workspace/k4c178w}; cd $W; mkdir -p run/i133; K4=$(cat run/k4.txt); A=support/all.bin
job(){ f=run/i133/$1.txt; shift; [ -s $f ] && tail -1 $f | grep -q '^END' && return; OMP_NUM_THREADS=6 "$@" | grep -v '^M' > $f.tmp && mv $f.tmp $f; }
job k4 run/gm177 $K4 $A k4 0 165782 0 6 6 10 1
while read lab ct rest; do job $lab run/gm177 $ct $A $lab 0 165782 0 6 6 10 1; done < <(cat run/fresh133.txt run/matched133.txt)
date > run/i133/done.txt
