"""Cycle 2 falsification battery for K4. Run: python3 tools/k4_cycle2.py > analysis/k4_cycle2_report.txt
Every test uses only the 24 official crib letters (positions 22-34, 64-74, 1-indexed). Deterministic, no randomness except
the seeded random-permutation baseline in test B."""
import itertools, random
from kryptos_text import K4, KA, K1, K2, K3
from solve_k1_k2_k3 import vig_dec, k3_dec
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIBS = {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}
KN = {p - 1 + i: ch for p, w in CRIBS.items() for i, ch in enumerate(w)}  # 0-indexed pos -> PT letter
N = len(K4)

def keyed_alphabet(word):
    s = "".join(dict.fromkeys(word.upper() + AZ)); return "".join(c for c in s if c in AZ)

def keyletter(alpha, c, p, mode):
    a, b = alpha.index(c), alpha.index(p)
    return (a - b) % 26 if mode == "vig" else (a + b) % 26 if mode == "beau" else (b - a) % 26

def periodic_check(pairs, P):
    """pairs: list of (key_index, keyvalue). Returns (consistent, n_constraints)."""
    seen, cons = {}, 0
    for i, k in pairs:
        r = i % P
        if r in seen:
            cons += 1
            if seen[r] != k: return False, cons
        else: seen[r] = k
    return True, cons

out = []
def say(*a): out.append(" ".join(str(x) for x in a))

# ---------------- Test A: Hill cipher ----------------
say("=" * 70); say("TEST A - Hill cipher (n=2,3), numbering AZ (A=0) and KA, all block alignments")
def hill_test(n, alpha, offset):
    # blocks: start positions s = offset + k*n; need all n PT and CT letters known (CT always known)
    blocks = [s for s in range(offset, N - n + 1, n) if all(s + j in KN for j in range(n))]
    if len(blocks) < n: return None, len(blocks)
    P = [[alpha.index(KN[s + j]) for j in range(n)] for s in blocks]
    C = [[alpha.index(K4[s + j]) for j in range(n)] for s in blocks]
    # CT_block = K * PT_block (mod 26). Each row r of K independently: C[b][r] = sum_j K[r][j]*P[b][j]
    rows = []
    for r in range(n):
        sols = [row for row in itertools.product(range(26), repeat=n)
                if all(sum(row[j] * P[b][j] for j in range(n)) % 26 == C[b][r] for b in range(len(blocks)))]
        rows.append(sols)
    from math import gcd
    full = 0
    for K in itertools.product(*rows):
        if n == 2: det = K[0][0]*K[1][1] - K[0][1]*K[1][0]
        else:
            det = (K[0][0]*(K[1][1]*K[2][2]-K[1][2]*K[2][1]) - K[0][1]*(K[1][0]*K[2][2]-K[1][2]*K[2][0])
                   + K[0][2]*(K[1][0]*K[2][1]-K[1][1]*K[2][0]))
        if gcd(det % 26, 26) == 1: full += 1
        if full > 1000: break
    return full, len(blocks)
for n in (2, 3):
    for an, alpha in (("AZ", AZ), ("KA", KA)):
        for off in range(n):
            f, nb = hill_test(n, alpha, off)
            say(f"n={n} alpha={an} offset={off}: fully-known blocks={nb}, invertible keys consistent with cribs={f}")
say("Result: a count of 0 FALSIFIES that Hill configuration (no invertible matrix maps the crib blocks).")

# ---------------- Test B: transposition + substitution ----------------
say("=" * 70); say("TEST B - transposition T combined with periodic substitution (vig/beau/varbeau; AZ, KA), P=1..26")
say("Models: (B1) CT = T(Sub(PT)) key indexed by PT position; (B2) CT = Sub(T(PT)) key indexed by CT position.")
say("T families: rows-of-w read by columns (top-down & bottom-up = K3-style rotation), inverses, keyed columnar")
say("(keywords below). K3-exact double rotation needs a full grid; 97 is prime, so only incomplete-row routes are used.")
def columnar(w, order=None, up=False):
    rows = (N + w - 1) // w
    cols = order if order else list(range(w))
    perm = []  # perm[k] = source index of k-th output letter
    for c in cols:
        rng = range(rows - 1, -1, -1) if up else range(rows)
        perm += [r * w + c for r in rng if r * w + c < N]
    return perm
def kw_order(word):
    word = word[:]
    return sorted(range(len(word)), key=lambda i: (word[i], i))
KEYWORDS = ["KRYPTOS", "PALIMPSEST", "ABSCISSA", "BERLIN", "CLOCK", "BERLINCLOCK", "WELTZEITUHR", "URANIA",
            "ALEXANDERPLATZ", "WORLDCLOCK", "LAYERTWO", "SHADOW", "IQLUSION", "EGYPT", "CARTER", "LANGLEY", "SANBORN", "SCHEIDT"]
perms = {}
for w in range(2, 49):
    for up in (False, True):
        p = columnar(w, up=up); perms[f"cols w={w} {'up' if up else 'down'}"] = p
for kw in KEYWORDS:
    p = columnar(len(kw), order=kw_order(kw)); perms[f"keyed-columnar {kw}"] = p
for name in list(perms):
    p = perms[name]; inv = [0] * N
    for k, s in enumerate(p): inv[s] = k
    perms[name + " (inverse)"] = inv
def test_perm(perm, minc):
    # perm[k] = PT index placed at CT position k  -> pos_ct_of_pt[i]
    ct_of = [0] * N
    for k, s in enumerate(perm): ct_of[s] = k
    hits = []
    for an, alpha in (("AZ", AZ), ("KA", KA)):
        for mode in ("vig", "beau", "varbeau"):
            for model in ("B1", "B2"):
                pairs = []
                for i, pt in KN.items():
                    k = keyletter(alpha, K4[ct_of[i]], pt, mode)
                    pairs.append((i if model == "B1" else ct_of[i], k))
                for P in range(1, 27):
                    ok, c = periodic_check(pairs, P)
                    if ok and c >= minc: hits.append((an, mode, model, P, c))
    return hits
