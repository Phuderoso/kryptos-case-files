"""Cycle 168 part A planted controls (independent string-level encryption, Sanborn-style additive tableaux).
Plaintext: Jane Eyre (Gutenberg 1260, not a key text) with EASTNORTHEAST/BERLINCLOCK at the official positions.
Key: a random offset in one of the cycle-168 key texts; substitution = one of bookrk's 24 additive modes
(md: ty = md%3 Vig/Beau/variant, plain/cipher/key-numbering alphabet AZ or KA by bits md/3, md/6, md/12);
Model A (substitute in plaintext order, then transpose) or B (transpose, then substitute in carved order).
Transposition: a random member of all.bin (decimations + routes). Writes ctlN.txt, ctlN_slice.bin (2,000 perms
containing the planted one at a random slot) and controls_planted.txt.
usage: rk168_controls.py all.bin texts.txt plain_source.txt N SEED"""
import sys, random, re, numpy as np
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
T = dict(l.split() for l in open(sys.argv[2]))
pt_src = re.sub("[^A-Z]", "", open(sys.argv[3], encoding="utf-8", errors="ignore").read().upper())
n, seed = int(sys.argv[4]), int(sys.argv[5]); rnd = random.Random(seed)
def enc(p, k, md):
    ty, ap, ac, ak = md % 3, (md // 3) & 1, (md // 6) & 1, (md // 12) & 1
    kv = KA.index(k) if ak else ord(k) - 65
    pp = KA.index(p) if ap else ord(p) - 65
    c = (pp + kv) % 26 if ty == 0 else (kv - pp) % 26 if ty == 1 else (pp - kv) % 26
    return KA[c] if ac else AZ[c]
names = ["carter1", "kjv_john", "cyc_K3pt", "natsec_act_1947_amended", "smith_rev", "kjv_nt", "reagan_berlin",
         "cyc_K1pt", "carter1_rev", "cyc_K123pt_K0", "kjv_nt_rev", "cyc_KAtableau_rows"]
info = []
for i in range(n):
    s = rnd.randrange(10000, len(pt_src) - 200); p = list(pt_src[s:s+97])
    p[21:34] = "EASTNORTHEAST"; p[63:74] = "BERLINCLOCK"; p = "".join(p)
    name = names[i % len(names)]; t = T[name]
    o = rnd.randrange(len(t) - 96); md = rnd.randrange(24)   # bookrk tests offsets 0..len-97
    if i == 0: md = 21   # ty 0 Vig, ap 1, ac 1, ak 1 (0+3+6+12): C = P + K in KA numbering (Sanborn's verified K1/K2 rule)
    model = "A" if i % 2 == 0 else "B"; j = rnd.randrange(P.shape[0]); perm = P[j]
    carved = [None]*97
    if model == "A":
        for pos in range(97): carved[perm[pos]] = enc(p[pos], t[o + pos], md)
    else:
        for x in range(97): carved[x] = enc(p[perm[x]], t[o + x], md)
    carved = "".join(carved)
    slot = rnd.randrange(2000); lo = min(max(0, j - slot), P.shape[0] - 2000)
    P[lo:lo+2000].tofile(f"ctl{i}_slice.bin")
    open(f"ctl{i}.txt", "w").write(carved + "\n")
    info.append(f"ctl{i}: perm {j} (slice index {j-lo}) model {model} mode {md} text {name} offset {o} pt {p}")
open("controls_planted.txt", "w").write("\n".join(info) + "\n"); print("\n".join(info))
