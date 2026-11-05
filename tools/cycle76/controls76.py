"""Cycle 76 planted controls for nulltr76 (model A: substitution in plaintext order -> nulls dropped in
outside the cribs -> transposition from the 165,065-member cycle-19 family).  English plaintext from the
cycle-74 corpus; the planted transposition is a random family member; nulls are random letters at random
non-crib slots.  Writes ctl_N.txt (carved text) and controls76_planted.json."""
import random, json, re
from kryptos_text import KA
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
src = re.sub("[^A-Z]", "", open("/workspace/k4c74/texts_long.txt").read().upper())
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
def enc(mode, A, p, k):
    pi, ki = A.index(p), A.index(k)
    return A[(pi + ki) % 26] if mode == 0 else A[(ki - pi) % 26] if mode == 1 else A[(pi - ki) % 26]
def build(rng, a, b, c, A, mode, kind, key, L=None):
    n = 97 - a - b - c
    s = rng.randrange(0, len(src) - n); pt = list(src[s:s + n])
    p1, p2 = 21 - a, 63 - a - b
    pt[p1:p1 + 13] = "EASTNORTHEAST"; pt[p2:p2 + 11] = "BERLINCLOCK"
    ct = []
    for j, ch in enumerate(pt):
        if kind == "periodic": k = key[j % len(key)]
        elif kind == "ptak": k = key[j] if j < L else pt[j - L]
        else: k = key[j] if j < L else ct[j - L]
        ct.append(enc(mode, A, ch, k))
    pre = rng.sample(range(21), a); mid = rng.sample(range(34, 63), b); suf = rng.sample(range(74, 97), c)
    nulls = set(pre + mid + suf); it = iter(ct)
    X = [rng.choice(AZ) if i in nulls else next(it) for i in range(97)]
    assert "".join(X[21:34]) and next(it, None) is None
    pi = rng.randrange(len(perms)); P = perms[pi]
    carved = [None] * 97
    for i in range(97): carved[P[i]] = X[i]
    return "".join(carved), pi, "".join(pt), sorted(nulls)
rng = random.Random(7676); out = []
def rk(n): return "".join(rng.choice(AZ) for _ in range(n))
specs = [  # (tab, mode, kind, key, L, a, b, c)
    ("KA", 0, "periodic", "SHADOWS", None, 4, 9, 6),
    ("AZ", 1, "periodic", "ABSCISSAPAL", None, 2, 17, 3),
    ("KA", 0, "ptak", "PALIMPSE", 8, 1, 24, 2),
    ("AZ", 2, "ptak", rk(37), 37, 3, 10, 5),
    ("KA", 1, "ctak", "KRY", 3, 0, 29, 0),
    ("AZ", 0, "ctak", rk(40), 40, 6, 0, 7),
]
for n, (tab, mode, kind, key, L, a, b, c) in enumerate(specs):
    A = KA if tab == "KA" else AZ
    carved, pi, pt, nulls = build(rng, a, b, c, A, mode, kind, key, L)
    open(f"ctl_{n}.txt", "w").write(carved)
    fam = {"periodic": "F0", "ptak": "F1", "ctak": "F2"}[kind]
    if kind == "periodic": sig = f"HIT F0 perm={pi} tab={tab} mode={mode} p={len(key)} b={b % len(key)} "
    else:
        d = L - 42 + b; dv = -12 <= d <= 10
        sig = (f"HIT {fam} perm={pi} tab={tab} mode={mode} L={L} d={d if dv else 'none'} " if L <= 12
               else f"HIT {fam} perm={pi} tab={tab} mode={mode} L=any d={d} ")
    out.append({"ctl": n, "tab": tab, "mode": ["vig", "beau", "var"][mode], "kind": kind, "key": key, "L": L,
                "a": a, "b": b, "c": c, "perm": pi, "signature": sig, "carved": carved, "plaintext": pt, "nulls": nulls})
json.dump(out, open("controls76_planted.json", "w"), indent=1)
for o in out: print(o["ctl"], o["signature"])
