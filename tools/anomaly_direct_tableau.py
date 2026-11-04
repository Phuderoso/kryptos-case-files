"""Cycle 24: one-letter anomaly applied DIRECTLY to the carved text (no transposition), fixed AZ/KA tableaux
(Vigenere/variant and Beaufort, PA,CA in {AZ,KA}), periods 1-48, every anomaly pattern of anomaly_sat.patterns()
in both crib conventions. Exact crib consistency; consistent configs decoded (unknown residues '?') and quadgram-scored.
Usage: python3 direct_tableau.py [K4|null:SEED]"""
import sys, random, json
import anomaly_sat as S
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
q = json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "quadgrams.json"))); FL = q["floor"]; Q = q["q"]
def score(s):
    v = [Q.get(s[i:i+4], FL) for i in range(len(s)-3) if "?" not in s[i:i+4]]; return sum(v)/max(len(v), 1), len(v)
def decode(CT, tag, PA, CA, mode, key, P):
    # rebuild the carved->key-index map for the whole text from the tag
    kind, rest = tag.split(" ", 1) if " " in tag else (tag, "")
    d = int(rest.split("=")[1]) if "d=" in rest else None
    out = []
    for i, c in enumerate(CT):
        if kind == "del-carved": k = i + (i >= d)
        elif kind == "ins-carved":
            if i == d: continue
            k = i - (i > d)
        elif kind == "del-plain": k = i + (i >= d)      # plaintext j paired with carved j-[j>d]
        elif kind == "ins-plain":
            if i == d: continue
            k = i - (i > d)
        else: k = i
        kv = key[k % P]
        if kv is None: out.append("?"); continue
        cv = CA.index(c); pv = (kv - cv) % 26 if mode == "beau" else (cv - kv) % 26; out.append(PA[pv])
    return "".join(out)
def run(CT, Pmax=48):
    pats = S.patterns(); hist = {}; best = []
    for lst, tag in pats.items():
        for PA in (AZ, KA):
            for CA in (AZ, KA):
                for mode in ("vig", "beau"):
                    kv = [((CA.index(CT[i]) + PA.index(p)) if mode == "beau" else (CA.index(CT[i]) - PA.index(p))) % 26 for i, p, _ in lst]
                    for P in range(1, Pmax+1):
                        key = [None]*P; ok = True
                        for (i, p, k), v in zip(lst, kv):
                            r = k % P
                            if key[r] is None: key[r] = v
                            elif key[r] != v: ok = False; break
                        if not ok: continue
                        hist[P] = hist.get(P, 0) + 1
                        cand = [(score(s)[0], tg, s) for tg in S.ALLTAGS[lst] for s in [decode(CT, tg, PA, CA, mode, key, P)]]
                        sc, tg, s = max(cand)
                        best.append((sc, P, tg, "KA" if PA == KA else "AZ", "KA" if CA == KA else "AZ", mode, s))
    best.sort(reverse=True)
    print("consistent configs per period:", dict(sorted(hist.items())))
    for b in best[:5]: print("  %.2f P=%d %s PA=%s CA=%s %s %s" % b)
    return hist, best
if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "K4"
    if a == "K4": CT = K4
    elif a.startswith("null:"):
        l = list(K4); random.Random(int(a[5:])).shuffle(l); CT = "".join(l)
    else:  # control: KA Quagmire III, key period 29 random letters, letter dropped at true index 50, carved convention
        r = random.Random(29); P = 29; key = [r.randrange(26) for _ in range(P)]
        full = ("SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTHX" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAIT")
        tru = "".join(KA[(KA.index(ch) + key[j % P]) % 26] for j, ch in enumerate(full)); CT = tru[:50] + tru[51:]
        print("CONTROL: KA Quagmire III, random period-29 key, true index 50 dropped (carved convention)")
    print("TEXT", a); run(CT)
