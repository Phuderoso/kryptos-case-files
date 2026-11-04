"""Cycle 17: K3's grid applied to K3 and K4 together.
Idea (open lead from cycle 14): Sanborn may have run K3's transposition (write in rows, rotate the grid, regrid, rotate
again) over the carved K3+K4 block as one text. K3 body (336) + '?' + K4 (97) = 434 = 14 x 31 letters, a suspiciously
tidy rectangle. If so, undoing that grid on the combined text must (a) still yield K3's known plaintext as a readable
run and (b) put K4's letters somewhere readable, optionally after one Quagmire-III (KRYPTOS) keyword layer.
Family: single and double rotations (CW or CCW each) with grid widths 2..62 and 217, ragged last row allowed, plus the
inverse of every permutation; three texts (K3+?+K4 = 434, K3+K4 = 433, K4+?+K3 = 434).
Scores: (1) K3 plaintext 8-grams recovered, (2) longest piece of EASTNORTHEAST / BERLINCLOCK found anywhere,
(3) quadgram score; (4) with a keyword layer (plain-sight words x Vigenere/Beaufort/variant, KA tableau) applied to the
whole output: exact NORTHEAST / BERLINCLOCK / EASTNORTHEAST anywhere.
Usage: python3 tools/k3k4_grid.py [control|null SEED|run]"""
import sys, re, json, random
import numpy as np
sys.path.insert(0, "tools")
from kryptos_text import K3, K4, KA
from solve_k1_k2_k3 import k3_dec
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
K3B = K3.rstrip("?"); K3PT = k3_dec(K3).rstrip("?")
WORDS = re.search(r'WORDS = """(.*?)"""', open("tools/k4_layers.py").read(), re.S).group(1).split()
KEYS = sorted(set(WORDS + ["PALIMPSEST", "ABSCISSA", "KRYPTOS", "LAYERTWO", "IDBYROWS", "BERLINCLOCK", "EASTNORTHEAST"]))
Q = json.load(open("data/quadgrams.json")); QF = Q["floor"]; QQ = Q["q"]
def qs(t):
    t = t.replace("?", ""); return sum(QQ.get(t[i:i+4], QF) for i in range(len(t) - 3)) / max(1, len(t) - 3)
def rot_perm(n, w, cw):
    rows = [list(range(i, min(i + w, n))) for i in range(0, n, w)]
    out = []
    cols = range(w) if cw else range(w - 1, -1, -1)
    for c in cols:
        rr = reversed(rows) if cw else rows
        out += [r[c] for r in rr if c < len(r)]
    return out          # output position k takes input index out[k]
def compose(p1, p2): return [p1[i] for i in p2]  # apply p1 then p2
def family(n):
    W = list(range(2, 63)) + [217]
    fam = {}
    for w1 in W:
        if w1 >= n: continue
        for d1 in (0, 1):
            p1 = rot_perm(n, w1, d1); fam[("rot", w1, d1)] = p1
            for w2 in W:
                if w2 >= n: continue
                for d2 in (0, 1):
                    fam[("rot2", w1, d1, w2, d2)] = compose(p1, rot_perm(n, w2, d2))
    for k, p in list(fam.items()):
        inv = [0] * n
        for i, j in enumerate(p): inv[j] = i
        fam[("inv",) + k] = inv
    return fam
K3G = {K3PT[i:i+8] for i in range(len(K3PT) - 7)}
CR = ["EASTNORTHEAST", "BERLINCLOCK"]
def crib_piece(t):
    best = 0
    for c in CR:
        for L in range(len(c), best, -1):
            if any(c[i:i+L] in t for i in range(len(c) - L + 1)): best = L; break
    return best
TAB = {k: [KA.index(ch) for ch in k] for k in KEYS}
KAI = np.array([KA.index(c) for c in AZ]); KAB = np.frombuffer(KA.encode(), dtype=np.uint8)
def sub_hits(t):
    letters = [c for c in t if c != "?"]
    x = KAI[np.array([ord(c) - 65 for c in letters])]
    hits = []
    for k, ki in TAB.items():
        kk = np.resize(np.array(ki), len(x))
        for m, y in (("vig", (x - kk) % 26), ("beau", (kk - x) % 26), ("var", (x + kk) % 26)):
            s = KAB[y].tobytes().decode()
            for c in ("EASTNORTHEAST", "BERLINCLOCK", "NORTHEAST", "BERLIN"):
                if c in s: hits.append((k, m, c, s.find(c)))
    return hits
