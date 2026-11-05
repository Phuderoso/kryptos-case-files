#!/bin/bash
# Cycle 80 runner: direct L<=6 and behind 165,065 perms L<=3, K4 + 5 shuffled nulls + planted controls.
cd "$(dirname "$0")"
K4=$(python3 -c "from kryptos_text import K4;print(K4)")
NP=165065; CH=$(( (NP+7)/8 ))
runall(){ tag=$1; ct=$2; for s in 0 1 2 3 4 5 6 7; do ./linrec80 $ct perms97.bin $((s*CH)) $(((s+1)*CH)) 3 > r_${tag}_$s.txt & done; wait; }
runall k4 $K4
for n in 0 1 2 3 4; do runall null$n $(cat null_$n.txt); done
for n in 0 1 2 3 4; do ./linrec80 $(cat null_$n.txt) perms97.bin 0 1 6 > rd_null$n.txt & done; wait
python3 - <<'P'
import json,subprocess
for c in json.load(open("controls80.json")):
    lo=max(0,c["perm"]-5000); hi=c["perm"]+5000 if c["perm"] else 1; L=6 if c["perm"]==0 else 3
    out=subprocess.run(["./linrec80",c["ct"],"perms97.bin",str(lo),str(hi),str(L)],capture_output=True,text=True).stdout
    open(f"r_ctl{c['ctl']}.txt","w").write(out)
P
echo DONE > done.flag
