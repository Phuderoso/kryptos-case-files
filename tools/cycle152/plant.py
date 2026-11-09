"""Cycle 152 controls: word-keyed zig-zag autokey (+ progressive shift), encrypted independently in Python.
Form at stream position j: MAP[val(word[j mod len]) mod r], val = index of the letter in the numbering alphabet
(A-Z or KRYPTOS), r = 3 (three forms) or 2 (two forms); forms 0 V (c=s+dj+p+f), 1 B (c=s+dj-p+f), 2 X (c=s+dj+p-f).
Feed f = c[j-L] (CT) or p[j-L] (PT), random primer. Plaintext: cycle 127/137 English control text (cribs in place).
Seed 15200; nulls: K4 shuffled with seeds 15201-15202.
Output: label src perm word r map nu L d feed text   (src '-' direct, 'P' bank entry, 'I' inverse of bank entry)"""
import sys, random, os
import numpy as np
sys.path.insert(0, "/tmp/kcf/tools/cycle127")
from plant import plain, K4
R = random.Random(15200); NUMS = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KRYPTOSABCDEFGHIJLMNQUVWXZ"]; A = [1, -1, 1]; B = [1, 1, -1]
def forms(word, r, mp, nu, n=97):
    N = NUMS[nu]; return [mp[N.index(word[j % len(word)]) % r] for j in range(n)]
def enc(text, word, r, mp, nu, L, d, feed):
    N = NUMS[nu]; Fs = forms(word, r, mp, nu, len(text)); s = R.randrange(26); pr = [R.randrange(26) for _ in range(L)]
    p = [N.index(x) for x in text]; c = []
    for j in range(len(p)):
        F = Fs[j]; f = pr[j] if j < L else (c[j-L] if feed == "CT" else p[j-L])
        c.append((s + d*j + A[F]*p[j] + B[F]*f) % 26)
    return "".join(N[v] for v in c)
def ctl(P, word, r, mp, nu, L, d, feed, ix, S):
    if ix == 0:
        Lt = enc(P, word, r, mp, nu, L, d, feed); C = [None]*97
        for i in range(97): C[S[i]] = Lt[i]
        return "".join(C)
    out = [None]*97
    for p in range(97): out[S[p]] = P[p]
    return enc("".join(out), word, r, mp, nu, L, d, feed)
if __name__ == "__main__":
    P = plain(); assert P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
    Bk = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97); I = list(range(97))
    spec = [  # label src perm word r map nu L d feed ix
        ("ctl1", "-", 0, "KRYPTOS", 3, (0,1,2), 0, 1, 0, "CT", 0),
        ("ctl2", "-", 0, "PALIMPSEST", 2, (0,1), 1, 7, 3, "CT", 0),
        ("ctl3", "P", 4242, "ABSCISSA", 3, (2,0,1), 0, 5, 0, "CT", 0),
        ("ctl4", "P", 120000, "BERLIN", 2, (1,2), 1, 13, 11, "CT", 1),
        ("ctl5", "I", 99999, "SHADOW", 3, (1,2,0), 0, 2, 1, "CT", 1),
        ("ctl6", "-", 0, "IQLUSION", 3, (0,2,1), 0, 40, 5, "PT", 0),
        ("ctl7", "-", 0, "LAYERTWO", 3, (0,1,2), 1, 3, 0, "CT", 0),   # one carved letter corrupted below
    ]
    for lab, src, q, w, r, mp, nu, L, d, feed, ix in spec:
        S = I if src == "-" else (list(Bk[q]) if src == "P" else list(np.argsort(Bk[q])))
        t = ctl(P, w, r, mp, nu, L, d, feed, ix, S)
        if lab == "ctl7":  # corrupt the carved letter at plaintext/carved position 30 (inside EASTNORTHEAST)
            t = t[:30] + chr((ord(t[30]) - 65 + 7) % 26 + 65) + t[31:]
        print(lab, src, q, w, r, "".join(map(str, mp)), nu, L, d, feed, ix, t)
    for z in (1, 2):
        l = list(K4); random.Random(15200+z).shuffle(l); print(f"null{z} - 0 - 0 - 0 0 0 - 0", "".join(l))
