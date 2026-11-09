"""Cycle 168 part B: an UNNAMED English running key behind K3-law decimations + spiral/diagonal routes (Model A:
substitute in plaintext order with the running key, then transpose). Undoing the transposition puts the cribs at
plaintext positions 21-33 / 63-73, so the 24 forced key letters are two contiguous fragments (13 + 11) of the key
text; score them with English quadgrams (case 19 method, tools/k4_runkey_trans.py, re-implemented vectorised).
Tableaux: KRYPTOS-keyed (KA) and straight (AZ) x Vigenere / Beaufort / variant. Permutation convention as bookrk
model A and periodic_exact59: perm[j] = carved position holding plaintext letter j.
usage: fragscore168.py all.bin quadgrams.json MODE   MODE = k4 | nulls:N:SEED | controls:N:SEED  (writes JSON lines)"""
import sys, json, random, re, numpy as np
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
CPOS = np.array(sorted(CRIB)); assert len(K4) == 97
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97).astype(np.int64)
q = json.load(open(sys.argv[2]))
QT = np.full(26**4, q["floor"], dtype=np.float32)
for k, v in q["q"].items():
    QT[((ord(k[0])-65)*26 + ord(k[1])-65)*26*26 + (ord(k[2])-65)*26 + ord(k[3])-65] = v
def frag_score(K):
    s = np.zeros(K.shape[0], dtype=np.float32)
    for a, b in ((0, 13), (13, 24)):
        for i in range(a, b - 3):
            s += QT[((K[:, i]*26 + K[:, i+1])*26 + K[:, i+2])*26 + K[:, i+3]]
    return s / 18.0
def run(text, top=5):
    res = []; PC = P[:, CPOS]
    for an, A in (("KA", KA), ("AZ", AZ)):
        cv = np.array([A.index(ch) for ch in text], dtype=np.int64)
        crib = np.array([A.index(CRIB[i]) for i in CPOS], dtype=np.int64)
        toAZ = np.array([ord(ch) - 65 for ch in A], dtype=np.int64)
        C = cv[PC]
        for mode in ("vig", "beau", "var"):
            kv = (C - crib) % 26 if mode == "vig" else (C + crib) % 26 if mode == "beau" else (crib - C) % 26
            K = toAZ[kv]; s = frag_score(K)
            for j in np.argpartition(-s, top)[:top]:
                res.append((float(s[j]), an, mode, int(j), "".join(AZ[x] for x in K[j, :13]), "".join(AZ[x] for x in K[j, 13:])))
    res.sort(reverse=True); return res
def clean(path): return re.sub("[^A-Z]", "", open(path, encoding="utf-8", errors="ignore").read().upper())
def control(rnd, pt, kt):
    s = rnd.randrange(20000, len(pt) - 200); p = list(pt[s:s+97])
    p[21:34] = "EASTNORTHEAST"; p[63:74] = "BERLINCLOCK"
    o = rnd.randrange(20000, len(kt) - 200); key = kt[o:o+97]
    an = rnd.choice(["KA", "AZ"]); A = KA if an == "KA" else AZ; mode = rnd.choice(["vig", "beau", "var"])
    j = rnd.randrange(P.shape[0])
    I = [A[{"vig": A.index(c) + A.index(k), "beau": A.index(k) - A.index(c), "var": A.index(c) - A.index(k)}[mode] % 26]
         for c, k in zip(p, key)]
    carved = [None]*97
    for pos in range(97): carved[P[j][pos]] = I[pos]
    return "".join(carved), dict(alphabet=an, mode=mode, perm=j, frag1=key[21:34], frag2=key[63:74])
if __name__ == "__main__":
    arg = sys.argv[3]
    if arg == "k4":
        r = run(K4, 10); print(json.dumps(dict(item="K4", best=r[0][0], top=r[:10])))
    elif arg.startswith("nulls:"):
        _, n, seed = arg.split(":"); rnd = random.Random(int(seed))
        for i in range(int(n)):
            l = list(K4); rnd.shuffle(l); r = run("".join(l), 3)
            print(json.dumps(dict(item=f"null{i}", text="".join(l), best=r[0][0], top=r[:3])), flush=True)
    elif arg.startswith("controls:"):
        _, n, seed = arg.split(":"); rnd = random.Random(int(seed))
        pt = clean(sys.argv[4]); kt = clean(sys.argv[5])   # plaintext source, key source (neither in the key bank)
        for i in range(int(n)):
            ct, truth = control(rnd, pt, kt); r = run(ct, 50)
            rank = next((k + 1 for k, x in enumerate(r) if x[1] == truth["alphabet"] and x[2] == truth["mode"]
                         and x[4] == truth["frag1"] and x[5] == truth["frag2"]), None)
            print(json.dumps(dict(item=f"ctl{i}", text=ct, truth=truth, rank=rank, best=r[0][0], top=r[:3])), flush=True)