MINC = 6
total = 0
for name, p in perms.items():
    h = test_perm(p, MINC); total += 1
    for x in h: say(f"  SURVIVOR {name}: alpha={x[0]} {x[1]} {x[2]} P={x[3]} constraints={x[4]}")
say(f"Permutations tested: {total} x 2 alphabets x 3 modes x 2 models x 26 periods = {total*312} configurations")
say(f"Survivor threshold: >= {MINC} independent crib constraints (chance pass ~ 26^-{MINC} = {26**-MINC:.1e} each).")
random.seed(1337); base = 0
for _ in range(2000):
    p = list(range(N)); random.shuffle(p); base += len(test_perm(p, MINC))
say(f"Baseline: 2000 random permutations produced {base} survivors at the same threshold.")

# ---------------- Test C: autokey & running keys ----------------
say("=" * 70); say("TEST C - non-periodic keys: ciphertext-autokey, plaintext-autokey, running keys")
for an, alpha in (("AZ", AZ), ("KA", KA)):
    for mode in ("vig", "beau", "varbeau"):
        good = []
        for L in range(1, 22):  # CT-autokey: key[i] = CT[i-L]; fully determined for i >= L
            ok = all(keyletter(alpha, K4[i], pt, mode) == alpha.index(K4[i - L]) for i, pt in KN.items())
            if ok: good.append(L)
        say(f"CT-autokey {an}-{mode}: lags consistent with all 24 cribs: {good or 'NONE'}")
        good = []
        for L in range(1, 13):  # PT-autokey: key[i] = PT[i-L]; testable where both known
            pairs = [(i, pt) for i, pt in KN.items() if i - L in KN]
            if pairs and all(keyletter(alpha, K4[i], pt, mode) == alpha.index(KN[i - L]) for i, pt in pairs):
                good.append((L, len(pairs)))
        say(f"PT-autokey {an}-{mode}: (lag, #tests) consistent: {good or 'NONE'}")
k2fix = K2[:-8] + "S" + K2[-8:]
texts = {"K1 plaintext": vig_dec(K1, "PALIMPSEST"), "K2 plaintext": vig_dec(k2fix, "ABSCISSA").replace("?", ""),
         "K3 plaintext": k3_dec(K3).replace("?", ""), "K1-K3 plaintext concatenated": None,
         "Kryptos tableau rows (KA shifted)": "".join(KA[i:] + KA[:i] for i in range(26)),
         "K0 Morse (VIRTUALLYINVISIBLE...)": "VIRTUALLYINVISIBLEDIGETALINTERPRETATITSHADOWFORCESLUCIDMEMORYTISYOURPOSITIONSOSRQ"}
texts["K1-K3 plaintext concatenated"] = texts["K1 plaintext"] + texts["K2 plaintext"] + texts["K3 plaintext"]
for tn, t in texts.items():
    for rev in (False, True):
        tt = t[::-1] if rev else t
        best = (0, None)
        for an, alpha in (("AZ", AZ), ("KA", KA)):
            for mode in ("vig", "beau", "varbeau"):
                for off in range(-N, len(tt)):
                    m = sum(1 for i, pt in KN.items() if 0 <= off + i < len(tt) and
                            keyletter(alpha, K4[i], pt, mode) == alpha.index(tt[off + i]))
                    if m > best[0]: best = (m, f"{an}-{mode} offset {off}")
        say(f"Running key '{tn}'{' reversed' if rev else ''}: best crib matches {best[0]}/24 ({best[1]}); per-offset chance ~0.9; maxima <=8 are noise; a true key needs 24/24")

# ---------------- Test D: keyword-mixed alphabets (misspelling & World Clock material) ----------------
say("=" * 70); say("TEST D - Quagmire-III-style tableaux built on candidate keyword alphabets, periodic key P=1..26")
MISS = ["Q", "U", "A", "E", "QUA", "QUAE", "AUQ", "YAR", "QUAYAR", "YARQUA", "XS", "QUAX", "QUAS", "IQLUSION", "UNDERGRUUND",
        "DESPARATLY", "PALIMPCEST", "LUCID", "DIGETAL", "INTERPRETATIT"]
WC = ["WELTZEITUHR", "URANIA", "ALEXANDERPLATZ", "WORLDCLOCK", "WELTZEIT", "BERLINWALL", "MAUER", "BERLINCLOCK",
      "MENGENLEHREUHR", "EGYPT", "TUTANKHAMUN", "KRYPTOS", "KRYPTOSQUA", "KRYPTOSYAR"]
surv = 0
for kw in MISS + WC:
    alpha = keyed_alphabet(kw)
    for mode in ("vig", "beau", "varbeau"):
        pairs = [(i, keyletter(alpha, K4[i], pt, mode)) for i, pt in KN.items()]
        okP = [P for P in range(1, 27) if periodic_check(pairs, P)[0]]
        if okP: surv += 1; say(f"  SURVIVOR {kw} {mode}: P={okP}")
say(f"Keywords tested: {len(MISS+WC)} (misspelling-derived: {len(MISS)}, World Clock/Berlin/Egypt: {len(WC)}); survivors: {surv}")
say("Note: any periodic key of length <=26 in AZ/KA (incl. QUA, YAR, WELTZEITUHR... used directly as Vigenere keys) was already falsified in cycle 1.")
print("\n".join(out))
