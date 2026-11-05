"""Cycle 77 planted controls for coord77: English plaintext (cycle-74 corpus) with the cribs at Sanborn's positions,
coordinate key k = a[col] + b[row] on a w-column grid with offset o, KA or A-Z tableau, Vigenere/Beaufort,
model A (key then transposition) or B (transposition then key); random cycle-19-family transposition."""
import random, json, re
import numpy as np
from kryptos_text import KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
src = re.sub("[^A-Z]", "", open("/workspace/k4c74/texts_long.txt").read().upper())
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
rng = random.Random(7777)
def enc(mode, A, p, k):
    pi = A.index(p); return A[(pi + k) % 26] if mode == 0 else A[(k - pi) % 26]
specs = [  # tab, mode, model, w, o, column word, row word
    ("KA", 0, "A", 8, 0, "ABSCISSA", "PALIMPSEST"),
    ("AZ", 1, "A", 7, 3, "KRYPTOS", "BERLINWALL"),
    ("KA", 1, "B", 5, 2, "SHADO", "IQLUSION"),
    ("AZ", 0, "B", 11, 0, "LAYERTWOXYZ", "ORDINATE"),
    ("KA", 0, "A", 13, 6, "UNDERGRUUNDX", "CLOCK"),
    ("AZ", 0, "A", 4, 1, "EAST", "WELTZEITUHR"),
]
out = []
for n, (tab, mode, model, w, o, cw, rw) in enumerate(specs):
    A = KA if tab == "KA" else AZ
    cw = (cw * 4)[:w]
    s = rng.randrange(0, len(src) - 97); pt = list(src[s:s + 97])
    pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    pi = rng.randrange(1, len(perms)); P = perms[pi]
    def key(q):  # q = grid index before offset
        q += o; return (A.index(cw[q % w]) + A.index(rw[(q // w) % len(rw)])) % 26
    carved = [None] * 97
    if model == "A":
        X = [enc(mode, A, pt[i], key(i)) for i in range(97)]
        for i in range(97): carved[P[i]] = X[i]
    else:
        T = [None] * 97
        for i in range(97): T[P[i]] = pt[i]
        carved = [enc(mode, A, T[j], key(j)) for j in range(97)]
    carved = "".join(carved)
    open(f"ctl_{n}.txt", "w").write(carved)
    sig = f"HIT perm={pi} alph={0 if tab=='KA' else 1} mode={mode} model={model} w={w} o={o} "
    out.append(dict(ctl=n, tab=tab, mode=["vig", "beau"][mode], model=model, w=w, o=o, col_word=cw, row_word=rw,
                    perm=int(pi), signature=sig, carved=carved, plaintext="".join(pt)))
json.dump(out, open("controls77_planted.json", "w"), indent=1)
for o_ in out: print(o_["ctl"], o_["signature"])
