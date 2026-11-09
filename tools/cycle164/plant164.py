"""Cycle 164 controls: Quagmire I/II/IV autokey with two different keyed alphabets, encrypted independently
(string alphabets, .index lookups), plus shuffled-K4 nulls (seeds 16401-16402).
Encryption at key index q: Vig c=Y[x(p)+z(k)], Beau c=Y[z(k)-x(p)], Var c=Y[x(p)-z(k)];
x = index in plain alphabet X, z = index in X (zX) or in Y (zY)."""
import sys, random
import numpy as np
sys.path.insert(0, "/workspace/k4c164/repo/tools/cycle127")
from plant import plain, K4
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def keyed(w):
    s = ""
    for c in (w if w != "AZ" else "") + AZ:
        if c not in s: s += c
    return s
def enc(X, Y, zY, f, p, k):
    x = X.index(p); z = (Y if zY else X).index(k)
    return Y[(x + z if f == 0 else z - x if f == 1 else x - z) % 26]
def autokey(text, primer, X, Y, zY, f, feed):
    L = len(primer); out = []
    for i, c in enumerate(text):
        k = primer[i] if i < L else (text[i - L] if feed == "PT" else out[i - L])
        out.append(enc(X, Y, zY, f, c, k))
    return "".join(out)
def move(t, s):
    o = [None] * 97
    for i, c in enumerate(t): o[int(s[i])] = c
    return "".join(o)
CTL = [  # name, X, Y, zY, form, feed, primer, order, perm, dir
 ("ctl1", "SHADOW", "PALIMPSEST", 1, 0, "PT", "LUCID", "carved", 4242, 0),
 ("ctl2", "BERLIN", "CLOCK", 0, 1, "PT", "ILLUSION", "pt", 99999, 1),
 ("ctl3", "KRYPTOS", "AZ", 0, 2, "PT", "ABCDEFGHIJKLMN", "carved", 160000, 0),
 ("ctl4", "AZ", "ABSCISSA", 1, 0, "CT", "NUANCE", "carved", 12345, 1),
 ("ctl5", "TOMB", "VERDIGRIS", 0, 0, "PT", "QX", "pt", 777, 0),
 ("ctl6", "EGYPT", "ZEBRAFISH", 1, 1, "PT", "MAGNETICFIELDSX", "direct", 0, 0),
]
if __name__ == "__main__":
    P = plain()
    assert len(P) == 97 and P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK"
    B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
    for name, x, y, zY, f, feed, primer, order, q, d in CTL:
        X, Y = keyed(x), keyed(y)
        s = B[q] if d == 0 else np.argsort(B[q])
        if order == "direct": ct = autokey(P, primer, X, Y, zY, f, feed)
        elif order == "pt": ct = move(autokey(P, primer, X, Y, zY, f, feed), s)
        else: ct = autokey(move(P, s), primer, X, Y, zY, f, feed)
        print(name, ct, x, y, "zY" if zY else "zX", ["vig","beau","var"][f], feed, primer, len(primer), order, q, d)
    for z in (1, 2):
        l = list(K4); random.Random(16400 + z).shuffle(l); print(f"null{z}", "".join(l))
