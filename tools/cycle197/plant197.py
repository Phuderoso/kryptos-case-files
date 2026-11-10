"""Cycle 197 planted controls (pre-registered list in PREREG197.md). Independent encryption from lib197 (not cmp197).
Writes ctl197.txt: name | carved text | source | N | kind | d | q | model | solver | alph/tab | form | m | n | keys."""
import random, sys
from lib197 import *
FILL = ("THEQUIETROOMHELDASINGLELAMPANDTHEMAPWASFOLDEDTWICEWHENTHEMESSAGECAMEWESTOODBYTHEWINDOWANDWAITEDFORTHESIGNAL"
        "UNDERTHEOLDBRIDGETHECOURIERLEFTAPACKAGEANDWALKEDAWAYSLOWLYTOWARDTHESTATIONBEFOREDAWN")
sup = sys.argv[1] if len(sys.argv) > 1 else "../../../sup"
def kv(word, alph): return [alph.index(ch) for ch in word]
def make(name, N, kind, d, out, model, solver, ab, form, wa, wb, rng, kpos=None, extra=None):
    P = list(FILL[:N]); kpos = kpos or CI
    for t, k in enumerate(kpos):
        if not (kpos is not CI and kind == "ins" and CI[t] == d): P[k] = PTC[t]
    m, n = len(wa), len(wb)
    if solver == "A":
        alph = AZ if ab == "AZ" else KA; a, b = kv(wa, alph), kv(wb, alph)
    else:
        T1, T2 = TABS[ab]; a, b = kv(wa, T1), kv(wb, T2)
    C = [None] * N
    for k in range(N):
        i = k if model in "PD" else out[k]
        if solver == "A":
            K = (a[i % m] + b[i % n]) % 26
            if extra: K = (K + extra[i % len(extra)]) % 26
            C[out[k]] = enc_add(form, alph, P[k], K)
        else: C[out[k]] = enc_two(ab, form, P[k], a[i % m], b[i % n])
    if kind == "del": carved = C[:d] + C[d + 1:]
    elif kind == "ins": carved = C[:d] + [rng.choice(AZ)] + C[d:]
    else: carved = C
    assert len(carved) == 97
    return "".join(carved), "".join(P)
rng = random.Random(197)
ident = lambda N: list(range(N))
rows = []
def R2kp(kind, d):
    if kind == "del": return [j if j < d else j + 1 for j in CI]
    return [j if j < d else (0 if j == d else j - 1) for j in CI]
# direct plants (rec mode)
rows.append(("P1", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", None))
rows.append(("P2", 96, "ins", 30, "directR2", 0, "D", "A", "AZ", "beau", "BERLIN", "KRYPTOS", None))
rows.append(("P3", 96, "ins", 5, "direct", 0, "D", "B", "AZ>KA", "VV", "CLOCK", "NORTHEAST", None))
rows.append(("P4", 98, "del", 70, "directR2", 0, "D", "B", "KA>AZ", "BV", "ABSCISSA", "PALIMPSEST", None))
rows.append(("P9", 97, "none", 0, "direct", 0, "D", "A", "AZ", "vig", "ABSCISSA", "PALIMPSEST", None))
rows.append(("N1", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "CLOCK", "KRYPTOS", "BERLINCLOCK"))
# decimation plants (perm mode, sample banks)
rows.append(("P5", 98, "del", 40, "dec98_s32", 1234, "P", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", None))
rows.append(("P6", 96, "ins", 80, "dec96_s32", 4321, "C", "A", "AZ", "vig", "CLOCK", "BERLIN", None))
rows.append(("P7", 98, "del", 60, "decM98_s8", 300, "C", "B", "AZ>KA", "VB", "TIME", "KRYPTOS", None))
rows.append(("P8", 96, "ins", 10, "decM96_s8", 200, "P", "B", "KA>AZ", "VV", "SHADOW", "LIGHT", None))
rows.append(("N2", 98, "del", 40, "dec98_s32", 1234, "P", "A", "KA", "vig", "CLOCK", "KRYPTOS", "BERLINCLOCK"))
with open("ctl197.txt", "w") as f:
    for (nm, N, kind, d, src, q, model, solver, ab, form, wa, wb, ex) in rows:
        if src.startswith("direct"):
            out = ident(N); kpos = R2kp(kind, d) if src == "directR2" else None
        else: out = load_perm(f"{sup}/{src}.bin", N, q); kpos = None
        exv = kv(ex, KA) if ex else None
        ctx, P = make(nm, N, kind if N != 97 else "none", d, out, model, solver, ab, form, wa, wb, rng, kpos, exv)
        f.write(" ".join(map(str, [nm, ctx, src, N, kind, d, q, model, solver, ab, form, len(wa), len(wb), wa + "+" + wb + ("+" + ex if ex else ""), P])) + "\n")
print(open("ctl197.txt").read())
