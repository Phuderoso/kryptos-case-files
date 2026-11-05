#!/bin/bash
# Cycle 81: order-4 linear-recurrence keys behind 165,065 perms (K4 L1-4, 5 nulls L4), controls, K4 L5 on perms 0-19,999 (checkpoint).
cd "$(dirname "$0")"
K4=$(python3 -c "from kryptos_text import K4;print(K4)")
NP=165065; CH=$(( (NP+7)/8 ))
runall(){ tag=$1; ct=$2; a=$3; b=$4; for s in 0 1 2 3 4 5 6 7; do ./linrec81 $ct perms97.bin $((s*CH)) $(((s+1)*CH)) $a $b > r_${tag}_$s.txt & done; wait; }
runall k4 $K4 1 4
for n in 0 1 2 3 4; do runall null$n $(cat null_$n.txt) 4 4; done
python3 - <<'P'
import json,subprocess
for c in json.load(open("controls81.json")):
    lo=max(0,c["perm"]-3000); hi=c["perm"]+3000 if c["perm"] else 1; a,b=(4,4) if c["perm"] else (1,6)
    out=subprocess.run(["./linrec81",c["ct"],"perms97.bin",str(lo),str(hi),str(a),str(b)],capture_output=True,text=True).stdout
    open(f"r_ctl{c['ctl']}.txt","w").write(out)
P
# L5 checkpoint: perms 0..19999 in 8 chunks of 2500
for s in 0 1 2 3 4 5 6 7; do ./linrec81 $K4 perms97.bin $((s*2500)) $(((s+1)*2500)) 5 5 > r_k4L5_$s.txt & done; wait
echo 20000 > L5_checkpoint.txt
echo DONE > done.flag
