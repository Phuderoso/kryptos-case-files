"""Gate T (PREREG242): independent pure-Python recount of every printed survivor line (viol and constraint count) for the given texts,
from the ciphertext, the alphabets and m242's group code only (no shared code with tri242.c)."""
import sys
from m242 import *
AL, TH, AK = rec('alpha.bin'), rec('themed144.bin'), rec('azka.bin')
ALPH = {'S1': (AL, AL), 'S2': (TH, TH), 'S3a': (AL, AK), 'S3b': (AK, AL)}
def viol(ct, model, g, f, X, Y, par, M):
    xi, yi = inv(X), inv(Y); mi = xi if M == 0 else yi
    k = {q: keyof(g, f, xi[ord(CR[j]) - 65], yi[ord(ct[q]) - 65]) for j, q in enumerate(POS)}
    if model == 'PER':
        cls = {}
        for q in POS: cls.setdefault(q % par, []).append(k[q])
        return sum(len(v) - max(v.count(a) for a in set(v)) for v in cls.values())
    if model == 'CA':
        bad = [q for q in POS if q - par >= 0 and mi[ord(ct[q - par]) - 65] != k[q]]
        if not bad: return 0
        if len(bad) == 1: return 1
        return 1 if len(bad) == 2 and bad[1] - par == bad[0] else 2
    pairs = [(q, q - par) for q in POS if q - par in POS]
    bad = [(q, r) for q, r in pairs if mi[ord(CR[POS.index(r)]) - 65] != k[q]]
    if not bad: return 0
    return 1 if any(all(s in b for b in bad) for s in POS) else 2
mism = n = 0
for name, ct in [a.split('=') for a in sys.argv[1:]]:
    for sc in ALPH:
        for ln in open(f'out/{name}/{sc}.txt'):
            a = ln.split()
            if a[0] != 'S': continue
            X, Y = ALPH[sc][0][int(a[4])], ALPH[sc][1][int(a[5])]
            v = viol(ct, a[1], int(a[2]), int(a[3]), X, Y, int(a[6]), 0 if a[7] in '-0' else 1)
            n += 1
            if v != int(a[8]): mism += 1; print('MISMATCH', name, sc, ln.strip(), 'py', v)
print(f'gate T: {n} lines rechecked, {mism} mismatches')
