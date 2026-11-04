"""Cycle 7: 'layers in plain sight'. Short, pre-registered hypothesis lists of SIMPLE composed operations.
Gate = the 24 official crib letters (exact). Survivors are then scored for English (quadgrams).
Layers: transposition T in {identity, reverse, K3-method decrypt rot(rot(.,a),b) both directions/all a,b<=48,
single rotations} composed with a KEYWORD substitution (Vigenere / Beaufort / variant-Beaufort) on the KA tableau,
the AZ tableau, or a tableau keyed by another plain-sight word; keys = plain-sight words, reversed words, all phases,
and two-word stacks (double Vigenere) on identity/reverse/K3 dims. Usage: python3 tools/k4_layers.py [control]"""
import sys, json, itertools
sys.path.insert(0, "tools")
import kryptos_text
from k4_anneal import AZ, KA, KN, N, quad
K4 = kryptos_text.K4
WORDS = """KRYPTOS PALIMPSEST ABSCISSA SHADOW LUCID MEMORY POSITION BERLIN CLOCK BERLINCLOCK EGYPT LAYERTWO XLAYERTWO
WESTXLAYERTWO IDBYROWS SANBORN SCHEIDT LANGLEY VIRTUALLYINVISIBLE DIGETALINTERPRETATU SHADOWFORCES LUCIDMEMORY
TISYOURPOSITION SOS RQ SOSRQ EQUAL QUAL QUA LOE YAR WHATSTHEPOINT POINT WHOSAYSITISHIDDEN HIDDEN UNDERGRUUND
IQLUSION DESPARATLY CANYOUSEEANYTHING CANYOUSEEANYTHINGQ TUTANKHAMUN CARTER HOWARDCARTER WELTZEITUHR URANIA
ALEXANDERPLATZ NORTHEAST EAST COMPASS LODESTONE MAGNETIC MAGNETICFIELD ANTIPODES CYRILLIC PROJECTOR INVISIBLE
ILLUSION NUANCE MASKING MASK DELIGHTFUL SCRAMBLED ONION LAYER LAYERS WALL BERLINWALL CIA KGB AGENCY LUXOR GIZA
PYRAMID TOMB CHAMBER CANDLE SLOWLY DESPERATELY UNDERGROUND TOTALLYINVISIBLE EARTHSMAGNETIC VIRGINIA ABSCISSAPALIMPSEST
PALIMPSESTABSCISSA KRYPTOSABCDEF THEPOINT WEST TWO X""".split()
DIGITKEYS = {"COORD385765N77844W": [3,8,5,7,6,5,7,7,8,4,4], "COORDS_385765": [3,8,5,7,6,5], "COORDW_77844": [7,7,8,4,4],
             "DATE1990": [1,9,9,0], "DATE11031990": [1,1,0,3,1,9,9,0], "DATE1986": [1,9,8,6], "DATE1989": [1,9,8,9]}
def keyed(w):
    out = ""
    for ch in w + AZ:
        if ch not in out: out += ch
    return out
ALPHAS = {"KA": KA, "AZ": AZ}
for w in ("PALIMPSEST", "ABSCISSA", "SHADOW", "BERLIN", "CLOCK", "EGYPT", "LUCID", "MEMORY", "POSITION", "SANBORN", "SCHEIDT", "LAYERTWO"):
    ALPHAS["KEYED_" + w] = keyed(w)

def rot_dec(text, w):  # exactly the K3 decrypt rotation (ragged last row tolerated)
    rows = [text[i:i+w] for i in range(0, len(text), w)]
    return "".join("".join(r[c] for r in reversed(rows) if c < len(r)) for c in range(w))
def rot_ccw(text, w):
    rows = [text[i:i+w] for i in range(0, len(text), w)]
    return "".join("".join(r[c] for r in rows if c < len(r)) for c in reversed(range(w)))
IDX = "".join(chr(0x100 + i) for i in range(N))
def as_perm(f):  # f maps CT-ordered string -> PT-ordered string ; return pt_from_ct[i] = CT position of PT index i
    return [ord(ch) - 0x100 for ch in f(IDX)]
def transpositions(full=True):
    T = {"identity": list(range(N)), "reverse": list(range(N))[::-1]}
    rng = range(2, 49) if full else (4, 7, 8, 12, 14, 24)
    for a in rng:
        T[("rot", a)] = as_perm(lambda t: rot_dec(t, a)); T[("rotccw", a)] = as_perm(lambda t: rot_ccw(t, a))
        for b in rng:
            T[("K3", a, b)] = as_perm(lambda t: rot_dec(rot_dec(t, a), b))
            T[("K3ccw", a, b)] = as_perm(lambda t: rot_ccw(rot_ccw(t, a), b))
    return T
