"""Cycle 9: creative-but-concrete layered hypotheses for K4, each an exact 24-crib gate plus a planted control.
Insight-first families (see case-file/07): Gromark / base change (Bean 2021; Scheidt 'change the language base'),
W-as-separator (W at 21 and 75 bracket the cribs), Berlin-clock arithmetic, K1-K3-derived running keys, K3-style
grids after making 97 composite (98 = 7x14 with the '?').
Run: python3 tools/k4_creative.py            -> analysis/k4_creative_report.txt
     python3 tools/k4_creative.py control    -> analysis/k4_creative_control.txt"""
import sys, random, itertools
import numpy as np
sys.path.insert(0, "tools")
from kryptos_text import K1, K2, K3, K4
from k4_anneal import AZ, KA, KN
from solve_k1_k2_k3 import vig_dec, k3_dec
from k4_layers import keyed, rot_dec, as_perm
N = 97
CRIBS = sorted(KN.items())
CI = np.array([i for i, _ in CRIBS])
ALPH = {"AZ": AZ, "KA": KA, "PALIMPSEST": keyed("PALIMPSEST"), "ABSCISSA": keyed("ABSCISSA"), "BERLINCLOCK": keyed("BERLINCLOCK")}
P1, P2, P3 = vig_dec(K1, "PALIMPSEST"), vig_dec(K2.replace("?", ""), "ABSCISSA"), k3_dec(K3.replace("?", ""))
W_POS = [i for i, c in enumerate(K4) if c == "W"]

def need(CT, pa, ca, mode, idx=None):
    """key value k required at each crib so that  c = CA[(PA.index(p) + k)]  (vig)  /  c = CA[(k - PA.index(p))] (beau)."""
    idx = CI if idx is None else idx
    out = []
    for (i, p), j in zip(CRIBS, idx):
        c = ca.index(CT[j]); q = pa.index(p)
        out.append((c - q) % 26 if mode == "vig" else (c + q) % 26)
    return np.array(out)
def enc(pt, key, pa, ca, mode):
    return "".join(ca[(pa.index(p) + k) % 26] if mode == "vig" else ca[(k - pa.index(p)) % 26] for p, k in zip(pt, key))
def pairs(full=False):
    names = list(ALPH) if full else ["AZ", "KA"]
    for a in names:
        for b in names:
            for mode in ("vig", "beau"):
                yield a, b, mode
def periodic_ok(req, kidx, P, minc=6):
    key = {}; n = 0
    for k, e in zip(kidx, req):
        if k % P in key:
            n += 1
            if key[k % P] != e: return False
        else: key[k % P] = e
    return n >= minc

# ---------- families ----------
def gromark_keys(b, L, n=N):
    prim = np.array(list(itertools.product(range(b), repeat=L)), dtype=np.int16)
    K = np.zeros((len(prim), n), dtype=np.int16); K[:, :L] = prim
    for t in range(L, n): K[:, t] = (K[:, t - L] + K[:, t - L + 1]) % b
    return prim, K
def H_gromark(CT, bases, Ls, full=True, label="Gromark"):
    tests = 0; surv = []
    for b in bases:
        for L in Ls:
            if b ** L > 2_000_000: continue
            prim, K = gromark_keys(b, L); KC = K[:, CI]
            for pa, ca, mode in pairs(full):
                for off in range(26):     # cipher-alphabet slide (Gromark writes CA under PA at some offset)
                    req = (need(CT, ALPH[pa], ALPH[ca], mode) - off) % 26
                    tests += len(prim)
                    if req.max() >= b: continue
                    hit = np.where((KC == req).all(axis=1))[0]
                    for h in hit: surv.append((label, b, L, pa, ca, mode, off, "".join(map(str, prim[h]))))
    return tests, surv
def segments():
    segs = []; s = 0
    for w in W_POS + [N]:
        segs.append(list(range(s, w))); s = w + 1
    return segs
