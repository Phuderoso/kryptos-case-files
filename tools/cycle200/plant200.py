"""Cycle 200 plants: English windows (Jane Eyre, Gutenberg) enciphered by K1-K3-style families.
Independent of lib200's statistics (only shares nothing but the alphabets)."""
import re
import numpy as np

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def corpus(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    i = t.find("CHAPTER I")
    j = t.find("*** END OF")
    return re.sub("[^A-Z]", "", t[i:j].upper())


def window(rng, txt, n=97):
    o = int(rng.integers(0, len(txt) - n))
    return txt[o:o + n]


def vig(pt, key, alpha=AZ, beau=False):
    out = []
    for i, c in enumerate(pt):
        k = alpha.index(key[i % len(key)]) if isinstance(key, str) else key[i]
        p = alpha.index(c)
        out.append(alpha[(k - p) % 26] if beau else alpha[(p + k) % 26])
    return "".join(out)


def columnar(s, order):
    w = len(order)
    cols = ["".join(s[i] for i in range(c, len(s), w)) for c in range(w)]
    return "".join(cols[c] for c in order)


def randkey(rng, p):
    return "".join(AZ[int(v)] for v in rng.integers(0, 26, p))


CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}   # 0-indexed starts (1-indexed 22-34, 64-74)


def with_cribs(pt):
    s = list(pt)
    for st, w in CRIBS.items():
        s[st:st + len(w)] = w
    return "".join(s)


def arbitrary_periodic(rng, pt, p):
    al = [rng.permutation(26) for _ in range(p)]
    return "".join(AZ[al[i % p][AZ.index(c)]] for i, c in enumerate(pt))


def family(name, rng, txt, n=97):
    pt = with_cribs(window(rng, txt, n)) if n == 97 else window(rng, txt, n)
    if name == "P1_vig_ka":            # K1/K2 style: KRYPTOS tableau, periodic key, p 4..12
        p = int(rng.integers(4, 13)); return vig(pt, randkey(rng, p), KA), dict(p=p)
    if name == "P2_beau_az":           # Beaufort A-Z, p 4..12
        p = int(rng.integers(4, 13)); return vig(pt, randkey(rng, p), AZ, beau=True), dict(p=p)
    if name == "P3_progressive":       # keyword shifts by s each lap, tableau AZ or KA
        p = int(rng.integers(5, 11)); s = int(rng.integers(1, 26)); al = AZ if rng.random() < .5 else KA
        base = [al.index(c) for c in randkey(rng, p)]
        ks = [(base[i % p] + s * (i // p)) % 26 for i in range(n)]
        return vig(pt, ks, al), dict(p=p, s=s, al=al[:2])
    if name == "P4_vig7_col14":        # case 97 shape: periodic p7 then columnar w14
        c = vig(pt, randkey(rng, 7), KA); o = rng.permutation(14); return columnar(c, list(o)), dict()
    if name == "P4b_vig7_col7":
        c = vig(pt, randkey(rng, 7), KA); o = rng.permutation(7); return columnar(c, list(o)), dict()
    if name == "P5_col_then_vig":      # columnar w 7..14 then periodic p 4..12
        w = int(rng.integers(7, 15)); p = int(rng.integers(4, 13))
        c = columnar(pt, list(rng.permutation(w))); return vig(c, randkey(rng, p), KA), dict(w=w, p=p)
    if name == "P6_vig_col_any":       # periodic p 4..12 then columnar w 5..14 (p need not divide w)
        w = int(rng.integers(5, 15)); p = int(rng.integers(4, 13))
        c = vig(pt, randkey(rng, p), KA); return columnar(c, list(rng.permutation(w))), dict(w=w, p=p)
    if name == "P7_pt_autokey":        # plaintext autokey, primer length L 1..10, AZ
        L = int(rng.integers(1, 11)); pr = randkey(rng, L)
        ks = [AZ.index(pr[i]) if i < L else AZ.index(pt[i - L]) for i in range(n)]
        return vig(pt, ks, AZ), dict(L=L)
    if name == "P8_running_key":       # English running key (another window), AZ
        k = window(rng, txt, n); return vig(pt, [AZ.index(c) for c in k], AZ), dict()
    if name == "P11_arbitrary_periodic":   # p arbitrary (non-tableau) alphabets, one per phase; p in {8, 13, 16} (open SAT cells)
        p = [8, 13, 16][int(rng.integers(0, 3))]
        return arbitrary_periodic(rng, pt, p), dict(p=p)
    if name == "P9_uniform":           # random letters: false-call gate
        return randkey(rng, n), dict()
    raise ValueError(name)


FAMILIES = ["P1_vig_ka", "P2_beau_az", "P3_progressive", "P4_vig7_col14", "P4b_vig7_col7",
            "P5_col_then_vig", "P6_vig_col_any", "P7_pt_autokey", "P8_running_key", "P11_arbitrary_periodic", "P9_uniform"]