def required(CT, ptfrom, alpha, mode, model):
    """For each crib PT index i: CT position k = ptfrom[i]; key index = k (model 'sub_last': CT=Sub(T(PT)))
    or i (model 'sub_first': CT=T(Sub(PT))). Returns list of (key_index, required_shift)."""
    req = []
    for i, p in KN.items():
        k = ptfrom[i]; c = alpha.index(CT[k]); q = alpha.index(p)
        s = (c - q) % 26 if mode == "vig" else (c + q) % 26 if mode == "beau" else (q - c) % 26
        req.append((k if model == "sub_last" else i, s))
    return req
def decrypt(CT, ptfrom, alpha, mode, model, key):
    out = []
    for i in range(N):
        k = ptfrom[i]; c = alpha.index(CT[k]); s = key[(k if model == "sub_last" else i) % len(key)]
        out.append(alpha[(c - s) % 26] if mode == "vig" else alpha[(s - c) % 26] if mode == "beau" else alpha[(c + s) % 26])
    return "".join(out)
def keylist(alpha):
    K = {}
    for w in WORDS:
        for name, ww in ((w, w), (w + "_rev", w[::-1])):
            if len(ww) >= 1: K[name] = [alpha.index(ch) for ch in ww]
    for n, d in DIGITKEYS.items(): K[n] = d
    return K
def stacked(alpha, words):
    K = {}
    for a, b in itertools.combinations(words, 2):
        A = [alpha.index(c) for c in a]; B = [alpha.index(c) for c in b]
        L = len(A) * len(B) // __import__("math").gcd(len(A), len(B))
        K[a + "+" + b] = [(A[i % len(A)] + B[i % len(B)]) % 26 for i in range(L)]
    return K
def run(CT, T, stack_T=("identity", "reverse", ("K3", 24, 8), ("K3", 8, 24)), alphas=None):
    tests = 0; best = []; surv = []
    for aname, alpha in (alphas or ALPHAS).items():
        keys = keylist(alpha)
        stack = stacked(alpha, [w for w in WORDS if len(w) <= 12][:60])
        for tname, ptfrom in T.items():
            K = dict(keys)
            if tname in stack_T: K.update(stack)
            for mode in ("vig", "beau", "varbeau"):
                for model in ("sub_last", "sub_first"):
                    req = required(CT, ptfrom, alpha, mode, model)
                    for kname, key in K.items():
                        L = len(key)
                        for ph in range(L):
                            tests += 1; m = 0
                            for idx, s in req:
                                if key[(idx + ph) % L] == s: m += 1
                            if m >= 10: best.append((m, aname, tname, mode, model, kname, ph))
                            if m == 24:
                                kk = key[ph:] + key[:ph]; pt = decrypt(CT, ptfrom, alpha, mode, model, kk)
                                surv.append(dict(alpha=aname, T=str(tname), mode=mode, model=model, key=kname, phase=ph,
                                                 quad_per_char=round(quad(pt)/(N-3), 3), pt=pt))
    return tests, surv, sorted(best, reverse=True)[:15]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "control":
        # planted: English with cribs, CT = Vig_KA(SHADOW, phase 2)( K3-method transposition dims (7,14) )
        eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKETWELVE"
        pt = list(eng[:N]); 
        for i, ch in KN.items(): pt[i] = ch
        pt = "".join(pt); ptfrom = as_perm(lambda t: rot_dec(rot_dec(t, 7), 14))
        key = [KA.index(c) for c in "SHADOW"]; key = key[2:] + key[:2]
        ct = [""] * N
        for i in range(N):
            k = ptfrom[i]; ct[k] = KA[(KA.index(pt[i]) + key[k % 6]) % 26]
        CT = "".join(ct); T = transpositions(full=False); T[("K3", 7, 14)] = ptfrom
        tests, surv, best = run(CT, T)
        print(f"CONTROL tests {tests}; survivors {len(surv)}")
        for s in surv: print("  ", json.dumps(s))
    else:
        from multiprocessing import Pool
        T = transpositions(full=True)
        with Pool() as pool:
            R = pool.starmap(run, [(K4, T, ("identity", "reverse", ("K3", 24, 8), ("K3", 8, 24)), {a: v}) for a, v in ALPHAS.items()])
        tests = sum(r[0] for r in R); surv = [x for r in R for x in r[1]]; best = sorted([x for r in R for x in r[2]], reverse=True)[:15]
        print(f"K4: transpositions {len(T)}; alphabets {len(ALPHAS)}; tests {tests:,}; full-crib survivors {len(surv)}")
        for s in surv: print("  SURVIVOR", json.dumps(s))
        print("best partial crib matches (m/24):"); [print("  ", b) for b in best]
