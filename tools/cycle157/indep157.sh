#!/bin/bash
# Cycle 157 independent checks (run from W): (1) profile of every null recomputed; (2) tools/cycle155/indep_check.py
# (pure Python, all 24 drops, no shared code with gromark1e.c) full L 4 recount per null vs the C lines;
# (3) single-primer Python confirmation of 2 sampled L 8 survivors per null; (4) K4 L 8 / L 11 survivor set == cycle 155.
D=$(cd $(dirname "$0"); pwd); REPO=${REPO:-$D/../..}; IC=$REPO/tools/cycle155/indep_check.py
python3 - <<'PY'
from collections import Counter
POS=list(range(21,34))+list(range(63,74)); k=open('ct_K4.txt').read().strip()
pk=sorted(Counter(k[i] for i in POS).values())
for l in open('nulls.txt'):
    n,t=l.split()[:2]; print('profile',n,'match' if sorted(Counter(t[i] for i in POS).values())==pk and sorted(t)==sorted(k) else 'MISMATCH')
PY
for T in ${ONLY:-$(cut -d' ' -f1 nulls.txt)}; do echo $T; done | xargs -P 8 -I{} sh -c 'python3 '$IC' $(cat ct_{}.txt) 4 {} P' > indep_L4.txt
python3 - <<'PY'
import re
c={}
for l in open('results_raw.txt'):
    m=re.match(r'C (\S+) P L=4 all lo=0 tested=(\d+) strict az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| one az:vig=(\d+) beau=(\d+) ka:vig=(\d+) beau=(\d+) \| pairs=(\d+)',l)
    if m: v=list(map(int,m.groups()[1:])); c[m.group(1)]=(v[0],sum(v[1:5]),sum(v[5:9]),v[9])
ok=0;n=0
for l in open('indep_L4.txt'):
    m=re.match(r'I (\S+) P L=4 primers=(\d+) strict=(\d+) one=(\d+) pairs=(\d+)',l); T=m.group(1); v=tuple(map(int,m.groups()[1:])); n+=1
    same=c.get(T)==v; ok+=same; print('L4',T,'C',c.get(T),'I',v,'same' if same else 'DIFF')
print(f'L4 recount identical {ok}/{n}')
PY
python3 - <<'PY' > sample_survivors.txt
import collections
s=collections.defaultdict(list)
for l in open('results_raw.txt'):
    if l.startswith('S ') and ' L=8 all ' in l and not l.startswith('S K4'):
        f=l.split(); s[f[1]].append(f[-1].split('=')[1])
for T in sorted(s):
    for p in sorted(set(s[T]))[:2]: print(T,p)
PY
while read T p; do python3 $IC $(cat ct_$T.txt) 8 $T P $p | tail -1; done < sample_survivors.txt > indep_single.txt
echo "single-primer survivors confirmed (one>0): $(grep -c 'one=[1-9]' indep_single.txt) of $(wc -l < sample_survivors.txt)"
grep '^S K4 P L=\(8 all\|11 perm\)' results_raw.txt | sort -u | sed 's/^S //' > k4_now.txt
grep '^S K4 P L=\(8 all\|11 perm\)' $REPO/data/cycle155/k4_survivors.txt | sort -u | sed 's/^S //' > k4_c155.txt
cmp -s k4_now.txt k4_c155.txt && echo "K4 L8/L11 survivor lines identical to cycle 155 ($(wc -l < k4_now.txt))" || echo "K4 survivor lines DIFFER"
