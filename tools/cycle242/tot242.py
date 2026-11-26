"""Gate T2 (added after the run, disclosed in case 228): pure-Python recount of tri242's T totals for scope S2 (themed 144 x 144,
20,736 pairs x 2 groups x 3 forms) on K4 for low-constraint cells that have non-zero counts, using check242.viol only."""
import sys
sys.argv = ['x']
from m242 import *
import check242 as C
TH = rec('themed144.bin'); K4 = open('k4.txt').read().strip()
cells = [('PER', 25, 0), ('PER', 26, 0), ('PER', 31, 0), ('PER', 32, 0), ('PER', 33, 0), ('PA', 10, 0), ('PA', 10, 1), ('PA', 33, 1), ('PA', 49, 0), ('CA', 1, 0), ('CA', 24, 1)]
cnt = {c: [0, 0] for c in cells}
for x in range(144):
    for y in range(144):
        for g in range(2):
            for f in range(3):
                for c in cells:
                    v = C.viol(K4, c[0], g, f, TH[x], TH[y], c[1], c[2])
                    if v <= 1: cnt[c][v] += 1
T = {}
for ln in open('out/K4/S2.txt'):
    a = ln.split()
    if a[0] != 'T' or a[1] == 'pairforms': continue
    if a[1] == 'PER': T[('PER', int(a[2]), 0)] = (int(a[-3]), int(a[-1]))
    else: T[(a[1], int(a[2]), int(a[3]))] = (int(a[-3]), int(a[-1]))
bad = 0
for c in cells:
    ok = tuple(cnt[c]) == T[c]; bad += not ok
    print(c, 'python', cnt[c], 'tri242', T[c], 'OK' if ok else 'MISMATCH')
print(f'gate T2: {len(cells)} cells, {bad} mismatches')
