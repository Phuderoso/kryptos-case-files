#!/usr/bin/env python3
"""Cycle 216 (PREREG216 Part A) planted controls: 20 plants with ONE corrupted carved crib letter. Seed 209226 (the only randomness).
Plants 0-7 direct (X, Y from alpha.bin), 8-13 behind bank.bin, 14-19 behind all.bin (X, Y from themed144.bin, random row and dir).
Key: even plants Gromark (L 2-20), odd plants periodic digits (P 2-20); ix random (0 = plaintext index, 1 = carved index; direct: 0).
Plaintext: a K1-K3 English 97-letter window with EASTNORTHEAST / BERLINCLOCK written at 0-idx 21-33 / 63-73. After encryption one
crib position j is chosen and its carved letter replaced by a different random letter (the resulting digit may or may not fall in 0..9).
writes plants216.tsv: id scope perm dir X Y form model L ix j digit_after plaintext ciphertext"""
import random, struct
r = random.Random(209226); POS = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEAST" + "BERLINCLOCK"
A = open('alpha.bin', 'rb').read(); NA = len(A) // 26; T = open('themed144.bin', 'rb').read()
eng = ''.join(c for c in open('k123_eng.txt').read().upper() if c.isalpha())
def perm(fn, q):
    with open(fn, 'rb') as f: f.seek(q * 194); return list(struct.unpack('<97h', f.read(194)))
def gromark(L):
    k = [r.randrange(10) for _ in range(L)]
    while len(k) < 97: k.append((k[-L] + k[-L + 1]) % 10 if L > 1 else (2 * k[-1]) % 10)
    return k
o = open('plants216.tsv', 'w')
for pid in range(20):
    scope = 'direct' if pid < 8 else 'bank' if pid < 14 else 'all'
    if scope == 'direct': Xa, Ya, q, d, S = r.randrange(NA), r.randrange(NA), -1, 0, list(range(97)); src = A
    else:
        fn = scope + '.bin'; nrow = {'bank': 165065, 'all': 165782}[scope]; q = r.randrange(nrow); d = r.randrange(2)
        s = perm(fn, q); S = s if d == 0 else [s.index(i) for i in range(97)]; Xa, Ya = r.randrange(144), r.randrange(144); src = T
    X = src[Xa * 26:(Xa + 1) * 26]; Y = src[Ya * 26:(Ya + 1) * 26]; xi = {v: i for i, v in enumerate(X)}
    form = r.randrange(3); model = 'gromark' if pid % 2 == 0 else 'periodic'; L = r.randint(2, 20)
    ix = 0 if scope == 'direct' else r.randrange(2)
    key = gromark(L) if model == 'gromark' else (lambda b: [b[t % L] for t in range(97)])([r.randrange(10) for _ in range(L)])
    st = r.randrange(len(eng) - 97); p = list(eng[st:st + 97])
    for jj, i in enumerate(POS): p[i] = PT[jj]
    p = ''.join(p); C = [''] * 97
    for i in range(97):
        x = xi[ord(p[i]) - 65]; k = key[i] if ix == 0 else key[S[i]]
        yv = (x + k) % 26 if form == 0 else (x - k) % 26 if form == 1 else (k - x) % 26
        C[S[i]] = chr(65 + Y[yv])
    j = r.randrange(24); i = POS[j]; old = C[S[i]]
    C[S[i]] = r.choice([c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c != old])
    yi = {v: n for n, v in enumerate(Y)}; y = yi[ord(C[S[i]]) - 65]; x = xi[ord(PT[j]) - 65]
    dig = (y - x) % 26 if form == 0 else (x - y) % 26 if form == 1 else (y + x) % 26
    o.write('\t'.join(map(str, [pid, scope, q, d, Xa, Ya, form, model, L, ix, j, dig, p, ''.join(C)])) + '\n')
