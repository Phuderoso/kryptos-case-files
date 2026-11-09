"""Cycle 170 planted Porta controls (independent string-level encryptor, no code shared with porta170.c).
Writes ctl/ctlN.txt (CT), ctl/ctlN_slice.bin (200 perms incl. the planted one at a random slot) and ctl/plants.txt.
Usage: python3 ctl170.py all.bin alpha.bin texts.txt NCTL SEED"""
import sys, random, numpy as np
allb, alphab, textsf, n, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
P = np.fromfile(allb, dtype=np.int16).reshape(-1, 97); A = np.fromfile(alphab, dtype=np.uint8).reshape(-1, 26)
texts = [l.split(' ', 1) for l in open(textsf).read().split('\n') if ' ' in l]
texts = [(a, ''.join(c for c in b if c.isalpha())) for a, b in texts]
rng = random.Random(seed)
PT = ("THEYCAMEATDAWNANDSTOOD" + "EASTNORTHEAST" + "OFTHEOLDSTONEWALLWHEREWESAWTHE" + "BERLINCLOCK" + "SHININGINTHEEMPTYSQUARETONIGHTX")
PT = (PT[:21] + "EASTNORTHEAST" + PT[34:63] + "BERLINCLOCK" + PT[74:])[:97]
assert len(PT) == 97 and PT[21:34] == "EASTNORTHEAST" and PT[63:74] == "BERLINCLOCK"
def porta(ch, o, k, var):
    i = o.index(ch)
    if i < 13: return o[13 + ((i + k) % 13 if var == 1 else (k - i) % 13)]
    h = i - 13
    return o[(h - k) % 13 if var == 1 else (k - h) % 13]
import os; os.makedirs('ctl', exist_ok=True); log = open('ctl/plants.txt', 'w')
for c in range(n):
    pi = rng.randrange(len(P)); perm = [int(x) for x in P[pi]]
    ai = rng.randrange(len(A)); alpha = ''.join(chr(65 + x) for x in A[ai]); split = rng.choice('FE')
    o = alpha if split == 'F' else alpha[0::2] + alpha[1::2]
    var = rng.choice([1, 2]); model = 'AB'[c % 2]; kind = 'per' if c % 3 != 2 else 'rk'
    if kind == 'per':
        L = rng.randint(3, 12); key = [rng.randrange(13) for _ in range(L)]; kf = lambda idx: key[idx % L]; desc = f"L{L} key{key}"
    else:
        tn, tx = rng.choice([t for t in texts if len(t[1]) > 2000]); t0 = rng.randrange(len(tx) - 97)
        fm = rng.randrange(2); s = rng.choice([1, -1]); c0 = rng.randrange(13)
        f = (lambda ch: (ord(ch) - 65) // 2) if fm == 0 else (lambda ch: o.index(ch) // 2)
        kf = lambda idx: (s * f(tx[t0 + idx]) + c0) % 13; desc = f"RK {tn} t{t0} f{fm} s{'+' if s>0 else '-'} c{c0}"
    ct = [None] * 97
    for j, ch in enumerate(PT):
        idx = j if model == 'A' else perm[j]
        ct[perm[j]] = porta(ch, o, kf(idx), var)
    ct = ''.join(ct)
    # self-check: decryption by reciprocity restores PT
    dec = [None] * 97
    for j in range(97):
        idx = j if model == 'A' else perm[j]; dec[j] = porta(ct[perm[j]], o, kf(idx), var)
    assert ''.join(dec) == PT
    sl = [rng.randrange(len(P)) for _ in range(200)]; slot = rng.randrange(200); sl[slot] = pi
    P[sl].tofile(f'ctl/ctl{c}_slice.bin'); open(f'ctl/ctl{c}.txt', 'w').write(ct)
    log.write(f"ctl{c} perm {pi} slot {slot} alpha {ai} split {split} ord {o} V{var} {model} {kind} {desc} CT {ct}\n")
log.close(); print(open('ctl/plants.txt').read())
