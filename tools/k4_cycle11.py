"""Cycle 11 (1)+(2).
(1) Scheidt 'change the base': keyword -> integer -> digits in base b (2..16) used as key:
    n_az = base-26 value (A=0..Z=25); n_a1 = decimal concatenation of A=1..Z=26; n_ka = base-26 value on KA indices.
    Uses: U1 digits repeated periodically; U2 first L=5 (and 4,6) digits as Gromark primer in base b.
    Each key is tested against the 24 cribs with BOTH alphabets unknown (union-find feasibility = exact necessary test
    over arbitrary PA/CA; survivors are re-checked exactly with the SAT model of k4_sat.py).
(2) multi-word key-phrase alphabets: every substring (len 4..30) of the K1/K2/K3 plaintexts + listed phrases, keyed on
    AZ and on KA, plus reverses. Tested as PA (CA from phrase set U 66k word alphabets) and as CA, for
    G: Gromark with Bean's 39 base-10 primer-5 feasible primers; Q: Quagmire-IV periodic key P=1..26 (key free).
Run: python3 tools/k4_cycle11.py [control]"""
import sys, json, random, numpy as np
sys.path.insert(0, "tools")
from kryptos_text import K4, KA
from k4_anneal import AZ, KN
from gromark_alphabet import feasible, keyed
import gromark_keyword as GK
N = 97; CR = sorted(KN.items()); CI = [i for i, _ in CR]
K123 = ["".join(ch for ch in l.split(": ", 1)[1] if ch.isalpha() and ch.isupper()) for l in open("analysis/k1_k3_decryptions.txt") if l.startswith(("K1:", "K2 (as", "K3:"))]
EXTRA = ["CANYOUSEEANYTHING", "YESWONDERFULTHINGS", "DELIVERINGAMESSAGE", "WHOKNOWSTHEEXACTLOCATION", "ONLYWW",
 "EASTNORTHEAST", "BERLINCLOCK", "WORLDCLOCK", "WELTZEITUHR", "MENGENLEHREUHR", "XLAYERTWO", "IDBYROWS", "LAYERTWO",
 "KRYPTOSPALIMPSEST", "KRYPTOSABSCISSA", "PALIMPSESTABSCISSA", "PALIMPSESTABSCISSAKRYPTOS", "JAMESSANBORN", "EDSCHEIDT",
 "WILLIAMWEBSTER", "CENTRALINTELLIGENCEAGENCY", "THEFALLOFTHEBERLINWALL", "BERLINWALL", "HOWARDCARTER", "TUTANKHAMUN",
 "VALLEYOFTHEKINGS", "MASKING", "CHANGETHEBASE", "SHADOWFORCES", "LUCIDMEMORY", "VIRTUALLYINVISIBLE", "DIGETAL",
 "INTERPRETATION", "UNDERGRUUND", "IQLUSION", "DESPARATLY", "LANGLEY", "THEPOINT", "NORTHEAST", "EGYPT", "CLOCK"]
def phrases():
    P = set(EXTRA)
    for t in K123:
        for a in range(len(t)):
            for L in range(4, 31):
                if a + L <= len(t): P.add(t[a:a + L])
    return P
def phrase_alphs():
    S = set()
    for p in phrases():
        for base in (AZ, KA):
            a = keyed(p, base); S.add(a); S.add(a[::-1])
    return sorted(S)
def posmat(alphs):
    M = np.zeros((len(alphs), 26), np.int16)
    for r, a in enumerate(alphs):
        for j, ch in enumerate(a): M[r, ord(ch) - 65] = j
    return M
def gromark(prim, b, n=N):
    k = list(prim)
    while len(k) < n: k.append((k[-len(prim)] + k[-len(prim) + 1]) % b)
    return k
def digits(n, b):
    d = []
    while n: d.append(n % b); n //= b
    return d[::-1] or [0]
def nums(w):
    return {"az": sum((ord(c) - 65) * 26 ** (len(w) - 1 - i) for i, c in enumerate(w)),
            "a1": int("".join(str(ord(c) - 64) for c in w)),
            "ka": sum(KA.index(c) * 26 ** (len(w) - 1 - i) for i, c in enumerate(w))}
