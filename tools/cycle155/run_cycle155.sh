#!/bin/bash
# Cycle 155 runner (resumable): jobs "text model L mode lo hi"; finished jobs (C lines in results_raw.txt) are skipped.
W=${W:-/workspace/k4c155}; D=$(cd $(dirname "$0"); pwd); cd $W
[ -x gromark1e ] || gcc -O3 -march=native -o gromark1e $D/gromark1e.c
ct(){ if [ $1 = K4 ]; then cat ${REPO:-$D/../..}/data/k4.txt; else grep "^$1 " controls.txt | cut -d' ' -f2; fi; }
for T in K4 null1 null2 null3 null4 null5 null6; do ct $T > ct_$T.txt; done
{ for T in K4 null1 null2; do
    for s in $(seq 0 15); do echo "$T P 12 perm $((s*30000000)) $(((s+1)*30000000))"; done
    for s in 0 1 2 3 4 5 6 7 8 9; do echo "$T P 9 all $((s*100000000)) $(((s+1)*100000000))"; done; done
  for T in K4 null1 null2 null3 null4 null5 null6; do
    for s in 0 1 2 3; do echo "$T P 8 all $((s*25000000)) $(((s+1)*25000000))"; done
    echo "$T P 11 perm 0 100000000"; echo "$T P 10 perm 0 100000000"; echo "$T P 9 perm 0 100000000"; echo "$T P 8 perm 0 100000000"
    for L in 7 6 5 4 3 2; do echo "$T P $L all 0 100000000"; done; done; } > jobs_all.txt
touch results_raw.txt
python3 - <<'PY' > jobs_todo.txt
import re
done=set()
for l in open('results_raw.txt'):
    m=re.match(r'C (\S+) (\S) L=(\d+) (\S+) lo=(\d+)',l)
    if m: done.add(m.groups())
for l in open('jobs_all.txt'):
    T,M,L,mode,lo,hi=l.split()
    if (T,M,L,mode,lo) not in done: print(l.strip())
PY
echo "todo $(wc -l < jobs_todo.txt) of $(wc -l < jobs_all.txt)"
xargs -P ${P:-8} -L 1 sh -c 'SHOW=1 ./gromark1e $(cat ct_$0.txt) $2 $3 $4 $5 $0 $1' < jobs_todo.txt >> results_raw.txt
