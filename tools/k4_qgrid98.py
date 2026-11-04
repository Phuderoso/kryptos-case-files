"""Cycle 18: the carved '?' as K4's first symbol -> 98 = 14 x 7 = 2 x 49 symbols.
Hypothesis: Sanborn transposed a 98-symbol block (97 letters + '?') with a K3-style or columnar grid, and a periodic
substitution sits before or after it. Instead of guessing keywords, test ALGEBRAICALLY: for each transposition and each
periodic substitution (Vigenere / Beaufort / variant; KRYPTOS or straight tableau; period 1..12), are the 24 known
plaintext letters (EASTNORTHEAST at 21-33, BERLINCLOCK at 63-73 of the 97-letter plaintext) consistent with ONE key?
Case A: C = T(S(P) + '?')   -> un-transpose, drop '?', key indexed by plaintext position.
Case B: C = S'(T(P + '?'))  -> key indexed by carved position (with or without '?' taking a key slot).
Transpositions: K3-style single/double rotations widths 2..49 (CW/CCW) + inverses; full keyed columnar on 7 columns
(all 5040 orders) and 14 columns (keyword orders), written by rows and read by columns, + inverses.
Usage: python3 tools/k4_qgrid98.py [control|null SEED|run]"""
import sys, random, itertools, re
sys.path.insert(0, "tools")
from kryptos_text import K4, KA
from k3k4_grid import rot_perm, compose, KEYS
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB = {21 + i: c for i, c in enumerate("EASTNORTHEAST")}; CRIB.update({63 + i: c for i, c in enumerate("BERLINCLOCK")})
N = 98
def inv(p):
    q = [0] * len(p)
    for i, j in enumerate(p): q[j] = i
    return q
def col_perm(n, order):
    w = len(order); out = []
    for c in order: out += list(range(c, n, w))
    return out
def kw_order(word, w):
    s = (word * 3)[:w]; return sorted(range(w), key=lambda i: (s[i], i))
def family():
    fam = {}
    W = range(2, 50)
    for w1 in W:
        for d1 in (0, 1):
            p1 = rot_perm(N, w1, d1); fam[("rot", w1, d1)] = p1
            for w2 in W:
                for d2 in (0, 1): fam[("rot2", w1, d1, w2, d2)] = compose(p1, rot_perm(N, w2, d2))
    for o in itertools.permutations(range(7)): fam[("col7",) + o] = col_perm(N, o)
    for k in KEYS:
        if len(k) >= 5: fam[("col14", k)] = col_perm(N, kw_order(k, 14))
    for k, p in list(fam.items()): fam[("inv",) + k] = inv(p)
    return fam
IDX = {"KA": {c: i for i, c in enumerate(KA)}, "AZ": {c: i for i, c in enumerate(AZ)}}
MODES = {"vig": lambda c, p: (c - p) % 26, "beau": lambda c, p: (c + p) % 26, "var": lambda c, p: (p - c) % 26}
def consistent(pairs):   # pairs: list of (key_index, cipher_letter, plain_letter)
    hits = []
    for tn, ix in IDX.items():
        for mn, f in MODES.items():
            ks = [(ki, f(ix[c], ix[p])) for ki, c, p in pairs]
            for per in range(1, 13):
                seen = {}; ok = True
                for ki, v in ks:
                    r = ki % per
                    if seen.setdefault(r, v) != v: ok = False; break
                if ok: hits.append((tn, mn, per, "".join((KA if tn == "KA" else AZ)[seen[r]] if r in seen else "." for r in range(per))))
    return hits
def test(ct98, fam):
    out = []
    for key, p in fam.items():
        y = [ct98[i] for i in p]              # undo transposition: y[k] = ct98[p[k]]
        q = y.index("?") if "?" in y else None
        # Case A: substitution then transposition; plaintext = y without '?'
        z = [c for c in y if c != "?"]
        h = consistent([(i, z[i], c) for i, c in CRIB.items()])
        out += [("A", key, q) + x for x in h]
        # Case B: transposition first, substitution on the carved string. plaintext pos i -> y index -> carved index
        ypos = [k for k in range(N) if y[k] != "?"]
        for skip in (0, 1):
            qi = ct98.index("?")
            pairs = []
            for i, c in CRIB.items():
                j = p[ypos[i]]                    # carved index
                kidx = j - (1 if (skip and j > qi) else 0)
                pairs.append((kidx, ct98[j], c))
            h = consistent(pairs)
            out += [("B%d" % skip, key, q) + x for x in h]
    return out
def control():
    rng = random.Random(18); fam = family(); keys = list(fam); rep = [f"family size {len(fam)}"]
    eng = re.sub("[^A-Z]", "", open("data/g1342.txt", encoding="utf-8", errors="ignore").read().upper()[300000:302000])
    pt = eng[:21] + "EASTNORTHEAST" + eng[34:63] + "BERLINCLOCK" + eng[74:97]
    for trial in range(4):
        kt = rng.choice(keys); p = fam[kt]; per = rng.randint(4, 9); key = [rng.randrange(26) for _ in range(per)]
        if trial % 2 == 0:   # case A, KA vigenere
            s = "".join(KA[(KA.index(c) + key[i % per]) % 26] for i, c in enumerate(pt)) + "?"
            ct = [None] * N
            for k in range(N): ct[p[k]] = s[k]
            case = "A"
        else:                # case B, AZ beaufort on carved string, '?' takes no key slot
            y = pt + "?"; ct = [None] * N
            for k in range(N): ct[p[k]] = y[k]
            j = 0; c2 = []
            for c in ct:
                if c == "?": c2.append("?"); continue
                c2.append(AZ[(key[j % per] - AZ.index(c)) % 26]); j += 1
            ct = c2; case = "B1"
        ct = "".join(ct)
        hits = test(ct, fam)
        good = [h for h in hits if h[1] == kt and h[0] == case and h[5] == per]
        rep.append(f"planted {trial}: case {case} perm {kt[:4]} period {per}: recovered {bool(good)}; total hits {len(hits)} (periods {sorted(set(h[5] for h in hits))})")
    return "\n".join(rep)
def summarize(hits, label):
    from collections import Counter
    c = Counter((h[0], h[5]) for h in hits)
    s = [f"{label}: {len(hits)} consistent (case, perm, tableau, mode, period) combos"]
    s.append("  by (case, period): " + ", ".join(f"{k}:{v}" for k, v in sorted(c.items())))
    for h in [h for h in hits if h[5] <= 8][:40]: s.append("  " + repr(h))
    return "\n".join(s)
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "control": print(control())
    elif mode == "null":
        fam = family()
        for seed in range(int(sys.argv[2]) if len(sys.argv) > 2 else 4):
            l = list(K4); random.Random(seed).shuffle(l)
            print(summarize(test("?" + "".join(l), fam), f"null seed {seed} (?+shuffled K4)"))
    else:
        fam = family()
        print(summarize(test("?" + K4, fam), "?+K4"))
        print(summarize(test(K4 + "?", fam), "K4+? (control orientation)"))