def basechange(CT, words, log):
    tests = hits = 0; out = []
    for w in words:
        for nm, n in nums(w).items():
            for b in range(2, 17):
                d = digits(n, b)
                if len(d) < 3: continue
                cands = [("rep", [d[i % len(d)] for i in range(N)])]
                for L in (4, 5, 6):
                    if len(d) >= L: cands.append((f"grom{L}", gromark(d[:L], b)))
                for use, k in cands:
                    tests += 1
                    ok, _ = feasible(CT, [k[i] for i in CI])
                    if ok: hits += 1; out.append((w, nm, b, use, "".join(map(str, d[:12]))))
    log(f"(1) base-change keys: {len(words)} words x 3 numberings x bases 2..16 x uses -> {tests} key tests, {hits} feasible (arbitrary PA/CA)")
    for h in out[:60]: log("   feasible:", *h)
    return out
def alph_tests(CT, PH, ALL, primers, log, Ps=range(1, 27)):
    """exact hash-join: Gromark needs CApos(c_i) - PApos(p_i) == k_i for all 24 cribs; Quagmire-IV needs the
    difference constant inside each residue class mod P, i.e. pos(x_a)-pos(x_rep(a)) agree between the two alphabets."""
    from collections import Counter, defaultdict
    MP, MA = posmat(PH), posmat(ALL)
    p_idx = np.array([ord(p) - 65 for _, p in CR]); c_idx = np.array([ord(CT[i]) - 65 for i in CI])
    reps = {P: np.array([min(b for b in range(24) if CI[b] % P == CI[a] % P) for a in range(24)]) for P in Ps}
    keys = {pm: np.array([gromark(list(map(int, pm)), 10)[i] for i in CI]) % 26 for pm in primers}
    hitsG = []; hitsQ = []; ntest = 0; cntQ = {}
    def index(M):
        d = {}
        for j, row in enumerate(map(bytes, (M % 26).astype(np.uint8))): d.setdefault(row, []).append(j)
        return d
    for side in ("PA=phrase", "CA=phrase"):
        fixed_cols, free_cols = (p_idx, c_idx) if side == "PA=phrase" else (c_idx, p_idx)
        F = MA[:, free_cols].astype(np.int64); X = MP[:, fixed_cols].astype(np.int64)
        for P in Ps:
            d = index(F - F[:, reps[P]]); ntest += len(PH) * len(ALL)
            for r, key in enumerate(map(bytes, ((X - X[:, reps[P]]) % 26).astype(np.uint8))):
                js = d.get(key)
                if js:
                    cntQ[P] = cntQ.get(P, 0) + len(js)
                    if len(hitsQ) < 200: hitsQ += [(side, P, PH[r], ALL[j]) for j in js[:5]]
            del d
        if keys:
            d = index(F)
            for pm, k in keys.items():
                ntest += len(PH) * len(ALL)
                need = (X + k) % 26 if side == "PA=phrase" else (X - k) % 26
                for r, key in enumerate(map(bytes, need.astype(np.uint8))):
                    for j in d.get(key, []): hitsG.append((side, pm, PH[r], ALL[j]))
            del d
    log(f"(2) phrase alphabets: {len(PH)} phrase alphabets x {len(ALL)} partner alphabets x 2 sides; Quagmire-IV P in {list(Ps)[:1]}..{list(Ps)[-1:] } + Gromark {len(primers)} primers -> {ntest:.3e} alphabet-pair tests (exact hash join)")
    log(f"   Gromark hits: {len(hitsG)}; Quagmire-IV hits total: {sum(cntQ.values())}")
    for h in hitsG[:40]: log("   G", *h)
    log("   Quagmire-IV hit counts by period (P>=13 are underdetermined by the cribs, see k4_sat.txt):", dict(sorted(cntQ.items())))
    for h in [h for h in hitsQ if h[1] < 13][:40]: log("   Q", *h)
    return hitsG, hitsQ
