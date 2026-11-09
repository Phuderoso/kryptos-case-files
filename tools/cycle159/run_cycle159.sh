#!/bin/bash
# Cycle 159 runner (IDEAS I-057), resumable: model P digit primers L 8 (all 10^8, 4 chunks of 25M) of the unchanged
# tools/cycle155/gromark1e.c on profile- AND cycle-rank-matched nulls (mknulls159.py). Finished chunks (C lines) are skipped.
# Jobs run quarter-major (all nulls' primers 0-25M first, then 25-50M, ...) so a budget stop leaves a common primer range.
# Usage: W=scratch REPO=repo_root [NN=48] [ONLY="rnull01 ..."] bash run_cycle159.sh
W=${W:-/workspace/k4c159/run}; D=$(cd $(dirname "$0"); pwd); REPO=${REPO:-$D/../..}; mkdir -p $W; cd $W
[ -x gromark1e ] || gcc -O3 -march=native -o gromark1e $REPO/tools/cycle155/gromark1e.c
[ -s nulls.txt ] || python3 $D/mknulls159.py ${NN:-48} 15900000 $REPO/data/k4.txt 8 > nulls.txt
cat $REPO/data/k4.txt > ct_K4.txt; while read n t rest; do [ "${n:0:1}" = "#" ] || echo $t > ct_$n.txt; done < nulls.txt
TEXTS="${ONLY:-$(cut -d' ' -f1 nulls.txt)}"
{ for T in $TEXTS; do for s in 0 1 2 3; do echo "$T 8 all $((s*25000000)) $(((s+1)*25000000))"; done; done; } > jobs_all.txt
touch results_raw.txt
python3 - <<'PY' > jobs_todo.txt
import re
done=set(); todo=[]
for l in open('results_raw.txt'):
    m=re.match(r'C (\S+) P L=(\d+) (\S+) lo=(\d+)',l)
    if m: done.add(m.groups())
for l in open('jobs_all.txt'):
    T,L,mode,lo,hi=l.split()
    if (T,L,mode,lo) not in done: todo.append((int(lo),T,l.strip()))
for lo,T,l in sorted(todo): print(l)      # quarter-major: at any stop, every null has the same primer ranges done
PY
echo "todo $(wc -l < jobs_todo.txt) of $(wc -l < jobs_all.txt)"
xargs -P ${P:-8} -L 1 sh -c 'SHOW=1 ./gromark1e $(cat ct_$0.txt) $1 $2 $3 $4 $0 P' < jobs_todo.txt >> results_raw.txt
