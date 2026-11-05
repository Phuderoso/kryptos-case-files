"""Planted controls for nulls75: English plaintext with the cribs at the official CARVED positions after
null insertion; nulls are random letters at random non-crib slots. Reports whether the planted (p, b) is found."""
import random, json, re
import nulls75
from kryptos_text import KA
AZ = nulls75.AZ
src = re.sub("[^A-Z]", "", open("/workspace/k4c74/texts_long.txt").read().upper())
def build(rng, a, b, c, enc):
    L = 97 - a - b - c
    s = rng.randrange(0, len(src) - L)
    pt = list(src[s:s + L])
    p1, p2 = 21 - a, 63 - a - b
    pt[p1:p1 + 13] = "EASTNORTHEAST"; pt[p2:p2 + 11] = "BERLINCLOCK"
    ctp = [enc(j, ch) for j, ch in enumerate(pt)]
    pre = sorted(rng.sample(range(21), a)); mid = sorted(rng.sample(range(34, 63), b)); suf = sorted(rng.sample(range(74, 97), c))
    nullpos = set(pre + mid + suf); out = []; it = iter(ctp)
    for i in range(97):
        out.append(rng.choice(AZ) if i in nullpos else next(it))
    return "".join(out), "".join(pt), sorted(nullpos)
rng = random.Random(7575); res = []
key = [KA.index(k) for k in "SHADOWS"]
ct, pt, np_ = build(rng, 4, 9, 6, lambda j, ch: KA[(KA.index(ch) + key[j % 7]) % 26])
H = nulls75.partB(ct)
res.append({"ctl": 0, "planted": "KA vig p7 b9 (a4 c6)", "found": any(h["alph"] == "KA" and h["mode"] == "vig" and h["p"] == 7 and h["b"] == 9 for h in H),
            "minp": min(h["p"] for h in H), "hits_p_le_10": [(h["alph"], h["mode"], h["p"], h["b"]) for h in H if h["p"] <= 10]})
h = [h for h in H if h["alph"] == "KA" and h["mode"] == "vig" and h["p"] == 7 and h["b"] == 9][0]
stream = [ch for i, ch in enumerate(ct) if i not in set(np_)]
dec = "".join(KA[(KA.index(c) - h["key"][(j + 4) % 7]) % 26] for j, c in enumerate(stream))  # crib frame shift a=4
res[-1]["full_decrypt_match"] = dec == pt; res[-1]["pt_len"] = len(pt); res[-1]["pt"] = pt
key = [AZ.index(k) for k in "ABSCISSAPAL"]
ct, pt, np_ = build(rng, 2, 0, 9, lambda j, ch: AZ[(key[j % 11] - AZ.index(ch)) % 26])
H = nulls75.partB(ct)
res.append({"ctl": 1, "planted": "AZ beau p11 b0 (a2 c9)", "found": any(h["alph"] == "AZ" and h["mode"] == "beau" and h["p"] == 11 and h["b"] == 0 for h in H),
            "minp": min(h["p"] for h in H)})
alphs = [rng.sample(AZ, 26) for _ in range(5)]
ct, pt, np_ = build(rng, 3, 12, 4, lambda j, ch: alphs[j % 5][AZ.index(ch)])
C = nulls75.partC(ct); res.append({"ctl": 2, "planted": "arbitrary p5 b12", "found": {"p": 5, "b": 12} in C, "C_p_le_7": [x for x in C if x["p"] <= 7]})
alphs = [rng.sample(AZ, 26) for _ in range(6)]
ct, pt, np_ = build(rng, 0, 20, 0, lambda j, ch: alphs[j % 6][AZ.index(ch)])
C = nulls75.partC(ct); res.append({"ctl": 3, "planted": "arbitrary p6 b20", "found": {"p": 6, "b": 20} in C, "C_p_le_7": [x for x in C if x["p"] <= 7]})
print(json.dumps(res, indent=1))
