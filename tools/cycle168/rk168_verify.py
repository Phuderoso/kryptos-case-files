"""Cycle 168 independent recount. (1) verify: for every FULL line of bookrk output, rebuild the whole 97-letter
decryption by string operations (no bitsets) and count crib letters; print the plaintext. (2) depth: recompute
bookrk's prefix depth histogram with numpy for a sample of permutations (exact same 24 constraint order).
usage: rk168_verify.py verify CARVED perms.bin texts.txt bookrk.out    |   depth CARVED perms.bin texts.txt NSAMPLE [tail]
(tail: mimic bookrk, whose depth histogram also counts offsets in the last bitset word beyond len-97; FULL hits are
masked to real offsets, so only the depth diagnostics differ)"""
import sys, numpy as np
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
    for l in open(sys.argv[5]):
        if not l.startswith("FULL"): continue
        d = dict(x.split("=") for x in l.split()[1:]); perm = P[int(d["perm"])]; md = int(d["mode"]); o = int(d["offset"])
        t = T[d["text"]]
        if md >= 24: print("XOR mode, skipped", l.strip()); continue
        if d["model"] == "A": pt = "".join(dec(car[perm[i]], t[o + i], md) for i in range(97))
        else:
            pt = [None]*97
            for x in range(97): pt[perm[x]] = dec(car[x], t[o + x], md)
            pt = "".join(pt)
        hits = sum(pt[i] == c for i, c in CR); print(f"{hits}/24", l.strip(), pt)
else:
    TAIL = len(sys.argv) > 6 and sys.argv[6] == "tail"
    rng = np.random.default_rng(168); idx = rng.choice(P.shape[0], int(sys.argv[5]) if len(sys.argv) > 5 else 20, replace=False)
    idx.sort(); P[idx].tofile("depth_sample.bin"); hist = {}
    for name, t in T.items():
        nofs = len(t) - 96
        if TAIL: nofs = 64 * ((nofs + 63) // 64)          # bookrk's bitset words also hold tail offsets >= len-96
        arr = np.frombuffer(t.encode() + b"\0" * 200, dtype=np.uint8)
        for p in idx:
            perm = P[p]; inv = np.argsort(perm)
            for m in "AB":
                for md in range(24):
                    acc = np.ones(nofs, bool); depth = 0
                    for i, c in CR:
                        q = i if m == "A" else inv[i]; ci = car[perm[i]] if m == "A" else car[inv[i]]
                        k = ord(keyreq(ci, c, md)); acc &= arr[q:q + nofs] == k
                        if not acc.any(): break
                        depth += 1
                    hist[depth] = hist.get(depth, 0) + 1
    print("PYDEPTH additive-only hist:", " ".join(f"{k}:{hist[k]}" for k in sorted(hist)))
