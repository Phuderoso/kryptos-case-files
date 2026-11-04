"""Cycle 15: long-period fixed-tableau keys (P = 27..96), incl. P=31 = "key restarts with every carved row".
Cycle 1 stopped at P=26. For P > 26 the cribs collide on few residues, so the test is: (1) are the cribs
consistent with ONE key letter per residue? (2) if so, the cribs fix the key on many residues, which fixes the
plaintext at every position in those residues -> that partial plaintext must read as English.
Families: alphabets AZ, KA; modes vig c=p+k, beau c=k-p, varbeau c=p-k (indices in the alphabet; same alphabet
for plain and cipher, i.e. the K1/K2 tableau when alphabet=KA). Optional row offset is irrelevant (relabels residues).
Usage: python3 tools/k4_longperiod.py [--control]"""
import sys, json, random
sys.path.insert(0, "tools"); import kryptos_text
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = kryptos_text.KA
CRIBS = {22: "EASTNORTHEAST", 64: "BERLINCLOCK"}
KN = {p - 1 + i: ch for p, w in CRIBS.items() for i, ch in enumerate(w)}
Q = json.load(open("data/quadgrams.json")); QF = Q["floor"]; QQ = Q["q"]
def kof(c, p, A, m):
    ci, pi = A.index(c), A.index(p)
    return {"vig": (ci - pi) % 26, "beau": (ci + pi) % 26, "varbeau": (pi - ci) % 26}[m]
def dec(c, k, A, m):
    ci = A.index(c)
    return A[{"vig": (ci - k) % 26, "beau": (k - ci) % 26, "varbeau": (ci + k) % 26}[m]]
def enc(p, k, A, m):
    pi = A.index(p)
    return A[{"vig": (pi + k) % 26, "beau": (k - pi) % 26, "varbeau": (pi - k) % 26}[m]]
def segscore(t):  # mean quadgram log10 over runs of known letters (excluding crib positions)
    s = n = 0
    for run in t.split("."):
        for i in range(len(run) - 3): s += QQ.get(run[i:i+4], QF); n += 1
    return (s / n if n else None), n
def run(CT, label):
    out = []; surv = []
    for P in range(27, 97):
        for an, A in (("AZ", AZ), ("KA", KA)):
            for m in ("vig", "beau", "varbeau"):
                key = {}; ok = True; coll = 0
                for i, ch in KN.items():
                    k = kof(CT[i], ch, A, m); r = i % P
                    if r in key:
                        coll += 1
                        if key[r] != k: ok = False; break
                    else: key[r] = k
                if not ok: continue
                pt = "".join(("" if False else (dec(CT[i], key[i % P], A, m) if i % P in key else ".")) for i in range(97))
                nonc = "".join(pt[i] if i not in KN else "." for i in range(97))
                sc, nq = segscore(nonc)
                surv.append((P, an, m, coll, pt.count(".") , sc, nq, pt))
    out.append(f"[{label}] families tested: {70*6}; consistent: {len(surv)}")
    for s in sorted(surv, key=lambda s: -(s[5] if s[5] is not None else -99)):
        out.append(f"P={s[0]:2d} {s[1]} {s[2]:7s} collisions={s[3]} unknown={s[4]:2d} quadgram/4gram(non-crib)={s[5] if s[5] is None else round(s[5],2)} n={s[6]}  {s[7]}")
    return out
if __name__ == "__main__":
    if "--control" in sys.argv:
        rnd = random.Random(15)
        base = ("THEYWEREBURIEDAWAYINTHEDARKFROMTHEWALLGOEASTNORTHEASTUNTILYOUREACHTHEOLDSTATIONNEARTHEBERLINCLOCKANDWAITFORTHEMAN")
        pt = list(base[:97])
        for i, ch in KN.items(): pt[i] = ch
        P = 31; keyw = [rnd.randrange(26) for _ in range(P)]
        ct = "".join(enc(pt[i], keyw[i % P], KA, "vig") for i in range(97))
        print("planted PT:", "".join(pt)); print("planted CT:", ct, "(KA vig, P=31 random key)")
        print("\n".join(run(ct, "control")[:6]))
        # null: shuffled K4
        for s in range(3):
            l = list(kryptos_text.K4); random.Random(s).shuffle(l)
            print(run("".join(l), f"null shuffle {s}")[0])
    else:
        print("\n".join(run(kryptos_text.K4, "K4")))
