"""Cycle 152 independent control check: for each control, take zigfree's survivor line(s), recover the form word from the
wordlist (forms at the crib stream positions must match MAP[val(letter) mod r] for some word, r in {2,3}, map, numbering,
allowing '0' = broken equation), then decrypt the WHOLE text in Python (no C code) and compare with the planted plaintext.
usage: python3 check.py controls.txt all.txt c_*.txt"""
import sys, itertools, numpy as np
sys.path.insert(0, "/tmp/kcf/tools/cycle127"); from plant import plain
NUMS = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KRYPTOSABCDEFGHIJLMNQUVWXZ"]; A = [1, -1, 1]; B = [1, 1, -1]
cpos = list(range(21, 34)) + list(range(63, 74)); FL = {"V": {0}, "B": {1}, "X": {2}, "M": {0,1}, "N": {0,2}, "Y": {1,2}, "T": {0,1,2}}
Bk = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
ctl = {l.split()[0]: l.split() for l in open(sys.argv[1])}; words = [w.strip() for w in open(sys.argv[2]) if w.strip().isalpha()]
P = plain(); ok = 0; tot = 0
def decrypt(C, S, ix, nu, L, d, s, Fs, feed):
    N = NUMS[nu]
    c = [N.index(C[S[i]]) for i in range(97)] if ix == 0 else [N.index(x) for x in C]
    p = [None]*97
    if feed == "PT":  # unknown primer: seed the chain with the crib letters (stream positions) and run it forward
        for k, j in enumerate(cpos if ix == 0 else [S[x] for x in cpos]): p[j] = N.index("EASTNORTHEASTBERLINCLOCK"[k])
    for j in range(97):
        if p[j] is not None and feed == "PT": continue
        if j < L: continue
        F = Fs[j]; f = c[j-L] if feed == "CT" else p[j-L]
        if f is None: continue
        p[j] = (A[F]*(c[j] - s - d*j - B[F]*f)) % 26
    st = "".join(N[v] if v is not None else "?" for v in p)
    return st if ix == 0 else "".join(st[S[q]] for q in range(97))
for fn in sys.argv[3:]:
    for line in open(fn):
        if not line.startswith("S "): continue
        kv = dict(x.split("=", 1) for x in line.split()[2:] if "=" in x); lab = line.split()[1]
        L, d, q, dr, ix, nu, s = (int(kv[k]) for k in ("L", "d", "perm", "dir", "ix", "num", "s")); feed = kv["feed"]; forms = kv["forms"]
        rec = ctl[lab]; C = rec[-1]
        S = list(range(97)) if rec[1] == "-" else (list(Bk[q]) if dr == 0 else list(np.argsort(Bk[q])))
        kj = cpos if ix == 0 else [S[p] for p in cpos]
        need = [(kj[k], FL[forms[k]]) for k in range(24) if forms[k] in FL]
        found = []
        for w in words:
            for r in (2, 3):
                for mp in itertools.permutations(range(3), r):
                    for wn in (0, 1):
                        N = NUMS[wn]
                        if all(mp[N.index(w[j % len(w)]) % r] in al for j, al in need): found.append((w, r, mp, wn))
        tot += 1; good = None
        for w, r, mp, wn in found:
            Fs = [mp[NUMS[wn].index(w[j % len(w)]) % r] for j in range(97)]
            pt = decrypt(C, S, ix, nu, L, d, s, Fs, feed)
            agree = sum(a == b for a, b in zip(pt, P) if a != "?"); known = sum(a != "?" for a in pt)
            if feed == "PT": known -= 24; agree -= 24   # do not count the seeded crib letters
            if known > 0 and agree >= known - 3: good = (w, r, mp, wn, agree, known, pt); break
        print(lab, "words_consistent=%d" % len(found), "planted=%s" % rec[3], "->", ("RECOVERED word=%s r=%d map=%s wnum=%d agree=%d/%d\n  %s" % good) if good else "NOT RECOVERED")
        ok += good is not None
print("controls recovered %d/%d" % (ok, tot))
