# Cycle 84 planted (p 7, 8) controls: ARBITRARY random 5x5 squares (random omitted letter outside the crib alphabet), random
# periodic outer keys p 4-6, enciphered by an independent Python Playfair (cycle 82's pf_enc) + outer key.
import random, json
from kryptos_text import KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; rng = random.Random(8401)
cpos = list(range(21, 34)) + list(range(63, 74)); crib = "EASTNORTHEASTBERLINCLOCK"; src = open("eng.txt").read()
def pf_enc(a, b, sq):
    p1, p2 = sq.index(a), sq.index(b); r1, c1, r2, c2 = p1 // 5, p1 % 5, p2 // 5, p2 % 5
    if r1 == r2: return sq[r1 * 5 + (c1 + 1) % 5], sq[r2 * 5 + (c2 + 1) % 5]
    if c1 == c2: return sq[((r1 + 1) % 5) * 5 + c1], sq[((r2 + 1) % 5) * 5 + c2]
    return sq[r1 * 5 + c2], sq[r2 * 5 + c1]
out = []
specs = [(7, "AZ", 1, 0), (8, "KA", 0, 1)]
for n, (p, tab, mode, a) in enumerate(specs):
    T = KA if tab == "KA" else AZ
    om = rng.choice([c for c in AZ if c not in set(crib)])
    letters = [c for c in AZ if c != om]; rng.shuffle(letters); sq = "".join(letters)
    key = "".join(rng.choice(AZ) for _ in range(p))
    o = rng.randrange(len(src) - 100); pt = list(src[o:o + 97])
    for i, ch in zip(cpos, crib): pt[i] = ch
    fill = "X" if om != "X" else "Z"
    pt = [fill if c == om else c for c in pt]
    for i in range(a, 96, 2):
        if pt[i] == pt[i + 1]: pt[i + 1] = fill if pt[i] != fill else "K"
    mid = pt[:]
    for i in range(a, 96, 2): mid[i], mid[i + 1] = pf_enc(pt[i], pt[i + 1], sq)
    ct = []
    for i, m in enumerate(mid):
        k = T.index(key[i % p]); q = T.index(m); c = (q + k) if mode == 0 else (k - q) if mode == 1 else (q - k); ct.append(T[c % 26])
    out.append(dict(ctl=n, square=sq, omitted=om, key=key, p=p, tab=tab, mode=mode, a=a, ct="".join(ct), pt="".join(pt)))
json.dump(out, open("controls84.json", "w"), indent=1)
for c in out: print(c["ctl"], c["p"], c["tab"], c["mode"], c["a"], c["omitted"], c["key"], c["ct"][:30])