def main(ctl):
    lines = []
    def log(*a): s = " ".join(map(str, a)); print(s, flush=True); lines.append(s)
    words = sorted(w for w in GK.vocab() if 3 <= len(w) <= 14) + sorted(phrases() & set(EXTRA))
    PH = phrase_alphs()
    ALL = sorted(set(GK.alphabets(GK.vocab()).values()) | set(PH))
    primers = json.load(open("analysis/gromark_feasible.json"))["general"]
    CT = K4
    if ctl:
        rng = random.Random(1111); pt = list("".join(rng.choice("ETAOINSHRDLU") for _ in range(N)))
        for i, ch in KN.items(): pt[i] = ch
        # control 1: base-change key, PALIMPSEST n_a1 base 7, repeated, random PA/CA
        PA = "".join(rng.sample(AZ, 26)); CA = "".join(rng.sample(AZ, 26))
        d = digits(nums("PALIMPSEST")["a1"], 7); k = [d[i % len(d)] for i in range(N)]
        C1 = "".join(CA[(PA.index(p) + k[i]) % 26] for i, p in enumerate(pt))
        log("CONTROL 1 planted: PALIMPSEST a1 base7 rep, random alphabets")
        basechange(C1, ["PALIMPSEST", "ABSCISSA", "KRYPTOS", "SHADOW", "BERLIN"], log)
        # control 2: Quagmire IV P=8 with phrase PA and word CA
        PA = keyed("THEYUSEDTHEEARTHSMAGNETICFIELD", AZ); CA = keyed("ABSCISSA", AZ); key = [3, 1, 4, 1, 5, 9, 2, 6]
        C2 = "".join(CA[(PA.index(p) + key[i % 8]) % 26] for i, p in enumerate(pt))
        # control 3: Gromark with phrase CA + word PA using Bean-style primer from planted text
        PA3 = keyed("SANBORN", AZ); CA3 = keyed("DOESLANGLEYKNOWABOUTTHIS", KA); g = gromark([2, 7, 1, 8, 2], 10)
        C3 = "".join(CA3[(PA3.index(p) + g[i]) % 26] for i, p in enumerate(pt))
        log("CONTROL 2 planted Quag-IV P=8 PA=keyed(THEYUSEDTHEEARTHSMAGNETICFIELD) CA=keyed(ABSCISSA)")
        alph_tests(C2, PH, ALL, [], log, Ps=[8])
        log("CONTROL 3 planted Gromark 27182 PA=keyed(SANBORN) CA=keyed_KA(DOESLANGLEYKNOWABOUTTHIS)")
        alph_tests(C3, PH, ALL, ["27182"], log, Ps=[8])
        open("analysis/k4_cycle11_control.txt", "w").write("\n".join(lines) + "\n"); return
    bc = basechange(CT, words, log) if '--skip1' not in sys.argv else []
    if bc: json.dump(bc, open("analysis/k4_basechange_feasible.json", "w"))
    if bc:
        import k4_sat as S
        conf = 0
        for w, nm, b, use, _ in bc:
            d = digits(nums(w)[nm], b)
            k = [d[i % len(d)] for i in range(N)] if use == "rep" else gromark(d[:int(use[-1])], b)
            m = S.M(); pa, ca = S.alphabets(m, CT)
            for i, p in CR:
                for u in range(26): m.cl.append([-pa[p][u], ca[CT[i]][(u + k[i]) % 26]])
            r, _ = S.solve(m); conf += r == "SAT"
        nb = 0; hb = []
        A = posmat(ALL); pcol = np.array([ord(p) - 65 for _, p in CR]); ccol = np.array([ord(CT[i]) - 65 for i in CI])
        dC = {}
        for j, row in enumerate(map(bytes, A[:, ccol].astype(np.uint8))): dC.setdefault(row, []).append(j)
        for w, nm, b, use, _ in bc:
            d = digits(nums(w)[nm], b)
            k = [d[i % len(d)] for i in range(N)] if use == "rep" else gromark(d[:int(use[-1])], b)
            kk = np.array([k[i] for i in CI]); nb += len(ALL) ** 2
            for r, key in enumerate(map(bytes, ((A[:, pcol] + kk) % 26).astype(np.uint8))):
                for j in dC.get(key, []): hb.append((w, nm, b, use, ALL[r], ALL[j]))
        log(f"   (1b) survivors x keyword/phrase alphabet pairs ({len(ALL)}^2 each, {nb:.2e} pair tests): {len(hb)} hits")
        for h in hb[:20]: log("   1b hit", *h)
        log(f"   SAT re-check of base-change survivors: {conf}/{len(bc)} exactly satisfiable")
    alph_tests(CT, PH, ALL, primers, log)
    open("analysis/k4_cycle11.txt", "w").write("\n".join(lines) + "\n")
if __name__ == "__main__": main("control" in sys.argv)
