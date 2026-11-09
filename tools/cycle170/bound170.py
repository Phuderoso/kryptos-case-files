"""Analytic chance bound for periodic Porta fits on the K4 stage-1 survivors: sum over (survivor, variant, model, L) of
13^-(checks), checks = 24 - number of distinct key residues hit by the crib indices. Usage: bound170.py all.bin out/k4.c*"""
import sys, re, numpy as np
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); CP = list(range(21, 34)) + list(range(63, 74))
E = {}; mins = {}
for fn in sys.argv[2:]:
    for l in open(fn):
        if not l.startswith('SURV'): continue
        perm = P[int(l.split()[2])]
        for md, ix in (('A', CP), ('B', [int(perm[j]) for j in CP])):
            for L in range(1, 27):
                c = 24 - len({x % L for x in ix}); E[(md, L)] = E.get((md, L), 0) + 2 * 13.0 ** -c
                mins[(md, L)] = min(mins.get((md, L), 99), c)
for md in 'AB':
    print(md, 'L<=20 expected chance fits %.2e' % sum(E[(md, L)] for L in range(1, 21)),
          '| L21-23 %.2e' % sum(E[(md, L)] for L in range(21, 24)), '| L24-26 %.2f' % sum(E[(md, L)] for L in range(24, 27)),
          '| min checks by L', [mins[(md, L)] for L in range(1, 27)])
