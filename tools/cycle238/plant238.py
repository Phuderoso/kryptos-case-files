"""PREREG238 gate P for audit238.py: seed 209706. Writes pl238.bin (60 windows: 20 clean random, 40 defective of 8 kinds x 5)
and pl238.tsv (index, kind, expected flag). usage: plant238.py outdir"""
import random, sys
rnd = random.Random(209706); N = 97
def rw(): return [rnd.randrange(26) for _ in range(N)]
kinds = []
rows = []
for _ in range(20): rows.append(('clean', None, rw()))
def zt():  w = rw(); p = rnd.randrange(30, 87); w[p:] = [0] * (N - p); return w   # zero tail >= 10
def ct():  w = rw(); p = rnd.randrange(30, 87); w[p:] = [w[p - 1]] * (N - p); return w   # clamp / size-cap: last value repeated
def kc():  return [rnd.randrange(26)] * N
def c3():  v = [rnd.randrange(26) for _ in range(3)]; return [rnd.choice(v) for _ in range(N)]
def hz():  w = rw(); p = rnd.randrange(12, 60); w[:p] = [7] * p; return w
def sc():  w = rw(); v = rnd.randrange(26); [w.__setitem__(i, v) for i in range(21, 34)]; [w.__setitem__(i, v) for i in range(63, 74)]; return w
def bc():  w = rw(); v = rnd.randrange(26); [w.__setitem__(i, v) for i in range(63, 74)]; return w
def pr():  p = rnd.randrange(2, 13); base = [rnd.randrange(26) for _ in range(p)]; return [base[i % p] for i in range(N)]
for name, f, exp in [('zerotail', zt, 'ZEROTAIL'), ('clamp', ct, 'TAILRUN'), ('const', kc, 'CONST60'), ('three', c3, 'DISTINCT3'),
                     ('headrun', hz, 'HEADRUN'), ('seatconst', sc, 'SEATCONST'), ('blockconst', bc, 'BLOCKCONST'), ('period', pr, 'PERIOD12')]:
    for _ in range(5): rows.append((name, exp, f()))
d = sys.argv[1]
open(d + '/pl238.bin', 'wb').write(b''.join(bytes(r[2]) for r in rows))
open(d + '/pl238.tsv', 'w').write('idx\tkind\texpected\n' + ''.join(f'{i}\t{r[0]}\t{r[1]}\n' for i, r in enumerate(rows)))
