"""Cycle 27 controls and nulls for hill_trans.c.
Planted controls: invented example English plaintext (NOT a K4 guess) carrying EASTNORTHEAST at 22-34 and
BERLINCLOCK at 64-74 (1-indexed), encrypted with a random invertible Hill matrix (n = 2,3,4; AZ or KA numbering)
on either side of a transposition drawn from the same family. Nulls: shuffled K4."""
import random, subprocess, math, itertools, numpy as np
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
pre = "WEWALKEDSOUTHUNTILTHE"; mid = "WINDTURNEDANDWEFOUNDTHEDOORX"; post = "WASSTRUCKATNOONTHERESTX"
PT = pre + "EASTNORTHEAST" + mid + "Y" + "BERLINCLOCK" + post
assert len(PT) == 97 and PT[21:34] == "EASTNORTHEAST" and PT[63:74] == "BERLINCLOCK", (len(PT))
perms = np.fromfile('perms97.bin', dtype=np.int16).reshape(-1, 97)
def rand_inv(n, rng):
    while True:
        K = np.array([[rng.randrange(26) for _ in range(n)] for _ in range(n)])
        if math.gcd(int(round(np.linalg.det(K))) % 26, 26) == 1: return K
def hill(text, K, n, a, A):
    v = [A.index(c) for c in text]; out = list(v)
    for s in range(a, 98 - n, n): out[s:s+n] = list(K.dot(np.array(v[s:s+n])) % 26)
    return ''.join(A[x] for x in out)
rng = random.Random(27)
lines = []
def run(ct, tag):
    open(f'{tag}.txt', 'w').write(ct)
    r = subprocess.run(['./hill_trans', 'perms97.bin', str(len(perms)), f'{tag}.txt'], capture_output=True, text=True).stdout
    open(f'{tag}_out.txt', 'w').write(r)
    return r
cases = [(2,'b','AZ'),(3,'b','KA'),(4,'b','AZ'),(2,'a','KA'),(3,'a','AZ'),(4,'a','KA')]
for i, (n, order, al) in enumerate(cases):
    A = KA if al == 'KA' else AZ
    pi = rng.randrange(len(perms)); p = [int(x) for x in perms[pi]]; a = rng.randrange(n); K = rand_inv(n, rng)
    if order == 'b':   # CT = T(Hill(P)) with Z[i] = CT[p[i]]  -> CT[p[i]] = H[i]
        H = hill(PT, K, n, a, A); ct = [''] * 97
        for j in range(97): ct[p[j]] = H[j]
    else:              # CT = Hill(T(P)) with Y[p[i]] = P[i]
        Y = [''] * 97
        for j in range(97): Y[p[j]] = PT[j]
        ct = list(hill(''.join(Y), K, n, a, A))
    ct = ''.join(ct)
    out = run(ct, f'ctl_{i+1}')
    hits = [l for l in out.splitlines() if l.startswith('HIT')]
    want = f"perm={pi} order={order} alph={al} n={n} align={a}"
    found = any(l.startswith('HIT ' + want) for l in hits)
    lines.append(f"control {i+1}: planted {want} -> {len(hits)} consistent configs, planted one found: {found}")
for k in range(5):
    l = list(K4); random.Random(1000 + k).shuffle(l)
    out = run(''.join(l), f'null_{k+1}')
    s = [x for x in out.splitlines() if x.startswith('SUMMARY')]
    lines.append(f"null {k+1}: " + ' | '.join(x.split('consistent=')[1].split(' ')[0] for x in s) + "  (consistent counts n=2,3,4,5)")
open('controls_report.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
