"""Cycle 27, control 7: like control 6 (order a, KA, n = 4) but drawn from a configuration the checker can test
(every row of D gets at least n+1 crib equations). Control 6 fell in the untestable zone (one row had 3 equations)."""
import random, numpy as np
from hill_controls_lib import *
rng = random.Random(77); n = 4
while True:
    pi = rng.randrange(len(perms)); p = [int(x) for x in perms[pi]]; a = rng.randrange(n)
    Yk = [0]*97
    for i in range(97):
        if PT_KNOWN[i]: Yk[p[i]] = 1
    if min(sum(1 for s in range(a, 98-n, n) if Yk[s+j]) for j in range(n)) >= n+1: break
K = rand_inv(n, rng); Y = ['']*97
for j in range(97): Y[p[j]] = PT[j]
ct = hill(''.join(Y), K, n, a, KA)
out = run(ct, 'ctl_7'); hits = [l for l in out.splitlines() if l.startswith('HIT')]
want = f"perm={pi} order=a alph=KA n={n} align={a}"
line = f"control 7: planted {want} -> {len(hits)} consistent configs, planted one found: {any(l.startswith('HIT '+want) for l in hits)}"
open('controls_report.txt','a').write(line + '\n'); print(line)
