#!/bin/sh
# resumable; each output gets a DONE line
NP=165066
one(){ f=$1; shift; [ -f $f ] && grep -q '^tests=' $f && return; ./rowkeyT78 "$@" > $f; }
one out_k4.txt $(cat ../k4c77/k4.txt) ../k4c77/perms97.bin 0 $NP 6 &
for n in 0 1 2 3 4 5 6; do one out_null$n.txt $(cat null_$n.txt) ../k4c77/perms97.bin 0 $NP 6 & done; wait
for n in 7 8 9 10 11; do one out_null$n.txt $(cat null_$n.txt) ../k4c77/perms97.bin 0 $NP 6 & done
python3 - <<'PY' &
import json,subprocess
for c in json.load(open("controls78.json")):
    lo=max(0,c["perm"]-2500); r=subprocess.run(["./rowkeyT78",c["ct"],"../k4c77/perms97.bin",str(lo),str(lo+5000),"6"],capture_output=True,text=True).stdout
    open(f"out_ctl{c['ctl']}.txt","w").write(r)
PY
wait
