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

lines = []
PT_KNOWN = [1 if (21 <= i < 34 or 63 <= i < 74) else 0 for i in range(97)]
def run(ct, tag):
    open(f'{tag}.txt', 'w').write(ct)
    r = subprocess.run(['./hill_trans', 'perms97.bin', str(len(perms)), f'{tag}.txt'], capture_output=True, text=True).stdout
    open(f'{tag}_out.txt', 'w').write(r)
    return r
