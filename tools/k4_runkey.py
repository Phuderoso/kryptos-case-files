"""Cycle 16: English running key (any source text) under themed tableaux.
Idea: if K4 = running-key Vigenere/Beaufort/variant with an English key text, then at the 24 crib positions the
recovered KEY letters are two contiguous fragments of English (13 at 22-34, 11 at 64-74) whatever the source.
Test A (source-agnostic): score those key fragments with English quadgrams over 264 single-word themed alphabets
(plain alphabet Pa, cipher alphabet Ca, key alphabet Ka in {Pa, Ca, AZ}) x 3 modes = 627,264 tableaux.
Test B (named texts): exact 24-crib search of every offset of specific untried key texts for every tableau
with Pa = Ca (Quagmire III style, K1/K2) and Ka in {Pa, AZ}.
Usage: python3 tools/k4_runkey.py [control|null SEED|texts]"""
import sys, re, json, random, itertools, os
import numpy as np
sys.path.insert(0, "tools")
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WORDS = re.search(r'WORDS = """(.*?)"""', open("tools/k4_layers.py").read(), re.S).group(1).split()
def keyed(w): return "".join(dict.fromkeys(w + AZ))
def aca_columnar(w):
    kw = "".join(dict.fromkeys(w)); rows = keyed(kw)
    cols = [rows[j::len(kw)] for j in range(len(kw))]
    return "".join(c for _, c in sorted(zip(kw, cols)))
A = {"AZ": AZ, "KA": KA, "ZA": AZ[::-1], "AK": KA[::-1]}
for w in WORDS: A["k:" + w] = keyed(w); A["r:" + w] = keyed(w)[::-1]; A["c:" + w] = aca_columnar(w)
uniq = {}
for n, a in A.items(): uniq.setdefault(a, n)
ALPH = [(n, a) for a, n in uniq.items()]
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}   # 0-indexed starts (official 22-34, 64-74)
POS = [s + i for s, w in CRIBS.items() for i in range(len(w))]
PT = "".join(w for w in CRIBS.values())
Q = json.load(open("data/quadgrams.json")); QF = Q["floor"]; QQ = Q["q"]
def qs(t): return sum(QQ.get(t[i:i+4], QF) for i in range(len(t) - 3))
def keyidx(c, p, Pa, Ca, m):
    ci, pi = Ca.index(c), Pa.index(p)
    return (ci - pi) % 26 if m == "vig" else (ci + pi) % 26 if m == "beau" else (pi - ci) % 26
def enc(p, k, Pa, Ca, Ka, m):
    ki, pi = Ka.index(k), Pa.index(p)
    return Ca[(pi + ki) % 26] if m == "vig" else Ca[(ki - pi) % 26] if m == "beau" else Ca[(pi - ki) % 26]
def frags(CT, Pa, Ca, Ka, m):
    ks = "".join(Ka[keyidx(CT[j], PT[i], Pa, Ca, m)] for i, j in enumerate(POS))
    return ks[:13], ks[13:]
def testA(CT, top=25):
    res = []
    for (pn, Pa), (cn, Ca) in itertools.product(ALPH, ALPH):
        for kn, Ka in (("=P", Pa), ("=C", Ca), ("AZ", AZ)):
            for m in ("vig", "beau", "var"):
                f1, f2 = frags(CT, Pa, Ca, Ka, m)
                res.append(((qs(f1) + qs(f2)) / 18, pn, cn, kn, m, f1, f2))
    res.sort(reverse=True)
    return res[:top], len(res)
def load_text(path): return re.sub("[^A-Z]", "", open(path, encoding="utf-8", errors="ignore").read().upper())
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "k4"
    if mode == "control":
        rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 16)
        plain = load_text("data/rk_plain.txt"); key = load_text("data/rk_key.txt")
        o = rnd.randrange(len(plain) - 200); P = list(plain[o:o+97])
        for s, w in CRIBS.items(): P[s:s+len(w)] = w
        k = key[rnd.randrange(len(key) - 200):][:97]
        Pa, Ca = keyed("PALIMPSEST"), keyed("BERLIN")
        if len(sys.argv) > 2: Pa, Ca = rnd.choice(ALPH)[1], rnd.choice(ALPH)[1]
        CT = "".join(enc(p, kk, Pa, Ca, Ca, "beau") for p, kk in zip(P, k))
        print("planted: Pa", Pa, "Ca", Ca, "Ka=Ca beau; true key fragments", k[21:34], k[63:74])
        top, n = testA(CT, 10)
    elif mode == "null":
        rnd = random.Random(int(sys.argv[2])); c = list(K4); rnd.shuffle(c); CT = "".join(c)
        top, n = testA(CT, 5)
    else:
        top, n = testA(K4, 25)
    print(f"tableaux tested: {n}")
    for r in top: print(f"{r[0]:.3f} Pa={r[1]} Ca={r[2]} Ka={r[3]} {r[4]:4s} key: {r[5]} .. {r[6]}")
