"""Cycle 3 battery for K4. Run from repo root: python3 tools/k4_cycle3.py > analysis/k4_cycle3_report.txt"""
import itertools, math, sys
from collections import Counter
import kryptos_text
K4 = kryptos_text.K4; KA = kryptos_text.KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; N = len(K4)
CRIBS = {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}
KN = {p - 1 + i: ch for p, w in CRIBS.items() for i, ch in enumerate(w)}
def say(*a): print(" ".join(str(x) for x in a))
def kal(word):
    s = "".join(dict.fromkeys(word + AZ)); return s
ENG = dict(zip(AZ, [8.17,1.49,2.78,4.25,12.70,2.23,2.02,6.09,6.97,0.15,0.77,4.03,2.41,6.75,7.51,1.93,0.10,5.99,6.33,9.06,2.76,0.98,2.36,0.15,1.97,0.07]))

# ---- E1: pure transposition (no substitution) ----
say("="*70); say("E1 - Pure transposition: CT letters would keep plaintext (English) frequencies")
c = Counter(K4); chi = sum((c.get(a,0) - N*ENG[a]/100)**2 / (N*ENG[a]/100) for a in AZ)
need = Counter("".join(CRIBS.values())); short = {a: need[a]-c.get(a,0) for a in need if need[a] > c.get(a,0)}
say(f"chi^2 vs English (25 dof) = {chi:.1f}  (p<0.001 critical value 52.6)")
say(f"Crib letters missing from K4 multiset: {short or 'none'}  -> {'IMPOSSIBLE as pure transposition' if short else 'multiset OK'}")
say(f"K4 has E={c['E']} vs ~{N*0.127:.0f} expected for English; IoC test from cycle 1 (0.036) also rejects.")

# ---- E2: unrestricted transposition + monoalphabetic shift (P=1) / periodic key: matching feasibility ----
say("="*70); say("E2 - Unrestricted transposition T then periodic shift (CT=Sub(T(PT))): is ANY T compatible?")
say("Feasibility = bipartite matching of 24 crib letters to CT positions with key fixed per residue class.")
def bip(adj):
    match = {}
    def aug(u, seen):
        for v in adj[u]:
            if v in seen: continue
            seen.add(v)
            if v not in match or aug(match[v], seen): match[v] = u; return True
        return False
    return sum(aug(u, set()) for u in adj)
for an, alpha in (("AZ", AZ), ("KA", KA)):
    for P in (1, 2, 3):
        feas = 0
        for key in itertools.product(range(26), repeat=P):
            adj = {i: [j for j in range(N) if (alpha.index(K4[j]) - key[j % P]) % 26 == alpha.index(pt)] for i, pt in KN.items()}
            if bip(adj) == 24: feas += 1
        say(f"{an} Vigenere P={P}: keys admitting a full crib matching = {feas}/{26**P}")
say("Interpretation: once P>=1 keys admit a matching, unrestricted transposition cannot be falsified by 24 cribs;"
    " structure (a rule-generated T) is required for any test to have power.")

# ---- E3: keyed columnar transposition, all column orders, widths 2..8 ----
say("="*70); say("E3 - Keyed columnar (all w! orders, w=2..8, read down) x {vig,beau}x{AZ,KA}x{B1,B2}, P=1..26; survivor needs >=6 constraints")
def kl(alpha, cc, p, mode):
    a, b = alpha.index(cc), alpha.index(p); return (a-b) % 26 if mode == "vig" else (a+b) % 26
TAB = {(an, m): {i: {j: kl(al, K4[j], pt, m) for j in range(N)} for i, pt in KN.items()} for an, al in (("AZ",AZ),("KA",KA)) for m in ("vig","beau")}
def check(ct_of, minc=6):
    hits = []
    for key, tab in TAB.items():
        for model in ("B1", "B2"):
            pairs = [((i if model == "B1" else ct_of[i]), tab[i][ct_of[i]]) for i in KN]
            for P in range(1, 27):
                seen = {}; cons = 0; ok = True
                for idx, k in pairs:
                    r = idx % P
                    if r in seen:
                        cons += 1
                        if seen[r] != k: ok = False; break
                    else: seen[r] = k
                if ok and cons >= minc: hits.append((key, model, P, cons))
    return hits
def columnar_ctof(w, order):
    rows = (N + w - 1)//w; ct_of = {}; k = 0
    for c in order:
        for r in range(rows):
            s = r*w + c
            if s < N:
                ct_of[s] = k; k += 1
    return ct_of
tested = surv = 0
for w in range(2, 9):
    for order in itertools.permutations(range(w)):
        ct_of = columnar_ctof(w, order); tested += 1
        h = check(ct_of)
        for x in h: surv += 1; say(f"  SURVIVOR w={w} order={order} {x}")
say(f"Column orders tested: {tested}; survivors: {surv}")

