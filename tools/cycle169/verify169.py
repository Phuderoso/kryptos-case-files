"""Cycle 169 independent checks (no bitsets).
 verify CARVED perms.bin texts.txt bookrk1e.out [quadgrams.json] : rebuild the 97-letter decryption of every FULL / FIT23
     line by string operations, count crib letters (must be 24 / 23), print the plaintext and its quadgram score.
 depth CARVED perms.bin texts.txt NSAMPLE SEED : numpy recount of bookrk1e's masked strict depth and one-error depth1
     histograms (24 additive modes) on a random sample of permutations; writes depth_sample.bin for the C run.
"""
import sys, json, math, numpy as np
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CR = [(21 + i, c) for i, c in enumerate("EASTNORTHEAST")] + [(63 + i, c) for i, c in enumerate("BERLINCLOCK")]
def dec(c, k, md):
    ty, ap, ac, ak = md % 3, (md // 3) & 1, (md // 6) & 1, (md // 12) & 1
    kv = KA.index(k) if ak else ord(k) - 65; cv = KA.index(c) if ac else ord(c) - 65
    pv = (cv - kv) % 26 if ty == 0 else (kv - cv) % 26 if ty == 1 else (cv + kv) % 26
    return KA[pv] if ap else AZ[pv]
def keyreq(c, p, md):
    for k in AZ:
        if dec(c, k, md) == p: return k
car, pf, tf = sys.argv[2], sys.argv[3], sys.argv[4]
P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97); T = dict(l.split() for l in open(tf))
if sys.argv[1] == "verify":
    Q = json.load(open(sys.argv[6])) if len(sys.argv) > 6 else None
    def qs(s):   # mean log10 quadgram (case 19 table: {"floor": f, "q": {QUAD: logp}})
        if not Q: return float("nan")
        return sum(Q["q"].get(s[i:i+4], Q["floor"]) for i in range(len(s) - 3)) / (len(s) - 3)
    for l in open(sys.argv[5]):
        if not (l.startswith("FULL") or l.startswith("FIT23")): continue
        d = dict(x.split("=") for x in l.split()[1:]); perm = P[int(d["perm"])]; md = int(d["mode"]); o = int(d["offset"])
        t = T[d["text"]]
        if md >= 24: print("XOR mode, not rebuilt:", l.strip()); continue
        if d["model"] == "A": pt = "".join(dec(car[perm[i]], t[o + i], md) for i in range(97))
        else:
            pt = [None]*97
            for x in range(97): pt[perm[x]] = dec(car[x], t[o + x], md)
            pt = "".join(pt)
        hits = sum(pt[i] == c for i, c in CR); miss = [j for j, (i, c) in enumerate(CR) if pt[i] != c]
        print(f"{hits}/24 miss={miss} q={qs(pt):.3f}", l.strip(), pt)
else:
    rng = np.random.default_rng(int(sys.argv[6])); idx = rng.choice(P.shape[0], int(sys.argv[5]), replace=False); idx.sort()
    P[idx].tofile("depth_sample.bin"); hS, h1 = {}, {}
    for name, t in T.items():
        nofs = len(t) - 96
        if nofs <= 0: continue
        arr = np.frombuffer(t.encode() + b"\0" * 200, dtype=np.uint8)
        for p in idx:
            perm = P[p]; inv = np.argsort(perm)
            for m in "AB":
                for md in range(24):
                    miss = np.zeros(nofs, np.int8); d0 = 0; d1 = 0; alive0 = True
                    for j, (i, c) in enumerate(CR):
                        q = i if m == "A" else inv[i]; ci = car[perm[i]] if m == "A" else car[inv[i]]
                        k = ord(keyreq(ci, c, md)); miss += (arr[q:q + nofs] != k)
                        if alive0 and (miss == 0).any(): d0 = j + 1
                        else: alive0 = False
                        if (miss <= 1).any(): d1 = j + 1
                        else: break
                    hS[d0] = hS.get(d0, 0) + 1; h1[d1] = h1.get(d1, 0) + 1
    print("PYDEPTH additive-only histS:", " ".join(f"{k}:{hS[k]}" for k in sorted(hS)), "hist1:", " ".join(f"{k}:{h1[k]}" for k in sorted(h1)))