def scan(text, label, do_sub=True, top=8):
    n = len(text); fam = family(n); res = []; nsub = 0; subh = []
    for key, p in fam.items():
        o = "".join(text[i] for i in p)
        k3 = sum(o[i:i+8] in K3G for i in range(n - 7))
        res.append((k3, crib_piece(o), qs(o), key, o))
    res.sort(key=lambda r: (-r[0], -r[1], -r[2]))
    out = [f"## {label}: n={n}, {len(fam)} permutations"]
    out.append("best K3-8gram recovery: " + ", ".join(f"{r[0]}@{r[3]}" for r in res[:top]))
    bc = max(res, key=lambda r: r[1]); out.append(f"longest crib piece anywhere (pure transposition): {bc[1]} @ {bc[3]}")
    bq = max(res, key=lambda r: r[2]); out.append(f"best quadgram (pure transposition): {bq[2]:.3f} @ {bq[3]}: {bq[4][:80]}...")
    if do_sub:
        from multiprocessing import Pool
        with Pool() as pool:
            for (k3, cp, q, key, o), hs in zip(res, pool.map(sub_hits, [r[4] for r in res], chunksize=200)):
                nsub += 1
                subh += [(key, h) for h in hs]
        strong = [x for x in subh if x[1][2] != "BERLIN"]
        out.append(f"keyword layer: {nsub} perms x {len(KEYS)} keys x 3 modes; BERLIN hits {len(subh)-len(strong)}, NORTHEAST/BERLINCLOCK/EASTNORTHEAST hits {len(strong)}")
        for s in strong[:10]: out.append(f"  hit {s}")
    return "\n".join(out), res, subh
def control():
    # K3 itself must be recovered by the family (identity check), and a planted 434-letter text with cribs must be found.
    rep = []
    fam336 = family(336)
    ok = any("".join(K3B[i] for i in p) == K3PT for p in fam336.values())
    rep.append(f"K3 alone (336): exact K3 plaintext reproduced by the family: {ok}")
    eng = re.sub("[^A-Z]", "", open("data/g1342.txt", encoding="utf-8", errors="ignore").read().upper()[200000:203000])[:434]
    pt = eng[:150] + "EASTNORTHEAST" + eng[163:300] + "BERLINCLOCK" + eng[311:]
    rng = random.Random(17)
    for trial in range(3):
        n = 434; fam = family(n); keys = list(fam); kt = keys[rng.randrange(len(keys))]; p = fam[kt]
        word = rng.choice(KEYS); ki = TAB[word]
        sub = "".join(KA[(KA.index(c) + ki[i % len(ki)]) % 26] for i, c in enumerate(pt))  # Vigenere on KA tableau
        inv = [0] * n
        for i, j in enumerate(p): inv[j] = i
        ct = "".join(sub[i] for i in inv)   # so that applying p recovers sub
        found = [h for h in sub_hits("".join(ct[i] for i in p)) if h[2] == "EASTNORTHEAST"]
        rank = None
        # full blind scan: does the scanner find it among all perms?
        blind = None
        if trial == 0:
            from multiprocessing import Pool
            ks = list(fam)
            with Pool() as pool: hs = pool.map(sub_hits, ["".join(ct[i] for i in fam[k]) for k in ks], chunksize=200)
            blind = [(k, h) for k, hh in zip(ks, hs) for h in hh if h[2] == "EASTNORTHEAST"]
        rep.append(f"planted trial {trial}: perm {kt}, key {word}: direct recovery {bool(found)}" + (f"; blind scan hits {len(blind)}, correct among them: {any(b[0]==kt for b in blind)}" if blind is not None else ""))
    return "\n".join(rep)
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "control": print(control())
    elif mode == "null":
        rng = random.Random(int(sys.argv[2])); k4 = list(K4); rng.shuffle(k4); k4 = "".join(k4)
        print(scan(K3B + "?" + k4, f"null seed {sys.argv[2]}: K3+?+shuffled K4")[0])
    else:
        for text, label in ((K3B + "?" + K4, "K3+?+K4"), (K3B + K4, "K3+K4"), (K4 + "?" + K3B, "K4+?+K3")):
            print(scan(text, label)[0]); print()
