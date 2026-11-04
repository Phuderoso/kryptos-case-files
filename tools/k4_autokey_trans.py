"""Cycle 19: exact algebraic test of AUTOKEY (ciphertext- and plaintext-fed) behind transpositions.
Model A: substitute (autokey) then transpose.  Model B: transpose then substitute.
Tableaux: KRYPTOS-keyed (KA) and straight (AZ); Vigenere, Beaufort, variant Beaufort.
Transpositions: all column orders w=2..8, K3-style single/double rotations (widths 2..49, 4 column reads),
plus inverses; 97 letters, and 98 symbols with the '?' (model A).
Usage: python3 k4_autokey_trans.py [K4|null:SEED|control:SEED]"""
import sys, itertools, random, numpy as np
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB = {21+i: c for i, c in enumerate("EASTNORTHEAST")}
CRIB.update({63+i: c for i, c in enumerate("BERLINCLOCK")})
CPOS = np.array(sorted(CRIB)); 
def cols(n, w, order, up=False):
    out = []
    for c in order:
        col = list(range(c, n, w))
        out += col[::-1] if up else col
    return out
def family(n):
    seen = set(); fam = []
    def add(p, tag):
        t = tuple(p)
        if t in seen: return
        seen.add(t); fam.append((np.array(p, dtype=np.int16), tag))
        inv = [0]*n
        for k, v in enumerate(p): inv[v] = k
        ti = tuple(inv)
        if ti not in seen: seen.add(ti); fam.append((np.array(inv, dtype=np.int16), tag+"^-1"))
    for w in range(2, 9):
        for o in itertools.permutations(range(w)):
            add(cols(n, w, o), f"col{w}{''.join(map(str,o))}")
    rot = {}
    for w in range(2, 50):
        for up in (0, 1):
            for rev in (0, 1):
                o = list(range(w))[::-1] if rev else list(range(w))
                rot[(w, up, rev)] = cols(n, w, o, bool(up))
    for k, p in rot.items(): add(p, f"rot{k}")
    rl = list(rot.items())
    for (k1, p1), (k2, p2) in itertools.product(rl, rl):
        add([p1[i] for i in p2], f"rot{k1}+{k2}")
    return fam
def idxs(s, A): return np.array([A.index(c) if c in A else -1 for c in s], dtype=np.int16)
def run(text, verbose=True):
    hits = []; best = {}
    for nlen in (97, 98):
        carved = ("?" + text) if nlen == 98 else text
        fam = family(nlen)
        P = np.stack([f[0] for f in fam]); tags = [f[1] for f in fam]
        for an, A in (("KA", KA), ("AZ", AZ)):
            cv = idxs(carved, A)
            crib = np.array([A.index(CRIB[i]) for i in CPOS], dtype=np.int16)
            # ---- Model A: C = carved[P]; strip '?' which must sit at an end
            CA = cv[P]
            if nlen == 98:
                qpos = (CA == -1).argmax(1)
                C97 = np.where((qpos == 0)[:, None], CA[:, 1:], CA[:, :97])
                okq = (qpos == 0) | (qpos == 97)
            else:
                C97 = CA; okq = np.ones(len(P), bool)
            invP = np.argsort(P, 1)
            # ---- Model B (97 only): plaintext crib i sits at carved position invP[i]
            for L in range(1, 22):
                for mode in ("vig", "beau", "var"):
                    for feed in ("CT", "PT"):
                        # Model A
                        c = C97[:, CPOS]; cprev = C97[:, CPOS - L]
                        if feed == "CT":
                            if mode == "vig": p = (c - cprev) % 26
                            elif mode == "beau": p = (cprev - c) % 26
                            else: p = (c + cprev) % 26
                            match = (p == crib); chk = np.ones_like(match)
                        else:  # PT autokey: need P[i-L] known (in crib)
                            prevknown = np.array([(i - L) in CRIB for i in CPOS])
                            pprev = np.array([A.index(CRIB[i - L]) if (i - L) in CRIB else 0 for i in CPOS])
                            if mode == "vig": pc = (crib + pprev) % 26
                            elif mode == "beau": pc = (pprev - crib) % 26
                            else: pc = (crib - pprev) % 26
                            match = (c == pc) & prevknown; chk = np.broadcast_to(prevknown, match.shape)
                        m = match.sum(1); k = chk.sum(1)
                        m = np.where(okq, m, -1)
                        key = ("A", nlen, feed)
                        best[key] = max(best.get(key, 0), int(m.max()))
                        for j in np.nonzero((m == k) & (k >= (12 if feed == "CT" else 6)) & okq)[0]:
                            hits.append(("A", nlen, an, mode, feed, L, tags[j], int(k[j])))
                        # Model B
                        if nlen == 97 and feed == "CT":
                            pos = invP[:, CPOS]; ok = pos >= L
                            cc = cv[pos]; cp = cv[np.maximum(pos - L, 0)]
                            if mode == "vig": p = (cc - cp) % 26
                            elif mode == "beau": p = (cp - cc) % 26
                            else: p = (cc + cp) % 26
                            mm = ((p == crib) & ok).sum(1); kk = ok.sum(1)
                            best[("B", 97, "CT")] = max(best.get(("B", 97, "CT"), 0), int(mm.max()))
                            for j in np.nonzero((mm == kk) & (kk >= 12))[0]:
                                hits.append(("B", 97, an, mode, "CT", L, tags[j], int(kk[j])))
        if verbose: print(f"n={nlen}: {len(fam)} transpositions", flush=True)
    return hits, best
def encrypt_control(seed):
    rnd = random.Random(seed)
    pt = "SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTH" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAIT"
    assert len(pt) == 97
    fam = family(97); perm, tag = rnd.choice(fam)
    A = rnd.choice([KA, AZ]); mode = rnd.choice(["vig", "beau", "var"]); L = rnd.randint(1, 21)
    feed = "PT" if seed >= 100 else "CT"
    model = "A" if feed == "PT" else rnd.choice("AB")
    if feed == "PT": L = rnd.randint(1, 12)
    def ak(src):
        out = []; prim = [rnd.randrange(26) for _ in range(L)]
        for i, ch in enumerate(src):
            p = A.index(ch); k = prim[i] if i < L else A.index((src if feed == 'PT' else out)[i - L])
            c = {"vig": p + k, "beau": k - p, "var": p - k}[mode] % 26; out.append(A[c])
        return "".join(out)
    if model == "A":
        C = ak(pt); carved = [None]*97
        for k, v in enumerate(perm): carved[k] = C[v]  # carved[k] = C[perm[k]] -> C = carved[invperm]... search covers inverses
        carved = "".join(carved)
    else:
        Pp = "".join(pt[v] for v in perm); carved = ak(Pp)
    return carved, (model, feed, tag, "KA" if A == KA else "AZ", mode, L)
if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "K4"
    if arg == "K4": text = K4; truth = None
    elif arg.startswith("null:"):
        r = random.Random(int(arg[5:])); l = list(K4); r.shuffle(l); text = "".join(l); truth = None
    else:
        text, truth = encrypt_control(int(arg[8:])); print("planted:", truth)
    hits, best = run(text)
    print("best partial matches:", {str(k): v for k, v in best.items()})
    print("full-consistency hits:", len(hits))
    for h in hits[:40]: print("  HIT", h)
