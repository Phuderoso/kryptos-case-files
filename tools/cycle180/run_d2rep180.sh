#!/bin/bash
# Cycle 180 add-on (PREREG180b): D2' on 40 fresh shuffles, seeds 18041-18080. Then prints the decision.
W=${W:-/workspace/k4c180/w}; cd $W; mkdir -p run/rep; K4=$(cat run/k4.txt)
python3 -c "
import random
K=open('run/k4.txt').read().strip()
for s in range(18041,18081):
    l=list(K); random.Random(s).shuffle(l); print(f'f{s}', ''.join(l))" > run/rep/fresh180.txt
while read lab ct; do f=run/rep/$lab.m1s8.txt; [ -s $f ] && tail -1 $f | grep -q '^END' && continue
  OMP_NUM_THREADS=6 run/lrk180 $ct support/all_s8.bin support/alpha172.txt $lab 0 999999 1 1 3 > $f.tmp && mv $f.tmp $f; done < run/rep/fresh180.txt
python3 - <<'PY'
import statistics as st
def d2(fn):
    s = {"q1": 0, "q2": 0, "q3": 0}
    for l in open(fn):
        a = l.split()
        if a[0] == "H" and a[5] == "vig": s[a[4]] += int(a[11])
    return sum(s.values()), s
k4, k4s = d2("run/out/k4.m1s8.txt"); labs = [l.split()[0] for l in open("run/rep/fresh180.txt")]
v = {l: d2(f"run/rep/{l}.m1s8.txt") for l in labs}; x = [v[l][0] for l in labs]
ge = sum(t >= k4 for t in x); pF = (1 + ge) / (len(x) + 1); m, sd = st.mean(x), st.stdev(x)
print(f"K4 D2' {k4} {k4s}"); print(f"fresh 40: min {min(x)} max {max(x)} mean {m:.1f} SD {sd:.1f} #>=K4 {ge} p_F {pF:.3f} z {(k4-m)/sd:+.2f}")
for t in ("q1", "q2", "q3"):
    y = [v[l][1][t] for l in labs]; print(f"  {t}: K4 {k4s[t]} fresh mean {st.mean(y):.1f} SD {st.stdev(y):.1f} #>=K4 {sum(a >= k4s[t] for a in y)}")
print("DECISION:", "REPLICATED" if pF <= 0.05 else "NOT REPLICATED")
for l in labs: print(l, v[l][0], v[l][1])
PY
