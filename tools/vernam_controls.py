"""Cycle 33: planted controls and shuffled nulls for the 5-bit Vernam test."""
import random, re, sys, numpy as np
sys.path.insert(0, '/workspace/kcl/tools')
from kryptos_text import K4
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
ITA2 = [0x03,0x19,0x0E,0x09,0x01,0x0D,0x1A,0x14,0x06,0x0B,0x0F,0x12,0x1C,0x0C,0x18,0x16,0x17,0x0A,0x05,0x10,0x07,0x1E,0x13,0x1D,0x15,0x11]
def codes(e):
    if e == 0: return ITA2
    if e in (1, 2): return [l + (e == 2) for l in range(26)]
    return [KA.index(chr(65 + l)) + (e == 4) for l in range(26)]
perms = np.fromfile('perms97.bin', dtype=np.int16).reshape(-1, 97)
PT = ("SLOWLYTHEDOORSWEREOPENEDANDWEFOUNDTHEROOMEASTNORTHEASTOFTHEOLDBERLINCLOCKTOWERWHEREALLLAYSILENTX")
# rebuild with cribs at official positions 21..33 and 63..73
base = "THELIGHTFELLONTHESTONE" [:21]
pt = list("X" * 97)
src = re.sub("[^A-Z]", "", "ITWASJUSTBEFOREDAWNWHENWELOOKEDOUTACROSSTHEFIELDANDSAWTHEOLDSTONEWALLSTANDINGSTILLINTHECOLDMISTXAGAIN")
pt = list(src[:97]); pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"; pt = "".join(pt)
def enc_periodic(seed):
    rnd = random.Random(seed)
    while True:
        e = rnd.randrange(5); m = rnd.randrange(2); L = rnd.randint(1, 20); p = rnd.randrange(len(perms)); P = perms[p]
        c = codes(e); d = {v: i for i, v in enumerate(c)}
        if m == 0:  # XOR on plaintext order, then carved[P[k]] = X[k]
            X = [None]*97; key = []
            for r in range(L):
                ok = [k for k in range(32) if all((c[ord(pt[i])-65] ^ k) in d for i in range(r, 97, L))]
                if not ok: break
                key.append(rnd.choice(ok))
            if len(key) < L: continue
            X = [chr(65 + d[c[ord(pt[i])-65] ^ key[i % L]]) for i in range(97)]
            carved = [None]*97
            for k in range(97): carved[P[k]] = X[k]
        else:  # transposition T[k] = pt[P[k]], then XOR by k
            T = [pt[P[k]] for k in range(97)]; key = []
            for r in range(L):
                ok = [k for k in range(32) if all((c[ord(T[i])-65] ^ k) in d for i in range(r, 97, L))]
                if not ok: break
                key.append(rnd.choice(ok))
            if len(key) < L: continue
            carved = [chr(65 + d[c[ord(T[i])-65] ^ key[i % L]]) for i in range(97)]
        return "".join(carved), dict(perm=p, enc=e, model="AB"[m], L=L)
def enc_running(seed, bk='g84'):
    rnd = random.Random(seed); book = re.sub("[^A-Z]", "", open('/workspace/kcl/data/' + bk + '.txt').read().upper())
    while True:
        e = rnd.randrange(5); p = rnd.randrange(len(perms)); P = perms[p]; off = rnd.randrange(len(book) - 100)
        c = codes(e); d = {v: i for i, v in enumerate(c)}
        X = [(c[ord(pt[i])-65] ^ c[ord(book[off+i])-65]) for i in range(97)]
        if all(x in d for x in X):
            carved = [None]*97
            for k in range(97): carved[P[k]] = chr(65 + d[X[k]])
            return "".join(carved), dict(perm=p, enc=e, model="A", off=off, key=book[off+21:off+34] + "|" + book[off+63:off+74])
if __name__ == "__main__":
    out = []
    for s in (1, 2, 3):
        ct, info = enc_periodic(s); open(f"ctl_p{s}.txt", "w").write(ct); out.append(f"ctl_p{s} {info}")
    for s in (1, 2):
        ct, info = enc_running(100 + s, ['g84','g98'][s-1]); open(f"ctl_r{s}.txt", "w").write(ct); out.append(f"ctl_r{s} {info}")
    for s in range(1, 11):
        l = list(K4); random.Random(1000 + s).shuffle(l); open(f"null_{s}.txt", "w").write("".join(l))
    open("controls_planted.txt", "w").write("plaintext=" + pt + "\n" + "\n".join(out) + "\n"); print("\n".join(out))