def H_wrestart(CT):
    """W = unenciphered separator; keyword restarts after every W (any length 1-26): key index = offset in segment."""
    tests = 0; surv = []; off = {}
    for seg in segments():
        for k, i in enumerate(seg): off[i] = k
    kidx = [off[i] for i, _ in CRIBS]
    for pa, ca, mode in pairs(True):
        req = need(CT, ALPH[pa], ALPH[ca], mode)
        for P in range(1, 27):
            tests += 1
            if periodic_ok(req, kidx, P, minc=6): surv.append(("W-restart", pa, ca, mode, P))
        # progressive inside segment: k = a + s*offset
        for s in range(26):
            tests += 1
            a = {(e - s * k) % 26 for e, k in zip(req, kidx)}
            if len(a) == 1: surv.append(("W-restart-progressive", pa, ca, mode, s, a.pop()))
    return tests, surv
def H_wnull(CT):
    """W = nulls: delete them, renumber, then periodic P1-26 and Gromark b<=10 on the 92 remaining letters."""
    keep = [i for i in range(N) if i not in W_POS]; newpos = {i: j for j, i in enumerate(keep)}
    kidx = np.array([newpos[i] for i, _ in CRIBS])
    tests = 0; surv = []
    for pa, ca, mode in pairs(True):
        req = need(CT, ALPH[pa], ALPH[ca], mode)
        for P in range(1, 27):
            tests += 1
            if periodic_ok(req, kidx, P): surv.append(("W-null periodic", pa, ca, mode, P))
    for b in (5, 10):
        prim, K = gromark_keys(b, 5, 92); KC = K[:, kidx]
        for pa, ca, mode in pairs(False):
            for off in range(26):
                req = (need(CT, ALPH[pa], ALPH[ca], mode) - off) % 26; tests += len(prim)
                if req.max() < b:
                    for h in np.where((KC == req).all(axis=1))[0]: surv.append(("W-null Gromark", b, pa, ca, mode, off, prim[h].tolist()))
    return tests, surv
def H_wcaesar(CT):
    """each W-delimited segment has its own single shift: all crib letters in a segment must agree."""
    seg_of = {i: s for s, seg in enumerate(segments()) for i in seg}
    tests = 0; surv = []
    for pa, ca, mode in pairs(True):
        req = need(CT, ALPH[pa], ALPH[ca], mode); tests += 1; d = {}
        ok = all(d.setdefault(seg_of[i], e) == e for (i, _), e in zip(CRIBS, req))
        if ok: surv.append(("W-segment Caesar", pa, ca, mode, d))
    return tests, surv
