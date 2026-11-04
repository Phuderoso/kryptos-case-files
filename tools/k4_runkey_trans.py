"""Cycle 20: English running key BEHIND a transposition (substitute first, then transpose = Model A).
Undoing the transposition puts the cribs back at plaintext positions 21-33 and 63-73, so the 24 forced
key letters are again two contiguous fragments of the key text (13 + 11 letters, 29 apart) and can be
scored as English with quadgrams, exactly as in cycle 16, without naming the book.
Transpositions: the cycle 19 family (all column orders w=2..8, K3-style single/double rotations, inverses).
Tableaux: KRYPTOS-keyed (KA) and straight (AZ); Vigenere, Beaufort, variant Beaufort.
Usage (from tools/): python3 k4_runkey_trans.py [K4|null:SEED|control:SEED]"""
import sys, json, random, re, numpy as np
from kryptos_text import K4, KA
from k4_autokey_trans import family, CRIB, CPOS, AZ
q = json.load(open("../data/quadgrams.json"))
QT = np.full(26**4, q["floor"], dtype=np.float32)
for k, v in q["q"].items():
    QT[((ord(k[0])-65)*26 + ord(k[1])-65)*26*26 + (ord(k[2])-65)*26 + ord(k[3])-65] = v
def frag_score(K):  # K: (N,24) AZ indices; fragments 0..12 and 13..23
    s = 0
    for a, b in ((0, 13), (13, 24)):
        for i in range(a, b - 3):
            s = s + QT[((K[:, i]*26 + K[:, i+1])*26 + K[:, i+2])*26 + K[:, i+3]]
    return s / 18.0
def keyletters(c, crib, mode):
    if mode == "vig": return (c - crib) % 26
    if mode == "beau": return (c + crib) % 26
    return (crib - c) % 26
FAM = family(97); P = np.stack([f[0] for f in FAM]); TAGS = [f[1] for f in FAM]
def run(text, top=10):
    res = []
    for an, A in (("KA", KA), ("AZ", AZ)):
        cv = np.array([A.index(ch) for ch in text], dtype=np.int16)
        crib = np.array([A.index(CRIB[i]) for i in CPOS], dtype=np.int16)
        toAZ = np.array([ord(ch)-65 for ch in A], dtype=np.int32)
        C = cv[P][:, CPOS]
        for mode in ("vig", "beau", "var"):
            K = toAZ[keyletters(C, crib, mode)]
            s = frag_score(K)
            for j in np.argsort(-s)[:top]:
                res.append((float(s[j]), an, mode, TAGS[j], "".join(AZ[x] for x in K[j, :13]), "".join(AZ[x] for x in K[j, 13:])))
    res.sort(reverse=True)
    return res
def control(seed):
    rnd = random.Random(seed)
    pt = re.sub("[^A-Z]", "", open("../data/g1260.txt", encoding="utf-8", errors="ignore").read().upper())
    kt = re.sub("[^A-Z]", "", open("../data/g345.txt", encoding="utf-8", errors="ignore").read().upper())
    s = rnd.randrange(20000, len(pt) - 200); p = list(pt[s:s+97])
    p[21:34] = "EASTNORTHEAST"; p[63:74] = "BERLINCLOCK"
    o = rnd.randrange(20000, len(kt) - 200); key = kt[o:o+97]
    A = rnd.choice([KA, AZ]); mode = rnd.choice(["vig", "beau", "var"])
    j = rnd.randrange(len(FAM)); perm = P[j]
    I = []
    for ch, k in zip(p, key):
        pi, ki = A.index(ch), A.index(k)
        I.append(A[{"vig": pi + ki, "beau": ki - pi, "var": pi - ki}[mode] % 26])
    carved = [None]*97
    for pos, v in enumerate(perm): carved[v] = I[pos]   # so that carved[perm] == I
    return "".join(carved), ("KA" if A == KA else "AZ", mode, TAGS[j], key[21:34], key[63:74])
if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "K4"
    if arg == "K4": text, truth = K4, None
    elif arg.startswith("null:"):
        r = random.Random(int(arg[5:])); l = list(K4); r.shuffle(l); text, truth = "".join(l), None
    else:
        text, truth = control(int(arg[8:])); print("planted:", truth)
    res = run(text)
    print(f"{arg}: {len(FAM)} transpositions x 6 tableaux; top 8 fragment scores (mean log10/quadgram):")
    for r in res[:8]: print("  %.3f %s %s %-22s %s / %s" % r)
    if truth:
        rank = [i for i, r in enumerate(res) if r[1] == truth[0] and r[2] == truth[1] and r[4] == truth[3]]
        print("planted key fragments found at rank:", rank[0] + 1 if rank else "NOT in top list")