# ---- E4: numeric keys ----
say("="*70); say("E4 - Numeric keys")
NUMS = {"1986": "1986", "1989": "1989", "19861989": "19861989", "K2 coords 3857 6.5 / 77 8 44": "385765778 44".replace(" ",""),
        "World Clock UTC offsets -12..+11": None, "Berlin UTC+1 offsets rel. Berlin": None, "11091989 (Wall)": "11091989", "26111922 (Carter)": "26111922"}
for name, d in NUMS.items():
    if d is None: continue
    key = [int(x) for x in d]
    for an, alpha in (("AZ",AZ),("KA",KA)):
        for mode in ("vig","beau"):
            ok = all(kl(alpha, K4[i], pt, mode) == key[i % len(key)] for i, pt in KN.items())
            if ok: say(f"  SURVIVOR digit key {name} {an} {mode}")
say("Digit-shift keys (1986, 1989, 19861989, 11091989, 26111922, K2 coordinate digits): 0 survivors (and a fortiori from cycle-1 periodicity proof).")
# Gromark: running digit key from primer via lagged Fibonacci k[i]=k[i-n]+k[i-n+1] mod 10, exhaustive primers len 2..5
say("Gromark-style lagged-Fibonacci digit keys, ALL primers of length 2..5 (111,100 primers) x AZ/KA x vig/beau:")
gs = 0
for n in range(2, 6):
    for primer in itertools.product(range(10), repeat=n):
        k = list(primer)
        while len(k) < N: k.append((k[-n] + k[-n+1]) % 10)
        for an, alpha in (("AZ",AZ),("KA",KA)):
            for mode in ("vig","beau"):
                if all(kl(alpha, K4[i], pt, mode) == k[i] for i, pt in KN.items()): gs += 1; say(f"  SURVIVOR gromark primer={primer} {an} {mode}")
say(f"Gromark survivors: {gs}")
wc_label = "World Clock offsets as a 24-step shift cycle (0..23 from each zone, both directions):"
wc = 0
for start in range(24):
    for d in (1, -1):
        key = [(start + d*i) % 24 for i in range(24)]
        for an, alpha in (("AZ",AZ),("KA",KA)):
            for mode in ("vig","beau"):
                if all(kl(alpha, K4[i], pt, mode) == key[i % 24] for i, pt in KN.items()): wc += 1
say(wc_label, f"survivors {wc}")

# ---- E5: Quagmire IV (two independent keyword alphabets), direct and with simple columnar ----
say("="*70); say("E5 - Two keyword alphabets (Quagmire IV: PT alphabet A1, CT alphabet A2), periodic P=1..26")
KW = ["KRYPTOS","PALIMPSEST","ABSCISSA","BERLIN","CLOCK","BERLINCLOCK","WELTZEITUHR","URANIA","ALEXANDERPLATZ","WORLDCLOCK",
      "EGYPT","CARTER","TUTANKHAMUN","LAYERTWO","SHADOW","IQLUSION","QUA","YAR","SANBORN","SCHEIDT","LANGLEY","HILL","MENGENLEHREUHR","NORTHEAST"]
q4 = 0
for a1, a2 in itertools.product(KW, KW):
    A1, A2 = kal(a1), kal(a2)
    pairs = [(i, (A2.index(K4[i]) - A1.index(pt)) % 26) for i, pt in KN.items()]
    for P in range(1, 27):
        seen = {}; ok = True; cons = 0
        for i, k in pairs:
            r = i % P
            if r in seen:
                cons += 1
                if seen[r] != k: ok = False; break
            else: seen[r] = k
        if ok and cons >= 6: q4 += 1; say(f"  SURVIVOR {a1}/{a2} P={P} cons={cons}")
say(f"Alphabet pairs: {len(KW)**2}; survivors: {q4}")

# ---- E6: Quagmire IV + route transpositions from cycle 2 (model B2: key indexed by CT position) ----
say("="*70); say("E6 - Quagmire IV (576 alphabet pairs) combined with the 224 cycle-2 route/keyed-columnar permutations, P=1..26")
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()):
    import k4_cycle2 as _c2
e6 = 0
for pname, perm in _c2.perms.items():
    ct_of = [0]*N
    for kk, s in enumerate(perm): ct_of[s] = kk
    for a1, a2 in itertools.product(KW, KW):
        A1, A2 = kal(a1), kal(a2)
        pairs = [(ct_of[i], (A2.index(K4[ct_of[i]]) - A1.index(pt)) % 26) for i, pt in KN.items()]
        for P in range(1, 27):
            seen = {}; ok = True; cons = 0
            for idx, k in pairs:
                r = idx % P
                if r in seen:
                    cons += 1
                    if seen[r] != k: ok = False; break
                else: seen[r] = k
            if ok and cons >= 6: e6 += 1; say(f"  SURVIVOR {pname} {a1}/{a2} P={P} cons={cons}")
say(f"Configurations: {len(_c2.perms)*len(KW)**2*26}; survivors: {e6}")