def H_progressive(CT):
    """k_i = a + s*i  and stepped  k_i = a + s*floor(i/m)  (clock hand advancing every m letters), m = 2..24."""
    tests = 0; surv = []
    for pa, ca, mode in pairs(True):
        req = need(CT, ALPH[pa], ALPH[ca], mode)
        for m in range(1, 25):
            for s in range(1, 26):
                tests += 1
                a = {(e - s * (i // m)) % 26 for (i, _), e in zip(CRIBS, req)}
                if len(a) == 1: surv.append(("progressive", pa, ca, mode, m, s, a.pop()))
    return tests, surv
def berlin_lamps(t):
    """Mengenlehreuhr: lit lamps at minute-of-day t (seconds lamp ignored): h//5 + h%5 + m//5 + m%5."""
    h, m = divmod(t % 1440, 60); return h // 5 + h % 5 + m // 5 + m % 5
def H_berlin(CT):
    """key_i = mult*lamps(t0 + step*i) + a, t0 = every minute of the day, step in {1,5,15,60}; also row-by-row lamp
    digits (h//5, h%5, m//5, m%5) of a fixed time t0 as a period-4 key -> already excluded by periodic (cycle 1)."""
    tests = 0; surv = []
    L = np.array([berlin_lamps(t) for t in range(1440 * 2)])
    for pa, ca, mode in pairs(False):
        req = need(CT, ALPH[pa], ALPH[ca], mode)
        for step in (1, 5, 15, 60):
            T = (np.arange(1440)[:, None] + step * CI[None, :]) % 1440
            lam = L[T]
            for mult in range(1, 26):
                diff = (req[None, :] - mult * lam) % 26
                tests += 1440
                ok = np.where((diff == diff[:, :1]).all(axis=1))[0]
                for t0 in ok: surv.append(("Berlin lamps", pa, ca, mode, step, mult, int(t0), int(diff[t0, 0])))
    return tests, surv
def H_running(CT):
    """running key from plain-sight texts: K1/K2/K3 plaintexts, K1-K3 ciphertexts, the KA tableau rows, forward and reversed."""
    tab = "".join(KA[r:] + KA[:r] for r in range(26))
    srcs = {"P1": P1, "P2": P2, "P3": P3, "P123": P1 + P2 + P3, "C123": (K1 + K2 + K3).replace("?", ""), "tableau": tab}
    srcs.update({k + "_rev": v[::-1] for k, v in list(srcs.items())})
    tests = 0; surv = []
    for pa, ca, mode in pairs(True):
        req = need(CT, ALPH[pa], ALPH[ca], mode)
        for an in ("AZ", "KA"):
            for name, s in srcs.items():
                for o in range(len(s) - N + 1):
                    tests += 1
                    if all(ALPH[an].index(s[o + i]) == e for (i, _), e in zip(CRIBS, req)):
                        surv.append(("running", pa, ca, mode, an, name, o))
    return tests, surv
def H_selfkey(CT):
    """ciphertext feedback with lag d: p_i = CT_i - CT_{i-d} (- a)  (cipher autokey generalised; d = 1..30)."""
    tests = 0; surv = []
    for an in ("AZ", "KA"):
        A = ALPH[an]
        for d in range(1, 31):
            for a in range(26):
                for sgn in (1, -1):
                    tests += 1
                    if all(i - d >= 0 and (A.index(CT[i]) - sgn * A.index(CT[i - d]) - a) % 26 == A.index(p) for i, p in CRIBS):
                        surv.append(("self-key", an, d, a, sgn))
    return tests, surv
def grid98():
    """K3 insight on K4: make 97 composite by keeping the '?' that precedes OBKR -> 98 = 7x14 = 14x7 = 2x49.
    K3 itself = rot_dec(rot_dec(ct,24),8) on 336 = 24x14 = 8x42. Try all ordered width pairs from divisors of 98."""
    ws = [2, 7, 14, 49]
    for w1 in ws:
        for w2 in ws + [None]:
            def f(s, w1=w1, w2=w2):
                t = rot_dec(s, w1)
                return rot_dec(t, w2) if w2 else t
            yield (w1, w2), f
def H_grid98(CT):
    tests = 0; surv = []
    for (w1, w2), f in grid98():
        for qpos in ("front", "back"):
            s = ("?" + CT) if qpos == "front" else (CT + "?")
            idx = list(range(98)); src = [s[i] for i in idx]
            tagged = f("".join(chr(0x100 + i) for i in range(98)))   # track positions through the rotation
            order = [ord(ch) - 0x100 for ch in tagged]               # PT position k <- source position order[k]
            sh = 1 if qpos == "front" else 0
            ptq = [k for k, o in enumerate(order) if o == (0 if qpos == "front" else 97)][0]
            pt_from_ct = [order[k] - sh for k in range(98) if k != ptq]  # drop the '?' in PT order
            for pa, ca, mode in pairs(False):
                req = []
                for i, p in CRIBS:
                    j = pt_from_ct[i]; c = ALPH[ca].index(CT[j]); q = ALPH[pa].index(p)
                    req.append((c - q) % 26 if mode == "vig" else (c + q) % 26)
                for model, kidx in (("sub_first", [i for i, _ in CRIBS]), ("sub_last", [pt_from_ct[i] for i, _ in CRIBS])):
                    for P in range(1, 27):
                        tests += 1
                        if periodic_ok(req, kidx, P): surv.append(("98-grid", qpos, w1, w2, pa, ca, mode, model, P))
    return tests, surv

FAMILIES = [
    ("H1 Gromark base 10, primer 5 (Hall/ACA; Bean 2021), 5 alphabets x 5 x 26 slides", lambda CT: H_gromark(CT, [10], [5])),
    ("H2 Gromark base 5 (Berlin-clock base) and bases 2-9, primers 2-6", lambda CT: H_gromark(CT, range(2, 10), range(2, 7), full=False, label="Gromark-b")),
    ("H3 Gromark base 10, primers 2-4 and 6 (lag variants)", lambda CT: H_gromark(CT, [10], [2, 3, 4, 6], full=False, label="Gromark-L")),
    ("H4 W = separator, keyword restarts at each W (any length) / progressive per segment", H_wrestart),
    ("H5 W = nulls removed, then periodic P1-26 or Gromark b5/b10", H_wnull),
    ("H6 W-delimited segments each a single shift", H_wcaesar),
    ("H7 progressive / stepped ('clock hand') key a + s*floor(i/m)", H_progressive),
    ("H8 Mengenlehreuhr lamp-count key from any start minute", H_berlin),
    ("H9 running key from K1/K2/K3 plaintexts, ciphertexts, tableau (+reversed)", H_running),
    ("H10 ciphertext-feedback (lagged self-key) d=1..30", H_selfkey),
    ("H11 '?'+K4 = 98 = 7x14: K3-style rotations then periodic sub", H_grid98),
]
def plant(rng):
    """planted controls: one member of several families, English text with the cribs, run through the matching family."""
    eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"
    pt = list(eng[:N])
    for i, ch in KN.items(): pt[i] = ch
    pt = "".join(pt); out = []
    _, K = gromark_keys(10, 5); key = (K[31415] + 3) % 26
    out.append(("H1 planted primer 31415 AZ->KA vig slide 3", enc(pt, key, AZ, KA, "vig"), FAMILIES[0][1]))
    _, K = gromark_keys(5, 5); key = K[1234] % 26
    out.append(("H2 planted base5 primer idx1234 KA->KA beau", enc(pt, key, KA, KA, "beau"), FAMILIES[1][1]))
    off = {}
    for seg in segments():
        for k, i in enumerate(seg): off[i] = k
    kw = [KA.index(c) for c in "SHADOWFORCES"]
    key = [kw[off[i] % 12] if i in off else 0 for i in range(N)]
    ct = list(enc(pt, key, KA, KA, "vig"))
    for w in W_POS: ct[w] = "W"
    out.append(("H4 planted W-restart KA vig SHADOWFORCES (12)", "".join(ct), FAMILIES[3][1]))
    key = [7 * berlin_lamps(600 + 5 * i) + 4 for i in range(N)]
    out.append(("H8 planted lamps t0=600 step5 mult7 a4 AZ vig", enc(pt, key, AZ, AZ, "vig"), FAMILIES[7][1]))
    key = [KA.index(P3[200 + i]) for i in range(N)]
    out.append(("H9 planted running key P3@200 KA", enc(pt, key, AZ, KA, "beau"), FAMILIES[8][1]))
    # H11: build CT such that '?'+CT rotated (7,14) gives PT-with-'?', then periodic KA vig ABSCISSA (sub_first)
    for (w1, w2), f in grid98():
        if (w1, w2) == (7, 14): break
    tagged = f("".join(chr(0x100 + i) for i in range(98))); order = [ord(c) - 0x100 for c in tagged]
    kw = [KA.index(c) for c in "ABSCISSA"]
    X = enc(pt, [kw[i % 8] for i in range(N)], KA, KA, "vig")
    ptq = order.index(0); full = [None] * 98; it = iter(X)
    for k in range(98):
        full[order[k]] = "?" if k == ptq else next(it)
    out.append(("H11 planted '?'front rot(7,14) + KA vig ABSCISSA sub_first", "".join(full[1:]), FAMILIES[10][1]))
    return out
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "control":
        for name, ct, fam in plant(random.Random(9)):
            t, s = fam(ct); print(f"{name}: tests {t}, survivors {len(s)}: {s[:4]}")
    else:
        print(f"W positions (1-indexed): {[w + 1 for w in W_POS]}; segment lengths {[len(s) for s in segments()]}")
        tot = 0
        for name, fam in FAMILIES:
            t, s = fam(K4); tot += t
            print(f"{name}: tests {t:,}; survivors {len(s)}"); [print("   ", x) for x in s[:20]]
        print(f"TOTAL tests {tot:,}")
