"""Cycle 25: TWO carving anomalies applied directly to the carved K4 (no transposition).
Anomaly types: del (a true ciphertext letter missing from the copper), ins (an extra junk letter carved),
chg (a changed carved letter under a crib -> that crib is dropped). Every unordered pair of anomalies,
both crib conventions (cribs at official CARVED positions, or at official TRUE/plaintext positions).
Fixed tableaux: PA,CA in {AZ,KA}; Vigenere-type (C=P+K, also covers variant Beaufort) and Beaufort (C=K-P).
Periods 1-26. Exact crib consistency; consistent configs decoded and quadgram-scored.
Usage: python3 two_anomaly_direct.py [K4|null:SEED|control:SEED] [Pmax]"""
import sys, random, json, os, itertools, time
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CR = [(21+i, c) for i, c in enumerate("EASTNORTHEAST")] + [(63+i, c) for i, c in enumerate("BERLINCLOCK")]
Q = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "quadgrams.json"))); FL = Q["floor"]; QQ = Q["q"]
def score(s):
    v = [QQ.get(s[i:i+4], FL) for i in range(len(s)-3) if "?" not in s[i:i+4]]; return sum(v)/max(len(v), 1)
def carved_map(dels, inss, ncarved=97):
    """dels: true indices missing from copper; inss: carved positions holding junk. Returns list carved->true idx|None."""
    N = ncarved + len(dels) - len(inss)
    tr = [t for t in range(N) if t not in dels]
    out = []; it = iter(tr)
    for c in range(ncarved): out.append(None if c in inss else next(it))
    return out
def edits():
    E = [("del", d) for d in range(99)] + [("ins", d) for d in range(97)] + [("chg", n) for n in range(24)]
    for a, b in itertools.combinations(E, 2):
        if a[0] == "chg" and b[0] == "chg": pass
        yield (a, b)
def patterns():
    pats = {}
    for a, b in edits():
        dels = {x[1] for x in (a, b) if x[0] == "del"}; inss = {x[1] for x in (a, b) if x[0] == "ins"}
        chg = {x[1] for x in (a, b) if x[0] == "chg"}
        if len(dels) + len(inss) + len(chg) < 2: continue
        try: cm = carved_map(dels, inss)
        except StopIteration: continue
        inv = {t: c for c, t in enumerate(cm) if t is not None}
        tag = f"{a[0]}{a[1]}+{b[0]}{b[1]}"
        # carved convention
        L = tuple((c, p, cm[c]) for n, (c, p) in enumerate(CR) if n not in chg and cm[c] is not None)
        pats.setdefault(L, (tag + " carved", cm))
        # true/plain convention
        L = tuple((inv[j], p, j) for n, (j, p) in enumerate(CR) if n not in chg and j in inv)
        pats.setdefault(L, (tag + " plain", cm))
    return pats
def run(CT, Pmax=26, top=8):
    pats = patterns(); hist = {}; best = []
    TABS = [(PA, CA, m) for PA in (AZ, KA) for CA in (AZ, KA) for m in ("vig", "beau")]
    for lst, (tag, cm) in pats.items():
        for PA, CA, mode in TABS:
            kv = [((CA.index(CT[i]) + PA.index(p)) if mode == "beau" else (CA.index(CT[i]) - PA.index(p))) % 26 for i, p, _ in lst]
            ks = [k for _, _, k in lst]
            for P in range(1, Pmax+1):
                key = [None]*P; ok = True
                for k, v in zip(ks, kv):
                    r = k % P
                    if key[r] is None: key[r] = v
                    elif key[r] != v: ok = False; break
                if not ok: continue
                hist[P] = hist.get(P, 0) + 1
                s = []
                for c, t in enumerate(cm):
                    if t is None or key[t % P] is None: s.append("?"); continue
                    cv = CA.index(CT[c]); kk = key[t % P]
                    s.append(PA[(kk - cv) % 26 if mode == "beau" else (cv - kk) % 26])
                s = "".join(s); known = sum(ch != "?" for ch in s)
                best.append((score(s), P, known, tag, "KA" if PA == KA else "AZ", "KA" if CA == KA else "AZ", mode, s))
    best.sort(reverse=True)
    print("patterns:", len(pats), " consistent configs per period:", dict(sorted(hist.items())))
    full = [b for b in best if b[2] >= 90]
    print("best with >=90 letters determined:")
    for b in full[:top]: print("  %.3f P=%d known=%d %s PA=%s CA=%s %s %s" % b)
    print("best overall:")
    for b in best[:top]: print("  %.3f P=%d known=%d %s PA=%s CA=%s %s %s" % b)
    return hist, best
def control(seed):
    r = random.Random(seed); P = r.choice([7, 8, 10, 11, 13]); key = [r.randrange(26) for _ in range(P)]
    PA, CA, mode = r.choice([(KA, KA, "vig"), (AZ, KA, "beau"), (KA, AZ, "vig")])
    full = "SLOWLYTHEREMAINSOFTHEEASTNORTHEASTPASSAGEWEREREMOVEDANDIHEARDTHXBERLINCLOCKSTRIKEATDUSKWHILEWEWAITEDXXYZ"
    # pick a del and an ins (carved convention): true text length 98, one true letter missing, one junk carved
    d = r.randrange(40, 60); ins = r.randrange(75, 95)
    cm = carved_map({d}, {ins})
    # carved convention: plaintext letter for true index t chosen so cribs land at carved positions
    pt = {}
    filler = iter(full)
    for c, t in enumerate(cm):
        if t is None: continue
        pt[t] = None
    for c, p in CR: pt[cm[c]] = p
    for t in sorted(pt):
        if pt[t] is None: pt[t] = r.choice(AZ)
    pt[d] = r.choice(AZ)
    def enc(t):
        k = key[t % P]; pv = PA.index(pt[t])
        return CA[(k - pv) % 26] if mode == "beau" else CA[(pv + k) % 26]
    CT = "".join(r.choice(AZ) if t is None else enc(t) for t in cm)
    print(f"CONTROL seed={seed}: P={P} PA={'KA' if PA==KA else 'AZ'} CA={'KA' if CA==KA else 'AZ'} {mode}, true idx {d} dropped, junk at carved {ins}")
    return CT
if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "K4"; Pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    if a == "K4": CT = K4
    elif a.startswith("null:"):
        l = list(K4); random.Random(int(a[5:])).shuffle(l); CT = "".join(l)
    else: CT = control(int(a.split(":")[1]))
    t = time.time(); run(CT, Pmax); print(f"time {time.time()-t:.0f}s")
