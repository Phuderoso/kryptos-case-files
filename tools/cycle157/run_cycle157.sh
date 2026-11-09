#!/bin/bash
# Cycle 157 runner (IDEAS I-052), resumable: jobs "text L mode lo hi" for model P of tools/cycle155/gromark1e.c;
# finished chunks (C lines in results_raw.txt) are skipped on rerun.  Usage: W=scratch REPO=repo_root bash run_cycle157.sh
W=${W:-/workspace/k4c157/run}; D=$(cd $(dirname "$0"); pwd); REPO=${REPO:-$D/../..}; mkdir -p $W; cd $W
[ -x gromark1e ] || gcc -O3 -march=native -o gromark1e $REPO/tools/cycle155/gromark1e.c
[ -s nulls.txt ] || python3 $D/mknulls157.py ${NN:-20} 15700000 $REPO/data/k4.txt > nulls.txt
cat $REPO/data/k4.txt > ct_K4.txt; while read n t rest; do echo $t > ct_$n.txt; done < nulls.txt
TEXTS="${ONLY:-$(cut -d' ' -f1 nulls.txt)}"   # ONLY="mnull01 ..." restricts a resume to some nulls
{ echo "K4 8 all 0 50000000"; echo "K4 8 all 50000000 100000000"; echo "K4 11 perm 0 100000000"
  for T in $TEXTS; do
    for s in 0 1 2 3; do echo "$T 8 all $((s*25000000)) $(((s+1)*25000000))"; done
    echo "$T 11 perm 0 100000000"; echo "$T 10 perm 0 100000000"; echo "$T 9 perm 0 100000000"; echo "$T 8 perm 0 100000000"
    for L in 7 6 5 4 3 2; do echo "$T $L all 0 100000000"; done; done; } > jobs_all.txt
touch results_raw.txt
python3 - <<'PY' > jobs_todo.txt
import re
done=set()
for l in open('results_raw.txt'):
    m=re.match(r'C (\S+) P L=(\d+) (\S+) lo=(\d+)',l)
    if m: done.add(m.groups())
for l in open('jobs_all.txt'):
    T,L,mode,lo,hi=l.split()
    if (T,L,mode,lo) not in done: print(l.strip())
PY
echo "todo $(wc -l < jobs_todo.txt) of $(wc -l < jobs_all.txt)"
xargs -P ${P:-8} -L 1 sh -c 'SHOW=1 ./gromark1e $(cat ct_$0.txt) $1 $2 $3 $4 $0 P' < jobs_todo.txt >> results_raw.txt
